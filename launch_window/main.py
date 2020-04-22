import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QApplication

from app import Psy
from app.func import Func
from lib import MessageBox, Settings
from .file_button_area import FileButtonArea
from .file_path_table import FilePathTable


class LaunchWindow(QWidget):
    def __init__(self):
        super(LaunchWindow, self).__init__()
        # title
        self.setWindowTitle("Welcome to PsyBuilder")
        self.setFixedSize(820, 450)
        self.setStyleSheet("background:rgb(245,245,245)")
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        # widget file_table and file frame
        self.file_path_table = FilePathTable()
        self.file_path_table.filePathClicked.connect(self.handleFileClicked)
        self.file_path_table.filePathDeleted.connect(self.handleFileDeleted)
        # load file paths from config
        self.loadFilePaths()
        self.file_button_area = FileButtonArea()
        self.file_button_area.fileCreated.connect(self.handleFileCreated)
        self.file_button_area.fileOpened.connect(self.handleFileOpened)
        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        if self.file_path_table.rowCount():
            layout.addWidget(self.file_path_table, 2)
            layout.addWidget(self.file_button_area, 3, Qt.AlignHCenter)
        else:
            layout.addWidget(self.file_button_area, 1, Qt.AlignHCenter)
        self.setLayout(layout)
        # data
        self.opening = False

    def loadFilePaths(self):
        """
        load file list from config
        :return:
        """
        file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
        for file_path in file_paths:
            self.file_path_table.addFilePath(-1, file_path)

    def startPsy(self):
        """
        start app
        :param file_path:
        :return:
        """
        if self.opening:
            return
        self.opening = True
        QApplication.restoreOverrideCursor()
        psy = Psy()
        psy.showMaximized()
        self.close()
        self.opening = False

    def handleFileCreated(self, file_path: str):
        """
        change config and start software
        :param dir:
        :return:
        """
        # change config
        file_directory = os.path.dirname(file_path)
        Settings("config.ini", Settings.IniFormat).setValue("file_path", file_path)
        Settings("config.ini", Settings.IniFormat).setValue("new", True)
        Settings("config.ini", Settings.IniFormat).setValue("file_directory", file_directory)
        # change file_paths
        file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
        if file_path not in file_paths:
            file_paths.insert(0, file_path)
        else:
            # move it to first
            file_paths.remove(file_path)
            file_paths.insert(0, file_path)
        Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)
        # start psy application
        self.startPsy()

    def handleFileOpened(self, file_path: str):
        """
        change config and start software(then restore it from file)
        :param file_path:
        :return:
        """
        # change file_paths
        file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
        if file_path not in file_paths:
            file_paths.insert(0, file_path)
        else:
            # move it to first
            file_paths.remove(file_path)
            file_paths.insert(0, file_path)
        Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)
        # change file_path and file_directory
        Settings("config.ini", Settings.IniFormat).setValue("file_path", file_path)
        Settings("config.ini", Settings.IniFormat).setValue("file_directory", os.path.dirname(file_path))
        # start psy
        self.startPsy()

    def handleFileDeleted(self, file_path: str):
        """
        delete data in config
        :param file_path:
        :return:
        """
        file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
        if file_path in file_paths:
            file_paths.remove(file_path)
            Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)

    def handleFileClicked(self, file_path: str):
        """
        open file if file existed
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            Settings("config.ini", Settings.IniFormat).setValue("file_path", file_path)
            Settings("config.ini", Settings.IniFormat).setValue("file_directory", os.path.dirname(file_path))
            self.startPsy()
        else:
            MessageBox.information(self, "Error", f"The path '{file_path}' does not exist.")
