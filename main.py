from controllers.threadCreation import ThreadController

from ui_files import mainWindow, connectElements
from ui_files.welcome import welcomeSettings_v2
import configUtils
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow

import sys


class MipasApp(mainWindow.Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, welcome=False, *args, **kwargs):
        if not welcome:
            super(MipasApp, self).__init__(*args, **kwargs)
        else:
            super(MipasApp, self).__init__(parent)
        self.setupUi(self)
        self._translate = QCoreApplication.translate
        connectElements.connect_main_window_elements(self)
        self.run_option = 0
        self.controller = ThreadController(self)

    def finished_crawler(self):
        self.update_status_pd("DONE")
        self.update_task_pd("Finished Downloading All Products For All Stores")
        self.im_progressBar_2.setValue(100)

    def update_progress_bar_sf(self, value):
        self.progressBar.setValue(value)
        if value >= 100:
            self.progressBar.setValue(0)

    def update_progress_bar_pd(self, value):  # todo - change in designer the progressBar ID!
        self.im_progressBar_2.setValue(value)
        if value >= 100:
            self.im_progressBar_2.setValue(0)

    def update_progress_bar_im(self, value):
        self.im_progressBar.setValue(value)
        if value >= 100:
            self.im_progressBar.setValue(0)

    def update_status_sf(self, value):
        self.status_label.setText(self._translate("MainWindow", value))

    def update_task_sf(self, value):
        self.task_label.setText(self._translate("MainWindow", value))

    def update_status_pd(self, value):
        self.pd_status_label.setText(self._translate("MainWindow", value))

    def update_task_pd(self, value):
        self.pd_task_label.setText(self._translate("MainWindow", value))

    def update_status_im(self, value):
        self.im_status_label.setText(self._translate("MainWindow", value))

    def update_task_im(self, value):
        self.im_task_label.setText(self._translate("MainWindow", value))

    def switch_to_parallel_screen(self):
        self.im_progressBar.setValue(0)
        self.im_progressBar_2.setValue(0)
        self.stackedWidget.setCurrentIndex(2)


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
            configUtils.create_config_file("Etsy", self.store_names.text(), self.store_main_category.text(), self.store_sub_categories.text(), self.path_str.text())
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

