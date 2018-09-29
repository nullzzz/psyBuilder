from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCompleter, QMessageBox, QComboBox, QFormLayout, QListWidgetItem, QWidget, QLineEdit

# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    varColor = "blue"

    def __init__(self, name: str, device_type: str, parent=None):
        super(DeviceOutItem, self).__init__(name, parent)
        self.attributes = []
        self.name = name
        self.device_type = device_type
        self.setIcon(QIcon("image/{}_device.png".format(self.device_type)))

        self.default_properties = {
            "Device name": self.name,
            "Device type": self.device_type,
            "Value or Msg": "",
            "Pulse Duration": ""
        }

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
            # if valid:
            #    pass
            # else:
            # QMessageBox.warning(self.pro, "Warning", "Invalid Attribute!". QMessageBox.Ok)

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
        self.default_properties["Pulse Duration"] = self.pulse_dur.currentText()
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties = device_info
        self.loadSetting()

    def loadSetting(self):
        self.value.setText(self.default_properties["Value or Msg"])
        self.pulse_dur.setCurrentText(self.default_properties["Pulse Duration"])
