from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QTabWidget, QTabBar, QMenu, QShortcut, QAction

from center.iconTabs.condition.switchBranch import SwitchBranch
from center.iconTabs.timeline.main import Timeline
from getImage import getImage
from .condition.ifBranch import IfBranch
from .events.cycle.main import Cycle
from .events.image.imageDisplay import ImageDisplay
from .events.soundOut.soundDisplay import SoundDisplay
from .events.text.textDisplay import TextDisplay
from .events.video.videoDisplay import VideoDisplay
from .eyeTracker.DC import EyeDC
from .eyeTracker.action import EyeAction
from .eyeTracker.calibrate import EyeCalibrate
from .eyeTracker.close import Close
from .eyeTracker.endR import EndR
from .eyeTracker.open import Open
from .eyeTracker.startR import StartR
from .quest.getvalue import QuestGetValue
from .quest.start import QuestInit
from .quest.update import QuestUpdate


class IconTabs(QTabWidget):
    # widget发送给properties窗口 (properties)
    propertiesShow = pyqtSignal(dict)
    # 新增cycle, 对于其信号要在main窗口中进行相应串接
    cycleAdd = pyqtSignal(str)
    # 同上
    ifBranchAdd = pyqtSignal(str)
    # 发送到structure (value)
    attributesShow = pyqtSignal(str)

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
        self.timeline_parent = {'Timeline.10001': None}

        self.timeline = Timeline(self)
        self.value_widget['Timeline.10001'] = self.timeline
        tab_icon = QIcon("image/timeLine.png")
        self.addTab(self.timeline, tab_icon, "Timeline")
        self.tabBar().setShape(QTabBar.TriangularNorth)
        # 右键菜单及快捷键
        self.setMenuAndShortcut()
        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # self
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.showTimelineAttributes)
        self.currentChanged.connect(self.showProperties)
        # timeline
        self.linkTimelineSignals('Timeline.10001')
        # cycle
        self.cycleAdd.connect(self.linkCycleSignals)
        # if branch
        self.ifBranchAdd.connect(self.linkIFBranchSignals)

    def linkTimelineSignals(self, value):
        try:
            self.value_widget[value].iconAdd.disconnect(self.addIcon)
            self.value_widget[value].iconAdd.connect(self.addIcon)
        except Exception:
            self.value_widget[value].iconAdd.connect(self.addIcon)
            self.value_widget[value].iconRemove.connect(self.removeIcon)
            self.value_widget[value].iconNameChange.connect(self.changeTabName)
            self.value_widget[value].icon_area.iconCopy.connect(self.copyIcon)
            self.value_widget[value].icon_area.icon_table.iconDoubleClicked.connect(self.openTab)
            self.value_widget[value].icon_area.icon_table.iconRemove.connect(self.deleteTab)
            self.value_widget[value].icon_area.icon_table.propertiesShow.connect(self.getWidgetProperties)
            self.value_widget[value].icon_area.icon_table.iconWidgetMerge.connect(self.changeValueWidget)

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

    def linkIFBranchSignals(self, value):
        try:
            try:
                self.value_widget[value].iconPropertiesShow.disconnect(self.showItemInIfBranchProperties)
                self.value_widget[value].iconPropertiesShow.connect(self.showItemInIfBranchProperties)
            except Exception:
                self.value_widget[value].iconPropertiesShow.connect(self.showItemInIfBranchProperties)
                self.value_widget[value].iconWidgetMerge.connect(self.changeValueWidget)
        except Exception:
            print("error happens in link if branch signals to structure. [main/main.py]")

    def setMenuAndShortcut(self):
        # right button menu
        self.right_button_menu = QMenu(self)

        self.close_action = QAction("Close", self.right_button_menu)
        self.close_other_action = QAction("Close Other", self.right_button_menu)
        self.close_all_action = QAction("Close All", self.right_button_menu)
        self.close_all_action.triggered.connect(self.closeAllTab)

        self.right_button_menu.addAction(self.close_action)
        self.right_button_menu.addAction(self.close_all_action)
        self.right_button_menu.addAction(self.close_other_action)
        # short cut
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(lambda: self.removeTab(self.currentIndex()))

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
        except Exception as e:
            print(f"error {e} happens in get timeline attribute. [iconTabs/main.py]")

    def showTimelineAttributes(self, tab_index):
        widget = self.widget(tab_index)
        if isinstance(widget, Timeline):
            self.attributesShow.emit(widget.value)

    def showProperties(self, current_index):
        try:
            widget = self.widget(current_index)
            if hasattr(widget, 'getInfo'):
                self.propertiesShow.emit(widget.getInfo())
            elif hasattr(widget, 'getProperties'):
                self.propertiesShow.emit(widget.getProperties())
            else:
                self.propertiesShow.emit({"error" : "can't get properties"})
        except Exception as e:
            print(f"error {e} happens in show properties. [iconTabs/main.py]")

    def openTab(self, value, name, can_open=True):
        try:
            widget_type = value.split('.')[0]
            if value in self.value_widget:
                widget = self.value_widget[value]
                tab_index = self.indexOf(widget)
                if tab_index != -1:
                    self.setCurrentIndex(tab_index)
                else:
                    tab_icon = getImage(widget_type, "icon")
                    self.setCurrentIndex(self.addTab(widget, tab_icon, name))
                # 我在cycle中生成timeline时, 就已经生成了timeline实体
                if value.startswith("Timeline."):
                    self.attributesShow.emit(value)

            else:
                widget = None
                tab_icon = getImage(widget_type, "icon")
                # 生成相应widget
                if widget_type == "Cycle":
                    widget = Cycle(value=value)
                elif widget_type == "Timeline":
                    widget = Timeline(value=value)
                elif widget_type == "SoundOut":
                    widget = SoundDisplay()
                elif widget_type == "Text":
                    widget = TextDisplay()
                elif widget_type == "Image":
                    widget = ImageDisplay()
                elif widget_type == "Video":
                    widget = VideoDisplay()
                elif widget_type == "Close":
                    widget = Close()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Action":
                    widget = EyeAction()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Calibration":
                    widget = EyeCalibrate()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "EndR":
                    widget = EndR()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Open":
                    widget = Open()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "DC":
                    widget = EyeDC()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "StartR":
                    widget = StartR()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestInit":
                    widget = QuestInit()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestUpdate":
                    widget = QuestUpdate()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestGetValue":
                    widget = QuestGetValue()
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "If_else":
                    widget = IfBranch(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Switch":
                    widget = SwitchBranch()
                    widget.tabClose.connect(self.closeTab)
                else:
                    pass

                if widget:
                    # 新生成widget放入字典
                    self.value_widget[value] = widget
                    if widget_type == 'Cycle':
                        self.cycleAdd.emit(value)
                    elif widget_type == "If_else":
                        self.ifBranchAdd.emit(value)
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
        except Exception as e:
            print("error {} happens in open tab. [iconTabs/main.py]".format(e))

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
        except Exception as e:
            properties = {"error": "can't get properties"}
            print("error {} happens in get properties. [iconTabs/main.py]".format(e))

        self.propertiesShow.emit(properties)

    def getChangedProperties(self, properties):
        self.propertiesShow.emit(properties)

    def changeTabName(self, parent_value, value, name):
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

    def changeTimelineName(self, parent_value, value, name):
        try:
            cycle = self.value_widget[parent_value]
            cycle.changeTimelineName(value, name)
        except Exception as e:
            print("error {} happens in change timeline name. [iconTabs/main.py]".format(e))

    def deleteItemInIfBranch(self, parent_value, value):
        try:
            if_branch = self.value_widget[parent_value]
            if_branch.deleteItem(value)
        except Exception as e:
            print("error {} happens in delete condition item. [iconTabs/main.py]".format(e))

    def changeItemInIfBranchName(self, parent_value, value, name):
        try:
            if_branch = self.value_widget[parent_value]
            if_branch.changeItemName(value, name)
        except Exception as e:
            print("error {} happens in change condition item name. [iconTabs/main.py]".format(e))

    def showItemInIfBranchProperties(self, properties):
        self.propertiesShow.emit(properties)

    def createTabForItemInIfBranch(self, parent_value, name,  pixmap, value, properties_window):
        try:
            self.openTab(value, name, False)
            widget = self.value_widget[value]
            if value.startswith('Video'):
                widget.pro = properties_window
                widget.pro.ok_bt.clicked.connect(widget.ok)
                widget.pro.cancel_bt.clicked.connect(widget.pro.close)
                widget.pro.apply_bt.clicked.connect(widget.apply)
            elif value.startswith('SoundOut'):
                widget.pro = properties_window
                widget.pro.ok_bt.clicked.connect(widget.ok)
                widget.pro.cancel_bt.clicked.connect(widget.pro.close)
                widget.pro.apply_bt.clicked.connect(widget.apply)
            elif value.startswith('Text'):
                widget.pro = properties_window
                widget.pro.ok_bt.clicked.connect(widget.ok)
                widget.pro.cancel_bt.clicked.connect(widget.pro.close)
                widget.pro.apply_bt.clicked.connect(widget.apply)
            elif value.startswith('Image'):
                widget.pro = properties_window
                widget.pro.ok_bt.clicked.connect(widget.ok)
                widget.pro.cancel_bt.clicked.connect(widget.pro.close)
                widget.pro.apply_bt.clicked.connect(widget.apply)
        except Exception as e:
            print("error {} happens in create tab for item in if branch.[iconTabs/main.py]".format(e))

    def closeTab(self, widget=None, index=-1):
        try:
            if widget and index == -1:
                tab_index = self.indexOf(widget)
                if tab_index != -1:
                    self.removeTab(tab_index)
            elif index != -1 and not widget:
                self.removeTab(index)
        except Exception as e:
            print(f"error {e} happens in close tab.")

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
            print(f"error {e} happen in delete icon in timeLine. [iconTabs/main.py]")

    def changeIconName(self, parent_value, value, name):
        try:
            timeline = self.value_widget[parent_value]
            timeline.changeIconName(value, name)
        except Exception as e:
            print("error {} happens in change icon name. [iconTabs/main.py]".format(e))

    def copyIcon(self, old_value, new_value, text):
        try:
            self.value_parent[new_value] = self.value_parent[old_value]
            # cycle 不能使用 deepcopy
            if old_value in self.value_widget:
                self.openTab(new_value, text, False)
                self.copyWidget(old_value, new_value)
        except Exception:
            print("some errors happen in copy icon. [iconTabs/main.py]")

    def changeValueWidget(self, value, exist_value):
        try:
            # 先删除旧的widget
            self.deleteTab(value)
            if exist_value in self.value_widget:
                self.value_widget[value] = self.value_widget[exist_value]
            else:
                self.openTab(exist_value, '', False)
                self.value_widget[value] = self.value_widget[exist_value]
        except Exception as e:
            print(f"error {e} happens in change value widget. [iconTabs/main.py]")

    def copyWidget(self, old_value, new_value):
        try:
            old_widget = self.value_widget[old_value]
            widget_type = old_value.split('.')[0]
            try:
                # ToDo 各个widget的复制, 在各个widget的内部实现
                print(f"I am copying {widget_type} widget.")
                self.value_widget[new_value] = old_widget.copy(new_value)
            except Exception:
                pass
        except Exception as e:
            print("error {} happens in copy widget. [iconTabs/main.py]".format(e))

    def contextMenuEvent(self, e):
        try:
            tab_index = self.tabBar().tabAt(e.pos())
            if tab_index != -1:
                self.close_action.disconnect()
                self.close_action.triggered.connect(lambda: self.closeTab(index=tab_index))
                self.close_other_action.disconnect()
                self.close_other_action.triggered.connect(lambda: self.closeOtherTab(index=tab_index))
                self.right_button_menu.exec(self.mapToGlobal(e.pos()))
        except Exception:
            print("error happens in showing tab bar right button menu. [iconTabs/main.py]")

    def closeAllTab(self):
        for i in range(0, self.count()):
            self.removeTab(0)

    def closeOtherTab(self, index):
        for i in range(index + 1, self.count()):
            self.removeTab(index + 1)
        for i in range(0, index):
            self.removeTab(0)
