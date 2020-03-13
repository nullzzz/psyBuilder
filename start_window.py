import os

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QSettings
from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QApplication, QFileDialog, QVBoxLayout, QLabel

from app import Psy
from app.func import Func
from app.info import Info
from lib import MessageBox, TableWidget, HoverButton


class FileText(QTextEdit):
    clicked = pyqtSignal()

    def __init__(self, file_path: str):
        # style
        super(FileText, self).__init__()
        self.setStyleSheet("""
        QTextEdit{
            border:none;
        }
        QTextEdit:hover{
            border-radius:4px;
            border: 2px solid rgb(186, 215, 251);
        }
        """)
        self.file_path = file_path
        file_name = os.path.basename(file_path)
        self.setText(f"""<b style="color:rgb(31,31,31)">{file_name}</b>""")
        if os.path.exists(file_path):
            self.append(f"""<p style="color:rgb(157,157,157)">{file_path}</p>""")
        else:
            self.append(f"""<p style="color:rgb(142,15,15)">{file_path}</p>""")
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mousePressEvent(self, QMouseEvent):
        super(FileText, self).mousePressEvent(QMouseEvent)
        self.clicked.emit()

    def enterEvent(self, QEvent):
        super(FileText, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def leaveEvent(self, QEvent):
        super(FileText, self).leaveEvent(QEvent)
        QApplication.setOverrideCursor(Qt.ArrowCursor)


class FileTable(TableWidget):
    """
    show some recent files
    """
    # emit file path
    fileClicked = pyqtSignal(str)
    fileDeleted = pyqtSignal(str)

    def __init__(self):
        super(FileTable, self).__init__()
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
        self.setRowHeight(index, 48)
        # insert line edit into table
        file = FileText(file_path)
        self.setCellWidget(index, 0, file)
        file.clicked.connect(lambda: self.fileClicked.emit(file_path))
        # button
        delete_button = HoverButton("menu/close")
        self.setCellWidget(index, 1, delete_button)
        delete_button.clicked.connect(lambda checked: self.handleFileDeleted(file_path))

    def handleFileDeleted(self, file_path):
        """

        :param checked:
        :return:
        """
        self.fileDeleted.emit(file_path)
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).file_path == file_path:
                self.removeRow(row)
                break


class FileFrame(QWidget):
    fileCreated = pyqtSignal(str)
    fileOpened = pyqtSignal(str)

    def __init__(self):
        super(FileFrame, self).__init__()
        # widget
        icon = QLabel()
        icon.setPixmap(Func.getImageObject("common/icon.png", type=0, size=QSize(180, 180)))
        # buttons
        create_button = HoverButton("menu/add", "Create New File")
        create_button.clicked.connect(self.handleCreateButtonClicked)
        open_button = HoverButton("menu/open", "Open")
        open_button.clicked.connect(self.handleOpenButtonClicked)
        # layout
        layout = QVBoxLayout()
        layout.addWidget(icon, 50, Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(create_button, 1, Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(open_button, 1, Qt.AlignVCenter | Qt.AlignLeft)
        layout.addStretch(20)
        self.setLayout(layout)

    def handleCreateButtonClicked(self, checked):
        """

        :return:
        """
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory", os.getcwd(), QFileDialog.ShowDirsOnly)
        if directory:
            self.fileCreated.emit(directory)

    def handleOpenButtonClicked(self, checked):
        """

        :return:
        """
        file, _ = QFileDialog.getOpenFileName(self, "Choose File", os.getcwd(), "Psy File (*.psy)")
        if file:
            self.fileOpened.emit(file)


class FileWindow(QWidget):
    def __init__(self, file_path: str = "", directory: str = ""):
        super(FileWindow, self).__init__()
        # title
        self.setWindowTitle("Welcome to Psy Builder")
        self.setFixedSize(820, 450)
        self.setStyleSheet("background:rgb(247,247,247)")
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        # widget file_table and file frame
        self.file_table = FileTable()
        self.file_table.fileClicked.connect(self.handleFileClicked)
        self.file_table.fileDeleted.connect(self.handleFileDeleted)
        self.file_frame = FileFrame()
        self.file_frame.fileCreated.connect(self.handleFileCreated)
        self.file_frame.fileOpened.connect(self.handleFileOpened)
        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.file_table, 2)
        layout.addWidget(self.file_frame, 3, Qt.AlignHCenter)
        self.setLayout(layout)
        # load files from config
        self.config = QSettings("./config.ini", QSettings.IniFormat)
        self.loadFiles()
        #
        if file_path and os.path.exists(file_path):
            self.startPsy(file_path)
        if directory:
            Info.FILE_DIRECTORY = directory
            Info.FILE_NAME = ""
            self.startPsy()

    def loadFiles(self):
        """
        load file list from config
        :return:
        """
        file_paths = self.config.value("file_paths", [])
        for file_path in file_paths:
            self.file_table.addFilePath(-1, file_path)

    def startPsy(self):
        """
        start app
        :param file_path:
        :return:
        """
        psy = Psy()
        psy.showMaximized()
        self.close()

    def handleFileCreated(self, file_directory: str):
        """
        change config and start software
        :param dir:
        :return:
        """
        # change config
        self.config.setValue("file_directory", file_directory)
        # start psy application
        self.startPsy()

    def handleFileOpened(self, file_path: str):
        """
        change config and start software(then restore it from file)
        :param file_path:
        :return:
        """
        # change file_paths
        file_paths = self.value("file_paths", [])
        if file_path not in file_paths:
            file_paths.insert(0, file_path)
        else:
            # move it to first
            file_paths.remove(file_path)
            file_paths.insert(0, file_path)
        self.config.setValue("file_paths", file_paths)
        # change file_path and file_directory
        self.config.setValue("file_path", file_path)
        self.config.setValue("file_directory", os.path.dirname(file_path))
        # start psy
        self.startPsy()

    def handleFileDeleted(self, file_path: str):
        """
        delete data in config
        :param file_path:
        :return:
        """
        file_paths = self.value("file_paths", [])
        if file_path in file_paths:
            file_paths.remove(file_path)
            self.config.setValue("file_paths", file_paths)

    def handleFileClicked(self, file_path: str):
        """
        open file if file existed
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            self.config.setValue("file_path", file_path)
            self.config.setValue("file_directory", os.path.dirname(file_path))
            self.startPsy()
        else:
            MessageBox.information(self, "Error", f"The path '{file_path}' does not exist.'")
