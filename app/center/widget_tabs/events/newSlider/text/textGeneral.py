from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QTextEdit, \
    QFontComboBox, QCompleter

from app.lib import PigComboBox, PigLineEdit, ColorListEditor


class TextGeneral(QWidget):
    def __init__(self, parent=None):
        super(TextGeneral, self).__init__(parent)

        self.attributes: list = []

        self.default_properties = {
            "Text": "Hello World",
            "Center X": "0",
            "Center Y": "0",
            "Fore color": "0,0,0",
            "Back color": "255,255,255",
            "Transparent": "100%",
        }


        self.cx_pos = PigComboBox()
        self.cx_pos.setEditable(True)
        self.cx_pos.addItem('100')

        self.cy_pos = PigComboBox()
        self.cy_pos.setEditable(True)
        self.cy_pos.addItem('100')


        self.fore_color = ColorListEditor()
        self.back_color = ColorListEditor()
        self.fore_color.setCurrentText("black")

        # self.fore_color_name = "black"
        # self.back_color_name = "white"

        self.transparent = PigLineEdit("100%")
        self.transparent.setReg(r"0%|[1-9]\d%|100%")

        self.flip_horizontal = PigComboBox()
        self.flip_horizontal.addItems(("False", "True"))
        self.flip_vertical = PigComboBox()
        self.flip_vertical.addItems(("False", "True"))

        self.font_box = QFontComboBox()

        self.style_box = PigComboBox()
        self.style_box.setEditable(True)
        self.style_box.addItems(
            ("normal_0", "bold_1", "italic_2", "underline_4", "outline_8", "overline_16", "condense_32", "extend_64"))
        # self.style_box.currentTextChanged.connect(self.fontChange)
        self.font_size_box = PigComboBox()
        self.font_size_box.setReg(r"\d+")
        self.font_size_box.setEditable(True)
        for i in range(12, 72, 2):
            self.font_size_box.addItem(str(i))

        self.right_to_left = PigComboBox()
        self.right_to_left.addItems(("no", "yes"))

        self.setUI()

    def setUI(self):
        # l0 = QLabel("Text:")

        l00 = QLabel("Center X:")
        l10 = QLabel("Center Y:")

        l02 = QLabel("Fore Color:")
        l12 = QLabel("Back Color:")

        l30 = QLabel("Transparent:")
        # l32 = QLabel("Wrapat Chars:")

        # l40 = QLabel("flip Horizontal:")
        # l42 = QLabel("flip Vertical:")

        l50 = QLabel("Font Family:")
        l52 = QLabel("Style:")
        l60 = QLabel("Font Size:")
        l70 = QLabel("Right to Left:")

        # l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l70.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # self.x_pos.addItems("0")
        # self.y_pos.addItem("0")

        group2 = QGroupBox("")
        layout2 = QGridLayout()

        layout2.addWidget(l00, 0, 0)
        layout2.addWidget(self.cx_pos, 0, 1)
        layout2.addWidget(l10, 1, 0)
        layout2.addWidget(self.cy_pos, 1, 1)

        layout2.addWidget(l02, 0, 2, 1, 2)
        layout2.addWidget(self.fore_color, 0, 4)
        layout2.addWidget(l12, 1, 2, 1, 2)
        layout2.addWidget(self.back_color, 1, 4)
        layout2.addWidget(l30, 2, 0)

        layout2.addWidget(self.transparent, 2, 1)
        layout2.addWidget(l70, 2, 2, 1, 2)
        layout2.addWidget(self.right_to_left, 2, 4)
        # layout2.addWidget(l40, 3, 0)
        # layout2.addWidget(self.flip_horizontal, 3, 1)
        # layout2.addWidget(l42, 3, 2)
        # layout2.addWidget(self.flip_vertical, 3, 3)
        layout2.addWidget(l50, 4, 0)
        layout2.addWidget(self.font_box, 4, 1, 1, 3)

        layout2.addWidget(l60, 5, 0)
        layout2.addWidget(self.font_size_box, 5, 1)
        layout2.addWidget(l52, 5, 2, 1, 2)
        layout2.addWidget(self.style_box, 5, 4)
        # layout2.addWidget(l70, 6, 0)
        # layout2.addWidget(self.right_to_left, 6, 1)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        # layout.addWidget(group1, 1)
        layout.addWidget(group2, 1)

        self.setLayout(layout)

    """
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
        font.setBold(bool(style & 1))
        font.setItalic(bool(style & 2))
        font.setUnderline(bool(style & 4))
        font.setStrikeOut(bool(style & 8))
        font.setOverline(bool(style & 16))

        self.text_edit.setFont(font)
    
    def refresh(self):
        pass
    """
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.cx_pos.setCompleter(QCompleter(self.attributes))
        self.cy_pos.setCompleter(QCompleter(self.attributes))
        self.fore_color.setCompleter(QCompleter(self.attributes))
        self.back_color.setCompleter(QCompleter(self.attributes))
        self.transparent.setCompleter(QCompleter(self.attributes))
        self.right_to_left.setCompleter(QCompleter(self.attributes))
        self.font_size_box.setCompleter(QCompleter(self.attributes))
        self.style_box.setCompleter(QCompleter(self.attributes))

    # def apply(self):
    #     self.html = self.text_edit.toHtml()

    def getInfo(self):
        self.default_properties.clear()
        # self.default_properties["Html"] = self.html
        # self.default_properties["Text"] = self.text_edit.toPlainText()
        self.default_properties["Center x"] = self.cx_pos.currentText()
        self.default_properties["Center y"] = self.cy_pos.currentText()
        self.default_properties["Fore color"] = self.fore_color.getColor()
        # print(f"line 230 getColor:{self.fore_color.getColor()}")
        self.default_properties["Back color"] = self.back_color.getColor()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Font family"] = self.font_box.currentText()
        self.default_properties["Font size"] = self.font_size_box.currentText()
        self.default_properties["Style"] = self.style_box.currentText()
        # self.default_properties["Flip horizontal"] = self.flip_horizontal.currentText()
        # self.default_properties["Flip vertical"] = self.flip_vertical.currentText()
        self.default_properties["Right to left"] = self.right_to_left.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        # self.html = html
        self.loadSetting()

    def setPosition(self, x, y):
        self.cx_pos.setCurrentText(str(int(x)))
        self.cy_pos.setCurrentText(str(int(y)))

    def loadSetting(self):
        # self.text_edit.setHtml(self.html)
        self.cx_pos.setCurrentText(self.default_properties["Center x"])
        self.cy_pos.setCurrentText(self.default_properties["Center y"])
        self.fore_color.setCurrentText(self.default_properties["Fore color"])
        self.back_color.setCurrentText(self.default_properties["Back color"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.right_to_left.setCurrentText(self.default_properties["Right to left"])
        # self.word_wrap.setText(self.default_properties["Wrapat chars"])
        self.font_box.setCurrentText(self.default_properties["Font family"])
        self.font_size_box.setCurrentText(self.default_properties["Font size"])


        self.style_box.setCurrentText(self.default_properties["Style"])
        # self.flip_horizontal.setCurrentText(self.default_properties["Flip horizontal"])
        # self.flip_vertical.setCurrentText(self.default_properties["Flip vertical"])

    def clone(self):
        clone_page = TextGeneral()
        clone_page.setProperties(self.default_properties)
        return clone_page
