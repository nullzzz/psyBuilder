from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QCheckBox, QVBoxLayout

from app.newDevice.describer.basis import Shower


class Keyboard(Shower):
    kb_id = ""

    def __init__(self, parent=None):
        super(Keyboard, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.device_index.setValidator(QRegExpValidator(QRegExp(r"\d+|auto")))
        self.is_kb_queue = QCheckBox()
        self.is_kb_queue.stateChanged.connect(self.changeState)
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Index:", self.device_index)
        layout.addRow("Is Kb Queue:", self.is_kb_queue)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)
        self.setLayout(vLayout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_index.setText(info.get("Device Index", "auto"))
        kb_queue = info.get("Is KB Queue", 0)
        if kb_queue == 2:
            if Keyboard.kb_id == self.device_id or Keyboard.kb_id == "":
                Keyboard.kb_id = self.device_id
                self.is_kb_queue.setCheckState(kb_queue)
            else:
                self.is_kb_queue.setCheckState(0)
        else:
            self.is_kb_queue.setCheckState(0)

        gpOrderNum = int(info.get("Device Id").split(".")[1]) + 1

        if gpOrderNum == 1:
            gpOrderStr = 'first'
        elif gpOrderNum == 2:
            gpOrderStr = 'second'
        else:
            gpOrderStr = f"{gpOrderNum}th"

        self.index_tip.setHtml("About Device Index ('auto' or an int):"
                               "<br><b>Int: </b> any keyboard index (returned by GetKeyboardIndices in MATLAB)"
                               f"<br><br><b>'auto':</b> will use the {gpOrderStr} value in keyboard indices for this keyboard (returned by GetKeyboardIndices in MATLAB)"
                               )

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
            "Is KB Queue": self.is_kb_queue.checkState(),
        }
        return properties

    def changeState(self, state):
        if Keyboard.kb_id == "" or Keyboard.kb_id == self.device_id:
            self.is_kb_queue.setCheckState(state)
            self.port_tip.setText("")
            if state == 0:
                Keyboard.kb_id = ""
            else:
                Keyboard.kb_id = self.device_id
        else:
            self.port_tip.setText(f"{Keyboard.kb_id}")
            self.is_kb_queue.setCheckState(0)
