from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QCompleter

from app.center.widget_tabs.condition.addDeleteButton import AddDeleteButton
from app.lib import PigComboBox, PigLineEdit
from lib.psy_message_box import PsyMessageBox as QMessageBox


class EachCondition(QFrame):
    placeholder_width = 100

    def __init__(self, parent=None):
        super(EachCondition, self).__init__(parent)

        self.vars: list = []

        self.attributes: list = []

        self.default_properties: dict = {
            "op": "and",
            "var": "",
            "compare": "=",
            "var value": ""
        }

        self.op = PigComboBox()
        self.op.addItems(('and', 'or', 'xor', 'nor', 'nand', 'xnor'))
        self.op.setFixedWidth(EachCondition.placeholder_width)

        self.var = PigComboBox()
        self.var.setEditable(True)
        self.var.setInsertPolicy(QComboBox.NoInsert)
        self.var.lineEdit().textChanged.connect(self.findVar)
        self.var.lineEdit().returnPressed.connect(self.finalCheck)

        self.compare = PigComboBox()
        self.compare.addItems(("=", ">", ">=", "<", "<=", "≠"))
        self.compare.setFixedWidth(EachCondition.placeholder_width)

        self.var_value = PigLineEdit()
        self.var_value.textChanged.connect(self.findVar)
        self.var_value.returnPressed.connect(self.finalCheck)

        self.add_bt = AddDeleteButton(button_type='add')
        self.del_bt = AddDeleteButton(button_type='delete')

    def addVar(self, var_choice: list):
        self.vars = var_choice
        self.var.addItems(var_choice)

    # todo 返回当前条件的真值
    def getBool(self):
        pass

    def getLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.op, 1, Qt.AlignVCenter)
        layout.addWidget(self.var, 4, Qt.AlignVCenter)
        layout.addWidget(self.compare, 1, Qt.AlignVCenter)
        layout.addWidget(self.var_value, 4, Qt.AlignVCenter)
        layout.addWidget(self.add_bt, 1, Qt.AlignVCenter)
        layout.addWidget(self.del_bt, 1, Qt.AlignVCenter)
        return layout

    def clone(self):
        clone_condition = EachCondition()
        clone_condition.addVar(self.vars)
        if isinstance(self.op, QLabel):
            clone_condition.op = QLabel()
            clone_condition.op.setFixedWidth(self.op.width())
        else:
            clone_condition.op.setCurrentText(self.op.currentText())
        clone_condition.var.setCurrentText(self.var.currentText())
        clone_condition.compare.setCurrentText(self.compare.currentText())
        clone_condition.var_value.setText(self.var_value.text())
        if not isinstance(self.del_bt, AddDeleteButton):
            clone_condition.del_bt = QLabel()
            clone_condition.del_bt.setFixedWidth(clone_condition.add_bt.width())
        return clone_condition

    def getInfo(self):
        self.default_properties.clear()
        if isinstance(self.op, QComboBox):
            self.default_properties["op"] = self.op.currentText()
        else:
            self.default_properties["op"] = ""
        self.default_properties["var"] = self.var.currentText()
        self.default_properties["compare"] = self.compare.currentText()
        self.default_properties["var value"] = self.var_value.text()
        return self.default_properties

    def loadSetting(self):
        if isinstance(self.op, QComboBox):
            self.op.setCurrentText(self.default_properties.get("op", "and"))
        self.var.setCurrentText(self.default_properties.get("var", ""))
        self.compare.setCurrentText(self.default_properties.get("compare", ">"))
        self.var_value.setText(self.default_properties.get("var value", ""))

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.addVar(attributes)
        self.var.setCompleter(QCompleter(attributes))
        self.var_value.setCompleter(QCompleter(attributes))

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

    def getCondition(self) -> str:
        """
        e.g. and ([var] == "var value")
        :return:
        """
        return f"{self.default_properties.get('op', '')} ({self.default_properties.get('var', '')}" \
            f"{self.default_properties.get('compare', '=')}{self.default_properties.get('var value')})"
