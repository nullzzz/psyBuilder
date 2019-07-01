from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QLineEdit, QCheckBox, QStackedLayout

from app.lib import ColorListEditor


class Shower(QWidget):
    portChanged = pyqtSignal(str)
    colorChanged = pyqtSignal(str)
    sampleChanged = pyqtSignal(str)
    ipPortChanged = pyqtSignal(str)
    baudChanged = pyqtSignal(str)
    bitsChanged = pyqtSignal(int)
    clientChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Shower, self).__init__(parent)
        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")
        self.device_port = QLineEdit("")
        self.device_port.textEdited.connect(self.showAddressTip)

        self.port_tip = QLabel("")

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, device_type, device_name, device_port, other):
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)
        if device_type in ("mouse", "keyboard", "game pad"):
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
            self.portChanged.emit(port)

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
        return flag

    def changeName(self, new_name: str):
        self.device_name.setText(new_name)


class Screen(Shower):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)
        self.bg_color = ColorListEditor()
        self.bg_color.colorChanged.connect(lambda x: self.colorChanged.emit(x))
        self.mu_sample = QLineEdit()
        self.mu_sample.textEdited.connect(lambda x: self.sampleChanged.emit(x))
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Screen Index:", self.device_port)
        layout.addRow("Back Color:", self.bg_color)
        layout.addRow("Multi Sample:", self.mu_sample)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, device_type, device_name, device_port, others):
        super().describe(device_type, device_name, device_port, others)
        self.bg_color.setCurrentText(others.get("Back Color", "0,0,0"))
        self.mu_sample.setText(others.get("Multi Sample", ""))


class Net(Shower):
    def __init__(self, parent=None):
        super(Net, self).__init__(parent=parent)
        self.device_ip_port = QLineEdit()
        # self.device_port.
        self.device_ip_port.textEdited.connect(lambda x: self.ipPortChanged.emit(x))

        self.is_client = QCheckBox()
        self.is_client.stateChanged.connect(lambda x: self.clientChanged.emit(x))
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

    def describe(self, device_type, device_name, device_address, others):
        super().describe(device_type, device_name, device_address, others)
        self.device_ip_port.setText(others.get("IP Port", "25576"))
        self.is_client.setChecked(others.get("Is Client", 0))


class Parallel(Shower):
    def __init__(self, parent=None):
        super(Parallel, self).__init__(parent=parent)
        # self.device_ip_port = QLineEdit()
        # self.device_port.
        # self.device_ip_port.textEdited.connect(lambda x: self.ipPortChanged.emit(x))
        # self.is_client = QCheckBox()
        # self.is_client.stateChanged.connect(lambda x: self.clientChanged.emit(x))
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        # layout.addRow("IP Port:", self.device_ip_port)
        # layout.addRow("Is Client:", self.is_client)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, device_type, device_name, device_address, others):
        super().describe(device_type, device_name, device_address, others)
        # self.device_port.setText(others.get("IP Port", "25576"))
        # self.is_client.setChecked(others.get("Is Client", 0))


class Serial(Shower):
    def __init__(self, parent=None):
        super(Serial, self).__init__(parent=parent)
        self.baud_rate = QLineEdit()
        # self.device_port.
        self.baud_rate.textEdited.connect(lambda x: self.baudChanged.emit(x))
        self.data_bits = QLineEdit()
        self.data_bits.textEdited.connect(lambda x: self.bitsChanged.emit(x))
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

    def describe(self, device_type, device_name, device_address, others):
        super().describe(device_type, device_name, device_address, others)
        self.baud_rate.setText(others.get("Baud Rate", "9600"))
        self.data_bits.setText(others.get("Data Bits", "8"))


# class Serial(Shower):
#     def __init__(self):
#         super(Serial, self).__init__()
#         self.baud_rate = QLineEdit()
#         # self.device_port.
#         self.baud_rate.textEdited.connect(lambda x: self.baudChanged.emit(x))
#         self.data_bits = QLineEdit()
#         self.data_bits.textEdited.connect(lambda x: self.bitsChanged.emit(x))
#         self.setUI()
#
#     def setUI(self):
#         layout = QFormLayout()
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.addRow("Device Type:", self.device_type)
#         layout.addRow("Device Name:", self.device_name)
#         layout.addRow("Device Port:", self.device_address)
#         layout.addRow("Baud Rate:", self.baud_rate)
#         layout.addRow("Data Bits:", self.data_bits)
#         layout.addRow("", self.port_tip)
#         self.setLayout(layout)
#
#     def describe(self, device_type, device_name, device_address, others):
#         super().describe(device_type, device_name, device_address, others)
#         self.baud_rate.setText(others.get("baud", "9600"))
#         self.data_bits.setText(others.get("bits", "8"))


