from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QCompleter, QListWidgetItem

from app.func import Func


# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    def __init__(self, device_name: str, device_id: str, parent=None):
        super(DeviceOutItem, self).__init__(device_name, parent)
        self.attributes = []
        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_id.split(".")[0]
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Id": self.device_id,
            "Device Name": self.device_name,
            "Device Type": self.device_type,
            "Value or Msg": "",
            "Pulse Duration": ""
        }

        self.value_or_msg = ""
        self.pulse_duration = "End of Duration"

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
        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Value or Msg"] = self.value_or_msg
        self.default_properties["Pulse Duration"] = self.pulse_duration
        return self.default_properties

    def getInProperties(self) -> dict:
        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Value or Msg"] = self.value_or_msg
        self.default_properties["Pulse Duration"] = self.pulse_duration
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties = device_info.copy()
        self.loadSetting()

    def loadSetting(self):
        self.value_or_msg = self.default_properties["Value or Msg"]
        self.pulse_duration = self.default_properties["Pulse Duration"]

    def changeValueOrMessage(self, value_or_msg: str):
        self.value_or_msg = value_or_msg

    def changePulseDuration(self, pulse_duration: str):
        self.pulse_duration = pulse_duration

    def getValue(self):
        return self.value_or_msg, self.pulse_duration

    def getType(self):
        return self.device_type

    def getDeviceId(self) -> str:
        return self.device_id

    def getDeviceName(self) -> str:
        return self.device_name

    def changeDeviceName(self, new_name: str):
        self.device_name = new_name
        self.setText(new_name)
