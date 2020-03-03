from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QMenu, QListWidgetItem

from .device.device import Device, Output, Quest, Tracker, Action


class DeviceHome(QListWidget):
    itemDoubleClick = pyqtSignal(QListWidgetItem)
    deviceChanged = pyqtSignal(str, dict)
    deviceDeleted = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(DeviceHome, self).__init__(parent)

        # 设备计数，生成设备id
        self.device_count = {
            # input device
            "mouse": 0,
            "keyboard": 0,
            "response box": 0,
            "game pad": 0,
            # output device
            "serial_port": 0,
            "parallel_port": 0,
            "network_port": 0,
            "screen": 0,
            "sound": 0,
            # quest
            "quest": 0,
            # tracker
            "tracker": 0,
            "action": 0,
        }

        # 存放当前选择设备名，避免重复，只通过create\delete操作
        self.device_list = []

        # 记录属性
        self.default_properties = {

        }

        self.currentItemChanged.connect(self.changeDevice)

        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)
        self.createContextMenu()

    def dropEvent(self, e):
        source = e.source()
        device_type = source.currentItem().getType()
        self.createDevice(device_type)

    def dragEnterEvent(self, e):
        source = e.source()
        if source != self:
            e.setDropAction(Qt.MoveAction)
        e.accept()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)
        self.rename_action = self.contextMenu.addAction("rename")
        self.rename_action.triggered.connect(lambda: self.itemDoubleClick.emit(self.currentItem()))

        self.delete_action = self.contextMenu.addAction("delete")
        self.delete_action.triggered.connect(lambda: self.deleteDevice(index=-1))
        self.clear_action = self.contextMenu.addAction("clear all")
        self.clear_action.triggered.connect(self.clearAll)

    def clearAll(self):
        """
        everything rollback
        :return:
        """
        for i in range(self.count() - 1, -1, -1):
            self.deleteDevice(i)
        for k in self.device_count.keys():
            self.device_count[k] = 0

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeDevice(self, item: Device, item_1: Device):
        if item:
            self.deviceChanged.emit(item.getDeviceId(), item.getInfo())

    def updateDevice(self, widget_id, info: dict):
        pass

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 从properties添加
        self.clearAll()
        for k, v in self.default_properties.items():
            v: dict
            device_id = k
            device_type = v.get("Device Type")
            device_name = v.get("Device Name")
            self.createDevice(device_type, device_id, device_name)
            # load count of devices
            self.device_count[device_type] += 1

    def createDeviceId(self, device_type):
        """
        生成设备标识符
        :param device_type:
        :return:
        """
        current_id = self.device_count[device_type]
        self.device_count[device_type] = current_id + 1
        return f"{device_type}.{current_id}"

    def deleteDevice(self, index: int = -1):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_device: Device = self.takeItem(index)
        device_name: str = del_device.getName()
        self.device_list.remove(device_name.lower())
        self.deviceDeleted.emit(del_device.getDeviceId(), {})

    def createDevice(self, device_type, device_id=None, device_name=None):
        """
        添加设备到已选列表
        :param device_name:
        :param device_id: 设备标识符
        :param device_type: 设备类型
        :return:
        """
        if device_id is None:
            device_id = self.createDeviceId(device_type)
        # 新建设备对象
        if device_type in ("sound", "screen", "network_port", "parallel_port", "serial_port"):
            device = Output(device_type, device_id)
        elif device_type in ("quest",):
            device = Quest(device_type, device_id)
        elif device_type in ("tracker",):
            device = Tracker(device_type, device_id)
        elif device_type in ("action",):
            device = Action(device_type, device_id)
        else:
            device = Device(device_type, device_id)

        if device_name is None:
            device_name = device_id.replace(".", "_")
        self.device_list.append(device_name.lower())
        device.setName(device_name)
        self.addItem(device)

    def changeCurrentName(self, new_name):
        self.currentItem().setText(new_name)

    def checkDeviceName(self, new_name: str):
        if new_name.lower() in self.device_list or new_name == "" or "." in new_name:
            return False
        return True