class Describer(QWidget):
    portChanged = pyqtSignal(str)
    colorChanged = pyqtSignal(str)
    sampleChanged = pyqtSignal(str)
    ipPortChanged = pyqtSignal(str)
    baudChanged = pyqtSignal(str)
    bitsChanged = pyqtSignal(int)
    clientChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Describer, self).__init__(parent=parent)
        self.screen = Screen(self)
        self.net = Net(self)
        self.parallel = Parallel(self)
        self.serial = Serial(self)
        self.other = Shower(self)
        self.other.setUI()

        self.screen.portChanged.connect(lambda x: self.portChanged.emit(x))
        self.net.portChanged.connect(lambda x: self.portChanged.emit(x))
        self.parallel.portChanged.connect(lambda x: self.portChanged.emit(x))
        self.serial.portChanged.connect(lambda x: self.portChanged.emit(x))
        self.other.portChanged.connect(lambda x: self.portChanged.emit(x))

        self.screen.colorChanged.connect(lambda x: self.colorChanged.emit(x))

        self.serial.baudChanged.connect(lambda x: self.baudChanged.emit(x))
        self.serial.bitsChanged.connect(lambda x: self.bitsChanged.emit(x))

        self.parallel.clientChanged.connect(lambda x: self.clientChanged.emit(x))

        self.net.ipPortChanged.connect(lambda x: self.ipPortChanged.emit(x))
        self.setUI()

    def setUI(self):
        self.layout = QStackedLayout()
        self.layout.addWidget(self.net)
        self.layout.addWidget(self.parallel)
        self.layout.addWidget(self.screen)
        self.layout.addWidget(self.serial)
        self.layout.addWidget(self.other)
        self.setLayout(self.layout)

    def describe(self, device_type, device_name, device_port, other: dict):
        if device_type == "network_port":
            self.layout.setCurrentIndex(0)
        elif device_type == "parallel_port":
            self.layout.setCurrentIndex(1)
        elif device_type == "screen":
            self.layout.setCurrentIndex(2)
        elif device_type == "serial_port":
            self.layout.setCurrentIndex(3)
        else:
            self.layout.setCurrentIndex(4)
        widget = self.layout.currentWidget()
        widget.describe(device_type, device_name, device_port, other)

    def changeName(self, new_name: str):
        self.layout.currentWidget().changeName(new_name)
