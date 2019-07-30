from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QMenu, QListWidgetItem

from app.deviceSelection.tracker.device import Tracker


class SelectArea(QListWidget):
    itemDoubleClick = pyqtSignal(QListWidgetItem)
    itemChanged = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(SelectArea, self).__init__(parent)

        # 设备计数，生成设备id
        self.tracker_count = {
            "tracker": 0,
        }

        # 存放当前选择设备名，避免重复，只通过create\delete操作
        self.tracker_name = []
        # 删除缓冲区
        self.delete_buffer = []
        # 新增缓冲区
        self.add_buffer = []

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

    def dropEvent(self, e):
        source = e.source()
        tracker_type = source.currentItem().getType()
        self.createTracker(tracker_type)

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
        self.delete_action.triggered.connect(lambda: self.deleteTracker(index=-1))
        self.clear_action = self.contextMenu.addAction("clear all")
        self.clear_action.triggered.connect(self.clearAll)

    def clearAll(self):
        """
        everything rollback
        :return:
        """
        for i in range(self.count() - 1, -1, -1):
            self.deleteTracker(i, record=False)
        for k in self.tracker_count.keys():
            self.tracker_count[k] = 0
        self.add_buffer.clear()
        self.delete_buffer.clear()

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeItem(self, item: Tracker, item_1: Tracker):
        if isinstance(item, Tracker):
            self.itemChanged.emit(item.getName(), item.getInfo())

    # 返回选择设备
    def getInfo(self):
        # 清空缓冲区
        self.add_buffer.clear()
        self.delete_buffer.clear()

        # 更新default_properties
        self.default_properties.clear()
        for i in range(self.count()):
            key = self.item(i).getId()
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
            tracker_id, tracker_type, tracker_name = new_add
            # search the tracker
            for i in range(self.count()):
                tracker = self.item(i)
                if tracker.getId() == tracker_id:
                    del_list.append(i)
                    self.tracker_count[tracker_type] -= 1
        # clear buffer
        self.add_buffer.clear()
        del_list.sort(reverse=True)
        for i in del_list:
            self.deleteTracker(i, record=False)

        for new_del in self.delete_buffer:
            tracker_id, tracker_type, tracker_name, = new_del
            self.createTracker(tracker_type, tracker_id, tracker_name, record=False)
        self.delete_buffer.clear()
        # 从properties添加
        if self.count() == 0:
            for k, v in self.default_properties.items():
                v: dict
                tracker_id = k
                tracker_type = v.get("Tracker Type")
                tracker_name = v.get("Tracker Name")
                self.createTracker(tracker_type, tracker_id, tracker_name)
                # load count of trackers
                self.tracker_count[tracker_type] += 1
        else:
            self.tracker_name.clear()
            for i in range(self.count()):
                item = self.item(i)
                tracker_id = item.getId()
                tracker_name = item.getName()
                self.tracker_name.append(tracker_name)
                tracker_info = self.default_properties.get(tracker_id)
                item.setProperties(tracker_info)

        # 更新显示信息
        item = self.currentItem()

        if item is not None:
            self.itemChanged.emit(item.getName(), item.getInfo())
        else:
            self.itemChanged.emit("Unselected", {})

    def createTrackerId(self, tracker_type):
        """
        生成设备标识符
        :param tracker_type:
        :return:
        """
        current_id = self.tracker_count[tracker_type]
        self.tracker_count[tracker_type] = current_id + 1
        return f"{tracker_type}.{current_id}"

    def deleteTracker(self, index: int = -1, record: bool = True):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :param record: 是否记录到缓冲区，以备恢复
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_tracker: Tracker = self.takeItem(index)
        tracker_id: str = del_tracker.getId()
        tracker_type: str = del_tracker.getType()
        tracker_name: str = del_tracker.getName()
        self.tracker_name.remove(tracker_name.lower())
        # 记录到缓冲区
        if record:
            record_flag = True
            for i in self.add_buffer:
                if tracker_id == i[0]:
                    record_flag = False
                    break
            if record_flag:
                self.delete_buffer.append((tracker_id, tracker_type, tracker_name))

    def createTracker(self, tracker_type, tracker_id=None, tracker_name=None, record: bool = True):
        """
        添加设备到已选列表
        :param record: 是否记录到缓冲区
        :param tracker_name:
        :param tracker_id: 设备标识符
        :param tracker_type: 设备类型
        :return:
        """
        if tracker_id is None:
            tracker_id = self.createTrackerId(tracker_type)
        # 新建设备对象
        tracker = Tracker(tracker_type, tracker_id)

        if tracker_name is None:
            tracker_name = tracker_id
        tracker.setName(tracker_name)
        # 保存设备名
        self.tracker_name.append(tracker_name)
        if record:
            self.add_buffer.append((tracker_id, tracker_type, tracker_name))
        self.addItem(tracker)

    def changeCurrentSelectTrackerType(self, select_tracker_type: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setSelectTrackerType(select_tracker_type)

    def changeCurrentEyeTrackerDatafile(self, eye_tracker_datafile: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setEyeTrackerDatafile(eye_tracker_datafile)

    def changeCurrentIsCalibrateTracker(self, calibrate_tracker: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setIsCalibrateTracker(calibrate_tracker)

    def changeCurrentIsCalibrationBeep(self, calibration_beep: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setIsCalibrationBeep(calibration_beep)

    def changeCurrentSaccadeVelocityThreshold(self, velocity_threshold: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setSaccadeVelocityThreshold(velocity_threshold)

    def changeCurrentSaccadeAccelerationThreshold(self, acceleration_threshold: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setSaccadeAccelerationThreshold(acceleration_threshold)

    def changeCurrentIsForceDriftCorrection(self, force_drift_correction: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setIsForceDriftCorrection(force_drift_correction)

    def changeCurrentPupilSizeMode(self, pupil_size_mode: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setPupilSizeMode(pupil_size_mode)

    def changeCurrentIPAddress(self, ip_address: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setIPAddress(ip_address)

    def changeCurrentSendPortNumber(self, send_port: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setSendPortNumber(send_port)

    def changeCurrentReceivePortNumber(self, receive_port: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setSendPortNumber(receive_port)

    def changeCurrentTobiiGlassesIpv46Address(self, ipv46_address: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setTobiiGlassesIpv46Address(ipv46_address)

    def changeCurrentTobiiGlassesUDPPortNumber(self, udp_port: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            item.setTobiiGlassesUDPPortNumber(udp_port)

    def changeCurrentName(self, name: str):
        item: Tracker = self.currentItem()
        if isinstance(item, Tracker):
            old_name: str = item.getName()
            self.tracker_name.remove(old_name)
            item.setName(name)
            self.tracker_name.append(name)

    def checkTrackerName(self, new_name: str):
        if new_name.lower() in self.tracker_name or new_name == "":
            return False
        return True
