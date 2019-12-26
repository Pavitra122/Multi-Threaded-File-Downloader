'''
Tests for Downloader Class
'''



from downloader import Downloader
import unittest



class TestDownloaderClass(unittest.TestCase):

    def test_bad_url(self):
        '''
        Test bad url input
        '''
        self.assertRaises(ValueError, Downloader, url = "garbage.html")
        self.assertRaises(ValueError, Downloader, url = "sdsd.html")


    def test_bad_num_threads(self):
        '''
        Test bad input for number of threads
        '''
        self.assertRaises(ValueError, Downloader, num_threads = 0, url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png")
        self.assertRaises(TypeError, Downloader, num_threads = "string", url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png")


    def test_simple_image_download(self):
        '''
        Test downloading small image, original file saved in tests_files/
        '''

        downloader = Downloader(url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png",
                    file_name = "tests_files/pikachu.png")
        downloader.finish()
        with open("tests_files/pikachu.png","rb") as newFile, open("tests_files/pikachu_original.png","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


    def test_multipe_threads(self):
        '''
        Test downloading small image using different number of threads to make sure that number of threads
        does not affect accuracy or introduce off by one errors, original file saved in tests_files/
        '''

        downloader = Downloader(url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png",
                    file_name = "tests_files/pikachu.png", num_threads=1)
        downloader.finish()
        with open("tests_files/pikachu.png","rb") as newFile, open("tests_files/pikachu_original.png","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


        downloader = Downloader(url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png",
                    file_name = "tests_files/pikachu.png", num_threads=5)
        downloader.finish()
        with open("tests_files/pikachu.png","rb") as newFile, open("tests_files/pikachu_original.png","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


        downloader = Downloader(url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png",
                    file_name = "tests_files/pikachu.png", num_threads=10)
        downloader.finish()
        with open("tests_files/pikachu.png","rb") as newFile, open("tests_files/pikachu_original.png","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


        downloader = Downloader(url = "https://i.pinimg.com/originals/cb/33/49/cb3349b86ca661ca61ae9a36d88d70d4.png",
                    file_name = "tests_files/pikachu.png", num_threads=100)
        downloader.finish()
        with open("tests_files/pikachu.png","rb") as newFile, open("tests_files/pikachu_original.png","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


    def test_download_pdf(self):
        '''
        Test downloading pdf file, original file saved in tests_files/
        '''
        downloader = Downloader(url = "https://www.illumio.com/hubfs/Illumio_Brochure_What_We_Do_2019_03.pdf?hsLang=en",
                    file_name = "tests_files/illumio_what_we_do.pdf", num_threads=100)
        downloader.finish()

        with open("tests_files/illumio_what_we_do.pdf","rb") as newFile, open("tests_files/illumio_original.pdf","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


    def test_large_image(self):
        '''
        Test downloading large 5000*7000 image, original file saved in tests_files/
        '''
        downloader = Downloader(url = "https://images.unsplash.com/photo-1576545533261-9d451d9b5799?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=5000&ixlib=rb-1.2.1&q=80&w=7000",
                    file_name = "tests_files/large_image.jpeg")
        downloader.finish()
        with open("tests_files/large_image.jpeg","rb") as newFile, open("tests_files/large_image_original.jpeg","rb") as original_file:
            self.assertEqual(newFile.read() , original_file.read())


if __name__ == '__main__':

    unittest.main()
