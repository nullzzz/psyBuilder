from PyQt5.QtCore import Qt, QByteArray, QDataStream, QMimeData, QIODevice
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QListView, QFrame, QTabWidget

from app.func import Func


class LeftBox(QTabWidget):
    def __init__(self, parent=None):
        super(LeftBox, self).__init__(parent=parent)
        self.basic = LeftList()
        self.stimuli = LeftList()

        image = Item("image")
        video = Item("video")
        text = Item("text")
        sound = Item("sound")

        self.basic.addItem(image)
        self.basic.addItem(video)
        self.stimuli.addItem(text)
        self.stimuli.addItem(sound)
        self.setUI()

    def setUI(self):
        tab = QTabWidget()
        self.addTab(self.basic, "Basic Geometry")
        self.addTab(self.stimuli, "Stimuli")


class LeftList(QListWidget):
    def __init__(self, parent=None):
        super(LeftList, self).__init__(parent)

        self.setViewMode(QListView.IconMode)
        self.setFlow(QListView.TopToBottom)
        self.setLayoutMode(QListView.Batched)
        self.setUniformItemSizes(True)
        self.setSortingEnabled(True)
        self.setAcceptDrops(False)
        self.setAutoFillBackground(True)
        self.setWrapping(False)
        self.setSpacing(10)
        self.setFrameStyle(QFrame.NoFrame)

        # self.setIconSize(QSize(40, 40))
        # self.setLayoutDirection(Qt.)

    def _addItems(self, items):
        for i in items:
            self.addItem(i)


class Item(QListWidgetItem):
    def __init__(self, text: str = ""):
        super(Item, self).__init__()
        self.setText(text)
        fp = Func.getImage(f"{text}.png")
        self.setIcon(QIcon(fp))
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        icon = self.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << icon
        mime_data = QMimeData()
        mime_data.setData("application/x-icon-and-text", data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()
