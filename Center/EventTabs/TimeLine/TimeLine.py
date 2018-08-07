from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
from .EventBar import EventBar
from PyQt5.QtGui import QPixmap
from .EventArea.EventArea import EventArea


class TimeLine(QWidget):
    # signal
    # 发送信号给structure
    eventAdd = pyqtSignal(str, str, QPixmap, str)
    eventRemove = pyqtSignal(str, str)
    eventMove = pyqtSignal(int, int, str, str)

    def __init__(self, parent=None, value='TimeLine.10001'):
        super(TimeLine, self).__init__(parent)

        self.eventBar = EventBar(self)
        self.eventArea = EventArea(self)
        self.value = value

        # 布局
        grid = QGridLayout(self)
        grid.addWidget(self.eventBar, 0, 0, 1, 1)
        grid.addWidget(self.eventArea, 1, 0, 10, 1)

        self.setLayout(grid)

        # 连接信号
        self.eventArea.addEvent.connect(self.sendAddEvent)
        self.eventArea.eventTable.eventRemove.connect(self.sendRemoveEvent)
        self.eventArea.eventMove.connect(self.sendMoveEventToStructure)

    def sendAddEvent(self, name, pixmap, value):
        self.eventAdd.emit(self.value, name, pixmap, value)

    def sendRemoveEvent(self, value):
        self.eventRemove.emit(self.value, value)

    def sendMoveEventToStructure(self, dragCol, targetCol, value):
        self.eventMove.emit(dragCol, targetCol, self.value, value)

    def getProperties(self):
        return {"Name" : "TimeLine"}
