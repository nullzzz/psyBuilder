from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem

from app.func import Func
from app.info import Info
from ..item.text import TextProperty


# todo: unknown
class TextItem(QGraphicsTextItem):
    """
    Text
    """
    # Image, Text, Video, Sound = range(5, 9)
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
        font.setPointSize(20)  # set the inital font size to 20 pt (dot)
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
            'Font Family': 'SimSun',
            'Font Size': '20',
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

    def changeSomething(self):

        text = self.toPlainText()

        x = self.properties.get("Center X")
        y = self.properties.get("Center Y")

        style = self.properties.get("Style")
        fore_color = self.properties.get("Fore Color")
        back_color = self.properties.get("Back Color")
        family = self.properties.get("Font Family")
        size = self.properties.get("Font Size")

        #  handle the ref values
        x = 0 if Func.isCitingValue(x) else int(x)
        y = 0 if Func.isCitingValue(y) else int(y)

        if Func.isCitingValue(style):
            style = 0

        fore_color = "0,0,0" if Func.isCitingValue(fore_color) else fore_color
        back_color = "255,255,255" if Func.isCitingValue(back_color) else back_color
        family = "Times" if Func.isCitingValue(family) else family
        size = 20 if Func.isCitingValue(size) else int(size)

        # create html
        html = f'<body style = "font-size: {size}pt; "font-family: {family}">\
                        <p style = "background-color: rgb({back_color})">\
                        <font style = "color: rgb({fore_color})">\
                         {text}</font></p></body>'

        font = QFont()

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

        style = int(style)

        font.setBold(bool(style & 1))
        font.setItalic(bool(style & 2))
        font.setUnderline(bool(style & 4))
        font.setStrikeOut(bool(style & 8))
        font.setOverline(bool(style & 16))
        if bool(style & 32):
            font.setStretch(75)  # condensed 75

        if bool(style & 64):
            font.setStretch(125)  # expanded 125
        # see detail in below site:
        # https://doc.qt.io/qtforpython/PySide2/QtGui/QFont.html

        self.setFont(font)

        self.setHtml(html)
        self.setPos(x, y)

    def getText(self) -> str:
        return self.toPlainText()

    def getInfo(self):
        return self.default_properties

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

    def clone(self):
        self.updateInfo()
        new = TextItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(TextItem, self).setZValue(z)
