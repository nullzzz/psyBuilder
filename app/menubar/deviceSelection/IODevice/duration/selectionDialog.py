from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QGridLayout, QDialog, QListWidget, QPushButton, QListView, QLabel

from app.func import Func
from app.info import Info


class SelectionDialog(QDialog):
    def __init__(self, io_type: int = 0, parent=None):
        super(SelectionDialog, self).__init__(parent)
        self.devices_list = QListWidget()
        if io_type == Info.INPUT_DEVICE:
            self.tip = QLabel("Please choose input device(s) from menu bar first!")
            self.setWindowTitle("Choose Input Device(s)")
        else:
            self.tip = QLabel("Please choose output device(s) from menu bar first!")
            self.setWindowTitle("Choose Output Device(s)")
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.tip.setAlignment(Qt.AlignCenter)
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setSpacing(20)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.tip, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: dict
    # 图片名与设备名相同
    def addDevices(self, devices: dict):
        for device_name, properties in devices.items():
            device_type = properties.get("Device Type")
            if device_type == "screen" or device_name == "sound":
                continue
            device_name = properties.get("Device Name")
            device_port = properties.get("Device Port")

            item = QListWidgetItem(device_name)
            item.setData(3, properties)
            item.setIcon(QIcon(Func.getImagePath(f"{device_type}_device")))
            self.devices_list.addItem(item)
            self.tip.hide()
