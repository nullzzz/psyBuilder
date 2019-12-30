from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDockWidget, QMainWindow

from app.func import Func
from app.info import Info
from app.kernel import Kernel
from lib import DockWidget, TabWidget


class Center(QMainWindow):
    """

    """
    # when current widget change, emit this to refresh. (widget_id -> main)
    currentWidgetChange = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # can't be closed
        # self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        # set tab widget as its main widget
        self.tab_widget = TabWidget()
        # self.setWidget(self.tab_widget)
        self.setCentralWidget(self.tab_widget)
        # link signals
        self.linkSignals()

    def linkSignals(self) -> None:
        """
        link necessary signals
        @return:
        """
        self.tab_widget.currentChanged.connect(self.dealTabChange)

    def openTab(self, widget_id: int) -> None:
        """
        open widget as tab according to its widget_id
        @param widget_id:
        @return:
        """
        # open widget as a tab in tab widget
        # first, we should ensure this widget has been created
        if widget_id in Kernel.Widgets:
            # this widget may have been opened in tab widget
            widget_type = Info.WidgetType[widget_id // Info.MaxWidgetCount]
            widget = Kernel.Widgets[widget_id]
            self.tab_widget.openTab(widget, widget_type, widget.widget_name)

    def closeTab(self, widget_id: int) -> None:
        """
        close widget in tab widget
        @param widget_id:
        @return:
        """
        widget = Kernel.Widgets[widget_id]
        self.tab_widget.closeTab(widget)

    def changeTabName(self, widget_id: int, widget_name: str) -> None:
        """
        if widget's was changed, its tab name should be changed as well.
        @param widget_id:
        @param widget_name: new widget's name
        @return:
        """
        widget = Kernel.Widgets[widget_id]
        self.tab_widget.changeTabName(widget, widget_name)

    def initInitialTimeline(self):
        """
        init initial timeline for other items
        @return:
        """
        widget_id = Func.generateWidgetId(Info.Timeline)
        widget_name = f"{Info.WidgetType[Info.Timeline]}.0"
        # create timeline widget
        Func.createWidget(widget_id, widget_name)
        # set it as tab
        self.openTab(widget_id)

    def dealTabChange(self, index: int):
        """
        when tab current tab change, we need to emit signal to refresh other docks.
        @param index:
        @return:
        """
        # if close all tab, index will be -1
        if index != -1:
            # emit currentWidgetChange signal to refresh other docks.
            widget = self.tab_widget.widget(index)
            self.currentWidgetChange.emit(widget.widget_id)
