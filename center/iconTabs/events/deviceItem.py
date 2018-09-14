from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QListWidgetItem, QWidget, QComboBox, QGridLayout, QLabel, \
    QFormLayout, QCompleter

# todo: 这个样式表要怎么写呢
lineEdit = """
    QLineEdit {
        border: 1px:
        border-radius: 1px;
        min-height: 10px;
    }
    QLineEdit:focus {
        border-width:1px;
        border-color: black;
    }
    """


# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    varColor = "blue"

    def __init__(self, name=None, parent=None):
        super(DeviceOutItem, self).__init__(name, parent)
        self.attributes = []

        self.default_properties = {
            "Value or Msg": "",
            "Pulse Duration": ""
        }

        self.name = name
        self.devices = []
        self.pro = QWidget()
        self.value = QLineEdit()
        self.value.textChanged.connect(self.findVar)
        self.value.returnPressed.connect(self.finalCheck)
        self.pulse_dur = QComboBox()
        self.pulse_dur.setEditable(True)
        self.pulse_dur.setInsertPolicy(QComboBox.NoInsert)
        self.pulse_dur.addItems(["End of Duration", "0", "100", "200", "300", "400", "500"])

        self.pulse_dur.lineEdit().textChanged.connect(self.findVar)
        self.pulse_dur.lineEdit().returnPressed.connect(self.finalCheck)

        self.setPro()

    def setPro(self):
        layout = QFormLayout()
        layout.addRow("Value or Msg:", self.value)
        layout.addRow("Pulse Dur:", self.pulse_dur)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 20, 10, 0)
        self.pro.setLayout(layout)

    def findVar(self, text):
        if text in self.attributes:
            self.pro.sender().setStyleSheet("color:{}".format(DeviceOutItem.varColor))
            self.pro.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.pro.sender().setStyleSheet("color:black")
            self.pro.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.pro.sender()
        if isinstance(temp, QLineEdit):
            text = temp.text()
        else:
            text = temp.currentText()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self.pro, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.value.setCompleter(QCompleter(self.attributes))
        self.pulse_dur.setCompleter(QCompleter(self.attributes))

    @staticmethod
    def setVarColor(self, color):
        DeviceOutItem.varColor = color

    def getInfo(self):
        self.default_properties["Value or Msg"] = self.value.text()
        self.default_properties["Pulse Duration"] = self.pulse_dur.text()
        return self.default_properties

    def loadSetting(self):
        self.value.setText(self.default_properties["Value or Msg"])
        self.pulse_dur.setText(self.default_properties["Pulse Duration"])


