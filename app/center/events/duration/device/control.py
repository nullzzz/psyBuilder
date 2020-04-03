from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListWidget

from app.center.events.duration.device.input import InputDevice
from app.center.events.duration.device.output import OutputDevice
from app.func import Func


class DeviceHome(QListWidget):
    deviceChanged = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(DeviceHome, self).__init__(parent)

        # 记录属性
        self.default_properties = {
            # device_id : device_info
        }

        #
        self.device_ids = []
        self.currentItemChanged.connect(self.changeDevice)

    def clearAll(self):
        """
        everything rollback
        :return:
        """
        for i in range(self.count() - 1, -1, -1):
            self.deleteDevice(i)

    def changeDevice(self, item, item_1):
        """
        :param item: to this item
        :param item_1: from this item
        :return:
        """
        if item is not None:
            self.deviceChanged.emit(item.getDeviceId(), item.updateInfo())

    def updateDeviceInfo(self):
        for i in range(self.count()):
            item = self.item(i)
            device_id = item.getDeviceId()
            item.setProperties(self.default_properties[device_id])

    def setProperties(self, properties: dict):
        self.default_properties.clear()
        self.default_properties.update(properties)
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 从properties添加
        self.clearAll()
        for k, v in self.default_properties.items():
            v: dict
            device_id = k
            device_name = v.get("Device Name")
            self.createDevice(device_id, device_name, device_info=v)

    def deleteDevice(self, index: int = -1):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_device = self.takeItem(index)
        device_id = del_device.getDeviceId()
        self.device_ids.remove(device_id)
        self.deviceChanged.emit(device_id, {})

    def createDevice(self, device_id, device_name, device_info=None):
        """
        添加设备到已选列表
        :param device_info: 设备信息
        :param device_name:
        :param device_id: 设备标识符
        :return:
        """
        if device_id in self.device_ids:
            return
        self.device_ids.append(device_id)
        device_type = device_id.split(".")[0]
        # 新建设备对象
        if device_type in ("network_port", "parallel_port", "serial_port", "quest", "tracker", "action"):
            device = OutputDevice(device_id, device_name)
        elif device_type in ("game pad", "mouse", "keyboard", "response box"):
            device = InputDevice(device_id, device_name)

        # 载入信息
        if device_info is not None:
            device.setProperties(device_info)
        self.addItem(device)
        self.setCurrentItem(device)

    def getDeviceInfo(self) -> dict:
        info = {}
        for i in range(self.count()):
            item = self.item(i)
            info[item.getDeviceId] = item.getDeviceName()
        return info

    def refresh(self):
        for i in range(self.count()):
            device = self.item(i)
            device_id = device.getDeviceId()
            if (new_name := Func.getDeviceNameById(device_id)) != "":
                device.setDeviceName(new_name)
