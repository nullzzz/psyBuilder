import re
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
        self.label.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setMinimumSize(400, 100)
        # self.setFixedSize(600, 100)

    def show(self):
        self.getLatestVersion()
        super(Update, self).show()

    def getLatestVersion(self):
        version_info = "The current version is the latest version."
        #############
        # get latest version information
        url = "https://yzhangpsy.myds.me:8001"
        try:
            res = request.urlopen(url)
            versionList = re.findall(r'Current version of PsyBuilder (\d+\.\d+)', res.read().decode('utf-8'))

            if len(versionList) > 0:
                version_str = versionList[0]
                version_info = f"The latest version is {version_str}, click <a href ='https://yzhangpsy.myds.me:8001'>me</a> to update."
            else:
                version_info = "Failed to consult PsyBuilder website, please try it later."

        except:
            version_info = "Failed to consult PsyBuilder website, please try it later."
            pass
        #############
        self.label.setText(version_info)
