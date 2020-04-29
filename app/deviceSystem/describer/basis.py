import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QFrame

from app.defi import *


class Shower(QWidget):
    def __init__(self, parent=None):
        super(Shower, self).__init__(parent)
        self.device_id = ""

        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")
        # you can show tips here!
        self.index_tip = QTextEdit("")
        self.index_tip.viewport().setAutoFillBackground(False)
        self.index_tip.setReadOnly(True)
        self.index_tip.setFrameShape(QFrame.NoFrame)
        self.index_tip.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.index_tip.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.port_tip = QLabel()

    def describe(self, info: dict):
        self.device_id = info.get("Device Id")
        device_type = info.get("Device Type", "ERROR")
        device_name = info.get("Device Name", "ERROR")
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)

    def showAddressTip(self, port: str):
        """
        端口有效性提示
        :param port:
        :return:
        """
        flag, tip = self.checkPort(port)
        if flag is False:
            self.port_tip.setText(tip)
        else:
            self.port_tip.clear()

    def checkPort(self, port: str):
        flag: bool = True
        tip = ""
        device_type: str = self.device_type.text()
        if device_type == DEV_SCREEN:
            if not port.isdigit() or int(port) > 10:
                flag = False
                tip = "Screen index should be in [0 to 10]"

        elif device_type == DEV_NETWORK_PORT:
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
            if flag is False:
                tip = "Invalid IP address"

        elif device_type == DEV_SERIAL_PORT:
            if port.startswith("COM") and port[3:].isdigit():
                # window
                pass
            elif port.startswith("/dev/cu.usbserial-"):
                # mac ox
                pass
            elif port.startswith("/dev/ttyS") and port[9:].isdigit():
                # linux
                pass
            else:
                flag = False
                tip = "Invalid serial address"

        elif device_type == DEV_RESPONSE_BOX:
            if port.startswith("COM") and port[3:].isdigit():
                # window
                pass
            elif port.startswith("/dev/cu.usbserial-"):
                # mac ox
                pass
            elif port.startswith("/dev/ttyS") and port[9:].isdigit():
                # linux
                pass
            else:
                flag = False
                tip = "Invalid Cedrus port address"

        elif device_type == DEV_PARALLEL_PORT:
            # Check whether a current_text string holds just a hexadecimal number
            if re.match('\A[0-9a-fA-F]+\Z', port) is None:
                flag = False
                tip = "Should be a hexadecimal"

        elif device_type == DEV_SOUND:
            flag = port.isdigit()
            if flag is False:
                tip = "Should be a digit"

        return flag, tip

    def changeName(self, new_name: str):
        self.device_name.setText(new_name)

    def getDeviceId(self):
        return self.device_id
