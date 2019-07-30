from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Device(QListWidgetItem):
    """
    :param device_type: 串、并、网口
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Device, self).__init__(device_type, parent)
        # 设备类型
        self.device_type = device_type
        # 地址
        self.port = "127.0.0.1"
        # 设备标识符
        self.device_id = device_id

        # 设置图标
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Type": self.device_type,
            "Device Name": device_id,
            "Device Port": self.port
        }

    def getType(self):
        return self.device_type

    def getDeviceId(self):
        return self.device_id

    def getName(self):
        return self.text()

    def getPort(self):
        return self.port

    def setPort(self, port):
        self.port = port

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])

    def getInfo(self):
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port
        return self.default_properties
