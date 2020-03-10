from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QTextEdit, \
    QFontComboBox, QCompleter

from app.func import Func
from lib import VarComboBox, VarLineEdit, ColorListEditor


class TextTab1(QWidget):
    def __init__(self, parent=None):
        super(TextTab1, self).__init__(parent)

        self.attributes: list = []

        self.default_properties = {
            "Text": "",
            "Alignment": "center",
            "Fore color": "0,0,0",
            "Back color": "255,255,255",
            "Screen name": "screen.0",
            "Transparent": "100%",
            "Word wrap": 0,
            "Clear after": "Yes"
        }

        self.text_edit = QTextEdit()
        self.text_edit.setLineWrapMode(QTextEdit.FixedColumnWidth)
        self.html = ""
        self.align_mode = "center"

        self.align_x = VarComboBox()
        self.align_x.setEditable(True)
        self.align_x.currentTextChanged.connect(self.alignChange)
        self.align_y = VarComboBox()
        self.align_y.setEditable(True)
        self.align_y.currentTextChanged.connect(self.alignChange)

        self.fore_color = ColorListEditor()
        self.back_color = ColorListEditor()
        self.fore_color.setCurrentText("black")
        self.fore_color_name = "black"
        self.back_color_name = "white"
        self.fore_color.colorChanged.connect(self.colorChange)
        self.back_color.colorChanged.connect(self.colorChange)

        self.clear_after = VarComboBox()
        self.transparent = VarLineEdit("100%")
        self.transparent.setReg(r"0%|[1-9]\d%|100%")
        self.word_wrap = VarLineEdit("80")
        self.word_wrap.setReg(r"\d+")
        self.word_wrap.textChanged.connect(self.wrapChange)
        self.text_edit.setLineWrapColumnOrWidth(80)

        self.flip_horizontal = VarComboBox()
        self.flip_horizontal.addItems(("No", "Yes"))
        self.flip_vertical = VarComboBox()
        self.flip_vertical.addItems(("No", "Yes"))

        self.font_box = QFontComboBox()
        self.font_box.currentFontChanged.connect(self.fontChange)
        self.style_box = VarComboBox()
        self.style_box.setEditable(True)
        self.style_box.addItems(
            ("normal_0", "bold_1", "italic_2", "underline_4", "outline_8", "overline_16", "condense_32", "extend_64"))
        self.style_box.currentTextChanged.connect(self.fontChange)
        self.font_size_box = VarComboBox()
        self.font_size_box.setReg(r"\d+")
        self.font_size_box.setEditable(True)
        for i in range(12, 72, 2):
            self.font_size_box.addItem(str(i))

        self.font_size_box.currentIndexChanged.connect(self.fontChange)

        self.right_to_left = VarComboBox()
        self.right_to_left.addItems(("No", "Yes"))

        self.using_screen_id: str = "screen.0"
        self.screen = VarComboBox()
        self.screen_info = Func.getScreenInfo()
        self.screen.addItems(self.screen_info.values())
        self.screen.currentTextChanged.connect(self.changeScreen)

        self.setUI()

    def setUI(self):
        l0 = QLabel("Text:")

        l00 = QLabel("Alignment X:")
        l10 = QLabel("Alignment Y:")

        l02 = QLabel("Fore Color:")
        l12 = QLabel("Back Color:")

        l20 = QLabel("Dont Clear After:")
        l22 = QLabel("Screen Name:")

        l30 = QLabel("Transparent:")
        l32 = QLabel("Wrapat Chars:")

        l40 = QLabel("flip Horizontal:")
        l42 = QLabel("flip Vertical:")

        l50 = QLabel("Font Family:")
        l52 = QLabel("Style:")
        l60 = QLabel("Font Size:")
        l70 = QLabel("Right to Left:")

        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l70.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.align_x.addItems(["center", "left", "right", "wrapat", "justifytomax"])
        self.align_y.addItem("center")

        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        self.screen.addItems(["screen.0"])

        group1 = QGroupBox("Text")
        layout1 = QGridLayout()
        layout1.addWidget(self.text_edit, 0, 0)
        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        layout2.addWidget(l00, 0, 0)
        layout2.addWidget(self.align_x, 0, 1)
        layout2.addWidget(l10, 1, 0)
        layout2.addWidget(self.align_y, 1, 1)

        layout2.addWidget(l02, 0, 2)
        layout2.addWidget(self.fore_color, 0, 3)
        layout2.addWidget(l12, 1, 2)
        layout2.addWidget(self.back_color, 1, 3)

        layout2.addWidget(l20, 2, 0)
        layout2.addWidget(self.clear_after, 2, 1)
        layout2.addWidget(l22, 2, 2)
        layout2.addWidget(self.screen, 2, 3)

        layout2.addWidget(l30, 3, 0)
        layout2.addWidget(self.transparent, 3, 1)
        layout2.addWidget(l32, 3, 2)
        layout2.addWidget(self.word_wrap, 3, 3)

        layout2.addWidget(l40, 4, 0)
        layout2.addWidget(self.flip_horizontal, 4, 1)
        layout2.addWidget(l42, 4, 2)
        layout2.addWidget(self.flip_vertical, 4, 3)

        layout2.addWidget(l50, 5, 0)
        layout2.addWidget(self.font_box, 5, 1, 1, 3)
        layout2.addWidget(l52, 6, 2)
        layout2.addWidget(self.style_box, 6, 3)
        layout2.addWidget(l60, 6, 0)
        layout2.addWidget(self.font_size_box, 6, 1)
        layout2.addWidget(l70, 7, 0)
        layout2.addWidget(self.right_to_left, 7, 1)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 1)
        layout.addWidget(group2, 2)
        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getScreenInfo()
        screen_id = self.using_screen_id
        self.screen.clear()
        self.screen.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen.setCurrentText(screen_name)
            self.using_screen_id = screen_id

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def colorChange(self, color: str):
        r, g, b = 255, 255, 255
        if "," in color:
            r, g, b = [int(x) for x in color.split(",")]
        if self.sender() == self.fore_color:
            self.fore_color_name = color
            self.text_edit.setTextColor(QColor(r, g, b))
        elif self.sender() == self.back_color:
            self.back_color_name = color
            self.text_edit.setTextBackgroundColor(QColor(r, g, b))

    def alignChange(self, align_mode: str):
        # html中要小写
        self.align_mode = align_mode.lower()
        if align_mode == "center":
            self.text_edit.setAlignment(Qt.AlignCenter)
        elif align_mode == "left":
            self.text_edit.setAlignment(Qt.AlignLeft)
        elif align_mode == "right":
            self.text_edit.setAlignment(Qt.AlignRight)
        elif align_mode == "justifytomax":
            self.text_edit.setAlignment(Qt.AlignJustify)

    def wrapChange(self, chars: str):
        if chars.isdigit():
            self.text_edit.setLineWrapColumnOrWidth(int(chars))
        else:
            self.text_edit.setLineWrapColumnOrWidth(80)

    def fontChange(self):
        f = self.font_box.currentFont().family()

        size = self.font_size_box.currentText()
        size = int(size) if size.isdigit() else 8
        font = self.text_edit.currentFont()
        font.setFamily(f)
        font.setPointSize(size)

        style = self.style_box.currentText()
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
            style = int(style) if style.isdigit() else 0
        font.setBold(style & 1)
        font.setItalic(style & 2)
        font.setUnderline(style & 4)
        font.setStrikeOut(style & 8)
        font.setOverline(style & 16)

        self.text_edit.setFont(font)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.align_x.setCompleter(QCompleter(self.attributes))
        self.align_y.setCompleter(QCompleter(self.attributes))
        self.fore_color.setCompleter(QCompleter(self.attributes))
        self.back_color.setCompleter(QCompleter(self.attributes))
        # self.clear_after.setCompleter(QCompleter(self.attributes))
        # self.screen_name.setCompleter(QCompleter(self.attributes))
        self.transparent.setCompleter(QCompleter(self.attributes))
        self.word_wrap.setCompleter(QCompleter(self.attributes))
        # self.flip_vertical.setCompleter(QCompleter(self.attributes))
        # self.flip_horizontal.setCompleter(QCompleter(self.attributes))
        # self.font_box.setCompleter(QCompleter(self.attributes))
        self.font_size_box.setCompleter(QCompleter(self.attributes))
        self.style_box.setCompleter(QCompleter(self.attributes))
        # self.right_to_left.setCompleter(QCompleter(self.attributes))

    def setScreen(self, screen: list):
        selected = self.screen.currentText()
        self.screen.clear()
        self.screen.addItems(screen)
        if selected in screen:
            self.screen.setCurrentText(selected)
        else:
            new_name = Func.getDeviceNameById(self.using_device_id)
            if new_name:
                self.screen.setCurrentText(new_name)

    def apply(self):
        self.html = self.text_edit.toHtml()

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Html"] = self.html
        self.default_properties["Text"] = self.text_edit.toPlainText()
        self.default_properties["Alignment X"] = self.align_x.currentText()
        self.default_properties["Alignment Y"] = self.align_y.currentText()
        self.default_properties["Fore color"] = self.fore_color.getColor()
        self.default_properties["Back color"] = self.back_color.getColor()
        self.default_properties["Screen name"] = self.screen.currentText()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        self.default_properties["Font family"] = self.font_box.currentText()
        self.default_properties["Font size"] = self.font_size_box.currentText()
        self.default_properties["Wrapat chars"] = self.word_wrap.text()
        self.default_properties["Style"] = self.style_box.currentText()
        self.default_properties["Flip horizontal"] = self.flip_horizontal.currentText()
        self.default_properties["Flip vertical"] = self.flip_vertical.currentText()
        self.default_properties["Right to left"] = self.right_to_left.currentText()

        return self.default_properties

    def setProperties(self, properties: dict, html: str):
        self.default_properties = properties.copy()
        self.html = html
        self.loadSetting()

    def loadSetting(self):
        self.text_edit.setHtml(self.default_properties["Html"])

        self.align_x.setCurrentText(self.default_properties["Alignment X"])
        self.align_y.setCurrentText(self.default_properties["Alignment Y"])
        self.fore_color.setCurrentText(self.default_properties["Fore color"])
        self.back_color.setCurrentText(self.default_properties["Back color"])
        self.screen.setCurrentText(self.default_properties["Screen name"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.word_wrap.setText(self.default_properties["Wrapat chars"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.font_box.setCurrentText(self.default_properties["Font family"])
        self.font_size_box.setCurrentText(self.default_properties["Font size"])
        self.style_box.setCurrentText(self.default_properties["Style"])

        self.flip_horizontal.setCurrentText(self.default_properties["Flip horizontal"])
        self.flip_vertical.setCurrentText(self.default_properties["Flip vertical"])
        self.right_to_left.setCurrentText(self.default_properties["Right to left"])

    def clone(self):
        clone_page = TextTab1()
        clone_page.setProperties(self.default_properties, self.html)
        return clone_page
