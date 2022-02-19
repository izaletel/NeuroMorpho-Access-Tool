# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtgui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QTabWidget, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 801, 551))
        self.tab_acquire = QWidget()
        self.tab_acquire.setObjectName(u"tab_acquire")
        self.brain_region_menu = QComboBox(self.tab_acquire)
        self.brain_region_menu.setObjectName(u"brain_region_menu")
        self.brain_region_menu.setGeometry(QRect(90, 20, 191, 21))
        self.species_choice_menu = QComboBox(self.tab_acquire)
        self.species_choice_menu.setObjectName(u"species_choice_menu")
        self.species_choice_menu.setGeometry(QRect(90, 50, 191, 21))
        self.cell_type_choice_menu = QComboBox(self.tab_acquire)
        self.cell_type_choice_menu.setObjectName(u"cell_type_choice_menu")
        self.cell_type_choice_menu.setGeometry(QRect(90, 80, 191, 21))
        self.brain_region_menu_label = QLabel(self.tab_acquire)
        self.brain_region_menu_label.setObjectName(u"brain_region_menu_label")
        self.brain_region_menu_label.setGeometry(QRect(10, 20, 81, 21))
        self.species_choice_menu_label = QLabel(self.tab_acquire)
        self.species_choice_menu_label.setObjectName(u"species_choice_menu_label")
        self.species_choice_menu_label.setGeometry(QRect(10, 50, 81, 21))
        self.cell_type_choice_menu_label = QLabel(self.tab_acquire)
        self.cell_type_choice_menu_label.setObjectName(u"cell_type_choice_menu_label")
        self.cell_type_choice_menu_label.setGeometry(QRect(10, 80, 81, 21))
        self.acq_progressbar = QProgressBar(self.tab_acquire)
        self.acq_progressbar.setObjectName(u"acq_progressbar")
        self.acq_progressbar.setGeometry(QRect(450, 10, 281, 23))
        self.acq_progressbar.setValue(0)
        self.acq_textbox = QTextBrowser(self.tab_acquire)
        self.acq_textbox.setObjectName(u"acq_textbox")
        self.acq_textbox.setGeometry(QRect(20, 150, 751, 371))
        self.acq_textbox.setOpenLinks(False)
        self.acq_button = QPushButton(self.tab_acquire)
        self.acq_button.setObjectName(u"acq_button")
        self.acq_button.setGeometry(QRect(330, 110, 111, 31))
        self.acq_entry = QLineEdit(self.tab_acquire)
        self.acq_entry.setObjectName(u"acq_entry")
        self.acq_entry.setGeometry(QRect(450, 60, 251, 21))
        self.acq_entry_label = QLabel(self.tab_acquire)
        self.acq_entry_label.setObjectName(u"acq_entry_label")
        self.acq_entry_label.setGeometry(QRect(450, 40, 251, 21))
        self.open_csv_file_button = QPushButton(self.tab_acquire)
        self.open_csv_file_button.setObjectName(u"open_csv_file_button")
        self.open_csv_file_button.setGeometry(QRect(520, 110, 131, 31))
        self.tabWidget.addTab(self.tab_acquire, "")
        self.tab_image = QWidget()
        self.tab_image.setObjectName(u"tab_image")
        self.img_textbox = QTextBrowser(self.tab_image)
        self.img_textbox.setObjectName(u"img_textbox")
        self.img_textbox.setGeometry(QRect(20, 150, 751, 371))
        self.img_textbox.setOpenLinks(False)
        self.img_progressbar = QProgressBar(self.tab_image)
        self.img_progressbar.setObjectName(u"img_progressbar")
        self.img_progressbar.setGeometry(QRect(450, 10, 281, 23))
        self.img_progressbar.setValue(0)
        self.img_button = QPushButton(self.tab_image)
        self.img_button.setObjectName(u"img_button")
        self.img_button.setGeometry(QRect(330, 110, 111, 31))
        self.img_csv_choice_list_label = QLabel(self.tab_image)
        self.img_csv_choice_list_label.setObjectName(u"img_csv_choice_list_label")
        self.img_csv_choice_list_label.setGeometry(QRect(20, 10, 81, 21))
        self.img_csv_choice_list = QLineEdit(self.tab_image)
        self.img_csv_choice_list.setObjectName(u"img_csv_choice_list")
        self.img_csv_choice_list.setGeometry(QRect(90, 10, 291, 21))
        self.img_open_csv_file_button = QPushButton(self.tab_image)
        self.img_open_csv_file_button.setObjectName(u"img_open_csv_file_button")
        self.img_open_csv_file_button.setGeometry(QRect(280, 50, 101, 21))
        self.open_images_directory_button = QPushButton(self.tab_image)
        self.open_images_directory_button.setObjectName(u"open_images_directory_button")
        self.open_images_directory_button.setGeometry(QRect(520, 110, 131, 31))
        self.tabWidget.addTab(self.tab_image, "")
        self.tab_about = QWidget()
        self.tab_about.setObjectName(u"tab_about")
        self.about_label = QLabel(self.tab_about)
        self.about_label.setObjectName(u"about_label")
        self.about_label.setGeometry(QRect(0, 0, 791, 521))
        self.tabWidget.addTab(self.tab_about, "")
        self.exit_button = QPushButton(self.centralwidget)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setGeometry(QRect(340, 560, 111, 31))
        self.open_file_location_button = QPushButton(self.centralwidget)
        self.open_file_location_button.setObjectName(u"open_file_location_button")
        self.open_file_location_button.setGeometry(QRect(10, 560, 111, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NeuroMorpho Access Tool", None))
        self.brain_region_menu_label.setText(QCoreApplication.translate("MainWindow", u"Brain region:", None))
        self.species_choice_menu_label.setText(QCoreApplication.translate("MainWindow", u"Species:", None))
        self.cell_type_choice_menu_label.setText(QCoreApplication.translate("MainWindow", u"Cell type:", None))
        self.acq_button.setText(QCoreApplication.translate("MainWindow", u"Generate CSV", None))
        self.acq_entry.setText(QCoreApplication.translate("MainWindow", u"NM_All_All_All.csv", None))
#if QT_CONFIG(accessibility)
        self.acq_entry_label.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.acq_entry_label.setText(QCoreApplication.translate("MainWindow", u"Name of file to generate:", None))
        self.open_csv_file_button.setText(QCoreApplication.translate("MainWindow", u"Open CSV file", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_acquire), QCoreApplication.translate("MainWindow", u"Generate CSV", None))
        self.img_button.setText(QCoreApplication.translate("MainWindow", u"Download Images", None))
        self.img_csv_choice_list_label.setText(QCoreApplication.translate("MainWindow", u"CSV File:", None))
        self.img_csv_choice_list.setText("")
        self.img_open_csv_file_button.setText(QCoreApplication.translate("MainWindow", u"Open CSV files", None))
        self.open_images_directory_button.setText(QCoreApplication.translate("MainWindow", u"Open Images Directory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_image), QCoreApplication.translate("MainWindow", u"Get Images", None))
        self.about_label.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), QCoreApplication.translate("MainWindow", u"About", None))
        self.exit_button.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.open_file_location_button.setText(QCoreApplication.translate("MainWindow", u"Open file location", None))
    # retranslateUi

