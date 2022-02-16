import csv
import requests
import os
import guithread

from config import text_width


class Imaging(guithread.GUIThread):
    def __init__(self, path='./', csv_file=''):

        self.path, self.csv_file = path, csv_file
        super().__init__()

    def run(self):
        path = self.path
        csv_file = self.csv_file
        if csv_file == 'None':
            self.print_to_textbox("No files available")
            return 0
        csv_filename = os.path.basename(csv_file)
        images_path = path + '/images/'
        images_subdir = images_path + csv_filename.split('.')[0] + '/'

        os.makedirs(images_subdir, exist_ok=True)
        self.print_to_textbox("File is " + csv_file)
        totalrows = sum(1 for _ in open(csv_file))
        progress_step = 100.0 / totalrows
        progress_current = 0.0
        self.set_progress(progress_current)
        with open(csv_file) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
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


def download_file(url, path='./'):
    local_filename = path + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
