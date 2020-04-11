import random

from PyQt5.QtCore import Qt, QRect, QRectF, QTimer
from PyQt5.QtGui import QPainterPath, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem

from app.center.events.slider.item.dot.dotProperty import DotProperty
from app.info import Info


class DotItem(QGraphicsItem):
    Dot = 12
    name = {
        Dot: Info.ITEM_DOT,
    }

    Interval = 300

    def __init__(self, item_type, item_name: str = ""):
        super(DotItem, self).__init__()

        super(DotItem, self).__init__()

        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        self.pro_window = DotProperty()
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

        self.rect = QRectF(-100, -100, 200, 200)
        self.dot_position: list = []

        self.dot_cnt: int = 50
        self.dot_type: int = 1
        self.dot_size: int = 6
        self.dot_color: QColor = QColor(Qt.black)
        self.back_color: QColor = QColor(Qt.lightGray)
        self.move_direction: int = 0

        self.generateDotPosition()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateDotPosition)
        self.timer.start(DotItem.Interval)

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def openPro(self):
        self.setPosition()
        self.pro_window.show()

    def setPosition(self):
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def getName(self):
        return self.item_name

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
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

    def changeSomething(self):
        __cx = self.properties["Center X"]
        cx = int(__cx) if __cx.isdigit() else self.scenePos().x()
        __cy = self.properties["Center Y"]
        cy = int(__cy) if __cy.isdigit() else self.scenePos().y()
        self.setPos(cx, cy)

        __w = self.properties["Width"]
        w = int(__w) if __w.isdigit() else self.rect.width()
        __h = self.properties["Height"]
        h = int(__h) if __h.isdigit() else self.rect.height()

        self.rect = QRectF(-w / 2, -h / 2, w, h)

        __dot_num = self.properties["Dot Num"]
        if __dot_num.isdigit():
            self.dot_cnt = int(__dot_num)

        __dot_type = self.properties["Dot Type"]
        if __dot_type.isdigit():
            self.dot_type = int(__dot_type)

        __dot_size = self.properties["Dot Size"]
        if __dot_size.isdigit():
            self.dot_size = int(__dot_size)

        __dot_color = self.properties["Dot Color"]
        if not __dot_color.startswith("["):
            rgba = [int(x) for x in __dot_color.split(",")]
            if len(rgba) == 4:
                r, g, b, a = rgba
            else:
                r, g, b = rgba
                a = 255
            self.dot_color = QColor(r, g, b, a)
        __back_color = self.properties["Back Color"]
        if not __back_color.startswith("["):
            rgba = [int(x) for x in __back_color.split(",")]
            if len(rgba) == 4:
                r, g, b, a = rgba
            else:
                r, g, b = rgba
                a = 255
            self.back_color.setRgb(r, g, b, a)

        self.update()

    def setBackColor(self, color: QColor):
        self.back_color = color
        old_rgb = self.properties["Back Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Back Color"] = rgb
            self.pro_window.general.setBackColor(rgb)

    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.rect)
        return path

    def generateDotPosition(self):
        """
        # todo
        you should complete this function.
        you can use such parameters:
        self.dot_cnt: int   the number of dot.
        self.dot_type: str  the type of dot.
        self.rect: QRectF   the bounding rectangle of this item.
        all above are not referenced variables.
        each dot position is a tuple, which has x and y.
        all dots' position stored in variable self.dot_position.
        """
        ps = []
        for i in range(self.dot_cnt):
            x = random.randint(self.rect.left(), self.rect.right())
            y = random.randint(self.rect.top(), self.rect.bottom())
            ps.append([x, y])
        self.dot_position = ps

    def updateDotPosition(self):
        # todo
        for dp in self.dot_position:
            dp[0] += random.choice((-3, -1, 1, 3))
            dp[1] += random.choice((-3, -1, 1, 3))
        self.update()

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.back_color))
        painter.drawEllipse(self.rect)
        painter.setBrush(QBrush(self.dot_color))
        for p in self.dot_position:
            p: tuple
            x = p[0]
            y = p[1]
            rect = QRect(x - self.dot_size, y - self.dot_size, self.dot_size, self.dot_size)
            painter.drawEllipse(rect)

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.default_properties["X"] = properties["X"]
        self.default_properties["Y"] = properties["Y"]
        self.default_properties["Z"] = properties["Z"]
        self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        self.updateInfo()
        new = DotItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(DotItem, self).setZValue(z)
