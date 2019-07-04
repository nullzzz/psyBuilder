from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextOption
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QApplication, QMessageBox, \
    QTextEdit, QCheckBox, QFontDialog, QPushButton

# text event专属页面
# 文本颜色设置为全体文本
# 对齐方式也是
from app.lib import PigComboBox, PigLineEdit, ColorListEditor


class TextTab1(QWidget):
    def __init__(self, parent=None):
        super(TextTab1, self).__init__(parent)
        self.html_header = (
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n")
        self.html_font = "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; " \
                         "font-style:normal;\">"

        self.attributes = []

        self.default_properties = {
            "Text": "",
            "Alignment": "Center",
            "Fore color": "0,0,0",
            "Back color": "255,255,255",
            "Screen name": "screen.0",
            "Transparent": 100,
            "Font": "SimSun",
            "Word wrap": 0,
            "Clear after": "Yes"
        }

        self.text_edit = QTextEdit()
        self.html = ""
        self.align = PigComboBox()
        self.align.currentTextChanged.connect(self.alignChange)
        self.align_mode = "center"
        self.fore_color = ColorListEditor()
        self.back_color = ColorListEditor()
        self.fore_color.setCurrentText("black")
        self.fore_color_name = "black"
        self.back_color_name = "white"
        self.fore_color.currentTextChanged.connect(self.colorChange)
        self.back_color.currentTextChanged.connect(self.colorChange)

        # self.transparent = QSpinBox()
        self.transparent = PigLineEdit()
        self.screen_name = PigComboBox()
        self.clear_after = PigComboBox()
        self.word_wrap = QCheckBox("Word wrap")
        self.word_wrap.stateChanged.connect(self.checkWrap)
        self.is_wrap = False
        self.font = QFont("SimSun", 9)
        self.new_font = QFont("SimSun", 9)

        self.font_bt = QPushButton("Font")
        self.font_bt.clicked.connect(self.getFont)
        self.font_label = QLabel()
        self.font_label.setText("SimSun")
        self.font_label.setFont(self.font)
        self.setGeneral()

    def setGeneral(self):
        l1 = QLabel("Text:")
        l2 = QLabel("Alignment:")
        l3 = QLabel("Screen Name:")
        l4 = QLabel("Fore Color:")
        l5 = QLabel("Back Color:")
        l6 = QLabel("Clear After:")
        l7 = QLabel("Transparent:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.align.addItems(["Center", "Left", "Right", "Justify"])
        self.clear_after.addItems(["Yes", "No"])

        self.transparent.setText("100%")
        self.screen_name.addItems(["screen.0"])

        group1 = QGroupBox("Text")
        layout1 = QGridLayout()
        layout1.addWidget(self.text_edit, 0, 0)
        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        layout2.addWidget(l2, 0, 0)
        layout2.addWidget(self.align, 0, 1)
        layout2.addWidget(l3, 1, 0)
        layout2.addWidget(self.screen_name, 1, 1)
        layout2.addWidget(l4, 0, 2)
        layout2.addWidget(self.fore_color, 0, 3)
        layout2.addWidget(l5, 1, 2)
        layout2.addWidget(self.back_color, 1, 3)
        layout2.addWidget(l6, 2, 0)
        layout2.addWidget(self.clear_after, 2, 1)
        layout2.addWidget(l7, 2, 2)
        layout2.addWidget(self.transparent, 2, 3)
        layout2.addWidget(self.font_bt, 3, 0)
        layout2.addWidget(self.font_label, 3, 1, 1, 2)
        layout2.addWidget(self.word_wrap, 3, 3)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 1)
        layout.addWidget(group2, 1)
        self.setLayout(layout)

    def colorChange(self, color):
        if "," in color:
            color = f"rgb({color})"
        print(color)
        if "." in color:
            return
        if self.sender() == self.fore_color:
            self.fore_color_name = color
        elif self.sender() == self.back_color:
            self.back_color_name = color
        self.setAll()

    def alignChange(self, align_mode: str):
        # html中要小写
        self.align_mode = align_mode.lower()
        self.setAll()

    # 获取字体
    def getFont(self):
        font, ok = QFontDialog.getFont(self.new_font, self)
        if ok:
            self.new_font = font
            self.font_label.setText(font.family())
            self.font_label.setFont(QFont(font.family(), 9))
            self.setAll()

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setScreen(self, screen: list):
        selected = self.screen_name.currentText()
        self.screen_name.clear()
        self.screen_name.addItems(screen)
        if selected in screen:
            self.screen_name.setCurrentText(selected)

    # 处理html获得格式
    # 对齐方式、颜色、内容
    def setAll(self):
        texts = self.text_edit.toPlainText().split("\n")
        self.html_font = f"</style></head><body style=\" font-family:'{self.new_font.family()}'; font-size:" \
            f"{self.new_font.pointSize()}pt; font-weight:{self.new_font.weight()}; font-style:" \
            f"{self.new_font.styleName()};\">"
        html = self.html_header + self.html_font
        for text in texts:
            html += f"\n<p align=\"{self.align_mode}\"style=\" margin-top:0px; margin-bottom:0px; " \
                f"margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent: 0px;\"><span style=\" " \
                f"color:{self.fore_color_name}; background-color:{self.back_color_name};\">{text}</span>"

        self.text_edit.setHtml(html)
        # 字体的style和划线在html中不体现
        self.text_edit.setFont(self.new_font)

    # 是否换行
    def checkWrap(self):
        self.is_wrap = self.word_wrap.checkState()
        if self.is_wrap:
            self.text_edit.setWordWrapMode(QTextOption.WordWrap)
        else:
            self.text_edit.setWordWrapMode(QTextOption.NoWrap)

    def apply(self):
        self.font = self.new_font
        self.html = self.text_edit.toHtml()

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Html"] = self.html
        self.default_properties["Text"] = self.text_edit.toPlainText()
        self.default_properties["Alignment"] = self.align.currentText()
        self.default_properties["Fore color"] = self.fore_color.getColor()
        self.default_properties["Back color"] = self.back_color.getColor()
        self.default_properties["Screen name"] = self.screen_name.currentText()
        self.default_properties["Transparent"] = self.transparent.text()
        # self.default_properties["Transparent"] = self.transparent.value()
        self.default_properties["Font"] = self.font.family()
        self.default_properties["Word wrap"] = self.word_wrap.checkState()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        return self.default_properties

    def setProperties(self, properties: dict, html: str, font: QFont):
        self.default_properties = properties.copy()
        self.html = html
        self.font = font
        self.loadSetting()

    def loadSetting(self):
        self.text_edit.setHtml(self.html)
        self.text_edit.setFont(self.font)
        self.font_label.setText(self.font.family())
        self.font_label.setFont(QFont(self.font.family(), 12))

        self.align.setCurrentText(self.default_properties["Alignment"])
        self.fore_color.setCurrentText(self.default_properties["Fore color"])
        self.back_color.setCurrentText(self.default_properties["Back color"])
        self.screen_name.setCurrentText(self.default_properties["Screen name"])
        self.transparent.setText(self.default_properties["Transparent"])
        # self.transparent.setValue(self.default_properties["Transparent"])
        self.word_wrap.setCheckState(self.default_properties["Word wrap"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])

    def clone(self):
        clone_page = TextTab1()
        clone_page.setProperties(self.default_properties, self.html, self.font)
        return clone_page


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = TextTab1()

    t.show()

    sys.exit(app.exec())
