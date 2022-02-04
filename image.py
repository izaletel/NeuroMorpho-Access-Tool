import csv
import requests
import os
import guithread

from config import text_width


def get_images_thread(progressbar='', progress_var='', textbox='', path='./', csv_file=''):
    img = Imaging(progressbar=progressbar, progress_var=progress_var, textbox=textbox,
                      path=path, csv_file=csv_file)
    img.start()


class Imaging(guithread.GUIThread):
    def __init__(self, progressbar='', progress_var='', textbox='',
                 path='./', csv_file=''):

        self.progressbar, self.progress_var, self.textbox = progressbar, progress_var, textbox
        self.path, self.csv_file = path, csv_file
        super().__init__(progressbar, progress_var, textbox)

    def run(self):
        path = self.path
        csv_file = self.csv_file
        if csv_file == 'None':
            self.print_to_textbox("No files available")
            return 0
        images_path = path + 'images/'
        images_subdir = images_path + csv_file.split('.')[0] + '/'

        os.makedirs(images_subdir, exist_ok=True)
        self.print_to_textbox("File is " + csv_file)
        totalrows = sum(1 for _ in open('./output/' + csv_file))
        progress_step = 100.0 / totalrows
        progress_current = 0.0
        self.set_progress(progress_current)
        with open('./output/' + csv_file) as f:
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


def get_filenames(path='./', suffix=".csv"):
    filenames = os.listdir(path)
    return [filename for filename in filenames if filename.endswith(suffix)]


def update_combobox_list(combobox):
    list = get_filenames(path='./output', suffix='.csv')
    combobox['values'] = list


def download_file(url, path='./'):
    local_filename = path + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename
