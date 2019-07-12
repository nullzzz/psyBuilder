from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListWidget

from app.deviceSelection.widgetSelection.OutputDeviceItem import DeviceOutItem


class ShowArea(QListWidget):
    itemChanged = pyqtSignal(tuple)
    outputDeletedOrChanged = pyqtSignal(str)
    areaStatus = pyqtSignal(int)
    usingOutputDeviceName = pyqtSignal(list)
    addOutDeviceRepeat = pyqtSignal()

    def __init__(self, device_type: int = 0, parent=None):
        super(ShowArea, self).__init__(parent)
        self.device_type = device_type

        # 存放当前选择设备名，避免重复
        self.device_name = []

        self.device_id_name: dict = {}
        # 删除缓冲区
        self.delete_buffer = []
        # 新增缓冲区
        self.add_buffer = []

        # 记录属性
        self.default_properties = {

        }

        self.currentItemChanged.connect(self.changeItem)

    def changeItem(self, item: DeviceOutItem):
        if item:
            self.itemChanged.emit(item.getValue())

    # 返回选择设备
    def getInfo(self):
        # 清空缓冲区
        self.add_buffer.clear()
        self.delete_buffer.clear()

        # 更新default_properties
        for i in range(self.count()):
            # 我也不知道为什么要加copy，不加的话
            key = self.item(i).text()
            info: dict = self.item(i).getInfo()
            self.default_properties[key] = info.copy()
            # {设备名： {设备名：“”， 设备类型： “”}}
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 处理缓冲区
        del_list: list = []
        for new_add in self.add_buffer:
            device_id, device_name = new_add
            # search the device
            for i in range(self.count()):
                device: DeviceOutItem = self.item(i)
                if device.getDeviceId() == device_id:
                    del_list.append(i)
        # clear buffer
        self.add_buffer.clear()
        del_list.sort(reverse=True)
        for i in del_list:
            self.delOutDevice(i, record=False)

        for new_del in self.delete_buffer:
            device_id, device = new_del
            self.addOutDevice(device, record=False)
        self.delete_buffer.clear()

        # 从properties添加
        if self.count() == 0:
            for k, v in self.default_properties.items():
                v: dict
                device_name = k
                device_id = v.get("Device Id")
                device = DeviceOutItem(device_name, device_id)
                device.setProperties(v)
                self.addOutDevice(device, record=False)
        else:
            self.device_name.clear()
            for i in range(self.count()):
                item: DeviceOutItem = self.item(i)
                device_name = item.getDeviceName()
                self.device_name.append(device_name.lower())
                device_info = self.default_properties.get(device_name)
                item.setProperties(device_info)

        # 更新显示信息
        item = self.currentItem()
        if item is not None:
            self.itemChanged.emit(item.getValue())

    def addOutDevice(self, item: DeviceOutItem, record=True):
        device_name = item.text()
        device_id = item.getDeviceId()
        self.device_id_name[device_id] = device_name
        # 提示信息
        if self.count() == 0:
            self.areaStatus.emit(1)
        if device_name not in self.device_name:
            self.device_name.append(device_name.lower())
            self.addItem(item)
            self.setCurrentItem(item)
            self.usingOutputDeviceName.emit(self.device_name)
            if self.count():
                self.areaStatus.emit(1)
            if record:
                self.add_buffer.append((device_id, device_name))
        else:
            self.addOutDeviceRepeat.emit()

    def delOutDevice(self, index: int = -1, record=True):
        if index == -1:
            index = self.currentRow()
        item: DeviceOutItem = self.takeItem(index)
        device_id = item.getDeviceId()
        device_name = item.getDeviceName()
        self.device_name.remove(device_name.lower())

        self.usingOutputDeviceName.emit(self.device_name)

        if self.count() == 0:
            self.areaStatus.emit(0)
        # 限制输出设备数为4
        elif self.count() < 4:
            self.areaStatus.emit(1)
        if record:
            self.delete_buffer.append((device_id, item))
