from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QWidget, QListWidgetItem


class OutputDevice(QListWidgetItem):
    """
    :param device_type: 串、并、网口
    :param name: 自定义设备名，即item的text
    """
    def __init__(self, device_type: str, name: str, parent=None):
        super(OutputDevice, self).__init__(name, parent)
        self.item_type = device_type
        self.item_name = name
        self.setIcon(QIcon("image/{}_device.png".format(self.item_type)))

        self.default_properties = {
            "Device type": self.item_type,
            "Device name": self.item_name,
            "Port": "127.0.0.1"
        }

        self.parameter = QWidget()
        self.name_label = QLabel()
        self.port = "127.0.0.1"
        self.port_line = QLineEdit()
        self.port_line.setText(self.port)
        self.port_line.textChanged.connect(self.setPort)
        lay = QFormLayout()
        lay.addRow("Type:", QLabel(self.item_type))
        lay.addRow("Name:", self.name_label)
        lay.addRow("Port:", self.port_line)
        self.parameter.setLayout(lay)

    def setPort(self, port):
        self.port = port

    def setName(self, name: str):
        self.setText(name)
        self.item_name = name
        self.name_label.setText(name)

    def getPort(self):
        return self.port

    def getType(self):
        return self.item_type

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device name"])
        self.setPort(self.default_properties["Port"])

    def getInfo(self):
        self.default_properties["Device name"] = self.text()
        self.default_properties["Port"] = self.getPort()
        return self.default_properties

    # todo 检查port合法性
    def checkPort(self):
        pass

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        item = OutputDevice(self.item_type, self.text())
        item.setProperties(self.default_properties)
        return item
