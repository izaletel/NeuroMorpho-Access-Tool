# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from acquisition import *
from image import *
from config import *
from tkinter.scrolledtext import ScrolledText

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QThreadPool, Slot
from qtgui import Ui_MainWindow

import sys
import os


class MainWindow(QMainWindow):

    def __init__(self):
        self.threadpool = QThreadPool()
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

    def set_filename(self, filebar, filename):
        filebar.setText(filename)

    @Slot()
    def acquisition_thread(self, brain_region='All', species='All', cell_type='All'):
        self.acq = Acquisition(brain_region=brain_region, species=species, cell_type=cell_type)

        self.acq.signals.text.connect(lambda text: self.print_to_textbox(ui_window.acq_textbox, text))
        self.acq.signals.progress.connect(lambda progress: self.set_progress(ui_window.acq_progressbar, progress))
        self.threadpool.start(self.acq)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    ui_window = Ui_MainWindow()
    ui_window.setupUi(window)

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

    # ui_window.exit_button.clicked.connect(app.quit())
    ui_window.acq_button.clicked.connect(
        lambda: window.acquisition_thread(
            ui_window.brain_region_menu.currentText(),
            ui_window.species_choice_menu.currentText(),
            ui_window.cell_type_choice_menu.currentText())
    )

    window.show()
    app.exec()
