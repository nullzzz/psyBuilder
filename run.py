import os
import sys

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication

from app import Psy
from launch import LaunchWindow
from lib import Settings
from source.qss import default_qss
from validation.main import ValidationWindow


class V(ValidationWindow):
    def start(self):
        # check open mode
        open_mode = Settings("config.ini", Settings.IniFormat).value("open_mode", "default mode")
        if open_mode == "default mode":
            # default open mode
            launch_window.show()
        else:
            # open a blank file directly
            Settings("config.ini", Settings.IniFormat).setValue("file_path", "")
            Settings("config.ini", Settings.IniFormat).setValue("file_directory", "")
            psy = Psy()
            psy.showMaximized()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # set qss and font
    QFontDatabase.addApplicationFont(os.path.abspath("source/fonts/GenShinGothic-Light.ttf"))
    app.setStyleSheet(default_qss)
    # launch window, this var must be defined here, otherwise it won't show.
    launch_window = LaunchWindow()
    # launch_window.show()
    v = V()
    sys.exit(app.exec_())
