from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QMenu, QListWidgetItem

from app.deviceSelection.quest.device import Quest


class SelectArea(QListWidget):
    itemDoubleClick = pyqtSignal(QListWidgetItem)
    itemChanged = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(SelectArea, self).__init__(parent)

        # 设备计数，生成设备id
        self.quest_count = {
            "quest": 0,
        }

        # 存放当前选择设备名，避免重复，只通过create\delete操作
        self.quest_name = []
        # 删除缓冲区
        self.delete_buffer = []
        # 新增缓冲区
        self.add_buffer = []

        # 记录上次apply选择的设备数量
        # for i in self.quest_count.keys():
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

    def dropEvent(self, e):
        source = e.source()
        quest_type = source.currentItem().getType()
        self.createQuest(quest_type)

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
        self.delete_action.triggered.connect(lambda: self.deleteQuest(index=-1))
        self.clear_action = self.contextMenu.addAction("clear all")
        self.clear_action.triggered.connect(self.clearAll)

    def clearAll(self):
        """
        everything rollback
        :return:
        """
        for i in range(self.count() - 1, -1, -1):
            self.deleteQuest(i, record=False)
        for k in self.quest_count.keys():
            self.quest_count[k] = 0
        self.add_buffer.clear()
        self.delete_buffer.clear()

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def changeItem(self, item: Quest, item_1: Quest):
        if item:
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
            print(f"{self.item(i)}")
            print(f"{self.default_properties}")
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 以default_properties导入
    def loadSetting(self):
        # 处理缓冲区
        del_list: list = []
        for new_add in self.add_buffer:
            quest_id, quest_type, quest_name = new_add
            # search the quest
            for i in range(self.count()):
                quest = self.item(i)
                if quest.getId() == quest_id:
                    del_list.append(i)
                    self.quest_count[quest_type] -= 1
        # clear buffer
        self.add_buffer.clear()
        del_list.sort(reverse=True)
        for i in del_list:
            self.deleteQuest(i, record=False)

        for new_del in self.delete_buffer:
            quest_id, quest_type, quest_name = new_del
            self.createQuest(quest_type, quest_id, quest_name, record=False)
        self.delete_buffer.clear()
        # 从properties添加
        if self.count() == 0:
            for k, v in self.default_properties.items():
                v: dict
                quest_id = k
                quest_type = v.get("Quest Type")
                quest_name = v.get("Quest Name")
                self.createQuest(quest_type, quest_id, quest_name)
                # load count of quests
                self.quest_count[quest_type] += 1
        else:
            self.quest_name.clear()
            for i in range(self.count()):
                item = self.item(i)
                quest_id = item.getId()
                quest_name = item.getName()
                self.quest_name.append(quest_name)
                quest_info = self.default_properties.get(quest_id)
                item.setProperties(quest_info)

        # 更新显示信息
        item = self.currentItem()
        if item is not None:
            self.itemChanged.emit(item.getName(), item.getInfo())
        else:
            self.itemChanged.emit("Unselected", {})

    def createQuestId(self, quest_type):
        """
        生成设备标识符
        :param quest_type:
        :return:
        """
        current_id = self.quest_count[quest_type]
        self.quest_count[quest_type] = current_id + 1
        return f"{quest_type}.{current_id}"

    def deleteQuest(self, index: int = -1, record: bool = True):
        """
        删除设备
        :param index: 设备索引，默认当前选中
        :param record: 是否记录到缓冲区，以备恢复
        :return:
        """
        if index == -1:
            index = self.currentRow()
        # 被删掉的设备
        del_quest: Quest = self.takeItem(index)
        quest_id: str = del_quest.getId()
        quest_type: str = del_quest.getType()
        quest_name: str = del_quest.getName()
        self.quest_name.remove(quest_name.lower())
        # 记录到缓冲区
        if record:
            record_flag = True
            for i in self.add_buffer:
                if quest_id == i[0]:
                    record_flag = False
                    break
            if record_flag:
                self.delete_buffer.append((quest_id, quest_type, quest_name))

    def createQuest(self, quest_type, quest_id=None, quest_name=None, record: bool = True):
        """
        添加设备到已选列表
        :param record: 是否记录到缓冲区
        :param quest_name:
        :param quest_id: 设备标识符
        :param quest_type: 设备类型
        :return:
        """
        if quest_id is None:
            quest_id = self.createQuestId(quest_type)
        # 新建设备对象
        quest = Quest(quest_type, quest_id)

        if quest_name is None:
            quest_name = quest_id
        quest.setName(quest_name)
        # 保存设备名
        self.quest_name.append(quest_name)
        if record:
            self.add_buffer.append((quest_id, quest_type, quest_name))
        self.addItem(quest)

    def changeCurrentThreshold(self, threshold: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setThreshold(threshold)

    def changeCurrentSD(self, sd: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setSD(sd)

    def changeCurrentDesired(self, desired: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setDesired(desired)

    def changeCurrentSteep(self, steepness: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setSteep(steepness)

    def changeCurrentProportion(self, proportion: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setProportion(proportion)

    def changeCurrentChanceLevel(self, chance_level: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setChanceLevel(chance_level)

    def changeCurentMethod(self, method: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setMethod(method)

    def changeCurrentMinimum(self, minimum: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setMinimum(minimum)

    def changeCurrentMaximum(self, maximum: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setMaximum(maximum)

    def changeCurrentIsTransform(self, is_transform: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setIsTransform(is_transform)

    def changeCurrentName(self, name: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            old_name: str = item.getName()
            self.quest_name.remove(old_name)
            item.setName(name)
            self.quest_name.append(name)

    def changeCurrentResolution(self, resolution: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setResolution(resolution)

    def changeCurrentRefreshRate(self, refresh_rate: str):
        item: Quest = self.currentItem()
        if isinstance(item, Quest):
            item.setResolution(refresh_rate)

    def checkQuestName(self, new_name: str):
        if new_name.lower() in self.quest_name or new_name == "":
            return False
        return True
