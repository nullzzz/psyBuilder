import os
import platform
import re
import sys

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QApplication, QFileDialog, QVBoxLayout, QLabel

from app import Psy
from app.func import Func
from app.info import Info
from lib import MessageBox, TableWidget, HoverButton
from qss import mac_qss, windows_qss


class File(QTextEdit):
    clicked = pyqtSignal()

    def __init__(self, file_path: str):
        # style
        super(File, self).__init__()
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
        super(File, self).mousePressEvent(QMouseEvent)
        self.clicked.emit()

    def enterEvent(self, QEvent):
        super(File, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def leaveEvent(self, QEvent):
        super(File, self).leaveEvent(QEvent)
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
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 20)

    def addFile(self, index: int, file_path: str):
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
        file = File(file_path)
        file.clicked.connect(lambda: self.fileClicked.emit(file_path))
        self.setCellWidget(index, 0, file)
        # button
        delete_button = HoverButton("menu/close")
        delete_button.clicked.connect(lambda checked: self.handleFileDeleted(file_path))
        self.setCellWidget(index, 1, delete_button)

    def deleteFile(self, file_path: str):
        """
        delete file in this table
        :param file_path:
        :return:
        """
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).file_path == file_path:
                self.removeRow(row)
                break

    def handleFileDeleted(self, file_path):
        """

        :param checked:
        :return:
        """
        self.fileDeleted.emit(file_path)
        self.deleteFile(file_path)


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
        dir = QFileDialog.getExistingDirectory(self, "Choose Directory", os.getcwd(), QFileDialog.ShowDirsOnly)
        self.fileCreated.emit(dir)

    def handleOpenButtonClicked(self, checked):
        """

        :return:
        """
        file, _ = QFileDialog.getOpenFileName(self, "Choose File", os.getcwd(), "Psy File (*.psy)")
        if file:
            self.fileOpened.emit(file)


class FileWindow(QWidget):
    def __init__(self):
        super(FileWindow, self).__init__()
        # title
        self.setWindowTitle("Welcome to Psy Builder")
        self.setFixedSize(820, 450)
        self.setStyleSheet("background:rgb(247,247,247)")
        self.setWindowIcon(Func.getImageObject("common/con.png", type=1))
        # widget
        self.file_table = FileTable()
        self.file_frame = FileFrame()
        self.file_table.fileClicked.connect(self.handleFileClicked)
        self.file_table.fileDeleted.connect(self.handleFileDeleted)
        self.file_frame.fileCreated.connect(self.handleFileCreated)
        self.file_frame.fileOpened.connect(self.handleFileOpened)
        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.file_table, 2)
        layout.addWidget(self.file_frame, 3, Qt.AlignHCenter)
        self.setLayout(layout)
        # load
        self.loadConfig()

    def loadConfig(self):
        """
        load file list from config
        :return:
        """
        file_paths = re.split(r"\$\^\$", Info.CONFIG.value("files", ""))
        if not file_paths[-1]:
            file_paths = file_paths[:-1]
        for file_path in file_paths:
            self.file_table.addFile(-1, file_path)

    def handleFileCreated(self, dir: str):
        """

        :param dir:
        :return:
        """
        # start psy and change Info.FILE_DIRECTORY
        Info.FILE_DIRECTORY = dir
        psy = Psy()
        Info.Psy = psy
        psy.showMaximized()
        self.close()

    def handleFileOpened(self, file_path: str):
        """"""
        file_paths = re.split(r"\$\^\$", Info.CONFIG.value("files", ""))
        if file_path not in file_paths:
            file_paths.insert(0, file_path)
            Info.CONFIG.setValue("files", "$^$".join(file_paths))
        else:
            # move it to first
            file_paths = re.split(r"\$\^\$", Info.CONFIG.value("files", ""))
            file_paths.remove(file_path)
            file_paths.insert(0, file_path)
            Info.CONFIG.setValue("files", "$^$".join(file_paths))
        Info.FILE_DIRECTORY = os.path.dirname(file_path)
        MessageBox.information(self, "Error", "Sorry for it isn't completed")
        # psy = Psy(file_path)
        # Info.Psy = psy
        # psy.showMaximized()
        self.close()

    def handleFileDeleted(self, file_path: str):
        """
        delete data in config
        :param file_path:
        :return:
        """
        file_paths = re.split(r"\$\^\$", Info.CONFIG.value("files", ""))
        file_paths.remove(file_path)
        Info.CONFIG.setValue("files", "$^$".join(file_paths))

    def handleFileClicked(self, file_path: str):
        """
        open file if file existed
        :param file_path:
        :return:
        """
        if os.path.exists(file_path):
            print("ok")
        else:
            MessageBox.information(self, "Error", "File not founded!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_window = FileWindow()
    file_window.show()
    # choose qss
    if platform.system() == "Windows":
        app.setStyleSheet(windows_qss)
    else:
        app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
