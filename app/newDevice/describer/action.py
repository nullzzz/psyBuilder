from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFormLayout, QVBoxLayout, QComboBox

from app.newDevice.describer.basis import Shower


class Action(Shower):
    simple_info = {}

    def __init__(self, parent=None):
        super(Action, self).__init__(parent)

        self.tracker = QComboBox()

        # 是否更新using external device id
        self.update_flag = True
        self.tracker.currentTextChanged.connect(self.changeExternalDevice)
        for k, v in Action.simple_info.items():
            if k.startswith("tracker"):
                self.tracker.addItem(v)

        self.setUI()

        self.using_tracker_id = ""
        self.tracker_name = ""

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("EyeTracker Name:", self.tracker)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)

    def describe(self, info: dict):
        super().describe(info)
        tracker_name = info.get("Tracker Name", "")
        self.tracker.setCurrentText(tracker_name)

        self.index_tip.setHtml("About eye action:"
                               "<br><br><br>Currently, only Eyelink action is supported, because we only have the EYELINK device for debug.")

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Tracker Name": self.tracker.currentText(),
        }
        return properties

    def updateExternalDeviceInformation(self):
        self.update_flag = False
        self.tracker.clear()
        for k, v in self.simple_info.items():
            if k.startswith("tracker"):
                self.tracker.addItem(v)

        if self.using_tracker_id in Action.simple_info.keys():
            self.tracker.setCurrentText(Action.simple_info[self.using_tracker_id])
        else:
            self.using_tracker_id = ""
        self.update_flag = True

    def changeExternalDevice(self, device_name: str):
        if self.update_flag:
            for k, v in Action.simple_info.items():
                if v == device_name:
                    self.using_tracker_id = k