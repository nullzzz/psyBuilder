from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QSpinBox, QCheckBox, QTextEdit


class Close(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None, value=''):
        super(Close, self).__init__(parent)
        self.value = value
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.pause_between_msg = QSpinBox()

        self.default_properties = {
            "Pause between message": 0,
            "Automatically log all variables": 0,
            "log message": ""
        }

        self.msg = ""
        self.automatically_log_all_variables = QCheckBox("Automatically log all variables")
        self.log_msg = QTextEdit()
        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.pause_between_msg.setFocus()

    def setUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Close")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Log")
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Writes information to the eye-tracker logfile")
        self.pause_between_msg.setSuffix(" ms")
        self.pause_between_msg.setMaximum(1000)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Pause between message:"), 2, 0, 1, 1)
        layout1.addWidget(self.pause_between_msg, 2, 1, 1, 1)
        layout1.addWidget(self.automatically_log_all_variables, 3, 1, 1, 1)
        layout1.addWidget(self.log_msg, 4, 0, 76, 4)

        layout2 = QHBoxLayout()
        layout2.addStretch(1)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self)

    def cancel(self):
        self.loadSetting()
        self.close()
        self.tabClosesed.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getInfo())

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def getInfo(self):
        self.default_properties["Pause between message"] = self.pause_between_msg.value()
        self.default_properties["Automatically log all variables"] = self.automatically_log_all_variables.checkState()
        self.default_properties["log message"] = self.log_msg.toPlainText()

        return self.default_properties

    def loadSetting(self):
        self.pause_between_msg.setValue(self.default_properties["Pause between message"])
        self.automatically_log_all_variables.setCheckState(self.default_properties["Automatically log all variables"])
        self.log_msg.setText(self.default_properties["log message"])

    def clone(self, value):
        clone_widget = Close(value=value)
        clone_widget.setProperties(self.default_properties)
        return clone_widget
