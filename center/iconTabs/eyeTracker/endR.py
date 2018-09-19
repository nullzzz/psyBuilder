from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, \
    QCompleter


class EndR(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(EndR, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.attributes = []
        self.default_properties = {
            "Statue message": ""
        }

        self.statue_msg = QLineEdit()
        self.statue_msg.textChanged.connect(self.findVar)
        self.statue_msg.returnPressed.connect(self.finalCheck)

        self.msg = ""
        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(["test"])

        self.statue_msg.setFocus()

    def setUI(self):
        self.setWindowTitle("endR")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("End recording")
        # self.tip1.setFocusPolicy(Qt.NoFocus)
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Ends recording of eye tracking data")
        # self.tip2.setFocusPolicy(Qt.NoFocus)
        self.statue_msg.setMaximumWidth(300)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Statue Message:"), 2, 0, 1, 1)
        layout1.addWidget(self.statue_msg, 2, 1, 1, 1)

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
        self.msg = self.statue_msg.text()
        self.propertiesChange.emit(self.getProperties())

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
        self.statue_msg.setCompleter(QCompleter(self.attributes))

    def getProperties(self):
        self.default_properties["Statue message"] =  self.statue_msg.text()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.statue_msg.setText(self.default_properties["Statue message"])

    def clone(self):
        clone_widget = EndR()
        clone_widget.setProperties(self.default_properties)
        return clone_widget
