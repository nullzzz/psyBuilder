from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListWidget

from app.deviceSelection.widgetSelection.InputDeviceItem import DeviceInItem
from app.deviceSelection.widgetSelection.OutputDeviceItem import DeviceOutItem
from app.info import Info


class ShowArea(QListWidget):
    infoChanged = pyqtSignal(tuple)
    respChanged = pyqtSignal(tuple)
    outputDeletedOrChanged = pyqtSignal(str)
    areaStatus = pyqtSignal(int)
    usingOutputDeviceUpdate = pyqtSignal(dict)
    addDeviceRepeat = pyqtSignal()

    def __init__(self, device_type: int = 1, parent=None):
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

    def changeItem(self, item):
        if item:
            self.infoChanged.emit(item.getValue())
            if self.device_type == Info.INPUT_DEVICE:
                self.respChanged.emit(item.getResp())

    # 返回选择设备
    def getInfo(self):
        # 清空缓冲区
        self.add_buffer.clear()
        self.delete_buffer.clear()
        self.default_properties.clear()
        # 更新default_properties
        for i in range(self.count()):
            key = self.item(i).text()
            info: dict = self.item(i).getInfo()
            self.default_properties[key] = info.copy()
            # {设备名： {设备名：“”， 设备类型： “”}}
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    def loadSetting(self):
        # 处理缓冲区
        del_list: list = []
        for new_add in self.add_buffer:
            device_id, device_name = new_add
            # search the device
            for i in range(self.count()):
                device = self.item(i)
                if device.getDeviceId() == device_id:
                    del_list.append(i)
        # clear buffer
        self.add_buffer.clear()
        del_list.sort(reverse=True)
        for i in del_list:
            self.delDevice(i, record=False)

        for new_del in self.delete_buffer:
            device_id, device = new_del
            self.addDevice(device, record=False)
        self.delete_buffer.clear()

        # 从properties添加
        if self.count() == 0:
            for k, v in self.default_properties.items():
                v: dict
                device_name = k
                device_id = v.get("Device Id")
                if self.device_type == Info.OUTPUT_DEVICE:
                    device = DeviceOutItem(device_name, device_id)
                else:
                    device = DeviceInItem(device_name, device_id)
                device.setProperties(v)
                self.addDevice(device, record=False)
        else:
            self.device_name.clear()
            self.device_id_name.clear()
            for i in range(self.count()):
                item = self.item(i)
                device_id = item.getDeviceId()
                device_name = item.getDeviceName()
                self.device_name.append(device_name.lower())
                self.device_id_name[device_id] = device_name
                device_info = self.default_properties.get(device_name)
                item.setProperties(device_info)

        # 更新显示信息
        item = self.currentItem()
        if item is not None:
            self.infoChanged.emit(item.getValue())
            if self.device_type == Info.INPUT_DEVICE:
                self.respChanged.emit(item.getResp())

    def addDevice(self, item, record=True):
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
            self.usingOutputDeviceUpdate.emit(self.device_id_name)
            if self.count():
                self.areaStatus.emit(1)
            if record:
                self.add_buffer.append((device_id, device_name))
        else:
            self.addDeviceRepeat.emit()

    def delDevice(self, index: int = -1, record=True):
        if index == -1:
            index = self.currentRow()
        item = self.takeItem(index)
        device_id = item.getDeviceId()
        device_name = item.getDeviceName()
        self.device_name.remove(device_name.lower())
        self.device_id_name.pop(device_id)
        self.usingOutputDeviceUpdate.emit(self.device_id_name)

        if self.count() == 0:
            self.areaStatus.emit(0)
        # 限制输出设备数为4
        elif self.count() < 4:
            self.areaStatus.emit(1)
        if record:
            # 判断删除的设备是否为新增未确定的设备
            # 若是，则不需要记录，即未确定设备删除不可恢复
            record_flag = True
            for i in self.add_buffer:
                if device_id == i[0]:
                    record_flag = False
                    break
            if record_flag:
                self.delete_buffer.append((device_id, item))

    def changeDeviceName(self, d_id, name):
        for i in range(self.count()):
            item = self.item(i)
            if item.getDeviceId() == d_id:
                item.changeDeviceName(name)
                item.setText(name)
                item.getInfo()
                self.setCurrentItem(item)

    def changeAllowable(self, x):
        if self.currentItem():
            self.currentItem().changeAllowable(x)

    def changeCorrect(self, x):
        if self.currentItem():
            self.currentItem().changeCorrect(x)

    def changeRtWindow(self, x):
        if self.currentItem():
            self.currentItem().changeRtWindow(x)

    def changeEndAction(self, x):
        if self.currentItem():
            self.currentItem().changeEndAction(x)

    def changeRight(self, x):
        if self.currentItem():
            self.currentItem().changeRight(x)

    def changeWrong(self, x):
        if self.currentItem():
            self.currentItem().changeWrong(x)

    def changeIgnore(self, x):
        if self.currentItem():
            self.currentItem().changeIgnore(x)

    def changeOutput(self, x):
        if self.currentItem():
            self.currentItem().changeOutput(x)

    def changeValueOrMessage(self, x):
        if self.currentItem():
            self.currentItem().changeValueOrMessage(x)

    def changePulseDuration(self, x):
        if self.currentItem():
            self.currentItem().changePulseDuration(x)
