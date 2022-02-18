import csv
import requests
import datetime

from guithread import GUIThread
from config import text_width, max_thread_count
from urllib.parse import urlparse
from os import path as ospath


class Imaging(GUIThread):
    def __init__(self, images_path, img_url_list, job_number=0):

        self.images_path, self.img_url_list, self.job_number = images_path, img_url_list, job_number

        super().__init__()

    def run(self):
        starttime = datetime.datetime.now()
        images_path = self.images_path

        progress_step = (100.0 / max_thread_count)
        for img_url in self.img_url_list:
            img_filename = ospath.basename(urlparse(img_url).path)
            if ospath.isfile("" + self.images_path + img_filename):
                self.print_to_textbox("File already exists: " + self.images_path + img_filename)
                continue
            try:
                download_file(img_url, path=images_path)
                self.print_to_textbox("Getting image: " + img_url)
            except Exception as e:
                self.print_to_textbox(str(e))
            self.set_progress(1)
        self.set_progress(0)
        self.print_to_textbox("DONE thread: " + str(self.job_number))
        self.print_to_textbox("\n" + "#" * text_width + "\n")
        finishtime = datetime.datetime.now() - starttime
        print(finishtime)


def download_file(url, path='./'):
    local_filename = path + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


