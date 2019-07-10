from PyQt5.QtCore import Qt, QRegExp, QObject, QEvent
from PyQt5.QtGui import QIcon, QFont, QRegExpValidator
from PyQt5.QtWidgets import QCompleter, QMessageBox, QComboBox, QFormLayout, QListWidgetItem, QWidget

from app.func import Func
from app.lib import PigComboBox, PigLineEdit


# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    varColor = "blue"

    def __init__(self, device_name: str, device_id: str, parent=None):
        super(DeviceOutItem, self).__init__(device_name, parent)
        self.attributes = []
        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_id.split(".")[0]
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device id": self.device_id,
            "Device name": self.device_name,
            "Device type": self.device_type,
            "Value or Msg": "",
            "Pulse Duration": ""
        }

        self.value_or_msg = ""
        self.pulse_duration = "End of Duration"

        self.pro = ItemWidget()

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.pro.attributes = attributes
        self.pro.value.setCompleter(QCompleter(self.attributes))
        self.pro.pulse_dur.setCompleter(QCompleter(self.attributes))

    @staticmethod
    def setVarColor(self, color):
        DeviceOutItem.varColor = color

    def getInfo(self) -> dict:
        self.default_properties["Value or Msg"] = self.pro.value.text()
        self.default_properties["Pulse Duration"] = self.pro.pulse_dur.currentText()
        return self.default_properties

    def getInProperties(self) -> dict:
        self.default_properties["Value or Msg"] = self.pro.value.text()
        self.default_properties["Pulse Duration"] = self.pro.pulse_dur.currentText()
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties = device_info.copy()
        self.loadSetting()

    def loadSetting(self):
        self.pro.value.setText(self.default_properties["Value or Msg"])
        self.pro.pulse_dur.setCurrentText(self.default_properties["Pulse Duration"])

    def changeValueOrMessage(self, value_or_msg: str):
        self.value_or_msg = value_or_msg

    def changePulseDuration(self, pulse_duration: str):
        self.pulse_duration = pulse_duration

    def getValue(self):
        return self.value_or_msg, self.pulse_duration


class ItemWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.attributes = []

        self.value = PigLineEdit()
        self.value.textChanged.connect(self.findVar)
        self.value.returnPressed.connect(self.finalCheck)
        self.pulse_dur = PigComboBox()
        self.pulse_dur.setEditable(True)
        self.pulse_dur.setInsertPolicy(QComboBox.NoInsert)
        self.pulse_dur.addItems(["End of Duration", "10", "20", "30", "40", "50"])

        valid_num = QRegExp("\[\w+\]|\d+|End of Duration")
        self.pulse_dur.setValidator(QRegExpValidator(valid_num))
        self.pulse_dur.lineEdit().textChanged.connect(self.findVar)
        self.pulse_dur.lineEdit().returnPressed.connect(self.finalCheck)

        self.value.installEventFilter(self)
        self.pulse_dur.installEventFilter(self)

        self.setPro()

    def setPro(self):
        layout = QFormLayout()
        layout.addRow("Value or Msg:", self.value)
        layout.addRow("Pulse Dur:", self.pulse_dur)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 20, 10, 0)
        self.setLayout(layout)

    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color:{}".format(DeviceOutItem.varColor))
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        if isinstance(temp, PigLineEdit):
            text = temp.text()
        else:
            text = temp.currentText()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.pulse_dur:
            if e.type() == QEvent.FocusOut:
                text = self.pulse_dur.currentText()
                if text not in self.attributes:
                    if text and text[0] == "[":
                        QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                        self.pulse_dur.setCurrentIndex(0)
        return QWidget.eventFilter(self, obj, e)
