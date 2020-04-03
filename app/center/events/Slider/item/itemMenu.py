from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu, QAction


class ItemMenu(QMenu):
    delSignal = pyqtSignal()
    froSignal = pyqtSignal()
    bacSignal = pyqtSignal()
    proSignal = pyqtSignal()

    def __init__(self):
        super(ItemMenu, self).__init__()
        self.delete_action = QAction("Delete")
        self.front_action = QAction("toFront")
        self.back_action = QAction("toBack")
        self.pro_action = QAction("Property")
        self.delete_action.triggered.connect(lambda: self.delSignal.emit())
        self.front_action.triggered.connect(lambda: self.froSignal.emit())
        self.back_action.triggered.connect(lambda: self.bacSignal.emit())
        self.pro_action.triggered.connect(lambda: self.proSignal.emit())
        self.addAction(self.delete_action)
        self.addAction(self.front_action)
        self.addAction(self.back_action)
        self.addAction(self.pro_action)