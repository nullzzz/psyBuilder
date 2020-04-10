from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

from app.func import Func
from app.info import Info
# 画图
from ..item.image import ImageProperty
from ..item.sound import SoundProperty
from ..item.video import VideoProperty


class PixItem(QGraphicsPixmapItem):
    """
    Image、Text、Video、Sound
    """
    Image, Video, Sound = [5, 7, 8]

    name = {
        Image: Info.ITEM_IMAGE,
        Video: Info.ITEM_VIDEO,
        Sound: Info.ITEM_SOUND,
    }

    def __init__(self, item_type, item_name: str = ""):
        super(PixItem, self).__init__()

        self.item_type = item_type

        self.item_name = item_name if item_name else self.generateItemName()

        if self.item_type == self.Image:
            self.pro_window = ImageProperty()
            self.setPixmap(QPixmap(Func.getImage("image.png")).scaled(100, 100))
        elif self.item_type == self.Video:
            self.pro_window = VideoProperty()
            self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(100, 100))
        elif self.item_type == self.Sound:
            self.pro_window = SoundProperty()
            self.setPixmap(QPixmap(Func.getImage("sound_item.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.properties = self.pro_window.default_properties
        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            "Properties": self.properties
        }

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def getName(self):
        return self.item_name

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.pro_window.show()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.changeSomething()

    def updateInfo(self):
        self.pro_window.updateInfo()
        self.default_properties["X"] = self.scenePos().x()
        self.default_properties["Y"] = self.scenePos().y()
        self.default_properties["Z"] = self.zValue()

    def getInfo(self):
        return self.default_properties

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.default_properties["X"] = properties["X"]
        self.default_properties["Y"] = properties["Y"]
        self.default_properties["Z"] = properties["Z"]
        self.loadSetting()

    def setPosition(self):
        """
        :get icon properties in scene and send it to info :
        """
        width = self.boundingRect().width()
        height = self.boundingRect().height()

        self.pro_window.general.setPosition(self.scenePos().x() + (width / 2), self.scenePos().y() + (height / 2))

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        self.updateInfo()
        new = PixItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def changeSomething(self):
        if self.item_type != self.Sound:
            __w = self.properties["Width"]
            w = int(__w) if __w.isdigit() else 100
            __h = self.properties["Height"]
            h = int(__h) if __h.isdigit() else 100

            __cx = self.properties["Center X"]
            cx = int(__cx) if __cx.isdigit() else self.scenePos().x()
            __cy = self.properties["Center Y"]
            cy = int(__cy) if __cy.isdigit() else self.scenePos().y()

            self.setPos(QPoint(cx - (w / 2), cy - (h / 2)))

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(PixItem, self).setZValue(z)
