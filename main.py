import os
from functools import partial

from PyQt5.QtCore import QSize, QThreadPool, QThread

from controllers.threadCreation import Worker, ThreadController
from controllers.ReaderWriterLockManager import LockManager
from resultsTable import Table
from ui_files import mainWindow, connectElements
from ui_files.welcome import welcomeSettings_v2
import configUtils
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
import sys
import time



class MipasApp(mainWindow.Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, welcome=False, *args, **kwargs):
        if not welcome:
            super(MipasApp, self).__init__(*args, **kwargs)
        else:
            super(MipasApp, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_result_button_clicked)
        self.results_dialog = None
        connectElements.set_initial_screen(self)
        self.last_num_of_results = 0
        self.current_num_of_results = 0
        self.task_changed = False
        self.check_results()
        self.num_of_stores = None

        self.controller = ThreadController(self)

    def check_results(self):
        results_path = "resources/photos/final_results.csv"
        if os.path.exists(results_path):
            lock_manager = LockManager()
            lines = lock_manager.read_results(results_path)
            if len(lines) > 1:
                self.update_matches(len(lines) - 1)
                self.current_num_of_results = len(lines) - 1
            else:
                self.update_matches(None)
                self.current_num_of_results = 0

    def start_timer(self, value):
        self.label_3.setText("Starting in {}".format(value))

    def change_task(self, value):
        self.task_changed = value

    def search_for_stores(self, value):
        self.label_3.setText("Searching for shops in Etsy platform{}".format(value))

    def explore_stores(self, value):
        if self.num_of_stores is None:
            self.num_of_stores = value.split('/')[1]
        self.check_results()
        self.label_3.setText("Exploring products for found store - {0}".format(value))

    def update_matches(self, value):
        if value is None:
            self.matches_found.setText("None")
            self.pushButton.setVisible(False)
        else:
            self.matches_found.setText(str(value))
            if not self.pushButton.isVisible():
                self.pushButton.setVisible(True)

    def on_result_button_clicked(self):
        if self.last_num_of_results != self.current_num_of_results:
            self.last_num_of_results = self.current_num_of_results
            data = connectElements.get_data_for_table()
            self.results_dialog = Table.Results(data)
            size = self.results_dialog.geometry()
            self.results_dialog.resize(size.width(), 800)
        self.results_dialog.statusBar().showMessage("")
        self.results_dialog.show()


class Welcome(welcomeSettings_v2.Ui_MainWindow, QMainWindow):

    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)
        QMainWindow.__init__(self)
        self.ui = welcomeSettings_v2.Ui_MainWindow()
        self.setupUi(self)
        self.__done_config = False
        connectElements.connect_welcome_buttons(self)
        self.finish_settings.clicked.connect(lambda: self.finish_settings_configuration())

    def finish_settings_configuration(self):
        if configUtils.is_all_settings_configured(self):
            configUtils.create_config_file("Etsy", self.store_names.text(), self.store_main_category.text(),
                                           self.store_sub_categories.text(), self.path_str.text())
            self.hide()
            self.__start_app()

    def __start_app(self):
        main = MipasApp(self, True)
        main.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if configUtils.is_settings_file_exists():
        mipas_app = MipasApp()
        mipas_app.show()
    else:
        window = Welcome()
        window.show()
    sys.exit(app.exec_())
