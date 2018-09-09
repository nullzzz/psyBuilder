from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QFileDialog, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap


class General(QWidget):
    def __init__(self, parent=None):
        super(General, self).__init__(parent)

        self.load_method = QComboBox(self)
        self.load_method.addItem("Embedded")
        self.load_method.addItem("File")
        self.load_method.addItem("Script")

        self.file_name = QLineEdit(self)
        self.open_button = QPushButton(self)

        self.open_button.clicked.connect(self.openFile)

        self.file_name.setEnabled(False)
        self.open_button.setEnabled(False)
        icon = QIcon()
        icon.addPixmap(QPixmap("image/folder.png"), QIcon.Normal, QIcon.Off)
        self.open_button.setIcon(icon)

        grid = QGridLayout(self)

        grid.addWidget(QLabel("Load Method: "), 0, 0, Qt.AlignRight)
        grid.addWidget(self.load_method, 0, 1, 1, 3)
        grid.addWidget(QLabel("File Name: "), 2, 0, Qt.AlignRight)
        grid.addWidget(self.file_name, 2, 1, 1, 5)
        grid.addWidget(self.open_button, 2, 6)
        grid.addWidget(QLabel(""), 3, 0)
        grid.setVerticalSpacing(20)

        self.setLayout(grid)

        self.load_method.currentIndexChanged.connect(self.setWidgetEnable)

    def openFile(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件", "C:/",
                                                         "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.file_name.setText(file_name)

    def setWidgetEnable(self, index):
        if index == 0:
            self.file_name.setEnabled(False)
            self.open_button.setEnabled(False)
        if index == 1:
            self.file_name.setEnabled(True)
            self.open_button.setEnabled(True)
        if index == 2:
            self.file_name.setEnabled(False)
            self.open_button.setEnabled(False)