from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTabWidget, QTabBar, QShortcut

from app.func import Func
from app.info import Info
from .events.cycle.main import Cycle
from .timeline.main import Timeline


class WidgetTabs(QTabWidget):
    # 当前tab变化时，properties要跟随变化 (widget_id -> properties)
    tabChange = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WidgetTabs, self).__init__(parent)
        # 美化
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabBar().setShape(QTabBar.TriangularNorth)
        self.tabBar().setUsesScrollButtons(True)

        # 初始化, 首页是一个timeline
        self.timeline = Timeline(widget_id=f"{Info.TIMELINE}.0")
        Info.WID_WIDGET[f"{Info.TIMELINE}.0"] = self.timeline
        self.addTab(self.timeline, Func.getWidgetImage(Info.TIMELINE, 'icon'), Info.TIMELINE)
        #
        self.setMenuAndShortcut()
        #
        self.linkSignals()

    def linkSignals(self):
        # 关闭tab
        self.tabCloseRequested.connect(self.removeTab)
        # 当前tab变化会引起：attributes和properties的变化
        self.currentChanged.connect(self.showProperties)

    def linkWidgetSignals(self, widget_id):
        # 通用信号
        pass
        # 特有信号
        widget_type = widget_id.split('.')[0]
        if widget_type == Info.TIMELINE:
            self.linkTimelineSignals(widget_id)
        elif widget_type == Info.CYCLE:
            self.linkCycleSignals(widget_id)
        elif widget_type in (
                Info.ACTION, Info.CALIBRATION, Info.CLOSE, Info.DC, Info.ENDR, Info.OPEN, Info.STARTR,
                Info.QUEST_GET_VALUE,
                Info.QUEST_INIT, Info.QUEST_UPDATE, Info.IF, Info.SWITCH):
            widget = Info.WID_WIDGET[widget_id]
            widget.tabClose.connect(self.closeTab)

    def linkTimelineSignals(self, widget_id):
        try:
            timeline: Timeline = Info.WID_WIDGET[widget_id]
            # 测试是否已经连接
            try:
                timeline.widget_icon_area.widget_icon_table.widgetOpen.disconnect(self.openWidget)
                timeline.widget_icon_area.widget_icon_table.widgetOpen.connect(self.openWidget)
            except Exception:
                timeline.widget_icon_area.widget_icon_table.widgetOpen.connect(self.openWidget)
                timeline.widget_icon_area.widget_icon_table.widgetIconNameChange.connect(self.changeTabName)
                timeline.widget_icon_area.widget_icon_table.widgetIconDelete.connect(self.closeTab)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [widget_tabs/main.py]")

    def linkCycleSignals(self, widget_id):
        try:
            cycle: Cycle = Info.WID_WIDGET[widget_id]
            try:
                pass
            except Exception:
                pass
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [main/main.py]")

    def setMenuAndShortcut(self):
        # ctrl + w 关闭当前页
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(lambda: self.removeTab(self.currentIndex()))

    # 只负责打开某个widget，该tab必须已经被创建
    def openWidget(self, widget_id: str):
        try:
            if widget_id in Info.WID_WIDGET:
                widget = Info.WID_WIDGET[widget_id]
                index = self.indexOf(widget)
                if index != -1:
                    self.setCurrentIndex(index)
                else:
                    self.setCurrentIndex(
                        self.addTab(widget, Func.getWidgetImage(widget_id.split('.')[0], 'icon'),
                                    Func.getWidgetName(widget_id)))
            else:
                raise Exception("fail to open tab, because widget can't be found. [widget_tabs/main.py]")
        except Exception as e:
            print(f"error {e} happens in open tab. [widget_tabs/main.py]")

    # 如果某个icon或node被删除，要关闭
    def closeTab(self, widget_id):
        try:
            if widget_id in Info.WID_WIDGET:
                index = self.indexOf(Info.WID_WIDGET[widget_id])
                if index != -1:
                    self.removeTab(index)
            else:
                for i in range(self.count()):
                    if widget_id == self.widget(i).widget_id:
                        self.removeTab(i)
        except Exception as e:
            print(f"error {e} happens in close tab. [widget_tabs/main.py]")

    # 如果icon修改或者structure中node修改，要同步修改
    def changeTabName(self, widget_id, widget_name):
        try:
            index = self.indexOf(Info.WID_WIDGET[widget_id])
            if index != -1:
                self.setTabText(index, widget_name)
        except Exception as e:
            print(f"error {e} happens in change tab name. [widget_tabs/main.py]")

    def showProperties(self, index):
        try:
            if index != -1:
                widget = self.widget(index)
                self.tabChange.emit(widget.widget_id)
        except Exception as e:
            print(f"error {e} happens in show properties. [widget_tabs/main.py]")
