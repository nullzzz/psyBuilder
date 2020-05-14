import re

from PyQt5.QtCore import QDataStream, QIODevice, QRegExp, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit

from app.info import Info
from .message_box import MessageBox


class VarLineEdit(QLineEdit):
    focusLost = pyqtSignal()

    Attribute = r"^\[[_\d\.\w]+\]$"
    Float = r"^(-?\d+)(\.\d+)?$"
    Integer = r"^-?\d+$"
    Percentage = r"^(100|[1-9]?\d?)%$|0$"

    def __init__(self, *__args):
        super(VarLineEdit, self).__init__(*__args)
        self.setAcceptDrops(True)
        self.textChanged.connect(self.findVar)
        self.focusLost.connect(self.checkValidity)
        self.valid_data: str = self.text()

        self.suffix: str = ""
        self.reg_exp: str = ""

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data(Info.AttributesToWidget)
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

    def setReg(self, reg_exp: str or list or tuple):
        if isinstance(reg_exp, str):
            self.reg_exp = f"{reg_exp}|{VarLineEdit.Attribute}"
        elif isinstance(reg_exp, list) or isinstance(reg_exp, tuple):
            self.reg_exp = f"{'|'.join(reg_exp)}|{VarLineEdit.Attribute}"
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
            MessageBox.warning(self, "Invalid", f"Invalid Parameter '{cur}'\nFormat must conform to\n{self.reg_exp}")
        else:
            self.valid_data = cur

    def setColor(self, rgb):
        self.setStyleSheet("background: {}".format(rgb))
