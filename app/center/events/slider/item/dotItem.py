from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainterPath, QBrush
from PyQt5.QtWidgets import QGraphicsItem

from app.center.events.slider.item.dot.dotProperty import DotProperty
from app.info import Info


class DotItem(QGraphicsItem):
    Dot = 12
    name = {
        Dot: Info.ITEM_DOT,
    }

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

        self.rect = QRect(-50, -50, 100, 100)
        # self.color = color
        # self.angle = angle
        # self.setPos(position)

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
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.pro_window.show()

    def setPosition(self):
        pass

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

        # todo bug
        self.rect.setWidth(w)
        self.rect.setHeight(h)

        __dot_num = self.properties["Dot Num"]
        dot_num = int(__dot_num) if __dot_num.isdigit() else 50
        __dot_type = self.properties["Dot Type"]
        dot_type = int(__dot_type) if __dot_type.isdigit() else 1
        __dot_size = self.properties["Dot Size"]
        dot_size = int(__dot_size) if __dot_size.isdigit() else 1

        __dot_color = self.properties["Dot Color"]
        dot_color = ""

        self.update()

    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.rect)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(DotItem.Rect)
        if option.levelOfDetailFromTransform(self.transform()) > 0.5:  # Outer eyes
            painter.setBrush(QBrush(Qt.yellow))
            painter.drawEllipse(-12, -19, 8, 8)
            painter.drawEllipse(-12, 11, 8, 8)
            if option.levelOfDetailFromTransform(self.transform()) > 0.8:  # Inner eyes
                painter.setBrush(QBrush(Qt.darkBlue))
                painter.drawEllipse(-12, -19, 4, 4)
                painter.drawEllipse(-12, 11, 4, 4)
                if option.levelOfDetailFromTransform(self.transform()) > 0.9:  # Nostrils
                    painter.setBrush(QBrush(Qt.white))
                    painter.drawEllipse(-27, -5, 2, 2)
                    painter.drawEllipse(-27, 3, 2, 2)

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
