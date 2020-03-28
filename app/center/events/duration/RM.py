from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QGroupBox

from app.center.events.duration.Dialog import DeviceDialog
from app.center.events.duration.describer.control import Describer
from app.center.events.duration.device.control import DeviceHome


class BiggerUP(QGroupBox):
    deviceChanged = pyqtSignal(dict)

    def __init__(self, title: str = "Stim Trigger", parent=None):
        super(BiggerUP, self).__init__(title, parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Del")
        self.del_bt.setEnabled(False)

        self.describer = Describer(0)

        self.default_properties = {}
        self.home.default_properties = self.default_properties
        self.describer.default_properties = self.default_properties

        self.dialog = DeviceDialog(0)
        self.dialog.deviceAdd.connect(self.add)
        self.add_bt.clicked.connect(self.dialog.show)
        self.del_bt.clicked.connect(self.delete)
        self.home.deviceChanged.connect(self.describer.describe)

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Output Devices"), 0, 0, 1, 2)
        layout.addWidget(QLabel("Trigger Info"), 0, 2, 1, 1)
        layout.addWidget(self.home, 1, 0, 2, 2)
        layout.addWidget(self.add_bt, 3, 0, 1, 1)
        layout.addWidget(self.del_bt, 3, 1, 1, 1)
        layout.addWidget(self.describer, 1, 2, 2, 2)
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def add(self, device_id, device_name):
        self.home.createDevice(device_id, device_name)
        self.del_bt.setEnabled(self.home.count() > 0)
        self.deviceChanged.emit(self.home.getDeviceInfo())

    def delete(self):
        self.home.deleteDevice()
        self.del_bt.setEnabled(self.home.count() > 0)
        self.deviceChanged.emit(self.home.getDeviceInfo())

    def getInfo(self):
        self.describer.updateInfo()
        self.home.updateDeviceInfo()
        return self.default_properties.copy()


class BiggerDown(QGroupBox):
    def __init__(self, title="Input Devices", parent=None):
        super(BiggerDown, self).__init__(title, parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Del")
        self.del_bt.setEnabled(False)

        self.default_properties: dict = {}
        self.home.default_properties = self.default_properties

        self.resp_info = Describer(1)
        self.resp_trigger = Describer(2)
        self.eye_action = Describer(3)

        self.dialog = DeviceDialog(1)
        self.dialog.deviceAdd.connect(self.add)
        self.add_bt.clicked.connect(self.dialog.show)
        self.del_bt.clicked.connect(self.delete)
        self.home.deviceChanged.connect(self.resp_info.describe)
        self.home.deviceChanged.connect(self.resp_trigger.describe)
        self.home.deviceChanged.connect(self.eye_action.describe)
        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Device(s)"), 0, 0, 1, 1)
        layout.addWidget(self.home, 1, 0, 3, 2)
        layout.addWidget(self.add_bt, 4, 0, 1, 1)
        layout.addWidget(self.del_bt, 4, 1, 1, 1)
        # layout.addWidget(self.in_tip1, 1, 2, 5, 2)
        layout.addWidget(self.resp_info, 0, 2, 5, 2)
        # layout.addWidget(self.in_tip2, 5, 0, 2, 4)
        layout.addWidget(self.resp_trigger, 5, 0, 2, 4)
        # layout.addWidget(self.in_tip3, 7, 0, 2, 4)
        layout.addWidget(self.eye_action, 7, 0, 2, 4)
        layout.setVerticalSpacing(0)
        self.setLayout(layout)

    def add(self, device_id, device_name):
        self.home.createDevice(device_id, device_name)
        self.del_bt.setEnabled(self.home.count() > 0)

    def delete(self):
        self.home.deleteDevice()
        self.del_bt.setEnabled(self.home.count() > 0)

    def updateExternalInfo(self, output_device: dict):
        self.resp_trigger.updateSimpleInfo(output_device)

    def getInfo(self):
        info1 = self.resp_info.getInfo()
        info2 = self.resp_trigger.getInfo()
        info3 = self.eye_action.getInfo()

        self.default_properties.clear()
        for k in info1.keys():
            self.default_properties[k] = {**info1[k], **info2[k], **info3[k]}
        self.home.updateDeviceInfo()
        return self.default_properties.copy()
