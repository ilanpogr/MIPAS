from PyQt5 import QtWidgets, QtCore
from pathlib import Path


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

    # for mockup!  ---- DEMO
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
    state = main_screen.comboBox.currentText()
    if state == "Start New Search":
        main_screen.run_option = 0
    elif state == "Search Found Stores From Previous Run":
        main_screen.run_option = 1
    elif state == "Compare Only With What I Got":
        main_screen.run_option = 2


def connect_main_window_elements(main_screen):
    main_screen.setWindowTitle("MIPAS")
    main_screen.progressBar.setValue(0)
    _translate = QtCore.QCoreApplication.translate
    main_screen.method_label.setText(_translate("MainWindow", main_screen.comboBox.currentText()))
    main_screen.comboBox.currentIndexChanged.connect(lambda: change_run_method(main_screen))
    main_screen.start_btn.clicked.connect(lambda: main_screen.stackedWidget.setCurrentIndex(1))


