import os
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import configUtils
from controllers.ReaderWriterLockManager import LockManager
from controllers.threadCreation import ThreadController
from resultsTable import Table
from ui_files import mainWindow, connectElements
from ui_files.welcome import welcomeSettings_v2


class MipasApp(mainWindow.Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, welcome=False, *args, **kwargs):
        if not welcome:
            super(MipasApp, self).__init__(*args, **kwargs)
        else:
            super(MipasApp, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_result_button_clicked)
        self.refresh_btn.clicked.connect(self.on_result_button_clicked)
        self.results_dialog = None
        connectElements.set_initial_screen(self)
        self.last_num_of_results = 0
        self.current_num_of_results = 0

        self.task_changed = False
        self.check_results()
        self.num_of_stores = None
        self.current_store_number = None
        self.first_run = True

        self.im_done = False
        self.id_done = False

        self.controller = ThreadController(self)

    def update_known_stores(self, value):
        self.num_of_stores = str(value)
        self.known_stores_lbl.setText(str(value))

    def update_current_store(self, value):
        if value is None or not value:
            self.current_store_lbl.setText("IDLE")
        if value.startswith("@%@") and self.current_store_lbl.text() == "IDLE":
            self.id_done = True
            self.current_store_lbl.setText(value[3:])
        elif not value.startswith("@%@"):
            self.current_store_lbl.setText(value)

    def update_known_products(self, value):
        self.kknown_prod_lbl.setText(str(value))

    def update_examined_products(self, value):
        self.check_results()
        prev = self.examined_prod_lbl.text()
        counter = 0
        if prev != "None":
            counter = int(prev)
        counter += value
        self.examined_prod_lbl.setText(str(counter))

    @staticmethod
    def get_num_of_susp_stores(lines):
        num_of_susp_stores = set()
        first_line = True
        for line in lines:
            if first_line:
                first_line = False
                continue
            num_of_susp_stores.add(line.split(",")[2].split('/')[-1])
        return str(len(num_of_susp_stores))

    def check_results(self):
        results_path = "resources/photos/final_results.csv"
        if os.path.exists(results_path):
            lock_manager = LockManager()
            lines = lock_manager.read_results(results_path)
            if len(lines) > 1:
                self.update_matches(len(lines) - 1)
                num = self.get_num_of_susp_stores(lines)
                self.susp_stores_lbl.setText(num)
                self.current_num_of_results = len(lines) - 1
            else:
                self.update_matches(None)
                self.current_num_of_results = 0

    def start_timer(self, value):
        self.id_done = False
        if self.first_run:
            self.label_3.setText("Starting in {}".format(value))
        else:
            self.label_3.setText("Starting another run in {}".format(value))

    def change_task(self, value):
        # change label colors
        if not value:
            self.label_7.setStyleSheet("color: #999999; font: 20px; ")
            self.current_store_lbl.setStyleSheet("color: #999999; font: 20px; ")
            self.label_10.setStyleSheet("color: #999999; font: 20px; ")
            self.examined_prod_lbl.setStyleSheet("color: #999999; font: 20px; ")
            self.label_9.setStyleSheet("color: #999999; font: 20px; ")
            self.kknown_prod_lbl.setStyleSheet("color: #999999; font: 20px; ")
            self.label_8.setStyleSheet("color: #ffffff; font: 20px; ")
            self.known_stores_lbl.setStyleSheet("color: #ffffff; font: 20px; ")
        else:
            self.label_7.setStyleSheet("color: #ffffff; font: 20px; ")
            self.current_store_lbl.setStyleSheet("color: #ffffff; font: 20px; ")
            self.label_10.setStyleSheet("color: #ffffff; font: 20px; ")
            self.examined_prod_lbl.setStyleSheet("color: #ffffff; font: 20px; ")
            self.label_9.setStyleSheet("color: #ffffff; font: 20px; ")
            self.kknown_prod_lbl.setStyleSheet("color: #ffffff; font: 20px; ")
            self.label_8.setStyleSheet("color: #999999; font: 20px; ")
            self.known_stores_lbl.setStyleSheet("color: #999999; font: 20px; ")
        if self.first_run and value:
            self.first_run = False
        self.task_changed = value

    def search_for_stores(self, value):
        self.label_3.setText("Searching for shops in Etsy platform - using {}".format(value))

    def explore_stores(self, value):
        split = value.split('/')
        if self.num_of_stores is None:
            self.num_of_stores = split[1]
        self.current_store_number = split[0]
        if value.startswith("@%@") and self.id_done:
            self.label_3.setText("Comparing products from found store - {0}/{1}".format(split[0][3:], self.num_of_stores))
        elif not value.startswith("@%@"):
            self.label_3.setText("Exploring products from found store - {0}/{1}".format(split[0], self.num_of_stores))

    def run_finished(self):
        self.label_3.setText("IDLE")
        self.controller = ThreadController(self)

    def update_matches(self, value):
        if value is None:
            self.matches_found.setText("None")
            self.pushButton.setVisible(False)
            self.susp_stores_lbl.setText("None")
        else:
            self.matches_found.setText(str(value))
            if not self.pushButton.isVisible():
                self.pushButton.setVisible(True)

    def on_result_button_clicked(self):
        if self.last_num_of_results != self.current_num_of_results:
            self.last_num_of_results = self.current_num_of_results
        data = connectElements.get_data_for_table()
        self.results_dialog = Table.Results(data, self.tableView, self.export_btn)
        self.stackedWidget.setCurrentIndex(1)


class Welcome(welcomeSettings_v2.Ui_MainWindow, QMainWindow):

    def __init__(self, parent=None):
        super(Welcome, self).__init__(parent)
        QMainWindow.__init__(self)
        self.ui = welcomeSettings_v2.Ui_MainWindow()
        self.setupUi(self)
        self.__done_config = False
        connectElements.connect_welcome_buttons(self)
        connectElements.set_style_for_welcome_screen(self)
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
    # time.sleep(5)
    app = QtWidgets.QApplication(sys.argv)
    if configUtils.is_settings_file_exists():
        mipas_app = MipasApp()
        mipas_app.show()
    else:
        window = Welcome()
        window.show()
    sys.exit(app.exec_())
