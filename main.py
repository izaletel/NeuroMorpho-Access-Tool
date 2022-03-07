# -*- coding: utf-8 -*-

from acquisition import *
from image import *
from config import *

from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtCore import QThreadPool, Slot
from qtgui import Ui_MainWindow

import sys
import os
import subprocess


class MainWindow(QMainWindow):

    def __init__(self):
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(max_thread_count)
        super().__init__()

    def print_to_textbox(self, textbox, text):
        try:
            text = text + '\n'
            print(text)
            textbox.insertPlainText(str(text))
        except Exception as e:
            print(e)

    def set_progress(self, progressbar, value):
        progressbar.setValue(value)

    def set_indefinite_progress(self, progressbar, indefinite):
        if indefinite:
            progressbar.setRange(0, 0)
        else:
            progressbar.setRange(0, 100)
            progressbar.setValue(0)

    def set_filename(self, filebar, filename):
        filebar.setText(filename)

    def get_image_csv(self, filebar):
        csv_files = QFileDialog.getOpenFileNames(self, 'Load CSV file', './output', '*.csv')
        string_csv_files = ",".join(csv_files[0])
        filebar.setText(string_csv_files)

    def set_finished(self, activate_button, open_button, path):
        activate_button.setDisabled(False)
        open_button.setDisabled(False)
        return path

    def set_acq_finished(self, activate_button, open_button, path):
        self.lastfilepath = self.set_finished(activate_button, open_button, path)
        ui_window.acq_button_continue.setDisabled(True)
        ui_window.acq_button_cancel.setDisabled(True)

    def set_img_finished(self, activate_button, open_button, path):
        self.lastimagepath = self.set_finished(activate_button, open_button, path)

    @Slot()
    def acquisition_thread(self, filename='default.csv', brain_region='All', species='All', cell_type='All'):
        ui_window.acq_button.setDisabled(True)
        self.acq = Acquisition(filename=filename, brain_region=brain_region, species=species, cell_type=cell_type)
        self.acq.is_paused = True
        ui_window.acq_button_continue.setDisabled(False)
        ui_window.acq_button_cancel.setDisabled(False)

        self.acq.signals.text.connect(lambda text: self.print_to_textbox(ui_window.acq_textbox, text))
        self.acq.signals.progress.connect(lambda progress: self.set_progress(ui_window.acq_progressbar, progress))
        self.acq.signals.finished.connect(
            lambda path: self.set_acq_finished(ui_window.acq_button, ui_window.open_csv_file_button, path)
        )
        ui_window.acq_button_continue.clicked.connect(lambda: self.acq.resume())
        ui_window.acq_button_cancel.clicked.connect(lambda: self.acq.kill())
        self.threadpool.start(self.acq)

    @Slot()
    def get_images_thread(self, path='./', csv_files=''):
        ui_window.img_button.setDisabled(True)
        self.img = Imaging(csv_files=csv_files, path=path)

        self.img.signals.text.connect(
            lambda text: self.print_to_textbox(ui_window.img_textbox, text)
        )
        self.img.signals.progress.connect(
            lambda progress: self.set_indefinite_progress(ui_window.img_progressbar, progress)
        )
        self.img.signals.finished.connect(
            lambda path: self.set_img_finished(ui_window.img_button, ui_window.open_images_directory_button, path)
        )
        self.threadpool.start(self.img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    ui_window = Ui_MainWindow()
    ui_window.setupUi(window)

    # Acquire tab
    ui_window.brain_region_menu.addItems(brain_regions)
    ui_window.species_choice_menu.addItems(species_all)
    ui_window.cell_type_choice_menu.addItems(cell_types)

    ui_window.brain_region_menu.currentTextChanged.connect(
        lambda: window.set_filename(
            ui_window.acq_entry,
            'NM_' + ui_window.brain_region_menu.currentText().replace(" ", "_") + '_' +
            ui_window.species_choice_menu.currentText().replace(" ", "_") + '_' +
            ui_window.cell_type_choice_menu.currentText().replace(" ", "_") + '.csv'
        )
    )
    ui_window.species_choice_menu.currentTextChanged.connect(
        lambda: window.set_filename(
            ui_window.acq_entry,
            'NM_' + ui_window.brain_region_menu.currentText().replace(" ", "_") + '_' +
            ui_window.species_choice_menu.currentText().replace(" ", "_") + '_' +
            ui_window.cell_type_choice_menu.currentText().replace(" ", "_") + '.csv'
        )
    )
    ui_window.cell_type_choice_menu.currentTextChanged.connect(
        lambda: window.set_filename(
            ui_window.acq_entry,
            'NM_' + ui_window.brain_region_menu.currentText().replace(" ", "_") + '_' +
            ui_window.species_choice_menu.currentText().replace(" ", "_") + '_' +
            ui_window.cell_type_choice_menu.currentText().replace(" ", "_") + '.csv'
        )
    )

    ui_window.acq_button.clicked.connect(
        lambda: window.acquisition_thread(
            ui_window.acq_entry.text(),
            ui_window.brain_region_menu.currentText(),
            ui_window.species_choice_menu.currentText(),
            ui_window.cell_type_choice_menu.currentText())
    )

    ui_window.open_csv_file_button.setDisabled(True)
    if os.name == 'nt':
        ui_window.open_csv_file_button.clicked.connect(lambda: os.startfile(os.getcwd() + window.lastfilepath))
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        ui_window.open_csv_file_button.clicked.connect(
            lambda: subprocess.call([opener, os.getcwd() + '/' + window.lastfilepath])
        )

    # Image tab

    ui_window.img_open_csv_file_button.clicked.connect(
        lambda: window.get_image_csv(
            ui_window.img_csv_choice_list
        )
    )

    ui_window.img_button.clicked.connect(
        lambda: window.get_images_thread(
            path='./output',
            csv_files=ui_window.img_csv_choice_list.text()
        )
    )

    ui_window.open_images_directory_button.setDisabled(True)
    if os.name == 'nt':
        ui_window.open_images_directory_button.clicked.connect(lambda: os.startfile(os.getcwd() + window.lastimagepath))
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        ui_window.open_images_directory_button.clicked.connect(
            lambda: subprocess.call([opener, os.getcwd() + '/' + window.lastimagepath])
        )


    # About tab

    ui_window.about_label.setHtml(about_text)
    ui_window.about_label.setOpenExternalLinks(True)
    ui_window.about_label.setOpenLinks(True)


    # Bottom part of GUI

    if os.name == 'nt':
        ui_window.open_file_location_button.clicked.connect(lambda: os.startfile(os.getcwd()))
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        ui_window.open_file_location_button.clicked.connect(
            lambda: subprocess.call([opener, os.getcwd() + '/'])
        )


    ui_window.exit_button.clicked.connect(app.quit)
    window.show()
    app.exec()
