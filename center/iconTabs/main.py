from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QTabBar

from center.iconTabs.timeline.main import Timeline
from .events.cycle.main import Cycle
from .events.image.imageDisplay import ImageDisplay
from .events.soundOut.main import SoundOut
from .events.text.main import TextDisplay
from .events.video.videoDisplay import VideoDisplay
from .eyeTracker.DC import EyeDC
from .eyeTracker.close import Close
from .eyeTracker.endR import EndR
from .eyeTracker.open import Open
from .eyeTracker.setup import SetUp
from .eyeTracker.startR import StartR
# from .quest.close import
from .quest.start import QuestStart
from .quest.update import QuestUpdate


class IconTabs(QTabWidget):
    # widget发送给properties窗口 (properties)
    propertiesShow = pyqtSignal(dict)
    # 新增cycle, 对于其信号要在main窗口中进行相应串接
    cycleAdd = pyqtSignal(str)

    def __init__(self, parent=None):
        super(IconTabs, self).__init__(parent)
        # 设置为Tab可以关闭
        self.setTabsClosable(True)
        self.setMovable(True)
        # 用一个字典存放所有tab, 每个tab有一个随机的特征值
        # 键为特征值, 值为widget
        self.value_widget = {}
        # value : parentValue
        self.value_parent = {}

        self.timeline = Timeline(self)
        self.value_widget['Timeline.10001'] = self.timeline
        tab_icon = QIcon(".\\.\\image\\timeLine.png")
        self.addTab(self.timeline, tab_icon, "Timeline")
        self.tabBar().setShape(QTabBar.TriangularNorth)

        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # self
        self.tabCloseRequested.connect(self.removeTab)
        # timeline
        self.linkTimelineSignals('Timeline.10001')

    def linkTimelineSignals(self, value):
        try:
            self.value_widget[value].iconAdd.disconnect(self.addIcon)
            self.value_widget[value].iconAdd.connect(self.addIcon)
        except Exception:
            self.value_widget[value].iconAdd.connect(self.addIcon)
            self.value_widget[value].iconRemove.connect(self.removeIcon)
            self.value_widget[value].icon_area.iconCopy.connect(self.copyIcon)
            self.value_widget[value].icon_area.icon_table.iconDoubleClicked.connect(self.openTab)
            self.value_widget[value].icon_area.icon_table.iconNameChange.connect(self.changeTabName)
            self.value_widget[value].icon_area.icon_table.iconRemove.connect(self.deleteTab)
            self.value_widget[value].icon_area.icon_table.propertiesShow.connect(self.getWidgetProperties)

    def addIcon(self, parent_value, name, pixmap, value):
        self.value_parent[value] = parent_value

    def removeIcon(self, parent_value, value):
        del self.value_parent[value]

    def openTab(self, value, name, can_open=True):
        try:
            widget_type = value.split('.')[0]
            if value in self.value_widget:
                widget = self.value_widget[value]
                tab_index = self.indexOf(widget)
                if tab_index != -1:
                    self.setCurrentIndex(tab_index)
                else:
                    self.setCurrentIndex(self.addTab(widget, name))
            else:
                widget = None
                tab_icon = None
                # 生成相应widget
                if widget_type == "Cycle":
                    widget = Cycle(value=value)
                    tab_icon = QIcon(".\\.\\image\\cycle.png")
                elif widget_type == "SoundOut":
                    widget = SoundOut()
                    tab_icon = QIcon(".\\.\\image\\sound.png")
                elif widget_type == "Text":
                    widget = TextDisplay()
                    tab_icon = QIcon(".\\.\\image\\text.png")
                elif widget_type == "Image":
                    widget = ImageDisplay()
                    tab_icon = QIcon(".\\.\\image\\imageDisplay.png")
                elif widget_type == "Video":
                    widget = VideoDisplay()
                    tab_icon = QIcon(".\\.\\image\\video.png")
                elif widget_type == "Close":
                    widget = Close()
                    tab_icon = QIcon(".\\.\\image\\close_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "DC":
                    widget = EyeDC()
                    tab_icon = QIcon(".\\.\\image\\DC_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "EndR":
                    widget = EndR()
                    tab_icon = QIcon(".\\.\\image\\end_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Open":
                    widget = Open()
                    tab_icon = QIcon(".\\.\\image\\open_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "SetUp":
                    widget = SetUp()
                    tab_icon = QIcon(".\\.\\image\\setup_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "StartR":
                    widget = StartR()
                    tab_icon = QIcon(".\\.\\image\\start_eye.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestStart":
                    widget = QuestStart()
                    tab_icon = QIcon(".\\.\\image\\start_quest.png")
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestUpdate":
                    widget = QuestUpdate()
                    tab_icon = QIcon(".\\.\\image\\update_quest.png")
                    widget.tabClose.connect(self.closeTab)
                else:
                    pass

                if widget:
                    # 新生成widget放入字典
                    self.value_widget[value] = widget
                    if widget_type == 'Cycle':
                        self.cycleAdd.emit(value)
                    # 各种widget的propertiesChange信号
                    widget.propertiesChange.connect(self.getChangedProperties)

                    if value != 'Timeline.10001' and value.startswith('Timeline.'):
                        self.linkTimelineSignals(value)

                    if can_open:
                        self.setCurrentIndex(self.addTab(widget, tab_icon, name))
        except Exception:
            print("error happens in open tab. [iconTabs/main.py]")

    def getWidgetProperties(self, value):
        properties = {"state": "not initialized"}
        try:
            widget = None
            if value in self.value_widget:
                widget = self.value_widget[value]

            if hasattr(widget, "getProperties"):
                properties = widget.getProperties()
            elif hasattr(widget, "getInfo"):
                properties = widget.getInfo()
        except Exception:
            properties = {"error": "can't get properties"}

        self.propertiesShow.emit(properties)

    def getChangedProperties(self, properties):
        self.propertiesShow.emit(properties)

    def changeTabName(self, value, name):
        if value in self.value_widget:
            tab_index = self.indexOf(self.value_widget[value])
            if tab_index != -1:
                self.setTabText(tab_index, name)

    def deleteTab(self, value):
        try:
            if value in self.value_widget:
                tab_index = self.indexOf(self.value_widget[value])
                if tab_index != -1:
                    self.removeTab(tab_index)
                del self.value_widget[value]
        except Exception:
            print("error happens delete tab. [iconTabs/main.py]")

    def closeTab(self, widget):
        tab_index = self.indexOf(widget)
        if tab_index != -1:
            self.removeTab(tab_index)

    def deleteIcon(self, value):
        try:
            if not value.startswith("Timeline."):
                parent_value = self.value_parent[value]
                timeline = self.value_widget[parent_value]
                timeline.icon_area.icon_table.removeIcon(value)
        except Exception:
            print("Some errors happen in delete icon in timeLine. [iconTabs/main.py]")

    def deleteTimeline(self, parent_value, value):
        try:
            cycle = self.value_widget[parent_value]
            cycle.deleteTimeline(value)
        except Exception:
            print("some errors happen in delete timeLine in cycle. [iconTabs/main.py]")

    def copyIcon(self, old_value, new_value, text):
        try:
            self.value_parent[new_value] = self.value_parent[old_value]
            # cycle 不能使用 deepcopy
            if old_value in self.value_widget:
                self.openTab(new_value, text, False)
                self.copyWidget(old_value, new_value)
        except Exception:
            print("some errors happen in copy icon. [iconTabs/main.py]")

    def copyWidget(self, old_value, new_value):
        try:
            old_widget = self.value_widget[old_value]
            widget_type = old_value.split('.')[0]
            if widget_type == 'Cycle':
                # properties
                # new_widget.properties = old_widget.properties
                pass
            else:
                self.value_widget[new_value] = old_widget
        except Exception:
            print("error happens in copy widget. [iconTabs/main.py]")
