from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.deviceSelection.globalSelection.port import ItemWidget
from app.func import Func


class OutputDevice(QListWidgetItem):
    """
    :param device_type: 串、并、网口、屏幕
    :param name: 自定义设备名，即item的text
    """

    def __init__(self, device_type: str, device_id: str = "null", parent=None):
        super(OutputDevice, self).__init__(device_type, parent)
        self.device_type = device_type
        self.item_name = device_type
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.device_id = device_id

        self.default_properties = {
            "Device type": self.device_type,
            "Device name": self.item_name,
            "Port": "127.0.0.1"
        }

        self.parameter = ItemWidget(self.device_type)
        # self.name_label = QLabel()
        # self.port = "127.0.0.1"
        # self.port_line = QLineEdit()
        # self.port_line.setText(self.port)
        # self.port_line.textChanged.connect(self.setPort)
        # self.port_line.installEventFilter(self.parameter)
        #
        # lay = QFormLayout()
        # lay.addRow("Type:", QLabel(self.item_type))
        # lay.addRow("Name:", self.name_label)
        # lay.addRow("Port:", self.port_line)
        # self.parameter.setLayout(lay)

    def setPort(self, port: str):
        self.parameter.setPort(port)

    def setName(self, name: str):
        self.setText(name)
        self.item_name = name
        self.parameter.name_label.setText(name)

    def getPort(self):
        return self.parameter.port

    def getType(self):
        return self.device_type

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

    def getProperties(self):
        return self.default_properties

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        item = OutputDevice(self.device_type)
        item.setProperties(self.default_properties)
        return item