# class Describer(QWidget):
#     portChanged = pyqtSignal(str)
#     colorChanged = pyqtSignal(str)
#     sampleChanged = pyqtSignal(str)
#     baudChanged = pyqtSignal(str)
#     bitsChanged = pyqtSignal(int)
#     clientChanged = pyqtSignal(int)
#
#     def __init__(self, parent=None):
#         super(Describer, self).__init__(parent=parent)
#         self.device_type = QLabel("Unselected")
#         self.device_name = QLabel("Unselected")
#         self.device_port = QLineEdit("")
#         self.port_tip = QLabel("")
#
#         self.device_port.textEdited.connect(self.showPortTip)
#         self.port: str = ""
#
#         self.setUI()
#
#     def setUI(self):
#         layout = QFormLayout()
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.addRow("Device Type:", self.device_type)
#         layout.addRow("Device Name:", self.device_name)
#         layout.addRow("Device Port:", self.device_port)
#         layout.addRow("", self.port_tip)
#         self.setLayout(layout)
#
#     def describe(self, device_type, device_name, device_port):
#         self.device_type.setText(device_type)
#         self.device_name.setText(device_name)
#         if device_type in ("mouse", "keyboard", "game pad"):
#             self.device_port.setText("Invalid")
#             self.device_port.setEnabled(False)
#         else:
#             self.device_port.setEnabled(True)
#             self.device_port.setText(device_port)
#             self.port = device_port
#             self.showPortTip(self.port)
#
#     def changeName(self, name):
#         self.device_name.setText(name)
#
#     def showPortTip(self, port: str):
#         """
#         端口有效性提示
#         :param port:
#         :return:
#         """
#         flag: bool = self.checkPort(port)
#
#         if flag is False:
#             self.port_tip.setText("Invalid Port")
#         else:
#             self.port_tip.setText("")
#             self.portChanged.emit(port)
#
#     def checkPort(self, port: str):
#         flag: bool = True
#         device_type: str = self.device_type.text()
#         if device_type == "screen":
#             if not port.isdigit() or int(port) > 10:
#                 flag = False
#         elif device_type == "network_port":
#             port_list = port.split(".")
#             if len(port_list) == 4:
#                 for i in port_list:
#                     if i.isdigit():
#                         if int(i) < 0 or int(i) > 255:
#                             flag = False
#                     else:
#                         flag = False
#             else:
#                 flag = False
#         elif device_type == "serial_port":
#             if port.startswith("com") and port[3:].isdigit():
#                 pass
#             else:
#                 flag = False
#         elif device_type == "parallel_port":
#             flag = port == "D010"
#         return flag
#
#     def changeSample(self, sample):
#         self.sampleChanged.emit(sample)
#
#     def changeColor(self, color):
#         self.colorChanged.emit(color)
#
#     def changeBits(self, bits):
#         self.bitsChanged.emit(bits)
#
#     def changeBaud(self, baud):
#         self.baudChanged.emit(baud)
#
#     def changeClient(self, client):
#         self.clientChanged.emit(client)
#
#
# class Describer1(Describer):
#     def __init__(self):
#         super(Describer1, self).__init__()
#         self.bg_color = ColorListEditor()
#         self.multi_sample = QLineEdit()
#
#         self.bg_color.colorChanged.connect(self.changeColor)
#         self.multi_sample.connect(self.changeSample)
#
#     def setUI(self):
#         layout = QFormLayout()
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.addRow("Device Type:", self.device_type)
#         layout.addRow("Device Name:", self.device_name)
#         layout.addRow("Device Port:", self.device_port)
#         layout.addRow("Back Color:", self.bg_color)
#         layout.addRow("Multi Sample:", self.multi_sample)
#         layout.addRow("", self.port_tip)
#         self.setLayout(layout)
#
#     def describe(self, device_type, device_name, device_port, color="0,0,0", sample="0"):
#         super().describe(device_type, device_name, device_port)
#         self.bg_color.setCurrentText(color)
#         self.multi_sample.setText(sample)
#
#
# class DescriberA(QWidget):
#     portChanged = pyqtSignal(str)
#     colorChanged = pyqtSignal(str)
#     sampleChanged = pyqtSignal(str)
#
#     def __init__(self, parent=None):
#         super(DescriberA, self).__init__(parent=parent)
#         self.device_type = QLabel("Unselected")
#         self.device_name = QLabel("Unselected")
#         self.device_port = QLineEdit("")
#         self.port_tip = QLabel("")
#
#         self.device_port.textEdited.connect(self.showPortTip)
#         self.port: str = ""
#
#         self.bg_color = ColorListEditor()
#         self.multi_sample = QLineEdit()
#
#         self.bg_color.colorChanged.connect(self.changeColor)
#
#         self.setUI()
#
#     def setUI(self):
#         layout = QFormLayout()
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.addRow("Device Type:", self.device_type)
#         layout.addRow("Device Name:", self.device_name)
#         layout.addRow("Device Port:", self.device_port)
#         layout.addRow("Back Color:", self.bg_color)
#         layout.addRow("Multi Sample:", self.multi_sample)
#         layout.addRow("", self.port_tip)
#         self.setLayout(layout)
#
#     def describe(self, device_type, device_name, device_port, color="0,0,0", sample="0"):
#         self.device_type.setText(device_type)
#         self.device_name.setText(device_name)
#
#         self.bg_color.setCurrentText(color)
#         self.multi_sample.setText(sample)
#
#         self.device_port.setEnabled(True)
#         self.device_port.setText(device_port)
#         self.port = device_port
#         self.showPortTip(self.port)
#
#     def changeName(self, name):
#         self.device_name.setText(name)
#
#     def showPortTip(self, port: str):
#         """
#         端口有效性提示
#         :param port:
#         :return:
#         """
#         flag: bool = self.checkPort(port)
#
#         if flag is False:
#             self.port_tip.setText("Invalid Port")
#         else:
#             self.port_tip.setText("")
#             self.portChanged.emit(port)
#
#     def checkPort(self, port: str):
#         flag: bool = True
#         device_type: str = self.device_type.text()
#         if device_type == "screen":
#             if not port.isdigit() or int(port) > 10:
#                 flag = False
#         elif device_type == "network_port":
#             port_list = port.split(".")
#             if len(port_list) == 4:
#                 for i in port_list:
#                     if i.isdigit():
#                         if int(i) < 0 or int(i) > 255:
#                             flag = False
#                     else:
#                         flag = False
#             else:
#                 flag = False
#         elif device_type == "serial_port":
#             if port.startswith("com") and port[3:].isdigit():
#                 pass
#             else:
#                 flag = False
#         elif device_type == "parallel_port":
#             flag = port == "D010"
#         return flag
#
#     def changeSample(self, sample):
#         self.sampleChanged.emit(sample)
#
#     def changeColor(self, color):
#         self.colorChanged.emit(color)
#
#
# class DescriberB(QWidget):
#     portChanged = pyqtSignal(str)
#     baudChanged = pyqtSignal(str)
#     bitsChanged = pyqtSignal(bool)
#
#     def __init__(self, parent=None):
#         super(DescriberB, self).__init__(parent=parent)
#         self.device_type = QLabel("Unselected")
#         self.device_name = QLabel("Unselected")
#         self.device_port = QLineEdit("")
#         self.port_tip = QLabel("")
#
#         self.device_port.textEdited.connect(self.showPortTip)
#         self.port: str = ""
#
#         self.baud_rate = QLineEdit()
#         self.bits = QCheckBox()
#
#         self.baud_rate.textEdited.connect(self.changeBaud)
#         self.bits.stateChanged.connect(self.changeBits)
#
#         self.setUI()
#
#     def setUI(self):
#         layout = QFormLayout()
#         layout.setLabelAlignment(Qt.AlignRight)
#         layout.addRow("Device Type:", self.device_type)
#         layout.addRow("Device Name:", self.device_name)
#         layout.addRow("Device Port:", self.device_port)
#         layout.addRow("Baud Rate", self.baud_rate)
#         layout.addRow("Data Bits:", self.bits)
#         layout.addRow("", self.port_tip)
#         self.setLayout(layout)
#
#     def describe(self, device_type, device_name, device_port, baud="0,0,0", bits=0):
#         self.device_type.setText(device_type)
#         self.device_name.setText(device_name)
#
#         self.baud_rate.setText(baud)
#         self.bits.setChecked(bits)
#
#         self.device_port.setEnabled(True)
#         self.device_port.setText(device_port)
#         self.port = device_port
#         self.showPortTip(self.port)
#
#     def changeName(self, name):
#         self.device_name.setText(name)
#
#     def showPortTip(self, port: str):
#         """
#         端口有效性提示
#         :param port:
#         :return:
#         """
#         flag: bool = self.checkPort(port)
#
#         if flag is False:
#             self.port_tip.setText("Invalid Port")
#         else:
#             self.port_tip.setText("")
#             self.portChanged.emit(port)
#
#     def checkPort(self, port: str):
#         flag: bool = True
#         device_type: str = self.device_type.text()
#         if device_type == "screen":
#             if not port.isdigit() or int(port) > 10:
#                 flag = False
#         elif device_type == "network_port":
#             port_list = port.split(".")
#             if len(port_list) == 4:
#                 for i in port_list:
#                     if i.isdigit():
#                         if int(i) < 0 or int(i) > 255:
#                             flag = False
#                     else:
#                         flag = False
#             else:
#                 flag = False
#         elif device_type == "serial_port":
#             if port.startswith("com") and port[3:].isdigit():
#                 pass
#             else:
#                 flag = False
#         elif device_type == "parallel_port":
#             flag = port == "D010"
#         return flag
#
#     def changeBits(self, bits):
#         self.bitsChanged.emit(bits)
#
#     def changeBaud(self, baud):
#         self.baudChanged.emit(baud)
