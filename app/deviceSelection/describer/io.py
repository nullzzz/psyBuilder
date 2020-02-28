from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QLineEdit, QCheckBox

from lib import ColorListEditor


class Shower(QWidget):
    def __init__(self, parent=None):
        super(Shower, self).__init__(parent)
        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")
        self.device_port = QLineEdit("")
        self.device_port.textEdited.connect(self.showAddressTip)
        self.port_tip = QLabel("")

    def describe(self, info: dict):
        device_type = info.get("Device Type", "UNKNOWN")
        device_name = info.get("Device Name", "UNKNOWN")
        device_port = info.get("Device Port", "UNKNOWN")
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)
        if device_type in ("currently none ",):
            self.device_port.setText("Invalid")
            self.device_port.setEnabled(False)
        else:
            self.device_port.setEnabled(True)
            self.device_port.setText(device_port)
            self.showAddressTip(device_port)

    def showAddressTip(self, port: str):
        """
        端口有效性提示
        :param port:
        :return:
        """
        flag: bool = self.checkPort(port)

        if flag is False:
            self.port_tip.setText("Invalid Port")
        else:
            self.port_tip.setText("")

    def checkPort(self, port: str):
        flag: bool = True
        device_type: str = self.device_type.text()
        if device_type == "screen":
            if not port.isdigit() or int(port) > 10:
                flag = False
        elif device_type == "network_port":
            port_list = port.split(".")
            if len(port_list) == 4:
                for i in port_list:
                    if i.isdigit():
                        if int(i) < 0 or int(i) > 255:
                            flag = False
                    else:
                        flag = False
            else:
                flag = False
        elif device_type == "serial_port":
            if port.startswith("com") and port[3:].isdigit():
                pass
            else:
                flag = False
        elif device_type == "parallel_port":
            flag = port == "D010"
        elif device_type == "sound":
            flag = port.isdigit()
        return flag

    def changeName(self, new_name: str):
        self.device_name.setText(new_name)


class Screen(Shower):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)
        self.bg_color = ColorListEditor()
        self.mu_sample = QLineEdit()
        self.resolution = QLineEdit("auto")
        self.refresh_rate = QLineEdit("auto")
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Screen Index:", self.device_port)
        layout.addRow("Back Color:", self.bg_color)
        layout.addRow("Multi Sample:", self.mu_sample)
        layout.addRow("Resolution:", self.resolution)
        layout.addRow("RefreshRate:", self.refresh_rate)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.bg_color.setCurrentText(info.get("Back Color", "0,0,0"))
        self.mu_sample.setText(info.get("Multi Sample", ""))
        self.resolution.setText(info.get("Resolution", "auto"))
        self.refresh_rate.setText(info.get("Refresh Rate", "auto"))


class Net(Shower):
    def __init__(self, parent=None):
        super(Net, self).__init__(parent=parent)
        self.device_ip_port = QLineEdit()
        self.is_client = QCheckBox()
        self.is_client.stateChanged.connect(self.changeClient)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("IP Address:", self.device_port)
        layout.addRow("IP Port:", self.device_ip_port)
        layout.addRow("Is Client:", self.is_client)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_ip_port.setText(info.get("IP Port", "25576"))
        self.is_client.setChecked(info.get("Is Client", "Yes") == "Yes")

    def changeClient(self, state):
        pass


class Serial(Shower):
    def __init__(self, parent=None):
        super(Serial, self).__init__(parent=parent)
        self.baud_rate = QLineEdit()
        self.data_bits = QLineEdit()
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        layout.addRow("Baud Rate:", self.baud_rate)
        layout.addRow("Data Bits:", self.data_bits)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.baud_rate.setText(info.get("Baud Rate", "9600"))
        self.data_bits.setText(info.get("Data Bits", "8"))


class Sound(Shower):
    def __init__(self, parent=None):
        super(Sound, self).__init__(parent=parent)
        self.sampling_rate = QLineEdit("auto")
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Index:", self.device_port)
        layout.addRow("Sampling Rate:", self.sampling_rate)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)
        self.sampling_rate.setText(info.get("Sampling Rate", "auto"))


class Parallel(Shower):
    def __init__(self, parent=None):
        super(Parallel, self).__init__(parent=parent)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port/index:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)


class Mouse(Shower):
    def __init__(self, parent=None):
        super(Mouse, self).__init__(parent=parent)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port/index:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)


class Keyboard(Shower):
    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent=parent)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port/index:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)


class GamePad(Shower):
    def __init__(self, parent=None):
        super(GamePad, self).__init__(parent=parent)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port/index:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)


class ResponseBox(Shower):
    def __init__(self, parent=None):
        super(ResponseBox, self).__init__(parent=parent)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port/index:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, info: dict):
        super().describe(info)