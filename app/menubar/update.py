import urllib.request as request

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog

from app.func import Func


class Update(QDialog):
    def __init__(self, parent=None):
        super(Update, self).__init__(parent=parent)

        self.setWindowTitle("Checking new version...")
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))

        self.label = QLabel("The current version is the latest version.")
        self.label.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedSize(400, 300)

    def show(self):
        self.getLatestVersion()
        super(Update, self).show()

    def getLatestVersion(self):
        version_info = "The current version is the latest version."
        #############
        # get latest version information
        # url = ""
        # res = request.urlopen(url)
        # version_info = res.read().decode('utf-8')
        #############
        self.label.setText(version_info)
