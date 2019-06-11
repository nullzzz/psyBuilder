from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QFormLayout, QLabel

from app.func import Func


class InputDevice(QListWidgetItem):
    """
    :param device_type: 串、并、网口
    :param name: 自定义设备名，即item的text
    """

    def __init__(self, device_type: str, parent=None):
        super(InputDevice, self).__init__(device_type, parent)
        # 设备类型
        self.device_type = device_type
        # 地址
        self.port = "127.0.0.1"
        # 设备标识符
        self.device_id = Func.createDeviceId(device_type)

        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device type": self.device_type,
            "Device name": device_type,
            "Port": self.port
        }

        self.parameter = QWidget()

        self.name_label = QLabel(self.text())
        self.port_label = QLabel(self.port)
        lay = QFormLayout()
        lay.addRow("Type:", QLabel(self.device_type))
        lay.addRow("Name:", self.name_label)
        lay.addRow("Port:", self.port_label)
        self.parameter.setLayout(lay)

    def getType(self):
        return self.device_type

    def setName(self, name: str):
        self.setText(name)
        self.name_label.setText(name)

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device name"])

    def getInfo(self):
        self.default_properties["Device name"] = self.text()
        return self.default_properties

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        item = InputDevice(self.device_type)
        item.setProperties(self.default_properties)
        return item
