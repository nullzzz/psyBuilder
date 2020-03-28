from PyQt5.QtWidgets import QPushButton, QGridLayout, QLabel, QGroupBox

from app.newDevice.duration.Dialog import DeviceDialog
from app.newDevice.duration.describer.control import RespTriggers
from app.newDevice.duration.device.control import DeviceHome


class BiggerUP(QGroupBox):
    def __init__(self, title: str = "Stim Trigger", parent=None):
        super(BiggerUP, self).__init__(title, parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Del")
        self.add_bt.clicked.connnect(self.add)
        self.del_bt.clicked.connnect(self.delete)

        self.describer = RespTriggers()

        self.dialog = DeviceDialog()
        self.dialog.deviceAdd.connect(self.home.add)

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

    def add(self):
        self.dialog.show()

    def delete(self):
        self.home.deleteDevice()


class BiggerDown(QGroupBox):
    def __init__(self, parent=None):
        super(BiggerDown, self).__init__(parent)
        self.home = DeviceHome()
        self.add_bt = QPushButton("Add")
        self.del_bt = QPushButton("Del")
        self.add_bt.clicked.connnect(self.add)
        self.del_bt.clicked.connnect(self.delete)

        self.describer = RespTriggers()

        self.dialog = DeviceDialog()
        self.dialog.deviceAdd.connect(self.home.add)

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

    def add(self):
        self.dialog.show()

    def delete(self):
        self.home.deleteDevice()
