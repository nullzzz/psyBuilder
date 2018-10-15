from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                             QCompleter)


class QuestGetValue(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None, value=''):
        super(QuestGetValue, self).__init__(parent)
        self.value = value
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.attributes = []

        self.default_properties = {
            "Line1": "",
            "Line2": "",
            "Experimental variable for test value": "quest test value",
        }
        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.experimental = QLineEdit()
        self.line1.returnPressed.connect(self.finalCheck)
        self.line2.returnPressed.connect(self.finalCheck)
        self.experimental.returnPressed.connect(self.finalCheck)
        self.line1.textChanged.connect(self.findVar)
        self.line2.textChanged.connect(self.findVar)
        self.experimental.textChanged.connect(self.findVar)

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(["test"])

        self.line1.setFocus()

    def setUI(self):
        self.setWindowTitle("GetValue")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("QUEST get value")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Get value for test")

        self.experimental.setText("quest test value")

        layout1 = QFormLayout()
        layout1.addRow(self.tip1)
        layout1.addRow(self.tip2)
        layout1.addRow("Line1:", self.line1)
        layout1.addRow("Line2:", self.line2)

        layout1.addRow("Experimental Variable For Test Value:", self.experimental)
        layout1.setLabelAlignment(Qt.AlignRight)

        layout2 = QHBoxLayout()
        layout2.addStretch(10)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        # 关闭信号
        self.tabClose.emit(self)

    def cancel(self):
        self.loadSetting()
        # self.close()
        # 关闭信号
        self.tabClose.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getInfo())

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

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        self.line1.setCompleter(QCompleter(self.attributes))
        self.line2.setCompleter(QCompleter(self.attributes))
        self.experimental.setCompleter(QCompleter(self.attributes))

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def getInfo(self):
        self.default_properties["Line1"] = self.line1.text()
        self.default_properties["Line2"] = self.line2.text()
        self.default_properties["Experimental variable for test value"] = self.experimental.text()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.line1.setText(self.default_properties["Line1"])
        self.line2.setText(self.default_properties["Line2"])
        self.experimental.setText(self.default_properties["Experimental variable for test value"])

    def clone(self, value):
        clone_widget = QuestGetValue(value=value)
        clone_widget.setProperties(self.default_properties)
        return clone_widget
