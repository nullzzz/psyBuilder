from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QMenu, QListWidgetItem

from app.deviceSelection.globalSelection.device import Device


class SelectArea(QListWidget):
    itemDoubleClick = pyqtSignal(QListWidgetItem)
    itemChanged = pyqtSignal(str, str, str, dict)

    def __init__(self, device_type: int = 0, parent=None):
        super(SelectArea, self).__init__(parent)
        self.device_type = device_type

        # 设备计数，生成设备id
        self.device_count = {
            "mouse": 0,
            "keyboard": 0,
            "response box": 0,
            "game pad": 0,
            "serial_port": 0,
            "parallel_port": 0,
            "network_port": 0,
            "screen": 0,
            "sound": 0
        }

        # 存放当前选择设备名，避免重复，只通过create\delete操作
        self.device_name = []
        # 删除缓冲区
        self.delete_buffer = []
        # 新增缓冲区
        self.add_buffer = []

        # 记录上次apply选择的设备数量
        # for i in self.device_count.keys():
        #     self.setProperty(i, 0)

        # 记录属性
        self.default_properties = {

        }

        self.currentItemChanged.connect(self.changeItem)

        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)
        self.createContextMenu()

        if device_type:
            self.createDevice("screen", record=False)
        else:
            self.createDevice("keyboard", record=False)
            self.createDevice("mouse", record=False)

    def dropEvent(self, e):
        source = e.source()
        device_type = source.currentItem().device_type
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
            self.deleteDevice(i, record=False)
        for k in self.device_count.keys():
            self.device_count[k] = 0
        self.add_buffer.clear()
        self.delete_buffer.clear()

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeItem(self, item: Device, item_1: Device):
        if item:
            self.itemChanged.emit(item.getType(), item.getName(), item.getPort(), item.getInfo())

    # 返回选择设备
    def getInfo(self):
        # 清空缓冲区
        self.add_buffer.clear()
        self.delete_buffer.clear()

        # 更新default_properties
        self.default_properties.clear()
        for i in range(self.count()):
            key = self.item(i).getDeviceId()
            info: dict = self.item(i).getInfo()
            self.default_properties[key] = info.copy()
            # {设备标识符： {设备名：“”， 设备类型： “”}}
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 处理缓冲区
        del_list: list = []
        for new_add in self.add_buffer:
            device_id, device_type, device_name, device_port = new_add
            # search the device
            for i in range(self.count()):
                device = self.item(i)
                if device.getDeviceId() == device_id:
                    del_list.append(i)
                    self.device_count[device_type] -= 1
        # clear buffer
        self.add_buffer.clear()
        del_list.sort(reverse=True)
        for i in del_list:
            self.deleteDevice(i, record=False)

        for new_del in self.delete_buffer:
            device_id, device_type, device_name, device_port = new_del
            self.createDevice(device_type, device_id, device_name, device_port, record=False)
        self.delete_buffer.clear()
        # 从properties添加
        if self.count() == 0:
            for k, v in self.default_properties.items():
                v: dict
                device_id = k
                device_type = v.get("Device Type")
                device_name = v.get("Device Name")
                device_port = v.get("Device Port")
                self.createDevice(device_type, device_id, device_name, device_port)
                # load count of devices
                self.device_count[device_type] += 1
        else:
            self.device_name.clear()
            for i in range(self.count()):
                item = self.item(i)
                device_id = item.getDeviceId()
                device_name = item.getName()
                self.device_name.append(device_name)
                device_info = self.default_properties.get(device_id)
                item.setProperties(device_info)

        # 更新显示信息
        item = self.currentItem()
        if item is not None:
            self.itemChanged.emit(item.getType(), item.getName(), item.getPort(), item.getInfo())
        else:
            self.itemChanged.emit("Unselected", "Unselected", "", {})

    def createDeviceId(self, device_type):
        """
        生成设备标识符
        :param device_type:
        :return:
        """
        current_id = self.device_count[device_type]
        self.device_count[device_type] = current_id + 1
        return f"{device_type}.{current_id}"

    def deleteDevice(self, index: int = -1, record: bool = True):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :param record: 是否记录到缓冲区，以备恢复
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_device: Device = self.takeItem(index)
        device_id: str = del_device.getDeviceId()
        device_type: str = del_device.getType()
        device_name: str = del_device.getName()
        device_port: str = del_device.getPort()
        self.device_name.remove(device_name.lower())
        # 记录到缓冲区
        if record:
            record_flag = True
            for i in self.add_buffer:
                if device_id == i[0]:
                    record_flag = False
                    break
            if record_flag:
                self.delete_buffer.append((device_id, device_type, device_name, device_port))

    def createDevice(self, device_type, device_id=None, device_name=None, device_port=None, record: bool = True):
        """
        添加设备到已选列表
        :param record: 是否记录到缓冲区
        :param device_port:
        :param device_name:
        :param device_id: 设备标识符
        :param device_type: 设备类型
        :return:
        """
        if device_id is None:
            device_id = self.createDeviceId(device_type)
        # 新建设备对象
        device = Device(device_type, device_id)
        if device_port is not None:
            device.setPort(device_port)
        else:
            device.setPort(device_id)
        if device_name is None:
            device_name = device_id
        device.setName(device_name)
        # 保存设备名
        self.device_name.append(device_name)
        if record:
            self.add_buffer.append((device_id, device_type, device_name, device_port))
        self.addItem(device)

    def changeCurrentPort(self, port: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setPort(port)

    def changeCurrentColor(self, color: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setColor(color)

    def changeCurrentSample(self, sample: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setSample(sample)

    def changeCurrentBaud(self, baud: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setBaud(baud)

    def changeCurrentBits(self, bits: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setBits(bits)

    def changeCurrentClient(self, client: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setClient(client)

    def changeCurrentSamplingRate(self, sampling_rate: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setSamplingRate(sampling_rate)

    def changeCurrentIpPort(self, ip_port: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setIpPort(ip_port)

    def changeCurrentName(self, name: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            old_name: str = item.getName()
            self.device_name.remove(old_name)
            item.setName(name)
            self.device_name.append(name)

    def changeCurrentResolution(self, resolution: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setResolution(resolution)

    def changeCurrentRefreshRate(self, refresh_rate: str):
        item: Device = self.currentItem()
        if isinstance(item, Device):
            item.setResolution(refresh_rate)

    def checkDeviceName(self, new_name: str):
        if new_name.lower() in self.device_name or new_name == "":
            return False
        return True
