# 重写输入设备选择弹窗
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QGridLayout, QDialog, QListWidget, QPushButton, QListView, QLabel


class DeviceInDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceInDialog, self).__init__(parent)
        self.devices_list = QListWidget()
        self.tip = QLabel("Please choose input device(s) from menu bar first!")
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Input Device(s)")
        self.tip.setAlignment(Qt.AlignCenter)
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        # self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.tip, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: list or tuple
    # 图片名与设备名相同
    def addDevices(self, devices):
        for device_name, device_type in devices.items():
            self.tip.hide()
            item = QListWidgetItem(device_name)
            item.setData(3, device_type)
            item.setIcon(QIcon("image/{}_device".format(device_type)))
            self.devices_list.addItem(item)


# 重写输出设备选择弹窗
class DeviceOutDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceOutDialog, self).__init__(parent)
        self.tip = QLabel("Please choose output device(s) from menu bar first!")
        self.devices_list = QListWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Output Device(s)")
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        # self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.tip, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: list or tuple
    # 图片名与设备名相同
    def addDevices(self, devices):
        for device_name, device_type in devices.items():
            self.tip.hide()
            item = QListWidgetItem(device_name)
            item.setData(3, device_type)
            item.setIcon(QIcon("image/{}_device".format(device_type)))
            self.devices_list.addItem(item)