# 重写下方输入设备
class DeviceInItem(QListWidgetItem):
    varColor = "blue"

    def __init__(self, name=None, parent=None):
        super(DeviceInItem, self).__init__(name, parent)
        self.attributes = []

        self.default_properties = {

        }

        self.name = name
        self.pro1 = QWidget()
        self.device_label = QLabel(name)
        self.allowable = QLineEdit()
        self.allowable.textChanged.connect(self.findVar)
        self.allowable.returnPressed.connect(self.finalCheck)
        self.correct = QLineEdit()
        self.correct.textChanged.connect(self.findVar)
        self.correct.returnPressed.connect(self.finalCheck)
        self.RT_window = QComboBox()
        self.RT_window.addItems(["(Same as duration)", "(End of timeline)", "1000", "2000", "3000", "4000", "5000"])
        self.RT_window.setEditable(True)
        self.RT_window.setInsertPolicy(QComboBox.NoInsert)
        self.RT_window.lineEdit().textChanged.connect(self.findVar)
        self.RT_window.lineEdit().returnPressed.connect(self.finalCheck)
        self.end_action = QComboBox()
        self.end_action.setInsertPolicy(QComboBox.NoInsert)
        self.action = QComboBox()
        self.action.setInsertPolicy(QComboBox.NoInsert)
        self.ROA = QLineEdit()
        self.ROA.textChanged.connect(self.findVar)
        self.ROA.returnPressed.connect(self.finalCheck)
        self.ROA2 = QComboBox()
        self.ROA2.addItems(["Outside", "Inside"])

        self.pro2 = QWidget()
        self.right = QLineEdit()
        self.right.textChanged.connect(self.findVar)
        self.right.returnPressed.connect(self.finalCheck)
        self.wrong = QLineEdit()
        self.wrong.textChanged.connect(self.findVar)
        self.wrong.returnPressed.connect(self.finalCheck)
        self.ignore = QLineEdit()
        self.ignore.textChanged.connect(self.findVar)
        self.ignore.returnPressed.connect(self.finalCheck)
        self.resp_trigger_out = QComboBox()
        self.setPro()

    def setPro(self):
        self.end_action.addItems(["Terminate", "(None)"])
        self.action.addItems(["Fixation", "Saccade"])
        if "eye" not in self.name:
            layout1 = QFormLayout()
            layout1.addRow("Response:", self.device_label)
            layout1.addRow("Allowable:", self.allowable)
            layout1.addRow("Correct:", self.correct)
            layout1.addRow("RT window:", self.RT_window)
            layout1.addRow("End action:", self.end_action)
            layout1.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        else:
            layout1 = QGridLayout()
            l1 = QLabel("Response:")
            l1.setAlignment(Qt.AlignRight)
            layout1.addWidget(l1, 0, 0, 1, 1)
            layout1.addWidget(self.device_label, 0, 1, 1, 2)
            l2 = QLabel("Action:")
            l2.setAlignment(Qt.AlignRight)
            layout1.addWidget(l2, 1, 0, 1, 1)
            layout1.addWidget(self.action, 1, 1, 1, 2)
            l3 = QLabel("ROA:")
            l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l3, 2, 0, 1, 1)
            layout1.addWidget(self.ROA, 2, 1, 1, 1)
            layout1.addWidget(self.ROA2, 2, 2, 1, 1)
            l4 = QLabel("Duration:")
            l4.setAlignment(Qt.AlignRight)
            layout1.addWidget(l4, 3, 0, 1, 1)
            layout1.addWidget(self.RT_window, 3, 1, 1, 2)
            l5 = QLabel("End Action:")
            l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l5, 4, 0, 1, 1)
            layout1.addWidget(self.end_action, 4, 1, 1, 2)
        layout1.setVerticalSpacing(20)
        layout1.setContentsMargins(10, 0, 0, 0)
        self.pro1.setLayout(layout1)

        layout2 = QGridLayout()
        layout2.addWidget(QLabel("Resp Trigger"), 0, 0, 1, 2)
        layout2.addWidget(QLabel("Right:"), 1, 0)
        layout2.addWidget(self.right, 1, 1)
        layout2.addWidget(QLabel("Wrong:"), 1, 2)
        layout2.addWidget(self.wrong, 1, 3)
        layout2.addWidget(QLabel("No resp:"), 1, 4)
        layout2.addWidget(self.ignore, 1, 5)
        layout2.addWidget(QLabel("Device:"), 1, 6)
        layout2.addWidget(self.resp_trigger_out, 1, 7)
        self.pro2.setLayout(layout2)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.pro1.sender().setStyleSheet("color:{}".format(DeviceInItem.varColor))
        else:
            self.pro1.sender().setStyleSheet("color:black")

    def finalCheck(self):
        temp = self.pro1.sender()
        if isinstance(temp, QLineEdit):
            text = temp.text()
        else:
            text = temp.currentText()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self.pro1, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    # 设置可选变量
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.allowable.setCompleter(QCompleter(self.attributes))
        self.correct.setCompleter(QCompleter(self.attributes))
        self.RT_window.setCompleter(QCompleter(self.attributes))
        self.ROA.setCompleter(QCompleter(self.attributes))
        self.right.setCompleter(QCompleter(self.attributes))
        self.wrong.setCompleter(QCompleter(self.attributes))
        self.ignore.setCompleter(QCompleter(self.attributes))

    @staticmethod
    def setVarColor(self, color):
        DeviceInItem.varColor = color

    def getInfo(self):
        # todo：当初说的啥眼动设备，属性不一样，现在还不知道是啥子
        if "eye" not in self.name:
            return {
                "Device name": self.name,
                "Allowable": self.allowable.text(),
                "Correct": self.correct.text(),
                "RT window": self.RT_window.currentText(),
                "End action": self.end_action.currentText(),
                "Right": self.right.text(),
                "Wrong": self.wrong.text(),
                "No resp": self.ignore.text(),
                "Output device": self.resp_trigger_out
            }
        else:
            return {
                "Device name": self.name,
                "Action": self.action.currentText(),
                "ROA": self.ROA.text(),
                "ROA action": self.action.currentText(),
                "duration": self.RT_window.currentText(),
                "End action": self.end_action.currentText(),
                "Right": self.right.text(),
                "Wrong": self.wrong.text(),
                "No resp": self.ignore.text(),
                "Output device": self.resp_trigger_out
            }
