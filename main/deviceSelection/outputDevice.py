from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QWidget, QListWidgetItem, QMessageBox


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

        self.parameter = ItemWidget(self.item_type)
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

    def getProperties(self):
        return self.default_properties

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        item = OutputDevice(self.item_type, self.text())
        item.setProperties(self.default_properties)
        return item


class ItemWidget(QWidget):
    def __init__(self, item_type: str, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.name_label = QLabel()
        self.port = "127.0.0.1"
        self.port_line = QLineEdit()
        self.port_line.setText(self.port)
        self.port_line.textChanged.connect(self.setPort)

        self.port_line.installEventFilter(self)

        layout = QFormLayout()
        layout.addRow("Type:", QLabel(item_type))
        layout.addRow("Name:", self.name_label)
        layout.addRow("Port:", self.port_line)
        self.setLayout(layout)

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.port_line:
            if e.type() == QEvent.FocusOut:
                port = self.port_line.text()
                if not self.checkPort(port):
                    QMessageBox.warning(self, "Warning", "Invalid Port!", QMessageBox.Ok)
                    self.port_line.setFocus()
        return QWidget.eventFilter(self, obj, e)

    def setPort(self, port: str):
        if self.checkPort(port):
            self.port = port
            self.port_line.setText(port)

    @staticmethod
    def checkPort(port: str):
        port_list = port.split(".")
        if len(port_list) == 4:
            for i in port_list:
                if i.isdigit():
                    if int(i) < 0 or int(i) > 255:
                        return False
                else:
                    return False
            return True
        else:
            return False
