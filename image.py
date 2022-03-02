import csv
import requests
import datetime
import concurrent.futures
import numpy as np

from guithread import GUIThread
from config import text_width, max_thread_count
from urllib.parse import urlparse
from os import path as ospath, makedirs


class Imaging(GUIThread):
    def __init__(self, csv_files, path):

        self.csv_files, self.path = csv_files, path
        self.images_path = path + '/images/'
        self.images_to_download = {}

        for csv_file in csv_files.split(','):
            csv_filename = ospath.basename(csv_file)
            csv_filename_nocsv = csv_filename.split('.')[0]
            img_url_list = self.create_list_from_csv(csv_file)
            if not img_url_list:
                continue
            self.images_to_download[csv_filename_nocsv] = img_url_list
            images_subdir = self.images_path + csv_filename_nocsv + '/'
            makedirs(images_subdir, exist_ok=True)
        print(self.images_to_download)
        super().__init__()

    def create_list_from_csv(self, csv_file):
        if csv_file == '':
            self.print_to_textbox("No files available")
            return []
        self.print_to_textbox("File is " + csv_file)
        urls = []
        with open(csv_file) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                url = row['Png URL']
                if url and url != "None":
                    try:
                        urls.append(url)
                    except Exception as e:
                        self.print_to_textbox(str(e))
        return urls

    def get_images(self, img_url_list, csv_filename_nocsv):
        images_subdir = self.images_path + csv_filename_nocsv + '/'
        for img_url in img_url_list:
            img_filename = ospath.basename(urlparse(img_url).path)
            if ospath.isfile("" + images_subdir + img_filename):
                self.print_to_textbox("File already exists: " + images_subdir + img_filename)
                continue
            try:
                download_file(img_url, path=images_subdir)
                self.print_to_textbox("Getting image: " + img_url)
            except Exception as e:
                self.print_to_textbox(str(e))
            self.set_progress(1)

    def run(self):
        try:
            starttime = datetime.datetime.now()
            images_path = self.images_path

            progress_step = (100.0 / max_thread_count)
            for csv, img_url_list in self.images_to_download.items():
                img_url_lists = np.array_split(img_url_list, max_thread_count)
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
                    futures = []
                    for i in img_url_lists:
                        futures.append(executor.submit(self.get_images, img_url_list=i, csv_filename_nocsv=csv))
                    for future in concurrent.futures.as_completed(futures):
                        self.print_to_textbox("Img thread done")

            self.set_progress(0)
            self.print_to_textbox("DONE!")
            self.print_to_textbox("\n" + "#" * text_width + "\n")
            finishtime = datetime.datetime.now() - starttime
            print(finishtime)
        except Exception as e:
            print(e)
        finally:
            self.signals.finished.emit(images_path)


def download_file(url, path='./'):
    local_filename = path + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename





