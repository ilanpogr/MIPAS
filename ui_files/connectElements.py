import os
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget

import resultsTable.resultsExctractor as resultsExtractor

results_file = "resources/photos/final_results.csv"


# background_image = ":/resources/images_app/DIAMOND-BANNER.png"


def set_initial_screen(main_window):
    main_window.setWindowTitle("MIPAS")
    # main_window.status_lbl.setText("IDLE")
    main_window.stackedWidget.setCurrentIndex(0)
    # main_window.resize(1532, 700)
    main_window.pushButton.setVisible(False)
    main_window.back_btn.clicked.connect(lambda: main_window.stackedWidget.setCurrentIndex(0))
    main_window.export_btn.setFixedHeight(40)
    main_window.back_btn.setFixedHeight(40)
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
    push_button.setText("Show\nReport")
    push_button.setStyleSheet(
        "QPushButton#pushButton { background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture.jpg) 0 0 0 0 stretch stretch; "
        "color: #671115; "
        "border-style: outset; "
        "border-width: 2px; "
        "border-radius: 50px; "
        "border-color: beige; "
        "font: bold 30px; "
        # "min-width: 5em; "
        "padding: 40px; } "
        "QPushButton#pushButton:hover { color: black; "
        "border-width: 3px;"
        "border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}"
        "QPushButton#pushButton:pressed {"
        "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);"
        "background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture_dark.jpg)}")
    # push_button.setStyleSheet(
    #     "QPushButton#pushButton { background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture.jpg) 0 0 0 0 stretch stretch; "
    #     "border-style: outset; "
    #     "border-width: 2px; "
    #     "border-radius: 10px; "
    #     "border-color: beige; "
    #     "color: #722f37; "
    #     "font: bold 14px; "
    #     "min-width: 10em; "
    #     "padding: 6px; } "
    #     "QPushButton#pushButton:hover { color: black; "
    #     "border-width: 3px;"
    #     "border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);}"
    #     "QPushButton#pushButton:pressed {"
    #     "background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);"
    #     "background-image: url(/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/Prestige-texture_dark.jpg)}")


