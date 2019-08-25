from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QFontComboBox, QCompleter

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
        self.flip_horizontal.addItems(("No", "Yes"))
        self.flip_vertical = PigComboBox()
        self.flip_vertical.addItems(("No", "Yes"))

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
            self.font_size_box.setCurrentText('20')

        self.right_to_left = PigComboBox()
        self.right_to_left.addItems(("No", "Yes"))

        self.setUI()

    def setUI(self):
        # l00 = QLabel("Center X:")
        # l10 = QLabel("Center Y:")
        l00 = QLabel("Left X:")
        l10 = QLabel("Top  Y:")

        l02 = QLabel("Fore Color:")
        l12 = QLabel("Back Color:")

        l30 = QLabel("Transparent:")

        l50 = QLabel("Font Family:")
        l52 = QLabel("Style:")
        l60 = QLabel("Font Size:")
        l70 = QLabel("Right to Left:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l70.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
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

        layout2.addWidget(l50, 4, 0)
        layout2.addWidget(self.font_box, 4, 1, 1, 3)

        layout2.addWidget(l60, 5, 0)
        layout2.addWidget(self.font_size_box, 5, 1)
        layout2.addWidget(l52, 5, 2, 1, 2)
        layout2.addWidget(self.style_box, 5, 4)

        group2.setLayout(layout2)

        layout = QVBoxLayout()

        layout.addWidget(group2, 1)

        self.setLayout(layout)

    """
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
        # self.right_to_left.setCompleter(QCompleter(self.attributes))
        self.font_size_box.setCompleter(QCompleter(self.attributes))
        self.style_box.setCompleter(QCompleter(self.attributes))

    # def apply(self):
    #     self.html = self.text_edit.toHtml()

    def getInfo(self):
        self.default_properties.clear()

        self.default_properties["Center x"] = self.cx_pos.currentText()
        self.default_properties["Center y"] = self.cy_pos.currentText()
        self.default_properties["Fore color"] = self.fore_color.getColor()

        self.default_properties["Back color"] = self.back_color.getColor()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Font family"] = self.font_box.currentText()
        self.default_properties["Font size"] = self.font_size_box.currentText()
        self.default_properties["Style"] = self.style_box.currentText()
        self.default_properties["Right to left"] = self.right_to_left.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        # self.html = html
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.cx_pos.currentText().startswith("["):
            self.cx_pos.setCurrentText(str(int(x)))
        if not self.cy_pos.currentText().startswith("["):
            self.cy_pos.setCurrentText(str(int(y)))

    def loadSetting(self):
        self.cx_pos.setCurrentText(self.default_properties["Center x"])
        self.cy_pos.setCurrentText(self.default_properties["Center y"])
        self.fore_color.setCurrentText(self.default_properties["Fore color"])
        self.back_color.setCurrentText(self.default_properties["Back color"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.right_to_left.setCurrentText(self.default_properties["Right to left"])
        self.font_box.setCurrentText(self.default_properties["Font family"])
        self.font_size_box.setCurrentText(self.default_properties["Font size"])

        self.style_box.setCurrentText(self.default_properties["Style"])

    def clone(self):
        clone_page = TextGeneral()
        clone_page.setProperties(self.default_properties)
        return clone_page
