from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal


class Switch(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Switch, self).__init__(parent)

        self.setWindowTitle("Switch")
