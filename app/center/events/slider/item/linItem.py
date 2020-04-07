from PyQt5.QtCore import Qt, QLineF, pyqtSignal
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem

from app.info import Info
from ..item.line.lineProperty import LineProperty


class LineItem(QGraphicsLineItem):
    propertyChanged = pyqtSignal(dict)

    def __init__(self, line: QLineF, item_name: str = ""):
        super(LineItem, self).__init__()
        self.item_type = 0
        self.item_name = item_name if item_name else self.generateItemName()

        self.setLine(line)

        self.pro_window = LineProperty()
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
            "Properties": self.properties,
        }

    def generateItemName(self) -> str:
        name = Info.ITEM_LINE
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

    def setPosition(self):

        x1 = self.line().x1() + self.scenePos().x()
        y1 = self.line().y1() + self.scenePos().y()
        x2 = self.line().x2() + self.scenePos().x()
        y2 = self.line().y2() + self.scenePos().y()
        self.setLine(x1, y1, x2, y2)
        self.pro_window.setPosition(x1, y1, x2, y2)

    def setWidth(self, width):
        if isinstance(width, str) and width.isdigit():
            width = int(width)
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)
        self.update()
        old_width = self.properties["Border Width"]
        if not old_width.startswith("["):
            self.properties["Border Width"] = str(width)
            self.pro_window.general.setLineWidth(str(width))

    def setLineColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        self.update()
        old_rgb = self.properties["Border Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Border Color"] = rgb
            self.pro_window.general.setLineColor(rgb)

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

    def changeSomething(self):
        x1: str = self.properties.get("X1")
        y1: str = self.properties.get("Y1")
        x2: str = self.properties.get("X2")
        y2: str = self.properties.get("Y2")
        if x1.startswith("[") or x2.startswith("[") or y1.startswith("[") or y2.startswith("["):
            pass
        else:
            line = QLineF(float(x1), float(y1), float(x2), float(y2))
            self.setLine(line)
        __color = self.properties.get("Border Color")
        color = "0,0,0" if __color.startswith("[") else __color
        r, g, b = [int(x) for x in color.split(",")]
        __width = self.properties.get("Border Width")
        width = 2 if __width.startswith("[") else int(__width)
        pen = QPen()
        pen.setColor(QColor(r, g, b))
        pen.setWidth(width)
        self.setPen(pen)
        self.update()

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
        # todo position of item and it's line
        line = QLineF(self.line().x1(), self.line().y1(), self.line().x2(), self.line().y2())
        new = LineItem(line)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(LineItem, self).setZValue(z)
