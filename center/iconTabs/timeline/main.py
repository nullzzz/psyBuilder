from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
from .iconBar import IconBar
from PyQt5.QtGui import QPixmap
from .iconArea.main import IconArea


class Timeline(QWidget):
    # 发送给structure
    iconAdd = pyqtSignal(str, str, QPixmap, str)
    iconRemove = pyqtSignal(str, str)
    iconMove = pyqtSignal(int, int, str, str)

    def __init__(self, parent=None, value='Timeline.10001'):
        super(Timeline, self).__init__(parent)
        self.value = value
        # widget
        self.icon_bar = IconBar(self)
        self.icon_area = IconArea(self)
        # layout
        grid = QGridLayout(self)
        grid.addWidget(self.icon_bar, 0, 0, 1, 1)
        grid.addWidget(self.icon_area, 1, 0, 10, 1)
        self.setLayout(grid)

        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        self.icon_area.iconAdd.connect(self.addIcon)
        self.icon_area.iconMove.connect(self.moveIcon)
        self.icon_area.icon_table.iconRemove.connect(self.removeIcon)

    def addIcon(self, name, pixmap, value):
        self.iconAdd.emit(self.value, name, pixmap, value)

    def removeIcon(self, value):
        self.iconRemove.emit(self.value, value)

    def moveIcon(self, dragCol, targetCol, value):
        self.iconMove.emit(dragCol, targetCol, self.value, value)

    def getProperties(self):
        return {"properties" : "None"}
