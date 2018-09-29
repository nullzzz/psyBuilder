from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QFormLayout, QLabel


class InputDevice(QListWidgetItem):
    """
    :param device_type: 串、并、网口
    :param name: 自定义设备名，即item的text
    """
    def __init__(self, device_type: str, name: str, parent=None):
        super(InputDevice, self).__init__(name, parent)
        self.item_type = device_type
        self.setIcon(QIcon("image/{}_device.png".format(self.item_type)))

        self.default_properties = {
            "Device type": self.item_type,
            "Device name": name
        }

        self.parameter = QWidget()

        self.name_label = QLabel(self.text())
        lay = QFormLayout()
        lay.addRow("Type:", QLabel(self.item_type))
        lay.addRow("Name:", self.name_label)
        self.parameter.setLayout(lay)

    def getType(self):
        return self.item_type

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
        item = InputDevice(self.item_type, self.text())
        item.setProperties(self.default_properties)
        return item
