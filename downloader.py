#!/usr/bin/env python3

'''
A multithreaded CLI tool for downloading files. Supports quick transfer of downloaded
files to external device using a QR code.
'''

import argparse
import queue
import requests
import threading
import time
import os
from progress.bar import Bar
import mimetypes


ENABLE_QR_CODE_DOWNLOADS = 1
DEFAULT_NUM_THREADS = 4
MAX_THREADS = 1000
CHUNK_SIZE = 1000000                       # Number of bytes that each thread will download in a iteration

DEFAULT_FILE_NAME = 'download'             # File name to to save download in if file name is not specified
                                           # with --filename

semaphore = threading.BoundedSemaphore()   # Lock for progress bar since the library does not support multithreaded
                                           # applications


'''
Class containing all the methods to implement the Downloader
'''
class Downloader:


    def threadHandler(self, start_location, end_location, url, filename):
        '''
        Inputs:

        start_location: Contains the location to start writing to in the file
        end_location: Contains the end location to write till
        url: url to fetch data for the corresponding location
        filename: file to write data into

        Method run by each thread. Initially runs the task passed to it as inputs
        and then fetches new tasks from a queue shared among threads
        '''

        while(1):
            # specify the starting and ending locations of the file
            headers = {'Range': 'bytes=%d-%d' % (start_location, end_location)}
            try:
            # request the specified part and get into variable
                r = requests.get(url, headers=headers, stream=True)
            except requests.exceptions.RequestException:
                # Task is not valid, skip
                continue

            # open the file and write the content into appropriate address in file.
            with open(filename, "r+b") as fp:
                fp.seek(start_location)
                fp.write(r.content)

            try:
                # Lock acquired so that other threads cannot increase progress bar
                semaphore.acquire()
                self.bar.next()
                semaphore.release()

                # Optmization to prevent calling costly get_nowait() method if queue is empty
                if not self.queue.empty():
                    # Get next task from the queue, no_wait since we do not want to wait if queue is empty
                    task = self.queue.get_nowait()
                    start_location = task['start_location']
                    end_location = task['end_location']
                    url = task['url']
                    filename = task['filename']
                else:
                    return
            except queue.Empty:
                return

    def __init__(self, url, file_name = "", num_threads=DEFAULT_NUM_THREADS):

        '''
        Inputs:

        url: url to fetch data for the corresponding location
        file_name: file to write data into
        num_threads: number of threads to download data concurrently

        1. Checks for invalid inputs
        2. Initializes downloader class variables
        3. Initializes the queue with tasks to be shared among threads
        '''

        if num_threads<1:
            raise ValueError('Number of threads should be greater than 0')

        self.url = url
        self.num_threads = int(num_threads)
        self.file_name = file_name
        self.queue = queue.Queue()
        self.chunk_size = CHUNK_SIZE

        try:
            r = requests.head(self.url)
        except:
            raise ValueError('URL is invalid')


        if r.status_code != 200:
            raise ValueError('URL is invalid')

        self.file_size = int(r.headers['content-length'])

        if not self.file_name:
            # If the file name is not provided, try to figure out the file extension from the URL
            # and store data in download.<extension>
            mimetype = mimetypes.guess_type(self.url)

            if mimetype == (None, None):
                raise Exception('Failed to extract file extension, please specify file name using --filename flag')
            self.file_name = DEFAULT_FILE_NAME + '.' + mimetype[0].split("/")[-1]


        # Initialize file with '\0'
        fp = open(self.file_name, "wb")
        fp.write(b'\0' * self.file_size)
        fp.close()


        # Create tasks and store in queue. The tasks are chunks of bytes CHUNK_SIZE and are coallased.
        # This is done so that if connection is lost during download, bytes at the start of the file are
        # all downloded. Check README for more details
        start_location = 0
        end_location = 0
        for i in range(int(self.file_size/self.chunk_size) + 1):
            start_location = self.chunk_size * i
            end_location = start_location + self.chunk_size
            if end_location > self.file_size:
                end_location = self.file_size
            self.queue.put({'start_location': start_location, 'end_location': end_location, 'url': self.url, 'filename': self.file_name})

        self.bar = Bar('Downloading', max=self.queue.qsize(), suffix='%(percent)d%%')


    def finish(self):

        '''
        Launch threads and finish the download
        '''

        for i in range(min(self.queue.qsize() ,self.num_threads)):
            task = self.queue.get()
            # create a Thread with start and locations
            t = threading.Thread(target=self.threadHandler, kwargs={'start_location': task['start_location'], 'end_location': task['end_location'], 'url': task['url'], 'filename': task['filename']})
            t.setDaemon(True)
            t.start()

        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()
        self.bar.finish()
        print("Downloaded at", self.file_name)



if __name__ == '__main__':

    # Parse arguments from command line
    parser = argparse.ArgumentParser(description='CLI based file downloader')
    parser.add_argument('URL', metavar='URL', #nargs='+',
                        help='URL to download file from')
    parser.add_argument('-c', dest='N_threads',
                        type=int,
                        default=4,
                        help='Number of threads, default is ' + str(DEFAULT_NUM_THREADS))
    parser.add_argument('--filename', dest='fileName',
                        default="",
                        help='Name of file to be downloaded')

    args = parser.parse_args()

    # Launch download
    downloader = Downloader(url = args.URL, file_name = args.fileName, num_threads = args.N_threads)
    downloader.finish()

    # Run open source tool to transfer file to phone using local network
    if ENABLE_QR_CODE_DOWNLOADS:
        print("File can be viewed/downloded on your phone using the QR code below")
        # Run command in a shell
        os.system("qr-filetransfer "+str(downloader.file_name))
