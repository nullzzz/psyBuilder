from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLabel, QToolBox, QSizePolicy, QFormLayout

from app.func import Func


class LeftBox(QToolBox):
    Line, Polygon, Circle, Arc, Rect, Image, Text, Video, Sound, Snow, Gabor = range(11)

    def __init__(self, parent=None):
        super(LeftBox, self).__init__(parent=parent)
        # here to create geometries items
        self.basic = QWidget()
        polygon = Item("Polygon", self.Polygon)
        circle = Item("Circle", self.Circle)
        arc = Item("Arc", self.Arc)
        rect = Item("Rect", self.Rect)

        self.stimuli = QWidget()
        image = Item("image", self.Image)
        video = Item("video", self.Video)
        text = Item("text", self.Text)
        sound = Item("sound", self.Sound)
        snow = Item("snow", self.Snow)
        gabor = Item("gabor", self.Gabor)

        self.addItem(self.basic, "Basic Geometries")
        self.addItem(self.stimuli, "Stimuli")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))

        basic_layout = QFormLayout()
        basic_layout.setAlignment(Qt.AlignCenter)
        basic_layout.addWidget(polygon)
        basic_layout.addWidget(circle)
        basic_layout.addWidget(arc)
        basic_layout.addWidget(rect)

        stim_Layout = QFormLayout()
        stim_Layout.setAlignment(Qt.AlignCenter)

        stim_Layout.addWidget(image)
        stim_Layout.addWidget(video)
        stim_Layout.addWidget(text)
        stim_Layout.addWidget(sound)
        stim_Layout.addWidget(snow)
        stim_Layout.addWidget(gabor)

        self.basic.setLayout(basic_layout)
        self.stimuli.setLayout(stim_Layout)

        # here to insert geometries layout
        geom_layout = QFormLayout()
        geom_layout.setAlignment(Qt.AlignCenter)


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
        # layout.setRowStretch(0, 2)
        # layout.setRowStretch(1, 0.2)
        # layout.setRowMinimumHeight(1,20)
        self.setLayout(layout)


class Button(QPushButton):
    def __init__(self, text: str, item_type: int, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.item_type = item_type
        if text == "text":
            text = "textpointer"

        fp = QPixmap(Func.getImage(f"{text}.png")).scaled(50, 50)
        self.setIcon(QIcon(fp))
        self.setIconSize(QSize(50, 50))
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
        t = QByteArray()
        t.setNum(self.item_type)
        mime_data.setData("item-type", t)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()
