from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QCheckBox, QVBoxLayout

from app.deviceSystem.describer.basis import Shower


class GamePad(Shower):
    kb_id = ""

    def __init__(self, parent=None):
        super(GamePad, self).__init__(parent=parent)
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
            if GamePad.kb_id == self.device_id or GamePad.kb_id == "":
                GamePad.kb_id = self.device_id
                self.is_kb_queue.setCheckState(kb_queue)
            else:
                self.is_kb_queue.setCheckState(0)
        else:
            self.is_kb_queue.setCheckState(0)

        order_num = int(info.get("Device Id").split(".")[1]) + 1

        if order_num == 1:
            gpOrderStr = 'first'
        elif order_num == 2:
            gpOrderStr = 'second'
        else:
            gpOrderStr = f"{order_num}th"

        self.index_tip.setHtml("About Device Index ('auto' or an int):<br>"
                               # "<br><b>Windows: </b>order number start from 0 (e.g., 0,1, for the first and second gampad)"
                               "<br><b>Windows: </b>any gamepad index (returned by GetGamepadIndices in MATLAB). At least it works on my computer (win 10) with logicool F310 and PTB(3.0.16), let us try.."
                               "<br><br><b>Mac OS or Linux: </b> any gamepad index (returned by GetGamepadIndices in MATLAB)"
                               f"<br><br><b>'auto':</b> will use the {gpOrderStr} value in gamepad indices for this gamepad (returned by GetGamepadIndices in MATLAB)"
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
        if GamePad.kb_id == "" or GamePad.kb_id == self.device_id:
            self.is_kb_queue.setCheckState(state)
            self.port_tip.clear()
            if state == 0:
                GamePad.kb_id = ""
            else:
                GamePad.kb_id = self.device_id
        else:
            self.showTip(f"{Shower.id_2_name[GamePad.kb_id]}")
            self.is_kb_queue.setCheckState(0)
