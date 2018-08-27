from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout)


class QuestGetValue(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(QuestGetValue, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.line1 = QLineEdit()
        self.line2 = QLineEdit()
        self.experimental = QLineEdit()

        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.line1.setFocus()

    def setUI(self):
        self.setWindowTitle("GetValue")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("QUEST get value")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Get value for test")

        self.experimental.setText("quest_test_value")

        layout1 = QFormLayout()
        layout1.addRow(self.tip1)
        layout1.addRow(self.tip2)
        layout1.addRow("Line1", self.line1)
        layout1.addRow("Line2", self.line2)

        layout1.addRow("Experimental variable for test value", self.experimental)
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
        self.close()
        # 关闭信号
        self.tabClose.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getInfo())

    def getInfo(self):
        return {
            "Line1": self.line1.text(),
            "Line2": self.line2.text(),
            "Experimental variable for test value": self.experimental.text(),
        }
