import csv
import requests
import os
import threading


def get_images_thread(path='./', csv_file=''):
    th = threading.Thread(target=get_images, args=(path, csv_file))
    th.start()


def download_file(url, path='./'):
    local_filename = path + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def get_images(path='./', csv_file=''):
    if csv_file == 'None':
        print("No files available")
        return 0
    images_path = path + 'images/'
    images_subdir = images_path + csv_file.split('.')[0] + '/'

    os.makedirs(images_subdir, exist_ok=True)
    with open('./output/' + csv_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            url = row['Png URL']
            if url and url != "None":
                print(url)
                try:
                    download_file(url, path=images_subdir)
                except Exception as e:
                    print(e)


def get_filenames(path='./', suffix=".csv"):
    filenames = os.listdir(path)
    return [filename for filename in filenames if filename.endswith(suffix)]

