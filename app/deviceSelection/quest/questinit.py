from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit

from app.deviceSelection.quest.describer import Describer
from app.deviceSelection.quest.device import Quest
from app.deviceSelection.quest.selectionList import SelectArea
from app.func import Func
from app.info import Info
from lib import MessageBox


class QuestInit(QWidget):
    deviceSelect = pyqtSignal(int, dict)
    deviceNameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(QuestInit, self).__init__(parent)

        self.setWindowTitle("Quest")
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))

        # 上方待选择设备
        self.quest_list = QListWidget()
        self.quest_list.setViewMode(QListView.IconMode)
        self.quest_list.setSortingEnabled(True)
        self.quest_list.setAcceptDrops(False)
        self.quest_list.setAutoFillBackground(True)
        self.quest_list.setWrapping(False)
        self.quest_list.setSpacing(10)
        self.quest_list.setFrameStyle(QFrame.NoFrame)
        self.quest_list.setIconSize(QSize(40, 40))

        self.quests: tuple = ("quest",)
        for quest in self.quests:
            self.quest_list.addItem(Quest(quest))

        # 已选择设备
        self.selected_devices = SelectArea()
        self.selected_devices.itemDoubleClicked.connect(self.rename)
        self.selected_devices.itemDoubleClick.connect(self.rename)
        self.selected_devices.itemChanged.connect(self.changeItem)

        # 展示区
        self.describer = Describer()
        self.describer.estimatedThresholdChanged.connect(self.changeThreshold)
        self.describer.stdDevChanged.connect(self.changeSD)
        self.describer.desiredProportionChanged.connect(self.changeDesired)
        self.describer.steepnessChanged.connect(self.changeSteep)
        self.describer.proportionChanged.connect(self.changeProportion)
        self.describer.chanceLevelChanged.connect(self.changeChanceLevel)
        self.describer.methodChanged.connect(self.changeMethod)
        self.describer.minimumChanged.connect(self.changeMinimum)
        self.describer.maximumChanged.connect(self.changeMaximum)
        self.describer.isTransformChanged.connect(self.changeIsTransform)

        # 按键区
        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):
        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.addWidget(self.selected_devices, 1)
        layout1.addWidget(self.describer, 1)

        layout2 = QHBoxLayout()
        layout2.addStretch(5)
        layout2.addWidget(self.ok_bt)
        layout2.addWidget(self.cancel_bt)
        layout2.addWidget(self.apply_bt)

        layout.addWidget(self.quest_list, 1)
        layout.addLayout(layout1, 3)
        layout.addLayout(layout2, 1)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()

    def cancel(self):
        self.selected_devices.loadSetting()

    def apply(self):
        self.getInfo()

    def changeItem(self, name, info: dict):
        self.describer.describe(name, **info)

    def changeThreshold(self, threshold: str):
        self.selected_devices.changeCurrentThreshold(threshold)

    def changeSD(self, sd: str):
        self.selected_devices.changeCurrentSD(sd)

    def changeDesired(self, desired: str):
        self.selected_devices.changeCurrentDesired(desired)

    def changeSteep(self, steepness: str):
        self.selected_devices.changeCurrentSteep(steepness)

    def changeProportion(self, proportion: str):
        self.selected_devices.changeCurrentProportion(proportion)

    def changeChanceLevel(self, chance_level: str):
        self.selected_devices.changeCurrentChanceLevel(chance_level)

    def changeMethod(self, method: str):
        self.selected_devices.changeCurentMethod(method)

    def changeMinimum(self, minimum: str):
        self.selected_devices.changeCurrentMinimum(minimum)

    def changeMaximum(self, maximum: str):
        self.selected_devices.changeCurrentMaximum(maximum)

    def changeIsTransform(self, is_transform: str):
        self.selected_devices.changeCurrentIsTransform(is_transform)

    def rename(self, item: Quest):
        name: str = item.text()
        item_name: str = name.lower()

        text, ok = QInputDialog.getText(self, "Change Quest Name", "Quest Name:", QLineEdit.Normal, item.text())
        if ok and text != '':
            text: str
            if text.lower() in self.selected_devices.quest_name and item_name != text.lower():
                MessageBox.warning(self, f"{text} is invalid!", "Quest name must be unique",
                                    MessageBox.Ok)
            else:
                self.selected_devices.changeCurrentName(text)
                self.describer.changeName(text)
                self.getInfo()
                self.deviceNameChanged.emit(item.getId(), text)

    # 参数导出, 记录到Info
    def getInfo(self):
        quest_info: dict = self.selected_devices.getInfo()
        Info.QUEST_INFO = quest_info.copy()

    # 参数导入
    def setProperties(self, properties: dict):
        self.selected_devices.clearAll()
        self.selected_devices.setProperties(properties)
        # 更新全局信息
        Info.QUEST_INFO = properties.copy()
