from PyQt5.QtWidgets import QTabWidget, QWidget, QTabBar
from PyQt5.QtCore import pyqtSignal
from .TimeLine.TimeLine import TimeLine
from .Cycle.Cycle import Cycle
from .SoundOut.main import SoundOut
from .Textdisplay.main import TextDisplay
from .Image.imageDisplay import ImageDisplay
from .Video.videoDisplay import VideoDisplay
from .EyeTracker.close import Close
from .EyeTracker.DC import EyeDC
from .EyeTracker.open import Open
from .EyeTracker.setup import SetUp
from .EyeTracker.startR import StartR
from .EyeTracker.endR import EndR
from .Quest.start import QuestStart
from .Quest.update import QuestUpdate


class EventTabs(QTabWidget):
    properties = pyqtSignal(dict)
    cycleAdded = pyqtSignal(str)
    def __init__(self, parent=None):
        super(EventTabs, self).__init__(parent)
        # 设置为Tab可以关闭
        self.setTabsClosable(True)
        self.setMovable(True)
        # 用一个字典存放所有tab, 每个tab有一个随机的特征值
        # 键为特征值, 值为widget
        self.tabs = {}
        # value : parentValue
        self.events = {}

        self.timeLine = TimeLine(self)
        self.tabs['TimeLine.10001'] = self.timeLine
        self.addTab(self.timeLine, "TimeLine")
        self.tabBar().setShape(QTabBar.TriangularNorth)

        # 连接信号
        self.linkSignal()

    def linkSignal(self):
        # 对于event的增删
        self.timeLine.eventAdd.connect(self.addEvent)
        self.timeLine.eventRemove.connect(self.removeEvent)

        self.timeLine.eventArea.eventTable.openTab.connect(self.addNewTab)
        self.timeLine.eventArea.eventTable.eventNameChanged.connect(self.changeTabName)
        self.timeLine.eventArea.eventTable.eventRemove.connect(self.deleteTab)
        self.timeLine.eventArea.eventTable.properties.connect(self.getProperties)

        self.tabCloseRequested.connect(self.removeTab)

    # 对cycle中新增的timeLine串接信号
    def linkNewSignal(self, value):
        self.tabs[value].eventArea.eventTable.openTab.connect(self.addNewTab)
        self.tabs[value].eventArea.eventTable.eventNameChanged.connect(self.changeTabName)
        self.tabs[value].eventArea.eventTable.eventRemove.connect(self.deleteTab)
        self.tabs[value].eventArea.eventTable.properties.connect(self.getProperties)
        self.tabs[value].eventAdd.connect(self.addEvent)
        self.tabs[value].eventRemove.connect(self.removeEvent)

    # 添加新的tab, 如果存在过,直接取出, 不存在则新增
    # 新增连接信号propertiesChanged
    def addNewTab(self, value, name):
        widgetType = value.split('.')[0]
        if value in self.tabs:
            widget = self.tabs[value]
            index = self.indexOf(widget)
            if index != -1:
                self.setCurrentIndex(index)
            else:
                self.setCurrentIndex(self.addTab(widget, name))
        else:
            widget = None
            if widgetType == "Cycle":
                widget = Cycle(value=value)
            elif widgetType == "TimeLine":
                widget = TimeLine(value=value)
            elif widgetType == "SoundOut":
                widget = SoundOut()
            elif widgetType == "Text":
                widget = TextDisplay()
            elif widgetType == "Image":
                widget = ImageDisplay()
            elif widgetType == "Video":
                widget = VideoDisplay()
            elif  widgetType == "Close":
                widget = Close()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "DC":
                widget = EyeDC()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "EndR":
                widget = EndR()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "Open":
                widget = Open()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "SetUp":
                widget = SetUp()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "StartR":
                widget = StartR()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "QuestStart":
                widget = QuestStart()
                widget.closed.connect(self.closeTab)
            elif  widgetType == "QuestUpdate":
                widget = QuestUpdate()
                widget.closed.connect(self.closeTab)

            if widgetType != "TimeLine":
                widget.propertiesChanged.connect(self.getChangedProperties)

            self.tabs[value] = widget

            if widgetType == "Cycle":
                self.cycleAdded.emit(value)

            self.setCurrentIndex(self.addTab(widget, name))

    def changeTabName(self, value, name):
        if value in self.tabs:
            index = self.indexOf(self.tabs[value])
            if index != -1:
                self.setTabText(index, name)

    def openTab(self, value, name):
        if value in self.tabs:
            index = self.indexOf(self.tabs[value])
            if index != -1:
                self.setCurrentIndex(index)
            else:
                self.setCurrentIndex(self.addTab(self.tabs[value], name))
        else:
            self.addNewTab(value, name)

    def deleteTab(self, value):
        if value in self.tabs:
            index = self.indexOf(self.tabs[value])
            if index != -1:
                self.removeTab(index)
            del self.tabs[value]

    def getProperties(self, value):
        if value in self.tabs:
            widget = self.tabs[value]
            if hasattr(widget, "getProperties"):
                properties = widget.getProperties()
            elif hasattr(widget, "getInfo"):
                properties = widget.getInfo()
            else:
                properties = {"State" : "None Properties"}
        else:
            properties = {"State" : "Not Initialized"}
        self.properties.emit(properties)

    # 接收组件的properties的更新信号
    def getChangedProperties(self, properties):
        self.properties.emit(properties)

    def closeTab(self, widget):
        index = self.indexOf(widget)
        if index != -1:
            self.removeTab(index)

    def addEvent(self, parentValue, name, pixmap, value):
        self.events[value] = parentValue

    def removeEvent(self, parentValue, value):
        del self.events[value]

    def deleteEvent(self, value):
        try:
            if not value.startswith("TimeLine."):
                parentValue = self.events[value]
                timeLine = self.tabs[parentValue]
                timeLine.eventArea.eventTable.removeEvent(value)
        except Exception:
            print("Some errors happen in delete event in timeLine.")

    # 删除在cycle中的timeLine, 实质是删除其table中所在那行
    def deleteTimeLineInCycle(self, parentValue, value):
        try:
            cycle = self.tabs[parentValue]
            cycle.deleteTimeLine(value)
        except Exception:
            print("some errors happen in delete timeLine in cycle (EventTabs.py)")