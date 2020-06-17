import os
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

import resultsTable.resultsExctractor as resultsExtractor

results_file = "resources/photos/final_results.csv"


def set_initial_screen(main_window):
    main_window.setWindowTitle("MIPAS")
    main_window.label_3.setText("Please wait, configuring data.")
    main_window.stackedWidget.setCurrentIndex(0)
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

    # for mock-up!  ---- DEMO
    # welcome_screen.store_names.setText("Store-A,Store-B")
    # welcome_screen.store_main_category.setText("jewelry")
    # welcome_screen.store_sub_categories.setText("necklaces,earrings,bracelets,rings")
    # welcome_screen.path_str.setText("F:/avi/test_image_maching/tmpCustomer")


def _open_file_dialog(welcome_screen):
    directory = str(QtWidgets.QFileDialog.getExistingDirectory(caption="Select Folder With All Your Pictures",
                                                               directory=str(Path.home())))
    if directory:
        welcome_screen.path_str.setText('{}'.format(directory))


def retranslate_welcome_ui(welcome_screen):
    _translate = QtCore.QCoreApplication.translate
    welcome_screen.setWindowTitle("MIPAS - Configure Settings")


def set_button_stylesheet(push_button):
    # Show Report button
    push_button.setText("Report")
    push_button.setStyleSheet(
        "QPushButton#pushButton { "
        "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #5B5B5B, stop:1 #EDEDED);"
        "font: bold 23px 'verdana';"
        "color: #333325;"
        "padding: 10; "
        "height: 40px;"
        "width: 120px;"
        "border: 3px solid;"
        "border-color: #8C8E81;"
        "border-radius: 14px;"
        "border-style: outset;"
        "}"
        "QPushButton#pushButton:hover { "
        "color: #454542;"
        "}"
        "QPushButton#pushButton:pressed {"
        "font: bold 22px 'verdana';"
        "text-align: center;"
        "display: inline-block;"
        "border-style: inset;"
        "}"
    )


def set_colors_to_elements(main_window):
    # Main Window background Image
    background_image = "/Users/ipogrebinsky/Documents/School/Final Project/GUI/MIPAS/resources/images_app/DIAMONDS-BANNER_crop.png"
    main_window.setStyleSheet("#MainWindow { border-image: url(%s) 0 0 0 0 stretch stretch;"
                              "background-color: #222222; }" % background_image)
    # Title
    main_window.label_5.setStyleSheet("color: #ffe34c; font: bold 70px 'Recoleta';")
    main_window.label_6.setStyleSheet("color: #ffe34c; font: 25px 'Trajan'; ")
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
    main_window.export_btn.setIcon(QIcon(icon_path))
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
    main_window.refresh_btn.setIcon(QIcon(icon_path))
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

def set_style_for_welcome_screen(welcome):
    welcome.centralwidget.setStyleSheet("QPushButton { "
                                     "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #5B5B5B, stop:1 #EDEDED);"
                                     "color: #333325;"
                                     "font: bold 12px 'verdana';"
                                     "padding: 10; "
                                     "width: 100%;"
                                     "border: 3px solid;"
                                     "border-color: #8C8E81;"
                                     "border-radius: 14px;"
                                     "border-style: outset;"
                                     "}"
                                     "QPushButton:hover { "
                                     "color: #454542;"
                                     "}"
                                     "QPushButton:pressed { "
                                     "font: bold 11px 'verdana';"
                                     "text-align: center;"
                                     "border-style: inset;"
                                     "}"
                                     "QToolButton { "
                                     "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #5B5B5B, stop:1 #EDEDED);"
                                     "color: #333325;"
                                     "font: 10px 'verdana';"
                                     "padding: 4; "
                                     "border: 3px solid;"
                                     "border-color: #8C8E81;"
                                     "border-radius: 8px;"
                                     "border-style: outset;"
                                     "}"
                                     "QToolButton::hover { "
                                     "color: #454542;"
                                     "}"
                                     "QToolButton:pressed { "
                                     "font: 9px 'verdana';"
                                     "text-align: center;"
                                     "border-style: inset;"
                                     "}")
    welcome.finish_settings.setStyleSheet("QPushButton { "
                                       "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #54163b, stop:1 #8d2663);"
                                       "color: #e5e5e5;"
                                       "font: bold 12px 'verdana';"
                                       "padding: 10; "
                                       "border: 3px solid;"
                                       "border-color: #8C8E81;"
                                       "border-radius: 14px;"
                                       "border-style: outset;"
                                       "}"
                                       "QPushButton::hover { "
                                       "color: #b2b2b2;"
                                       "}"
                                       "QPushButton:pressed { "
                                       "font: bold 11px 'verdana';"
                                       "text-align: center;"
                                       "border-style: inset;"
                                       "}")
    welcome.next_page2.setStyleSheet("QPushButton { "
                                     "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #5B5B5B, stop:1 #EDEDED);"
                                     "color: #333325;"
                                     "font: bold 12px 'verdana';"
                                     "padding: 10; "
                                     "width: 100%;"
                                     "border: 3px solid;"
                                     "border-color: #8C8E81;"
                                     "border-radius: 14px;"
                                     "border-style: outset;"
                                     "}"
                                     "QPushButton:hover { "
                                     "color: #454542;"
                                     "}"
                                     "QPushButton:pressed { "
                                     "font: bold 11px 'verdana';"
                                     "text-align: center;"
                                     "border-style: inset;"
                                     "}"
                                     "QToolButton { "
                                     "background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,stop:0 #5B5B5B, stop:1 #EDEDED);"
                                     "color: #333325;"
                                     "font: bold 12px 'verdana';"
                                     "padding: 10; "
                                     "border: 3px solid;"
                                     "border-color: #8C8E81;"
                                     "border-radius: 14px;"
                                     "border-style: outset;"
                                     "}"
                                     "QToolButton::hover { "
                                     "color: #454542;"
                                     "}"
                                     "QToolButton:pressed { "
                                     "font: bold 11px 'verdana';"
                                     "text-align: center;"
                                     "border-style: inset;"
                                     "}")
