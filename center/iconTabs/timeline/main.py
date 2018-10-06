from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout

from .iconArea.main import IconArea
from .iconBar import IconBar


class Timeline(QWidget):
    # 发送给structure
    iconAdd = pyqtSignal(str, str, QPixmap, str)
    iconRemove = pyqtSignal(str, str)
    iconMove = pyqtSignal(int, int, str, str)
    iconNameChange = pyqtSignal(str, str, str)
    iconChange = pyqtSignal(str, str)

    def __init__(self, parent=None, value='Timeline.10001'):
        super(Timeline, self).__init__(parent)
        # data
        self.value = value
        # widget
        self.icon_bar = IconBar(self)
        self.icon_area = IconArea(self, self.value)
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
        self.icon_area.iconChange.connect(self.changeIcon)
        self.icon_area.icon_table.iconRemove.connect(self.removeIcon)
        self.icon_area.icon_table.iconNameChange.connect(self.sendIconNameChange)

    def addIcon(self, name, pixmap, value):
        self.iconAdd.emit(self.value, name, pixmap, value)

    def removeIcon(self, value):
        self.iconRemove.emit(self.value, value)

    def removeIconSimply(self, value):
        self.icon_area.icon_table.removeIcon(value)

    def moveIcon(self, dragCol, targetCol, value):
        self.iconMove.emit(dragCol, targetCol, self.value, value)

    def changeIcon(self, value):
        self.iconChange.emit(self.value, value)

    def sendIconNameChange(self, value, name):
        self.iconNameChange.emit(self.value, value, name)

    def changeIconName(self, value, name):
        for col in range(1, self.icon_area.icon_table.fill_count + 1):
            if self.icon_area.icon_table.cellWidget(1, col).value == value:
                self.icon_area.icon_table.item(3, col).setText(name)

    def getProperties(self):
        return {"properties": "None"}

    # todo copy timeline
    def copy(self, value):
        try:
            # 返回自身的复制
            timeline_copy = Timeline(value=value)
            # icon_bar不需要复制
            # icon_area需要复制
            self.icon_area.copy(timeline_copy.icon_area)
            return timeline_copy
        except Exception as e:
            print(f"error {e} happens in copy timeline. [timeline/main.py]")

