from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal


class QuestUpdate(QWidget):
    propertiesChanged = pyqtSignal(dict)
    closed = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(QuestUpdate, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.response_variable = QLineEdit()
        self.resp = ""
        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
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
        layout1.addWidget(QLabel("Response variable (0 or 1):"), 2, 0, 1, 1)
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
        self.closed.emit(self)

    def cancel(self):
        self.close()
        self.closed.emit(self)

    def apply(self):
        self.resp = self.response_variable.text()
        self.propertiesChanged.emit(self.getInfo())

    def getInfo(self):
        return {"Response variable": self.resp}
