from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog

from app.func import Func


class Update(QDialog):
    def __init__(self, parent=None):
        super(Update, self).__init__(parent=parent)

        self.setWindowTitle("About developers of PsyBuilder 0.1")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))

        self.label = QLabel("www.baidu.com")
        self.label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
