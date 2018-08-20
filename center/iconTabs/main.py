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
    # 发送到attributes窗口 (attributes)
    attributesShow = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(IconTabs, self).__init__(parent)
        # 设置为Tab可以关闭
        self.setTabsClosable(True)
        self.setMovable(True)
        # 用一个字典存放所有tab, 每个tab有一个随机的特征值
        # 键为特征值, 值为widget
        self.value_widget = {}
        # value : parentValue, 仅仅限于timeline和其中icon, 不包含cycle和其中的timeline
        self.value_parent = {}
        # timeline属性及父节点timeline
        self.timeline_parent = {'Timeline.10001' : None}

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
        self.currentChanged.connect(self.showTimelineAttributes)
        # timeline
        self.linkTimelineSignals('Timeline.10001')
        # cycle
        self.cycleAdd.connect(self.linkCycleSignals)

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

    def linkCycleSignals(self, value):
        try:
            cycle = self.value_widget[value]
            try:
                cycle.timelineAdd.disconnect(self.addTimeline)
                cycle.timelineAdd.connect(self.addTimeline)
            except Exception:
                cycle.timelineAdd.connect(self.addTimeline)
                cycle.attributeAdd.connect(self.addTimelineAttribute)
                cycle.attributeChange.connect(self.changeTimelineAttribute)
        except Exception:
            print("error happens in link cycle signals. [iconTabs\main.py]")

    def addIcon(self, parent_value, name, pixmap, value):
        self.value_parent[value] = parent_value

    # 单纯的保存所有timeline中的icon增减
    def removeIcon(self, parent_value, value):
        del self.value_parent[value]

    def addTimeline(self, cycle_value, timeline_name, timeline_pixmap, timeline_value):
        try:
            # timeline 相关属性
            timeline_parent = self.value_parent[cycle_value]
            self.timeline_parent[timeline_value] = timeline_parent
            # 在此函数就去生成timeline实体, 以便去处理timeline的attribute
            self.openTab(timeline_value, timeline_name, False)
            # 取出该timeline所在行已有attribute
            cycle = self.value_widget[cycle_value]
            row = cycle.value_row[timeline_value]
            for col in range(2, cycle.timeline_table.columnCount()):
                attribute_name = cycle.timeline_table.col_header[col]
                attribute_value = cycle.timeline_table.item(row, col).text()
                self.value_widget[timeline_value].attributes[attribute_name] = attribute_value
        except Exception:
            print("error happens in add timeline. [iconTabs/main.py]")

    def removeTimeline(self):
        pass

    def addTimelineAttribute(self, cycle_value, name, default_value):
        try:
            cycle = self.value_widget[cycle_value]
            for row in cycle.row_value:
                timeline_value = cycle.row_value[row]
                if timeline_value in self.value_widget:
                    timeline = self.value_widget[timeline_value]
                    timeline.attributes[name] = default_value
        except Exception:
            print("error happens in add new timeline attribute. [iconTabs/main.py]")

    def changeTimelineAttribute(self, timeline_value, attribute_name, attribute_value):
        try:
            if timeline_value in self.value_widget:
                timeline = self.value_widget[timeline_value]
                timeline.attributes[attribute_name] = attribute_value
        except Exception:
            print("error happens in change timeline attribute value. [iconTabs/main.py]")

    def getTimelineAttributes(self, value):
        try:
            attributes = {}
            now_timeline = self.value_widget[value]
            now_value = value
            while True:
                for name in now_timeline.attributes:
                    if name not in attributes:
                        attributes[name] = now_timeline.attributes[name]
                if self.timeline_parent[now_value]:
                    now_value = self.timeline_parent[now_value]
                    now_timeline = self.value_widget[now_value]
                else:
                    break
            return attributes
        except Exception:
            print("error happens in get timeline attribute. [iconTabs/main.py]")

    def showTimelineAttributes(self, tab_index):
        widget = self.widget(tab_index)
        if isinstance(widget, Timeline):
            self.attributesShow.emit(self.getTimelineAttributes(widget.value))

    def openTab(self, value, name, can_open=True):
        try:
            widget_type = value.split('.')[0]
            if value in self.value_widget:
                widget = self.value_widget[value]
                tab_index = self.indexOf(widget)
                if tab_index != -1:
                    self.setCurrentIndex(tab_index)
                else:
                    tab_icon = None
                    # 生成相应widget
                    if widget_type == "Cycle":
                        tab_icon = QIcon(".\\.\\image\\cycle.png")
                    elif widget_type == "Timeline":
                        tab_icon = QIcon(".\\.\\image\\timeLine.png")
                    elif widget_type == "SoundOut":
                        tab_icon = QIcon(".\\.\\image\\sound.png")
                    elif widget_type == "Text":
                        tab_icon = QIcon(".\\.\\image\\text.png")
                    elif widget_type == "Image":
                        tab_icon = QIcon(".\\.\\image\\imageDisplay.png")
                    elif widget_type == "Video":
                        tab_icon = QIcon(".\\.\\image\\video.png")
                    elif widget_type == "Close":
                        tab_icon = QIcon(".\\.\\image\\close_eye.png")
                    elif widget_type == "DC":
                        tab_icon = QIcon(".\\.\\image\\DC_eye.png")
                    elif widget_type == "EndR":
                        tab_icon = QIcon(".\\.\\image\\end_eye.png")
                    elif widget_type == "Open":
                        tab_icon = QIcon(".\\.\\image\\open_eye.png")
                    elif widget_type == "SetUp":
                        tab_icon = QIcon(".\\.\\image\\setup_eye.png")
                    elif widget_type == "StartR":
                        tab_icon = QIcon(".\\.\\image\\start_eye.png")
                    elif widget_type == "QuestStart":
                        tab_icon = QIcon(".\\.\\image\\start_quest.png")
                    elif widget_type == "QuestUpdate":
                        tab_icon = QIcon(".\\.\\image\\update_quest.png")
                    else:
                        pass
                    self.setCurrentIndex(self.addTab(widget, tab_icon, name))
                # 我在cycle中生成timeline时, 就已经生成了timeline实体
                if value.startswith("Timeline."):
                    self.attributesShow.emit(self.getTimelineAttributes(value))
            else:
                widget = None
                tab_icon = None
                # 生成相应widget
                if widget_type == "Cycle":
                    widget = Cycle(value=value)
                    tab_icon = QIcon(".\\.\\image\\cycle.png")
                elif widget_type == "Timeline":
                    widget = Timeline(value=value)
                    tab_icon = QIcon(".\\.\\image\\timeLine.png")
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
                    try:
                        widget.propertiesChange.connect(self.getChangedProperties)
                    except Exception:
                        if widget_type == "Timeline":
                            pass
                        else:
                            print("error happens in connect propertiesChange. [iconTabs/main.py]")

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
                # 如果是cycle, 要级联删除其中的timeline及timeline中的一切
                if value.startswith("Cycle."):
                    cycle = self.value_widget[value]
                    for row in range(0, cycle.timeline_table.rowCount()):
                        try:
                            timeline_value = cycle.row_value[row]
                            self.deleteTimeline(value, timeline_value)
                        except Exception:
                            pass
                # 如果是timeline, 要删除其中所有的icon
                elif value.startswith("Timeline."):
                    timeline = self.value_widget[value]
                    for col in range(1, timeline.icon_area.icon_table.fill_count + 1):
                        try:
                            icon_value = timeline.icon_area.icon_table.cellWidget(1, col).value
                            self.deleteTab(icon_value)
                        except Exception:
                            print("row may be out. [iconTabs/main.py]")

                del self.value_widget[value]
        except Exception:
            print("error happens delete {} tab. [iconTabs/main.py]".format(value.split('.')[0]))

    # 删除cycle中的timeline, timeline只能通过在structure中删除
    def deleteTimeline(self, parent_value, value):
        try:
            # 删除timeline所在cycle中那一行
            cycle = self.value_widget[parent_value]
            cycle.deleteTimeline(value)

            try:
                del self.timeline_parent[value]
                # 关闭timeline的tab及其所有icon的tab
                self.deleteTab(value)
            except Exception:
                print("some error happens in delete timeline in icon tabs. [iconTabs/main.py]")
        except Exception:
            print("some errors happen in delete timeline in cycle. [iconTabs/main.py]")

    def closeTab(self, widget):
        tab_index = self.indexOf(widget)
        if tab_index != -1:
            self.removeTab(tab_index)

    # 删除某个icon, 感觉和之前的removeIcon有点重复造成浪费
    def deleteIcon(self, value):
        try:
            if not value.startswith("Timeline.") and value in self.value_parent:
                parent_value = self.value_parent[value]
                timeline = self.value_widget[parent_value]
                timeline.icon_area.icon_table.removeIcon(value)
                # 删除该tab相关属性
                if not value.startswith("Timeline."):
                    del self.value_parent[value]
        except Exception as e:
            print("some errors happen in delete icon in timeLine. [iconTabs/main.py]")

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
