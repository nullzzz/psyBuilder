from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem

from app.info import Info
from .text import TextProperty


class TextItem(QGraphicsTextItem):
    Text = 8

    name = {
        Text: Info.ITEM_TEXT,
    }

    def __init__(self, item_type, item_name: str = ""):
        super(TextItem, self).__init__()

        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        self.pro_window = TextProperty()

        self.setPlainText('Hello World')
        font = QFont()
        font.setPointSize(20)  # set the initial font size to 20 pt (dot)
        self.setFont(font)

        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.properties = self.pro_window.default_properties
        self.default_properties = {
            'Name': self.item_name,
            'Text': 'Hello World',
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            "Properties": self.properties,
        }

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def getName(self):
        return self.item_name

    def openPro(self):
        self.setPosition()
        self.pro_window.show()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

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

    def changeSomething(self):
        __lx = self.properties.get("Left X")
        cx = int(__lx) if __lx.isdigit() else self.scenePos().x()
        __ty = self.properties.get("Top Y")
        cy = int(__ty) if __ty.isdigit() else self.scenePos().y()
        self.setPos(cx, cy)

        family = self.pro_window.general.font_box.currentFont().family()
        size = self.properties.get("Font Size")
        if size.isdigit():
            size = int(size)
        else:
            size = 20

        fore_color = self.properties.get("Fore Color")
        if fore_color.startswith("["):
            fore_color = "0,0,0"

        back_color = self.properties.get("Back Color")
        if back_color.startswith("["):
            back_color = "255,255,255"

        # r2l = self.properties.get("Right To Left")

        # if r2l == "Yes":
        #     textWithDir = '<dir="rtl"' + self.getText() + ">"
        # else:
        #     textWithDir = self.getText()

        html = f'<body style = "font-size: {size}pt; "font-family: {family}">\
                        <p style = "background-color: rgb({back_color})">\
                        <font style = "color: rgb({fore_color})">\
                         {self.getText()}</font></p></body>'
        style = self.properties.get("Style")
        if style == "normal_0":
            style = 0
        elif style == "bold_1":
            style = 1
        elif style == "italic_2":
            style = 2
        elif style == "underline_4":
            style = 4
        elif style == "outline_8":
            style = 8
        elif style == "overline_16":
            style = 16
        elif style == "condense_32":
            style = 32
        elif style == "extend_64":
            style = 64
        else:
            style = 0
        font = self.font()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(style & 1)
        font.setItalic(style & 2)
        font.setUnderline(style & 4)
        font.setStrikeOut(style & 8)
        font.setOverline(style & 16)
        if style & 32:
            font.setStretch(75)  # condensed 75
        if style & 64:
            font.setStretch(125)  # expanded 125
        self.setFont(font)
        self.setHtml(html)

    def getText(self) -> str:
        return self.toPlainText()

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.default_properties["X"] = properties["X"]
        self.default_properties["Y"] = properties["Y"]
        self.default_properties["Z"] = properties["Z"]
        self.loadSetting()

    def setPosition(self):
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    def clone(self):
        self.updateInfo()
        new = TextItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(TextItem, self).setZValue(z)

    def mouseDoubleClickEvent(self, event):
        self.openPro()