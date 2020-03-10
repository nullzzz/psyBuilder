import re

from PyQt5.QtCore import QDataStream, QIODevice, QRegExp, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit

from .message_box import MessageBox


class PigLineEdit(QLineEdit):
    focusLost = pyqtSignal()

    def __init__(self, *__args):
        super(PigLineEdit, self).__init__(*__args)
        self.setAcceptDrops(True)
        self.textChanged.connect(self.findVar)
        self.editingFinished.connect(self.checkValidity)
        self.returnPressed.connect(self.checkValidity)
        self.focusLost.connect(self.checkValidity)
        self.valid_data: str = self.text()

        # font = self.font()  # lineedit current font
        # font.setPointSize(12)  # change it's size
        # font.setFamily("Times")
        # self.setFont(font)  # set font

        self.suffix: str = ""
        self.reg_exp: str = ""

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("attributes/move-attribute"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data("attributes/move-attribute")
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.setText(text)

    # 检查变量
    def findVar(self, text: str):
        if text.startswith("[") and text.endswith("]"):
            self.setStyleSheet("color: blue")
            self.setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.setStyleSheet("color: black")
            self.setFont(QFont("宋体", 9, QFont.Normal))

    def setSuffix(self, suffix: str):
        self.suffix = suffix

    def setReg(self, reg_exp: str):
        self.reg_exp = reg_exp + r"|\[[_\d\w]+\]"
        self.setValidator(QRegExpValidator(QRegExp(self.reg_exp), self))

    def addSuffix(self, text: str):
        if text != "" and not text.endswith(self.suffix):
            self.setText(text.replace(self.suffix, "") + self.suffix)
            self.cursorForward(False)

    def focusOutEvent(self, e):
        self.focusLost.emit()
        QLineEdit.focusOutEvent(self, e)

    def checkValidity(self):
        cur = self.text()
        if self.reg_exp != "" and re.fullmatch(self.reg_exp, cur) is None:
            self.setText(self.valid_data)
            MessageBox.warning(self, "Invalid", f"Invalid Parameter {cur}\nformat must conform to\n {self.reg_exp}")
        else:
            self.valid_data = cur
