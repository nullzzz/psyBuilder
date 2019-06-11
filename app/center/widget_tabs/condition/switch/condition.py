from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QMessageBox, QCompleter

from app.lib import PigComboBox


class SwitchCondition(QWidget):
    def __init__(self, parent=None):
        super(SwitchCondition, self).__init__(parent)

        self.attributes: list = []

        self.switch_choice = PigComboBox()
        self.switch_choice.setEditable(True)
        self.switch_choice.setInsertPolicy(QComboBox.NoInsert)
        self.switch_choice.lineEdit().textChanged.connect(self.findVar)
        self.switch_choice.lineEdit().returnPressed.connect(self.finalCheck)
        self.switch_choice.currentTextChanged.connect(self.changeSwitch)
        self.vars: list = []
        self.current_var = ""
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Switch", self.switch_choice)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def addVar(self, var_choice: list):
        self.vars = var_choice
        self.switch_choose.addItems(var_choice)

    def changeSwitch(self, new_var):
        self.current_var = new_var

    def getProperties(self):
        return self.current_var

    def setProperties(self, new_var: str):
        self.switch_choice.setCurrentText(new_var)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.switch_choice.addItems(attributes)
        self.switch_choice.setCompleter(QCompleter(attributes))
