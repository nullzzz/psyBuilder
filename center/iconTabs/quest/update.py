from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QMessageBox, \
    QCompleter


class QuestUpdate(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None, value=''):
        super(QuestUpdate, self).__init__(parent)
        self.value = value
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.attributes = []
        self.default_properties = {
            "Response variable": "correct"
        }
        self.response_variable = QLineEdit()
        self.response_variable.textChanged.connect(self.findVar)
        self.response_variable.returnPressed.connect(self.finalCheck)

        self.resp = ""
        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(["test"])

        self.response_variable.setFocus()

    def setUI(self):
        self.setWindowTitle("Update")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("QUEST staircase next")
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Updates the Quest test value based on a response")
        self.response_variable.setText("correct")

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Response Variable (0 or 1):"), 2, 0, 1, 1)
        layout1.addWidget(self.response_variable, 2, 1, 1, 1)

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
        self.tabClose.emit(self)

    def cancel(self):
        self.loadSetting()
        # self.close()
        self.tabClose.emit(self)

    def apply(self):
        self.resp = self.response_variable.text()
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
        self.response_variable.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties["Response variable"] = self.response_variable.text()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.response_variable.setText(self.default_properties["Response variable"])

    def clone(self, value):
        clone_widget = QuestUpdate(value=value)
        clone_widget.setProperties(self.default_properties)
        return clone_widget
