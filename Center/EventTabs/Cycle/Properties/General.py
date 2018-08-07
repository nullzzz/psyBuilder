from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QPushButton, QFileDialog, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap


class General(QWidget):
    def __init__(self, parent=None):
        super(General, self).__init__(parent)

        self.loadMethod = QComboBox(self)
        self.loadMethod.addItem("Embedded")
        self.loadMethod.addItem("File")
        self.loadMethod.addItem("Script")

        self.fileName = QLineEdit(self)
        self.openButton = QPushButton(self)

        self.openButton.clicked.connect(self.openFile)

        self.fileName.setEnabled(False)
        self.openButton.setEnabled(False)
        icon = QIcon()
        icon.addPixmap(QPixmap(".\\.\\image\\folder.png"), QIcon.Normal, QIcon.Off)
        self.openButton.setIcon(icon)

        grid = QGridLayout(self)

        grid.addWidget(QLabel("Load Method: "), 0, 0, Qt.AlignRight)
        grid.addWidget(self.loadMethod, 0, 1, 1, 3)
        grid.addWidget(QLabel("File Name: "), 2, 0, Qt.AlignRight)
        grid.addWidget(self.fileName, 2, 1, 1, 5)
        grid.addWidget(self.openButton, 2, 6)
        grid.addWidget(QLabel(""), 3, 0)
        grid.setVerticalSpacing(20)

        self.setLayout(grid)

        self.loadMethod.currentIndexChanged.connect(self.setWidgetEnable)

    def openFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", "C:/",
                                                         "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.fileName.setText(fileName)

    def setWidgetEnable(self, index):
        if index == 0:
            self.fileName.setEnabled(False)
            self.openButton.setEnabled(False)
        if index == 1:
            self.fileName.setEnabled(True)
            self.openButton.setEnabled(True)
        if index == 2:
            self.fileName.setEnabled(False)
            self.openButton.setEnabled(False)