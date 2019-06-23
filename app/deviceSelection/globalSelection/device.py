from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Device(QListWidgetItem):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Device, self).__init__(device_type, parent)
        # 设备类型
        self.device_type = device_type

        # 地址
        if device_type == "network_port":
            self.port = "127.0.0.1"
        elif device_type == "parallel_port":
            self.port = "D010"
        elif device_type == "serial_port":
            self.port = "com1"
        elif device_type == "screen":
            self.port = "0"
        else:
            self.port = "null"

        # screen 专属
        self.back_color = "0,0,0"
        self.sample = "0"
        # parallel
        self.client: int = 0
        # net
        self.ip_port = "25576"
        # serial
        self.baud_rate = "9600"
        self.data_bits = "8"
        # 设备标识符
        self.device_id = device_id

        # 设置图标
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Type": self.device_type,
            "Device Name": device_id,
            "Device Port": self.port
        }

    def getType(self) -> str:
        return self.device_type

    def setName(self, name: str):
        self.setText(name)

    def getDeviceId(self) -> str:
        return self.device_id

    def getName(self) -> str:
        return self.text()

    def getPort(self):
        return self.port

    def getColor(self):
        if self.device_type == "screen":
            return self.back_color
        return ""

    def getSample(self):
        if self.device_type == "screen":
            return self.sample
        return ""

    def setPort(self, port: str):
        if port.startswith("screen"):
            self.port = port.split(".")[-1]
        elif port.startswith("serial_port"):
            self.port = f"com{port.split('.')[-1]}"
        elif port.startswith(self.device_type):
            pass
        else:
            self.port = port

    def setColor(self, color):
        self.back_color = color

    def setSample(self, sample):
        self.sample = sample

    def setBaud(self, baud):
        self.baud_rate = baud

    def setBits(self, bits):
        self.data_bits = bits

    def setClient(self, client):
        self.client = client

    def setIpPort(self, ip_port):
        self.ip_port = ip_port

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])
        self.setColor(self.default_properties.get("Back Color", "0,0,0"))
        self.setPort(self.default_properties.get("Multi Sample", "0"))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port
        self.default_properties["Back Color"] = self.back_color
        self.default_properties["Multi Sample"] = self.sample
        self.default_properties["Baud Rate"] = self.baud_rate
        self.default_properties["Data Bits"] = self.data_bits
        self.default_properties["IP Port"] = self.ip_port
        self.default_properties["Is Client"] = self.client
        return self.default_properties
