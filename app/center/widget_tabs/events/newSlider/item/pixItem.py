from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

# 画图
from app.center.widget_tabs.events.newSlider.image.imageProperty import ImageProperty
from app.center.widget_tabs.events.newSlider.item.itemMenu import ItemMenu
from app.center.widget_tabs.events.newSlider.sound.soundProperty import SoundProperty
from app.center.widget_tabs.events.newSlider.text.textProperty import TextProperty
from app.center.widget_tabs.events.newSlider.video.videoProperty import VideoProperty
from app.func import Func
from app.info import Info


class PixItem(QGraphicsPixmapItem):
    """
    Image、Text、Video、Sound
    """
    Image, Text, Video, Sound = 2, 3, 4, 5
    name = {
        Image: "image",
        Text: "text",
        Video: "video",
        Sound: "sound",
    }

    def __init__(self, pix_type, parent=None):
        super(PixItem, self).__init__(parent)

        self.item_type = pix_type
        self.item_name = self.generateItemName()

        self.attributes: list = []
        if self.item_type == self.Image:
            self.pro_window = ImageProperty()
            self.setPixmap(QPixmap(Func.getImage("image.png")).scaled(100, 100))
        elif self.item_type == self.Text:
            self.pro_window = TextProperty()
            self.setPixmap(QPixmap(Func.getImage("text.png")).scaled(100, 100))
        elif self.item_type == self.Video:
            self.pro_window = VideoProperty()
            self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(100, 100))
        elif self.item_type == self.Sound:
            self.pro_window = SoundProperty()
            self.setPixmap(QPixmap(Func.getImage("sound.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.flag = False
        self.arbitrary_resize = False
        self.keep_resize = False

        self.default_properties = {
            'name': self.item_type,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties
        }

        self.menu = ItemMenu()

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def mousePressEvent(self, event):
        if self.item_type < 8:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier:
                self.arbitrary_resize = True
                self.setCursor(Qt.SizeAllCursor)
            elif event.button() == Qt.LeftButton and event.modifiers() == Qt.ShiftModifier:
                self.keep_resize = True
                self.setCursor(Qt.SizeAllCursor)
            else:
                super(PixItem, self).mousePressEvent(event)
        else:
            super(PixItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.arbitrary_resize:
            self.flag = True
        if self.keep_resize:
            self.flag = True
            if x > y:
                x = y
            else:
                y = x
        if self.flag:
            self.setPixmap(QPixmap(Func.getImage(f"{self.name[self.item_type]}.png")).scaled(x, y))
            self.update()
        else:
            super(PixItem, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.unsetCursor()
        self.arbitrary_resize = False
        self.keep_resize = False
        self.flag = False
        super(PixItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttributes(self.attributes)
        self.pro_window.show()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.menu.exec_(event.screenPos())
        # self.contextMenu.exec_(event.screenPos())

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.pro_window.getInfo()
        self.default_properties = {
            'name': self.item_type,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties
        }

    def restore(self, properties: dict):
        if properties:
            self.pro_window.setProperties(properties)

    def clone(self):
        new = PixItem(self.item_type)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        new.setPixmap(self.pixmap())
        new.setZValue(self.zValue())

        return new
