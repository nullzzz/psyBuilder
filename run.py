import os
import re
import sys

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QApplication, QFileDialog, QLabel, QMenu, QGridLayout, \
    QFrame

from app import Psy
from app.func import Func
from lib import MessageBox, TableWidget, HoverButton, Settings
from qss import qss


class Version(QTextEdit):
    def __init__(self, name: str, version: str):
        super(Version, self).__init__()
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
                QTextEdit{
                    border:none;
                }
                """)
        # set text
        self.setAlignment(Qt.AlignHCenter)
        self.setText(f"""
        <div style="text-align: center;">
            <b style="font:36px;vertical-align: middle;">{name}</b><br />
            <b style="color:rgb(157,157,157); font:18px;vertical-align: middle;">{version}</b>
        </div>
        """)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def enterEvent(self, QEvent):
        super(Version, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def leaveEvent(self, QEvent):
        super(Version, self).leaveEvent(QEvent)
        QApplication.restoreOverrideCursor()


class FilePath(QTextEdit):
    clicked = pyqtSignal()

    def __init__(self, file_path: str):
        # style
        super(FilePath, self).__init__()
        self.setStyleSheet("""
        QTextEdit{
            border:none;
            padding-left:10px;
        }
        QTextEdit:hover{
            border-radius:2px;
            border: 1px solid rgb(110, 110, 110);
        }
        """)
        self.file_path = file_path
        file_name = os.path.basename(file_path)
        self.setText(f"""<b style="color:rgb(31,31,31)">{file_name}</b>""")
        if os.path.exists(file_path):
            self.append(f"""<p style="color:rgb(157,157,157); font:12px">{file_path}</p>""")
        else:
            self.append(f"""<p style="color:rgb(142,15,15); font:12px">{file_path}</p>""")
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mousePressEvent(self, QMouseEvent):
        super(FilePath, self).mousePressEvent(QMouseEvent)
        self.clicked.emit()

    def enterEvent(self, QEvent):
        super(FilePath, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def leaveEvent(self, QEvent):
        super(FilePath, self).leaveEvent(QEvent)
        QApplication.restoreOverrideCursor()


class FilePathTable(TableWidget):
    """
    show some recent files
    """
    # emit file path
    filePathClicked = pyqtSignal(str)
    filePathDeleted = pyqtSignal(str)

    def __init__(self):
        super(FilePathTable, self).__init__()
        self.setShowGrid(False)
        self.setStyleSheet("border:none;border-right:1px solid rgb(236,236,236);background:white;")
        # hide headers
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        # one column
        self.setColumnCount(2)
        self.setColumnWidth(0, 298)
        self.setColumnWidth(1, 20)

    def addFilePath(self, index: int, file_path: str):
        """
        add file into table
        :param index:
        :param file_name:
        :param file_path:
        :return:
        """
        # add new row
        if index == -1:
            index = self.rowCount()
        self.insertRow(index)
        self.setRowHeight(index, 56)
        # insert line edit into table
        file = FilePath(file_path)
        self.setCellWidget(index, 0, file)
        file.clicked.connect(lambda: self.filePathClicked.emit(file_path))
        # button
        delete_button = HoverButton("menu/close")
        self.setCellWidget(index, 1, delete_button)
        delete_button.clicked.connect(lambda checked: self.handleFileDeleted(file_path))

    def handleFileDeleted(self, file_path):
        """

        :param checked:
        :return:
        """
        self.filePathDeleted.emit(file_path)
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).file_path == file_path:
                self.removeRow(row)
                break
        if not self.rowCount():
            self.hide()


class FileButtonArea(QWidget):
    fileCreated = pyqtSignal(str)
    fileOpened = pyqtSignal(str)

    def __init__(self):
        super(FileButtonArea, self).__init__()
        # widget
        icon = QLabel()
        icon.setPixmap(Func.getImageObject("common/icon.png", type=0, size=QSize(60, 60)))
        # menu
        self.menu = QMenu()
        self.default_mode_action = self.menu.addAction(Func.getImageObject("menu/checked", 1), "Default Mode",
                                                       lambda: self.changeOpenMode("default mode"))
        self.open_blank_file_action = self.menu.addAction(Func.getImageObject("menu/checked", 1),
                                                          "Open Blank File",
                                                          lambda: self.changeOpenMode("open blank file"))
        open_mode = Settings("config.ini", Settings.IniFormat).value("open_mode", "default mode")
        self.changeOpenMode(open_mode)
        # buttons
        create_button = HoverButton("menu/add", "Create New File")
        create_button.clicked.connect(self.handleCreateButtonClicked)
        open_button = HoverButton("menu/open", "Open")
        open_button.clicked.connect(self.handleOpenButtonClicked)
        setting_button = HoverButton("menu/setting", "Change Open Mode")
        setting_button.clicked.connect(
            lambda checked: self.menu.exec(self.mapToGlobal(setting_button.pos())))
        # layout
        layout = QGridLayout()
        for i in range(6):
            layout.setColumnStretch(i, 1)
        layout.addWidget(icon, 0, 1, 1, 5, Qt.AlignHCenter)
        layout.setRowStretch(0, 13)
        layout.addWidget(Version("Psy Builder", "Version 0.1"), 1, 1, 1, -1)
        layout.setRowStretch(1, 12)
        layout.addWidget(create_button, 2, 2, 1, 2, Qt.AlignLeft)
        layout.setRowStretch(2, 1)
        layout.addWidget(open_button, 3, 2, 1, 2, Qt.AlignLeft)
        layout.setRowStretch(3, 1)
        layout.addWidget(setting_button, 4, 2, 1, 2, Qt.AlignLeft)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 20)
        self.setLayout(layout)

    def handleCreateButtonClicked(self, checked):
        """

        :return:
        """
        directory = Settings("config.ini", Settings.IniFormat).value("file_directory", "")
        if not directory:
            directory = os.getcwd()
        file_path, _ = QFileDialog().getSaveFileName(self, "Create file", directory, "Psy Files (*.psy);")
        if file_path:
            if not re.search(r"\.psy$", file_path):
                file_path = file_path + ".psy"
            self.fileCreated.emit(file_path)

    def handleOpenButtonClicked(self, checked):
        """

        :return:
        """
        directory = Settings("config.ini", Settings.IniFormat).value("file_directory", "")
        if not directory:
            directory = os.getcwd()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose File", directory, "Psy File (*.psy)")
        if file_path:
            self.fileOpened.emit(file_path)

    def changeOpenMode(self, mode: str):
        """
        change open mode in config and menu
        """
        # config
        Settings("config.ini", Settings.IniFormat).setValue("open_mode", mode)
        # menu
        mode = ("default mode" == mode)
        self.default_mode_action.setIconVisibleInMenu(mode)
        self.open_blank_file_action.setIconVisibleInMenu(not mode)


class FileWindow(QWidget):
    def __init__(self):
        super(FileWindow, self).__init__()
        # title
        self.setWindowTitle("Welcome to Psy Builder")
        self.setFixedSize(820, 450)
        self.setStyleSheet("background:rgb(247,247,247)")
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
        if self.file_path_table.rowCount():
            layout.addWidget(self.file_path_table, 2)
            layout.addWidget(self.file_button_area, 3, Qt.AlignHCenter)
        else:
            layout.addWidget(self.file_button_area, 1, Qt.AlignCenter)
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
            MessageBox.information(self, "Error", f"The path '{file_path}' does not exist.'")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # set qss
    app.setStyleSheet(qss)
    # check open mode
    open_mode = Settings("config.ini", Settings.IniFormat).value("open_mode", "default mode")
    if open_mode == "default mode":
        # default open mode
        file_window = FileWindow()
        file_window.show()
    else:
        # open a blank file directly
        Settings("config.ini", Settings.IniFormat).setValue("file_path", "")
        Settings("config.ini", Settings.IniFormat).setValue("file_directory", "")
        psy = Psy()
        psy.showMaximized()
    sys.exit(app.exec_())
