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
            self.port = "COM1"
        elif device_type == "screen":
            self.port = "0"
        elif device_type == "sound":
            self.port = "1"
        elif device_type in ("keyboard","mouse","game pad"):
            self.port = "auto"
        else:
            self.port = "null"

        # screen 专属
        self.back_color = "0,0,0"
        self.sample = "0"
        self.resolution = "auto"
        self.refresh_rate = "auto"
        # parallel
        self.is_client: str = "Yes"
        # net
        self.ip_port: str = "25576"
        # serial
        self.baud_rate: str = "9600"
        self.data_bits: str = "8"
        # sound
        self.sampling_rate: str = "auto"
        # 设备标识符
        self.device_id: str = device_id

        # 设置图标
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Type": self.device_type,
            "Device Name": self.text(),
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

    def getPort(self) -> str:
        return self.port

    def getColor(self) -> str:
        if self.device_type == "screen":
            return self.back_color
        return ""

    def getSample(self) -> str:
        if self.device_type == "screen":
            return self.sample
        return ""

    def getSamplingRate(self) -> str:
        if self.device_type == "sound":
            return self.sampling_rate
        return ""

    def getResolution(self) -> str:
        return self.resolution

    def getRefreshRate(self) -> str:
        return self.refresh_rate

    def setPort(self, port: str):
        if port.startswith("screen") or port.startswith("sound"):
            self.port = port.split(".")[-1]
        elif port.startswith("serial_port"):
            self.port = f"COM{port.split('.')[-1]}"
        elif port.startswith("keyboard") or port.startswith("mouse") or port.startswith("game pad"):
            self.port = 'auto'
            # only works for the old input devices
            # self.port = port.split(".")[-1]
        elif port.startswith(self.device_type):
            pass
        else:
            self.port = port

    def setColor(self, color: str):
        self.back_color = color

    def setSample(self, sample: str):
        self.sample = sample

    def setBaud(self, baud: str):
        self.baud_rate = baud

    def setBits(self, bits: str):
        self.data_bits = bits

    def setClient(self, client: str):
        self.is_client = client

    def setIpPort(self, ip_port: str):
        self.ip_port = ip_port

    def setSamplingRate(self, sampling_rate: str):
        self.sampling_rate = sampling_rate

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def setResolution(self, resolution):
        self.resolution = resolution

    def setRefreshRate(self, refresh_rate):
        self.refresh_rate = refresh_rate

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])
        self.setColor(self.default_properties.get("Back Color", "0,0,0"))
        self.setPort(self.default_properties.get("Multi Sample", "0"))
        self.setBaud(self.default_properties.get("Baud Rate", "9600"))
        self.setBits(self.default_properties.get("Data Bits", "8"))
        self.setIpPort(self.default_properties.get("IP Port", "25576"))
        self.setClient(self.default_properties.get("Is Client", "1"))
        self.setSamplingRate(self.default_properties.get("Sampling Rate", "auto"))
        self.setResolution(self.default_properties.get("Resolution", "auto"))
        self.setRefreshRate(self.default_properties.get("Refresh Rate", "auto"))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port
        self.default_properties["Back Color"] = self.back_color
        self.default_properties["Multi Sample"] = self.sample
        self.default_properties["Baud Rate"] = self.baud_rate
        self.default_properties["Data Bits"] = self.data_bits
        self.default_properties["IP Port"] = self.ip_port
        self.default_properties["Is Client"] = self.is_client
        self.default_properties["Sampling Rate"] = self.sampling_rate
        self.default_properties["Resolution"] = self.resolution
        self.default_properties["Refresh Rate"] = self.refresh_rate

        return self.default_properties