def set_colors_to_elements(main_window):
    # Main Window background Image
    background_image = "/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/DIAMONDS-BANNER_crop.png"
    main_window.setStyleSheet("#MainWindow { border-image: url(%s) 0 0 0 0 stretch stretch;"
                              "background-color: #222222; }" % background_image)
    # Frames borders
    # main_window.frame.setStyleSheet("border: 0")
    # Title
    main_window.label_5.setStyleSheet("color: #ffe34c; font: bold 70px; ")
    main_window.label_6.setStyleSheet("color: #ffe34c; font: 25px; ")
    # labels
    main_window.label.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_2.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.matches_found.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_3.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_4.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.susp_stores_lbl.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_7.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.current_store_lbl.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_8.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.known_stores_lbl.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_9.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.kknown_prod_lbl.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.label_10.setStyleSheet("color: #EEEEEE; font: 20px; ")
    main_window.examined_prod_lbl.setStyleSheet("color: #EEEEEE; font: 20px; ")
    # Button Show Report
    set_button_stylesheet(main_window.pushButton)
    main_window.stackedWidget.setStyleSheet(
        "QStackedWidget QTableWidget#Page1 QHeaderView::section {"
        " background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
        " stop:0 #616161, stop: 0.5 #505050,"
        " stop: 0.6 #434343, stop:1 #656565);"
        " color: white;"
        " padding-left: 4px;"
        " border: 1px solid #6c6c6c;"
        "}")
    # Table
    main_window.tableView.setStyleSheet("QTableView { background-color: #383838;"
                                        "gridline-color: #000000;"
                                        "}"
                                        "QHeaderView::section {"
                                        "background-color: #708090;"
                                        "padding: 4px;"
                                        "}"
                                        "QTableView QTableCornerButton::section { background: #708090;"
                                        "border: 1px inset #708090;"
                                        "}"
                                        "QHeaderView { font-size: 20pt; "
                                        "qproperty-defaultAlignment: AlignHCenter;"
                                        "background-color: #383838;"
                                        "}")
    # Button Export
    main_window.export_btn.setObjectName("button_export")
    icon_path = '/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/export-icon.png'
    icon = QIcon(icon_path)
    main_window.export_btn.setIcon(icon)
    main_window.export_btn.setStyleSheet("QPushButton#button_export { "
                                         "color: #333; "
                                         "font-weight: bold;"
                                         "border: 2px solid #555; "
                                         "border-radius: 20px; "
                                         "border-style: outset; "
                                         "background: qradialgradient( "
                                         "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                         "radius: 1.35, stop: 0 #fff, stop: 1 #8d2663 "
                                         "); "
                                         "padding: 60px; "
                                         "} "
                                         "QPushButton#button_export:hover { "
                                         "background: qradialgradient( "
                                         "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                         "radius: 1.35, stop: 0 #fff, stop: 1 #7e2259 "
                                         "); "
                                         "} "
                                         "QPushButton#button_export:pressed { "
                                         "border-style: inset; "
                                         "background: qradialgradient( "
                                         "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                         "radius: 1.35, stop: 0 #e5e5e5, stop: 1 #701e4f "
                                         "); "
                                         "}")
    # Button Back
    main_window.back_btn.setObjectName("button_back")
    main_window.back_btn.setStyleSheet("QPushButton#button_back { "
                                       "color: #333; "
                                       "border: 2px solid #555; "
                                       "border-radius: 20px; "
                                       "border-style: outset; "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #fff, stop: 1 #888 "
                                       "); "
                                       "padding: 5px; "
                                       "} "
                                       "QPushButton#button_back:hover { "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #fff, stop: 1 #7a7a7a "
                                       "); "
                                       "} "
                                       "QPushButton#button_back:pressed { "
                                       "border-style: inset; "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #e5e5e5, stop: 1 #6d6d6d "
                                       "); "
                                       "}")
    # Button Refresh
    main_window.refresh_btn.setObjectName("refresh_btn")
    icon_path = '/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/refresh.png'
    icon = QIcon(icon_path)
    main_window.refresh_btn.setIcon(icon)
    main_window.refresh_btn.setIconSize(QSize(28, 28))
    main_window.refresh_btn.setStyleSheet("QPushButton#refresh_btn { "
                                       "color: #333; "
                                       "border: 2px solid #555; "
                                       "border-radius: 21px; "
                                       "border-style: outset; "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #fff, stop: 1 #7ec490 "
                                       "); "
                                       "padding: 5px; "
                                       "} "
                                       "QPushButton#refresh_btn:hover { "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #fff, stop: 1 #71b081 "
                                       "); "
                                       "} "
                                       "QPushButton#refresh_btn:pressed { "
                                       "border-style: inset; "
                                       "background: qradialgradient( "
                                       "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, "
                                       "radius: 1.35, stop: 0 #e5e5e5, stop: 1 #649c73 "
                                       "); "
                                       "}")
    # main_window.export_btn.setStyleSheet("QPushButton#button_export { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383838, stop: 1 #8d2663); "
    #                                      "color: white;"
    #                                      "font-weight: bold;"
    #                                      "font-size: 16px;"
    #                                      "width: 120"
    #                                      "border-style: solid;"
    #                                      "border-color: black;"
    #                                      "border-width: 5px;"
    #                                      "border-radius: 10px;"
    #                                      "}"
    #                                      "QPushButton#button_export:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2c2c2c, stop: 1 #621a45); "
    #                                      "color: #DCDCDC;"
    #                                      "}")
    # main_window.back_btn.setStyleSheet("QPushButton#button_back { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #383838, stop: 1 #8d2663); "
    #                                    "color: white;"
    #                                    "font-size: 16px;"
    #                                    "width: 120"
    #                                    "border-style: solid;"
    #                                    "border-color: black;"
    #                                    "border-width: 5px;"
    #                                    "border-radius: 10px;"
    #                                    "}"
    #                                    "QPushButton#button_back:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2c2c2c, stop: 1 #621a45); "
    #                                    "color: #DCDCDC;"
    #                                    "font-size: 16px;"
    #                                    "}")
