from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QTabWidget, QTabBar, QMenu, QShortcut, QAction

from Info import Info
from center.iconTabs.condition.switchBranch.main import SwitchBranch
from center.iconTabs.timeline.main import Timeline
from getImage import getImage
from structure.main import Structure
from .condition.ifBranch.main import IfBranch
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
    timelineAdd = pyqtSignal(str)
    switchBranchAdd = pyqtSignal(str)
    # 发送到attribute (attributes)
    attributesShow = pyqtSignal(dict)
    # 先发送到structure去copyNode (value, exist_value)
    iconNodeCopy = pyqtSignal(str, str)

    value_widget_global = {}

    def __init__(self, parent=None):
        super(IconTabs, self).__init__(parent)
        # 设置为Tab可以关闭
        self.setTabsClosable(True)
        self.setMovable(True)
        # 用一个字典存放所有tab, 每个tab有一个随机的特征值
        # 键为特征值, 值为widget
        self.value_widget = {}
        # value : parentValue, 仅仅限于timeline和其中icon
        self.value_parent = {}
        # timeline属性及父节点timeline
        self.timeline_parent = {'Timeline.10001': None}

        self.timeline = Timeline(self)
        self.timeline.attributes['subName'] = ''
        self.timeline.attributes['subNum'] = ''
        self.timeline.attributes['subSex'] = ''
        self.timeline.attributes['subAge'] = ''
        self.timeline.attributes['subHandness'] = ''
        self.timeline.attributes['sessionNum'] = ''
        self.value_widget['Timeline.10001'] = self.timeline
        Info.VALUE_WIDGET["Timeline.10001"] = self.timeline
        IconTabs.value_widget_global['Timeline.10001'] = self.timeline
        tab_icon = QIcon("image/timeLine.png")
        self.addTab(self.timeline, tab_icon, "Timeline")
        self.tabBar().setShape(QTabBar.TriangularNorth)
        self.tabBar().setUsesScrollButtons(True)
        # 右键菜单及快捷键
        self.setMenuAndShortcut()
        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # self
        self.tabCloseRequested.connect(self.restoreTab)
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.showTimelineAttributes)
        self.currentChanged.connect(self.showProperties)
        self.currentChanged.connect(self.showAttributes)
        # timeline
        self.linkTimelineSignals('Timeline.10001')
        # cycle
        self.cycleAdd.connect(self.linkCycleSignals)
        # if branch
        self.ifBranchAdd.connect(self.linkIFBranchSignals)
        # switch
        self.switchBranchAdd.connect(self.linkSwitchBranchSignals)

    def linkTimelineSignals(self, value):
        try:
            try:
                self.value_widget[value].iconAdd.disconnect(self.addIcon)
                self.value_widget[value].iconAdd.connect(self.addIcon)
            except Exception:
                self.value_widget[value].iconAdd.connect(self.addIcon)
                self.value_widget[value].iconRemove.connect(self.removeIcon)
                self.value_widget[value].iconChange.connect(self.changeIcon)
                self.value_widget[value].iconNameChange.connect(self.changeTabName)
                self.value_widget[value].icon_area.iconCopy.connect(self.copyIcon)
                self.value_widget[value].icon_area.icon_table.iconDoubleClicked.connect(self.openTab)
                self.value_widget[value].icon_area.icon_table.iconRemove.connect(self.deleteTab)
                self.value_widget[value].icon_area.icon_table.propertiesShow.connect(self.getWidgetProperties)
                self.value_widget[value].icon_area.icon_table.iconWidgetMerge.connect(self.mergeValueWidget)
                self.value_widget[value].icon_area.icon_table.iconWidgetSplit.connect(self.splitValueWidget)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [iconTabs/main.py]")

    def linkCycleSignals(self, value):
        try:
            cycle: Cycle = self.value_widget[value]
            try:
                cycle.timelineAdd.disconnect(self.addTimeline)
                cycle.timelineAdd.connect(self.addTimeline)
            except Exception:
                cycle.timelineAdd.connect(self.addTimeline)
                cycle.attributeAdd.connect(self.addTimelineAttribute)
                cycle.attributeNameChange.connect(self.changeTimelineAttributeName)
                cycle.attributeValueChange.connect(self.changeTimelineAttributeValue)
                cycle.timelineWidgetMerge.connect(self.mergeValueWidget)
                cycle.timelineWidgetSplit.connect(self.splitValueWidget)
                cycle.timelineCopyWidget.connect(self.copyWidget)
        except Exception:
            print("error happens in link cycle signals. [iconTabs\main.py]")

    def linkIFBranchSignals(self, value):
        try:
            try:
                self.value_widget[value].iconPropertiesShow.disconnect(self.showIconPropertiesInBranch)
                self.value_widget[value].iconPropertiesShow.connect(self.showIconPropertiesInBranch)
            except Exception:
                self.value_widget[value].nodeAdd.connect(self.createTabForItemInBranch)
                self.value_widget[value].iconPropertiesShow.connect(self.showIconPropertiesInBranch)
                self.value_widget[value].iconWidgetMerge.connect(self.mergeValueWidget)
                self.value_widget[value].iconWidgetSplit.connect(self.splitValueWidget)
                self.value_widget[value].iconTabDelete.connect(self.deleteTab)
        except Exception:
            print("error happens in link if branch signals. [iconTabs/main.py]")

    def linkSwitchBranchSignals(self, value):
        try:
            switch: SwitchBranch = self.value_widget[value]
            try:
                switch.iconPropertiesShow.disconnect(self.showIconPropertiesInBranch)
                switch.iconPropertiesShow.connect(self.showIconPropertiesInBranch)
            except Exception:
                switch.iconPropertiesShow.connect(self.showIconPropertiesInBranch)
                switch.caseAdd.connect(self.createTabForItemInBranch)
                switch.caseTabDelete.connect(self.deleteTab)
        except Exception as e:
            print(f"error {e} happens in link switch branch signals. [iconTabs/main.py]")

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

    def changeIcon(self, new_parent, value):
        self.value_parent[value] = new_parent

    # 单纯的保存所有timeline中的icon增减
    def removeIcon(self, parent_value, value):
        del self.value_parent[value]

    def removeInWidget(self, parent_value, value):
        try:
            widget = self.value_widget[parent_value]
            widget.removeIconSimply(value)
        except Exception as e:
            print(f"error {e} happens in remove icon in widget. [iconTabs/main.py]")

    def addTimeline(self, cycle_value, timeline_name, timeline_pixmap, timeline_value):
        try:
            # timeline 相关属性
            timeline_parent = self.value_parent[cycle_value]
            self.timeline_parent[timeline_value] = timeline_parent
            # 在此函数就去生成timeline实体
            self.openTab(timeline_value, timeline_name, False)
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
                    # 对此timeline下面对varChoose进行新增
                    values = {"If_else": [], 'Switch': []}
                    Structure.getIfAndSwitchInTimeline(timeline.value, values)
                    # if else
                    for value in values['If_else']:
                        if value in self.value_widget:
                            if_else: IfBranch = self.value_widget[value]
                            if_else.addVarComboBoxAttribute(name)
                    # switch
                    for value in values['Switch']:
                        if value in self.value_widget:
                            switch: SwitchBranch = self.value_widget[value]
                            switch.addVarComboBoxAttribute(name)
        except Exception:
            print("error happens in add new timeline attribute. [iconTabs/main.py]")

    def changeTimelineAttributeValue(self, timeline_value, attribute_name, attribute_value):
        try:
            if timeline_value in self.value_widget:
                timeline = self.value_widget[timeline_value]
                timeline.attributes[attribute_name] = attribute_value
        except Exception:
            print("error happens in change timeline attribute value. [iconTabs/main.py]")

    def changeTimelineAttributeName(self, cycle_value, old_header, new_header):
        try:
            cycle: Cycle = self.value_widget[cycle_value]
            for row in cycle.row_value:
                timeline = self.value_widget[cycle.row_value[row]]
                timeline.attributes[new_header] = timeline.attributes[old_header]
                del timeline.attributes[old_header]
                # 再修改该timeline下面的所有属性
                # 先从structure那边拿到该timeline下面的所有if和switch的value
                values = {"If_else" : [], 'Switch' : []}
                Structure.getIfAndSwitchInTimeline(timeline.value, values)
                # if else
                for value in values['If_else']:
                    if_else:IfBranch = self.value_widget[value]
                    if_else.changeVarComboBoxAttribute(old_header, new_header)
                # switch
                for value in values['Switch']:
                    switch:SwitchBranch = self.value_widget[value]
                    switch.changeVarComboBoxAttribute(old_header, new_header)
        except Exception as e:
            print(f"error {e} happens in change timeline attribute name. [iconTabs/main.py]")

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
            # self.attributesShow.emit(widget.value)
            pass

    def showProperties(self, current_index):
        try:
            widget = self.widget(current_index)
            properties = {"error": "can't get properties"}
            if hasattr(widget, 'getInfo'):
                properties = widget.getInfo()
            elif hasattr(widget, 'getProperties') or not properties:
                properties = widget.getProperties()
            if not properties:
                properties = {"error": "can't get properties"}
            self.propertiesShow.emit(properties)
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
                    # self.attributesShow.emit(value)
                    pass
            else:
                widget = None
                tab_icon = getImage(widget_type, "icon")
                # 生成相应widget
                if widget_type == "Cycle":
                    widget = Cycle(value=value)
                elif widget_type == "Timeline":
                    widget = Timeline(value=value)
                elif widget_type == "SoundOut":
                    widget = SoundDisplay(value=value)
                elif widget_type == "Text":
                    widget = TextDisplay(value=value)
                elif widget_type == "Image":
                    widget = ImageDisplay(value=value)
                elif widget_type == "Video":
                    widget = VideoDisplay(value=value)
                elif widget_type == "Close":
                    widget = Close(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Action":
                    widget = EyeAction(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Calibration":
                    widget = EyeCalibrate(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "EndR":
                    widget = EndR(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Open":
                    widget = Open(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "DC":
                    widget = EyeDC(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "StartR":
                    widget = StartR(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestInit":
                    widget = QuestInit(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestUpdate":
                    widget = QuestUpdate(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "QuestGetValue":
                    widget = QuestGetValue(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "If_else":
                    widget = IfBranch(value=value)
                    widget.tabClose.connect(self.closeTab)
                elif widget_type == "Switch":
                    widget = SwitchBranch(value=value)
                    widget.tabClose.connect(self.closeTab)
                else:
                    pass

                if widget:
                    # 新生成widget放入字典
                    self.value_widget[value] = widget
                    Info.VALUE_WIDGET[value] = widget
                    IconTabs.value_widget_global[value] = widget
                    if widget_type == 'Cycle':
                        self.cycleAdd.emit(value)
                    elif widget_type == "If_else":
                        self.ifBranchAdd.emit(value)
                    elif widget_type == 'Switch':
                        self.switchBranchAdd.emit(value)
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
            if value in self.value_widget:
                widget = self.value_widget[value]
                if hasattr(widget, "getProperties"):
                    properties = widget.getProperties()
                elif hasattr(widget, "getInfo"):
                    properties = widget.getInfo()
        except Exception as e:
            properties = {"error": "can't get properties"}
            print("error {} happens in get properties. [iconTabs/main.py]".format(e))
        if not properties:
            properties = {"error": "can't get properties"}
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

                widget = self.value_widget[value]
                del widget
                del self.value_widget[value]
                del IconTabs.value_widget_global[value]
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

    def deleteItemInSwitchBranch(self, parent_value, value):
        try:
            switch: SwitchBranch = self.value_widget[parent_value]
            switch.deleteAndClearCase(value)
        except Exception as e:
            print(f"error {e} happens in delete case. [iconTabs/main.py]")

    def changeItemInSwitchBranchName(self, parent_value, value, name):
        try:
            switch: SwitchBranch = self.value_widget[parent_value]
            switch.changeCaseName(value, name)
        except Exception as e:
            print(f"error {e} happens in change case name. [iconTabs/main.py]")

    def showIconPropertiesInBranch(self, properties):
        self.propertiesShow.emit(properties)

    def createTabForItemInBranch(self, parent_value, name, pixmap, value, properties_window):
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
            print("error {} happens in create tab for Item in if branch.[iconTabs/main.py]".format(e))

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
                    if value in self.value_widget:
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
            if old_value in self.value_widget:
                print("I am copying icon in timeline.")
                # 调用structure中的copyNode
                self.iconNodeCopy.emit(new_value, old_value)
                self.copyWidget(new_value, old_value)
        except Exception:
            print("some errors happen in copy icon. [iconTabs/main.py]")

    def mergeValueWidget(self, value, exist_value):
        try:
            # 先删除旧的widget
            print("I am merging widget.")
            self.deleteTab(value)
            if exist_value in self.value_widget:
                self.value_widget[value] = self.value_widget[exist_value]
                IconTabs.value_widget_global[value] = IconTabs.value_widget_global[value]
            else:
                self.openTab(exist_value, '', False)
                self.value_widget[value] = self.value_widget[exist_value]
                IconTabs.value_widget_global[value] = IconTabs.value_widget_global[value]
        except Exception as e:
            print(f"error {e} happens in change value widget. [iconTabs/main.py]")

    def splitValueWidget(self, value, old_exist_value):
        try:
            print("I am splitting widget.")
            if old_exist_value in self.value_widget:
                self.copyWidget(value, old_exist_value)
        except Exception as e:
            print(f"error {e} happens in split widget. [iconTabs/main.py]")

    def copyWidget(self, value: str, exist_value):
        try:
            widget_type = exist_value.split('.')[0]
            if exist_value in self.value_widget:
                print(f"I am copying {widget_type} widget.")
                old_widget = self.value_widget[exist_value]
                try:
                    if hasattr(old_widget, 'copy'):
                        self.value_widget[value] = old_widget.copy(value)
                        IconTabs.value_widget_global[value] = self.value_widget[value]
                    elif hasattr(old_widget, 'clone'):
                        self.value_widget[value] = old_widget.clone(value)
                        IconTabs.value_widget_global[value] = self.value_widget[value]
                    # 通用属性连接(propertiesChange, tabClose)
                    if not value.startswith('Timeline.'):
                        self.value_widget[value].propertiesChange.connect(self.getChangedProperties)
                    try:
                        self.value_widget[value].tabClose.connect(self.closeTab)
                    except Exception:
                        pass
                    # 特殊属性
                    if value.startswith('Cycle'):
                        self.cycleAdd.emit(value)
                    elif value.startswith('Timeline.'):
                        self.linkTimelineSignals(value)
                        self.timelineAdd.emit(value)
                    elif value.startswith('If_else'):
                        self.ifBranchAdd.emit(value)
                    elif value.startswith('Switch'):
                        self.switchBranchAdd.emit(value)
                    print(f"I have finished copying {widget_type} widget.")
                except Exception:
                    print(f"Fail to copy {widget_type} widget.")
        except Exception as e:
            print("error {} happens in copy widget. [iconTabs/main.py]".format(e))
            print(f"Fail to copy {widget_type} widget.")

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

    # todo switch
    def restoreTab(self, index):
        widget = self.widget(index)
        if isinstance(widget, IfBranch):
            widget.restoreIcons()

    def closeOtherTab(self, index):
        for i in range(index + 1, self.count()):
            self.removeTab(index + 1)
        for i in range(0, index):
            self.removeTab(0)

    def showAttributes(self, index):
        try:
            widget = self.widget(index)
            widget_value = widget.value
            # 得到attributes，并发送到attribute
            self.attributesShow.emit(IconTabs.getAttributes(widget_value))
        except Exception as e:
            print(f"error {e} happens in show attributes. [iconTabs/main.py]")

    @staticmethod
    def getAttributes(value):
        # 调用structure中静态函数获取timeline values
        values = Structure.getTimelineValues(value)
        # 通过values得到属性
        attributes = {}
        for value in values:
            for attribute in IconTabs.value_widget_global[value].attributes:
                if attribute not in attributes:
                    attributes[attribute] = IconTabs.value_widget_global[value].attributes[attribute]

        return attributes

    @staticmethod
    def checkConflictAboutVar():
        # 目前先检测if和switch里面的var comboBox
        pass
