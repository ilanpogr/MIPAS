
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

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)
        if value >= 100:
            self.progressBar.setValue(0)

    def update_status(self, value):
        self.status_label.setText(self._translate("MainWindow", value))

    def update_task(self, value):
        self.task_label.setText(self._translate("MainWindow", value))


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
        print("PROPERTIES FOUND...")
        mipas_app = MipasApp()
        mipas_app.show()
    else:
        print("PROPERTIES NOT FOUND...")
        window = Welcome()
        window.show()
    sys.exit(app.exec_())

