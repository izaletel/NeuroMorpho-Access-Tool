import csv
import requests
import datetime

from guithread import GUIThread
from config import text_width, max_thread_count
from os import makedirs, path as ospath


class Imaging(GUIThread):
    def __init__(self, path='./', csv_file='', job_number=0):

        self.path, self.csv_file, self.job_number = path, csv_file, job_number
        super().__init__()

    def run(self):
        starttime = datetime.datetime.now()
        path = self.path
        csv_file = self.csv_file
        if csv_file == 'None':
            self.print_to_textbox("No files available")
            return 0
        csv_filename = ospath.basename(csv_file)
        images_path = path + '/images/'
        images_subdir = images_path + csv_filename.split('.')[0] + '/'

        makedirs(images_subdir, exist_ok=True)
        self.print_to_textbox("File is " + csv_file)
        totalrows = sum(1 for _ in open(csv_file))

        jobrows = totalrows // max_thread_count
        if self.job_number == max_thread_count - 1:
            row_numbers = range(self.job_number * jobrows, totalrows)
        else:
            row_numbers = range(self.job_number * jobrows, (self.job_number + 1) * jobrows)

        progress_step = 100.0 / totalrows
        progress_current = 0.0
        self.set_progress(progress_current)
        row_number = -1
        with open(csv_file) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                row_number += 1
                if row_number not in row_numbers:
                    continue
                url = row['Png URL']
                if url and url != "None":
                    try:
                        download_file(url, path=images_subdir)
                        self.print_to_textbox("Getting image: " + url)
                    except Exception as e:
                        self.print_to_textbox(str(e))
                progress_current += progress_step
                self.set_progress(progress_current)
        self.set_progress(0)
        self.print_to_textbox("DONE!")
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
