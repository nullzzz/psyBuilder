from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QToolBox, QSizePolicy, QFormLayout

from app.func import Func


class LeftBox(QToolBox):
    Line, Polygon, Circle, Arc, Rect, Image, Text, Video, Sound, Snow, Gabor = range(11)

    def __init__(self, parent=None):
        super(LeftBox, self).__init__(parent=parent)
        self.basic = QWidget()
        image = Item("image", self.Image)
        video = Item("video", self.Video)
        text = Item("text", self.Text)
        sound = Item("sound", self.Sound)
        snow = Item("snow", self.Snow)
        gabor = Item("gabor", self.Gabor)

        self.stimuli = QWidget()
        self.addItem(self.basic, "Basic Geometries")
        self.addItem(self.stimuli, "Stimuli")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))

        layout1 = QFormLayout()
        layout1.setAlignment(Qt.AlignCenter)
        layout1.addWidget(image)
        layout1.addWidget(video)
        layout1.addWidget(text)
        layout1.addWidget(sound)
        layout1.addWidget(snow)
        layout1.addWidget(gabor)
        self.stimuli.setLayout(layout1)


class Item(QWidget):
    itemType = pyqtSignal(int)

    def __init__(self, text: str, item_type: int, parent=None):
        super(Item, self).__init__(parent=parent)
        self.text = text
        self.item_type = item_type
        self.bt = Button(text, item_type)
        self.bt.clicked.connect(lambda: self.itemType.emit(self.item_type))
        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(self.bt, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(self.text), 1, 0, Qt.AlignCenter)
        self.setLayout(layout)


class Button(QPushButton):
    def __init__(self, text: str, item_type: int, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.item_type = item_type
        fp = Func.getImage(f"{text}.png")
        self.setIcon(QIcon(fp))

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        icon = self.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << icon
        mime_data = QMimeData()
        mime_data.setData("application/x-icon-and-text", data)
        t = QByteArray()
        t.setNum(self.item_type)
        mime_data.setData("item-type", t)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()
