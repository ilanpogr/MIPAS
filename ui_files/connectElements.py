import os

from PyQt5 import QtWidgets, QtCore
from pathlib import Path

from PyQt5.QtWidgets import QDesktopWidget
import resultsTable.resultsExctractor as resultsExtractor

results_file = "resources/photos/final_results.csv"
background_image = ":/resources/images_app/DIAMOND-BANNER.png"


def set_colors_to_elements(main_window):
    # Frames borders
    main_window.frame.setStyleSheet("border: 0")
    # Title
    main_window.label_5.setStyleSheet("color: #ffe34c")
    main_window.label_6.setStyleSheet("color: #ffe34c")
    # labels
    main_window.label.setStyleSheet("color: #EEEEEE")
    main_window.label_2.setStyleSheet("color: #EEEEEE")
    main_window.matches_found.setStyleSheet("color: #EEEEEE")
    main_window.label_3.setStyleSheet("color: #EEEEEE")
    # Button
    set_button_stylesheet(main_window.pushButton)


def set_initial_screen(main_window):
    main_window.setWindowTitle("MIPAS")
    # main_window.status_lbl.setText("IDLE")
    main_window.resize(700, 350)
    main_window.pushButton.setVisible(False)
    qr = main_window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    main_window.move(qr.topLeft())
    set_colors_to_elements(main_window)


def get_data_for_table():
    if os.path.isfile(results_file):
        results = resultsExtractor.ResultsExtractor(results_file)
        return results.read_results()


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
    directory = str(QtWidgets.QFileDialog.getExistingDirectory(caption="Select Folder With All Your Pictures",
                                                               directory=str(Path.home())))
    if directory:
        welcome_screen.path_str.setText('{}'.format(directory))


def retranslate_welcome_ui(welcome_screen):
    _translate = QtCore.QCoreApplication.translate
    welcome_screen.setWindowTitle("MIPAS - Configure Settings")


# def change_run_method(main_screen):
#     _translate = QtCore.QCoreApplication.translate
#     state = main_screen.comboBox.currentText()
#     if state == "Start New Search":
#         main_screen.run_option = 0
#     elif state == "Search Found Stores From Previous Run":
#         main_screen.run_option = 1
#     elif state == "Compare Only With What I Got":
#         main_screen.run_option = 2
#     main_screen.method_label.setText(_translate("MainWindow", state))
#     main_screen.method_label_2.setText(_translate("MainWindow", state))


def set_button_stylesheet(push_button):
    texture_path = "/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture.jpg"
    push_button.setStyleSheet(
        "QPushButton#pushButton { background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture.jpg) 0 0 0 0 stretch stretch; "
        "border-style: outset; "
        "border-width: 2px; "
        "border-radius: 10px; "
        "border-color: beige; "
        "color: #722f37; "
        "font: bold 14px; "
        "min-width: 10em; "
        "padding: 6px; } "
        "QPushButton#pushButton:hover { color: black; "
        "border-width: 3px;"
        "border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}"
        "QPushButton#pushButton:pressed {"
        "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);"
        "background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture_dark.jpg)}")