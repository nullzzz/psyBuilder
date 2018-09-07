from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QComboBox, QSpinBox, QApplication, \
    QMessageBox, QTextEdit, QCheckBox, QFontDialog, QPushButton

from center.iconTabs.colorBobox import ColorListEditor


# text event专属页面
class TextTab1(QWidget):
    def __init__(self, parent=None):
        super(TextTab1, self).__init__(parent)
        self.attributes = []
        self.text = QTextEdit()

        self.align = QComboBox()
        self.fore_color = ColorListEditor()
        self.fore_color.setCurrentText("black")
        self.back_color = ColorListEditor()
        self.transparent = QSpinBox()
        self.screen_name = QComboBox()
        self.clear_after = QComboBox()
        # self.word_wrap = QComboBox()
        self.word_wrap = QCheckBox("Word wrap")
        self.font = QFont("宋体", 9)
        self.font_bt = QPushButton("Font")
        self.font_bt.clicked.connect(self.getFont)
        self.font_label = QLabel()
        self.setGeneral()

    def setGeneral(self):
        l1 = QLabel("Text:")
        l2 = QLabel("Alignment:")
        l3 = QLabel("Screen Name:")
        l4 = QLabel("Fore Color:")
        l5 = QLabel("Back Color:")
        l6 = QLabel("Clear After:")
        l7 = QLabel("Transparent:")
        # l8 = QLabel("Word wrap:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.align.addItems(["Center", "Left", "Right", "Justify"])
        self.clear_after.addItems(["Yes", "No"])
        # self.word_wrap.addItems(["Yes", "No"])

        self.transparent.setMaximum(100)
        self.transparent.setSuffix("%")
        self.transparent.setValue(100)
        self.screen_name.addItems(["Display"])

        group1 = QGroupBox("Text")
        layout1 = QGridLayout()
        # layout1.addWidget(QLabel("Text"), 0, 0)
        layout1.addWidget(self.text, 0, 0)
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
        layout2.addWidget(self.font_label, 3, 1)
        layout2.addWidget(self.word_wrap, 3, 3)
        # layout2.addWidget(self.font_label, 4, 0, 1, 4)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 1)
        layout.addWidget(group2, 1)
        self.setLayout(layout)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color: black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def getFont(self):
        font, ok = QFontDialog.getFont(QFont(self.font_label.text()), self)
        if ok:
            self.font = font
            self.font_label.setText(font.family())
            normal_font = font
            normal_font.setPointSize(12)
            # self.font_label.setFont(normal_font)
            self.font_label.setFont(normal_font)

    def setAttributes(self, attributes):
        self.attributes = attributes

    def getInfo(self):
        return {
            "Text": self.text.toPlainText(),
            "Alignment": self.align.currentText(),
            "Fore color": self.fore_color.currentText(),
            "Back color": self.back_color.currentText(),
            "Screen name": self.screen_name.currentText(),
            "Transparent": "{}%".format(self.transparent.value()),
            "Word wrap": bool(self.word_wrap.checkState()),
            "Clear after": self.clear_after.currentText()
        }


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = TextTab1()

    t.show()

    sys.exit(app.exec())
