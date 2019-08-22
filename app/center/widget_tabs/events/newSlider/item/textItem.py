from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem

# 画图
from app.center.widget_tabs.events.newSlider.item.itemMenu import ItemMenu
from app.center.widget_tabs.events.newSlider.item.text import TextProperty
from app.func import Func
from app.info import Info


class TextItem(QGraphicsTextItem):
    """
    Text
    """
    # Image, Text, Video, Sound = range(5, 9)
    Text = 6

    name = {
        Text: "text",
    }

    def __init__(self, item_type, item_name: str = "", parent=None):
        super(TextItem, self).__init__(parent)

        self.item_type = item_type

        self.item_name = item_name if item_name else self.generateItemName()

        self.attributes: list = []

        if self.item_type == self.Text:
            self.pro_window = TextProperty()

            self.setPlainText('Hello World')

            self.setTextInteractionFlags(Qt.TextEditorInteraction)

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.default_properties = {
            'Name': 'text',
            'Font family': 'SimSun',
            'Font size': '12',
            'Text': 'Hello World',
            'z': self.zValue(),
            'x': 1,
            'y': 1,
        }
        self.menu = ItemMenu()

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
        self.attributes = attributes
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        # get input parameters from GUI
        self.getInfo()
        # take effect
        self.changeSomething()

    def changeSomething(self):
        text = self.toPlainText()

        x = self.default_properties.get("Center x")
        y = self.default_properties.get("Center y")
        z = self.default_properties.get("z")

        style = self.default_properties.get("Style")
        foreColor = self.default_properties.get("Fore color")
        backColor = self.default_properties.get("Back color")
        family = self.default_properties.get("Font family")
        size = self.default_properties.get("Font size")
        transparent = self.default_properties.get("Transparent")

        z = float(z)
        #  handle the ref values
        x = 0 if Func.isCitingValue(x) else int(x)
        y = 0 if Func.isCitingValue(y) else int(y)

        if Func.isCitingValue(style):
            style = 0

        foreColor = "0,0,0" if Func.isCitingValue(foreColor) else foreColor
        backColor = "255,255,255" if Func.isCitingValue(backColor) else backColor
        family = "Times" if Func.isCitingValue(family) else family
        size = 18 if Func.isCitingValue(size) else int(size)
        transparent = "100%" if Func.isCitingValue(transparent) else transparent


        # create html
        html = f'<body style = "font-size: {size}pt; "font-family: {family}">\
                        <p style = "background-color: rgb({backColor})">\
                        <font style = "color: rgb({foreColor})">\
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

        self.setFont(font)

        self.setHtml(html)
        self.setPos(x, y)
        self.setZValue(z)

    def getInfo(self):
        self.default_properties = {
            'Name': self.item_name,
            'Text': self.toPlainText(),
            'z': self.zValue(),
            'x': self.scenePos().x(),
            'y': self.scenePos().y(),
            **self.pro_window.getInfo(),
        }
        return self.default_properties

    def getText(self) -> str:
        return self.toPlainText()

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.pro_window.setProperties(properties)
            self.loadSetting()

    def setPosition(self):
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def loadSetting(self):
        # x = self.default_properties.get("x", 0)
        # y = self.default_properties.get("y", 0)
        # z = self.default_properties.get("z", 0)
        # self.setPos(x, y)
        # self.setZValue(z)

        self.changeSomething()

    def clone(self):
        new = TextItem(self.item_type)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)

        new.setPlainText(self.toPlainText())  # maybe a bug here
        new.setTextInteractionFlags(Qt.TextEditorInteraction)
        new.setZValue(self.zValue())

        return new
