# 重写输入设备选择弹窗
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QGridLayout, QDialog, QListWidget, QPushButton, QListView


class DeviceInDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceInDialog, self).__init__(parent)
        self.devices_list = QListWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Input Device(s)")
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        item1 = QListWidgetItem("eye")
        item1.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item1)
        item2 = QListWidgetItem("device2")
        item2.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item2)
        item3 = QListWidgetItem("device1")
        item3.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item3)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: list or tuple
    # 图片名与设备名相同
    def addDevices(self, devices):
        for device_name, device_type in devices.items():
            item = QListWidgetItem(device_name)
            item.setIcon(QIcon(".\\.\\image\\{}_device".format(device_name)))
            self.devices_list.addItem(item)


# 重写输出设备选择弹窗
class DeviceOutDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceOutDialog, self).__init__(parent)
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
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        item1 = QListWidgetItem("eye")
        item1.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item1)
        item2 = QListWidgetItem("device2")
        item2.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item2)
        item3 = QListWidgetItem("device1")
        item3.setIcon(QIcon(".\\.\\image\\ff"))
        self.devices_list.addItem(item3)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    # devices: list or tuple
    # 图片名与设备名相同
    def addDevices(self, devices):
        for device_name, device_type in devices:
            item = QListWidgetItem(device_name)
            item.setIcon(QIcon(".\\.\\image\\{}_device".format(device_name)))
            self.devices_list.addItem(item)
