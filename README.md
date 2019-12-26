# Multi-Threaded-File-Downloader

A multithreaded CLI tool to download a file from a URL and transfer downloaded files acrosss devices easily.

#### Features
1. Multithreaded to allow concurretly downloading different parts of the file.
2. Detects bad network connections and can pauses/resumes download automatically. 
3. The downloaded file can be quickly transferred across devices through a local network using a QR code.
4. Progress bar to see the status of download.


![Demo](demo/demo.gif)

## Installation

```
git clone https://github.com/Pavitra122/Multi-Threaded-File-Downloader
cd Multi-Threaded-File-Downloader
pip3 install -r requirements.txt
chmod +x downloader.py
```

## Usage

```
./downloader.py <URL> -c nThreads --filename <fileName>

Note: nThreads and fileName are optional arguments
```
Example:
```
./downloader.py "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/images/BigBuckBunny.jpg"
```

Can be used as 
```
./downloader.py <URL> -c nThreads --filename <fileName>
```
by renaming downloader.py to downloader. Note that this breaks the dependency link to run the unit tests.


## Unit Tests

```
python3 test_downloader.py
```


## Implementation Details

Uses a consumer-producer synchronised queue of tasks across threads. Given a URL, a list of tasks are created each assigned to a certain portion of the 




