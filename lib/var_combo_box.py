import re

from PyQt5.QtCore import QDataStream, QIODevice, Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import QComboBox, QMessageBox

from app.info import Info


class VarComboBox(QComboBox):
    focusLost = pyqtSignal()

    def __init__(self, parent=None):
        super(VarComboBox, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.currentTextChanged.connect(self.findVar)
        self.focusLost.connect(self.checkValidity)
        # self.lineEdit().returnPressed.connect(self.checkValidity)
        self.valid_data: str = ""
        self.reg_exp = ""

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data(Info.AttributesToWidget)
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        index = self.findText(text, Qt.MatchExactly)
        if index == -1:
            self.addItem(text)
        self.setCurrentText(text)

    # 检查变量
    def findVar(self, text: str):
        if text.startswith("[") and text.endswith("]"):
            self.setStyleSheet("color: blue")
            self.setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.setStyleSheet("color: black")
            self.setFont(QFont("宋体", 9, QFont.Normal))

    def setReg(self, reg_exp: str):
        self.reg_exp = reg_exp + r"|\[[\w\d_\.]+\]"
        self.setValidator(QRegExpValidator(QRegExp(self.reg_exp), self))

    def focusOutEvent(self, e):
        self.focusLost.emit()
        QComboBox.focusOutEvent(self, e)

    def checkValidity(self):
        cur = self.currentText()
        if self.reg_exp != "" and re.fullmatch(self.reg_exp, cur) is None:
            self.setCurrentText(self.valid_data)
            QMessageBox.warning(self, "Invalid", f"Invalid Parameter {cur}\nformat must conform to\n {self.reg_exp}")
        else:
            self.valid_data = cur
