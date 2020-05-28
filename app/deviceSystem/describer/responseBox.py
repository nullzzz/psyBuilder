from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout

from app.deviceSystem.describer.basis import Shower


class ResponseBox(Shower):
    def __init__(self, parent=None):
        super(ResponseBox, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.device_index.textEdited.connect(self.showAddressTip)

        self.index_tip.setHtml("About Device Port:"
                               "<br><br>Currently, only Cedrus's response box devices are supported, because we only have this device"
                               "<br><br><b>Windows: </b> serial port name: e.g., <br>'COM2' for auto"
                               "<br><br><b>Mac OS: </b> serial port name: e.g., <br>'/dev/cu.usbserial-FTDI125ZX9' for auto"
                               "<br><br><b>Linux: </b> serial port name: e.g., <br>'/dev/ttyS0' for auto"
                               )
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_index)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)

    def describe(self, info: dict):
        self.device_index.setText(info.get("Device Index", "0"))
        super().describe(info)

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
        }
        return properties
