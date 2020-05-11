import os

from PyQt5 import QtWidgets, QtCore
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QDesktopWidget
import resultsTable.resultsExctractor as resultsExtractor
from resultsTable.Table import PandasModel

results_file = "resources/photos/final_results.csv"
background_image = ":/resources/images/DIAMOND-BANNER.png"


def set_initial_screen(main_window):
    main_window.setWindowTitle("MIPAS")
    main_window.status_lbl.setText("IDLE")
    main_window.resize(700, 350)
    main_window.pushButton.setVisible(False)
    qr = main_window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_window.move(qr.topLeft())

def connect_results_to_table(table):
    if os.path.isfile(results_file):
        df = get_results_as_df()
        model = PandasModel(df)
        table.setModel(model)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(1)
        table.doubleClicked.connect(resultsExtractor.ResultsExtractor.open_link)


def connect_welcome_buttons(welcome_screen):
    welcome_screen.next_page2.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(1))
    welcome_screen.next_page3.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(2))
    welcome_screen.next_page4.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(3))
    welcome_screen.next_page5.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(4))
    welcome_screen.next_page6.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(5))
    welcome_screen.prev_page1.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(0))
    welcome_screen.prev_page2.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(1))
    welcome_screen.prev_page3.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(2))
    welcome_screen.prev_page4.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(3))
    welcome_screen.prev_page5.clicked.connect(lambda: welcome_screen.stackedWidget.setCurrentIndex(4))
    welcome_screen.dataset_path.clicked.connect(lambda: _open_file_dialog(welcome_screen))
    retranslate_welcome_ui(welcome_screen)

    # todo - for mock-up!  ---- DEMO
    welcome_screen.store_names.setText("Store-A,Store-B")
    welcome_screen.store_main_category.setText("jewelry")
    welcome_screen.store_sub_categories.setText("necklaces,earrings,bracelets,rings")
    welcome_screen.path_str.setText("/Users/ipogrebinsky/Documents/School/Final Project/Artisan Pictures_mini")


def _open_file_dialog(welcome_screen):
    directory = str(QtWidgets.QFileDialog.getExistingDirectory(caption="Select Folder With All Your Pictures", directory=str(Path.home())))
    if directory:
        welcome_screen.path_str.setText('{}'.format(directory))


def retranslate_welcome_ui(welcome_screen):
    _translate = QtCore.QCoreApplication.translate
    welcome_screen.setWindowTitle("MIPAS - Configure Settings")


def change_run_method(main_screen):
    _translate = QtCore.QCoreApplication.translate
    state = main_screen.comboBox.currentText()
    if state == "Start New Search":
        main_screen.run_option = 0
    elif state == "Search Found Stores From Previous Run":
        main_screen.run_option = 1
    elif state == "Compare Only With What I Got":
        main_screen.run_option = 2
    main_screen.method_label.setText(_translate("MainWindow", state))
    main_screen.method_label_2.setText(_translate("MainWindow", state))


def get_results_as_df():
    results = resultsExtractor.ResultsExtractor(results_file)
    return results.read_results()



