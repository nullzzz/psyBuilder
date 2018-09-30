from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QStackedWidget, QMenu, QListWidgetItem, QLabel

from main.deviceSelection.inputDevice import InputDevice
from main.deviceSelection.outputDevice import OutputDevice


class SelectArea(QListWidget):
    itemDoubleClick = pyqtSignal(QListWidgetItem)

    def __init__(self, device_type: int=0, parent=None):
        super(SelectArea, self).__init__(parent)
        self.device_type = device_type
        # 对已选择设备计数
        self.device_count = {
            "mouse": 0,
            "keyboard": 0,
            "response box": 0,
            "game pad": 0,
            "serial_port": 0,
            "parallel_port": 0,
            "network_port": 0
        }

        # 存放当前选择设备名，避免重复
        self.device_name = []

        # 记录上次apply选择的设备数量
        for i in self.device_count.keys():
            self.setProperty(i, 0)

        # 记录属性
        self.default_properties = {

        }

        self.parameters = QStackedWidget()
        tip_label = QLabel("Device parameters")
        tip_label.setAlignment(Qt.AlignCenter)
        self.parameters.addWidget(tip_label)
        self.currentItemChanged.connect(self.changeItem)

        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)
        self.createContextMenu()

    def dropEvent(self, e):
        source = e.source()
        drop_item = source.currentItem().clone()
        item_type = drop_item.item_type
        # 设备命名，不区分大小写
        item_name = "{}.{}".format(item_type, self.device_count[item_type])
        self.device_count[item_type] += 1
        while item_name in self.device_name:
            item_name = "{}.{}".format(item_type, self.device_count[item_type])
            self.device_count[item_type] += 1

        drop_item.setName(item_name)

        self.device_name.append(item_name.lower())

        # 外部添加
        if source != self:
            self.addItem(drop_item)
            self.parameters.addWidget(drop_item.parameter)
        self.setCurrentItem(drop_item)

    def dragEnterEvent(self, e):
        source = e.source()
        if source != self:
            e.setDropAction(Qt.MoveAction)
        e.accept()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)
        self.delete_action = self.contextMenu.addAction("rename")
        self.delete_action.triggered.connect(lambda: self.itemDoubleClick.emit(self.currentItem()))

        self.delete_action = self.contextMenu.addAction("delete")
        self.delete_action.triggered.connect(self.deleteItem)
        self.clear_action = self.contextMenu.addAction("clear")
        self.clear_action.triggered.connect(self.clearAll)

    def deleteItem(self):
        index = self.currentRow()
        self.delItem(index)

    def delItem(self, index):
        del_item = self.takeItem(index)
        self.parameters.removeWidget(del_item.parameter)
        item_name: str = del_item.text()
        if item_name in self.default_properties.keys():
            self.default_properties.pop(item_name)
        self.device_name.remove(item_name.lower())

    def clearAll(self):
        for i in range(self.count()-1, -1, -1):
            self.delItem(i)
        for k in self.device_count.keys():
            self.device_count[k] = 0
            self.setProperty(k, 0)
        # print(self.device_count)

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeItem(self, item):
        if item:
            self.parameters.setCurrentWidget(item.parameter)

    # 返回选择设备
    #
    def getInfo(self):
        # 更新property记录的设备数量
        for k, v in self.device_count.items():
            self.setProperty(k, v)
        for i in range(self.count()):
            # 我也不知道为什么要加copy，不加的话
            key = self.item(i).text()
            info = self.item(i).getInfo()
            self.default_properties[key] = info.copy()
            # {设备名： {设备名：“”， 设备类型： “”}}
        return self.default_properties

    def setDeviceCount(self, device_count: dict):
        self.device_count = device_count

    def loadSetting(self):
        # 多余的删掉
        del_index = []
        for i in range(self.count()):
            item = self.item(i)
            if item.text() in self.default_properties.keys():
                pass
            else:
                del_index.insert(0, i)
        for i in del_index:
            self.delItem(i)

        # 删掉的加上
        current_devices = []
        for i in range(self.count()):
            current_devices.append(self.item(i).text())
        deleted_out_devices = [device for device in self.default_properties.keys()
                               if device not in current_devices]

        if self.device_type:
            for device in deleted_out_devices:
                properties: dict = self.default_properties[device]
                device_type = properties["Device type"]
                item = OutputDevice(device_type, device)
                item.setProperties(properties)
        else:
            for device in deleted_out_devices:
                properties: dict = self.default_properties[device]
                device_type = properties["Device type"]
                item = InputDevice(device_type, device)
                item.setProperties(properties)
        del_index.clear()

        # 恢复设备计数
        for device_type in self.device_count.keys():
            self.device_count[device_type] = self.property(device_type)

    def clone(self):
        area_clone = SelectArea()
        area_clone.setDeviceCount(self.device_count)
        for i in range(self.count()):
            item = self.item(i)
            area_clone.addItem(item.clone())
        return area_clone
