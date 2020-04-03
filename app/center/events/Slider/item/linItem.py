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

        self.attributes: list = []
        self.pro_window = LineProperty()
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            **self.pro_window.getInfo(),
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
        self.setPos(0, 0)
        self.setLine(x1, y1, x2, y2)
        self.pro_window.setPosition(x1, y1, x2, y2)

    def setWidth(self, width):
        if isinstance(width, str) and width.isdigit():
            width = int(width)
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)
        self.update()
        old_width = self.default_properties["Border Width"]
        if not old_width.startswith("["):
            self.pro_window.default_properties["Border Width"] = str(width)
            self.default_properties["Border Width"] = str(width)
            self.pro_window.general.border_width.setText(str(width))

    def setColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        self.update()
        old_rgb = self.default_properties["Border Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.pro_window.default_properties["Border Color"] = rgb
            self.default_properties["Border Color"] = rgb
            self.pro_window.general.border_color.setCurrentText(rgb)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        self.changeSomething()

    def getInfo(self):
        self.setPosition()
        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': self.scenePos().x(),
            'Y': self.scenePos().y(),
            **self.pro_window.getInfo(),
        }
        return self.default_properties

    def changeSomething(self):
        x1: str = self.default_properties.get("X1")
        y1: str = self.default_properties.get("Y1")
        x2: str = self.default_properties.get("X2")
        y2: str = self.default_properties.get("Y2")
        if x1.startswith("[") or x2.startswith("[") or y1.startswith("[") or y2.startswith("["):
            pass
        else:
            line = QLineF(float(x1), float(y1), float(x2), float(y2))
            self.setLine(line)
        __color = self.default_properties.get("Border Color")
        color = "0,0,0" if __color.startswith("[") else __color
        r, g, b = [int(x) for x in color.split(",")]
        __width = self.default_properties.get("Border Width")
        width = 2 if __width.startswith("[") else int(__width)
        pen = QPen()
        pen.setColor(QColor(r, g, b))
        pen.setWidth(width)
        self.setPen(pen)
        self.update()

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.pro_window.setProperties(properties)
            self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        new = LineItem(self.line())
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        return new
