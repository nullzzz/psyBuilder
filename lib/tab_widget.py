from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTabWidget, QWidget, QShortcut, QTabBar

from app.func import Func


class TabWidget(QTabWidget):
    """
    center's main widget, it's used to contain all tab item widget.
    """
    # when current tab change, emit a signal.
    tabChange = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        # set tab can be closed, it makes me concerned.
        self.setTabsClosable(True)
        self.tabBar().setObjectName("TabWidget")
        self.tabCloseRequested.connect(self.removeTab)
        # set short and menu
        self.setMenuAndShortcut()

    def setMenuAndShortcut(self):
        """

        :return:
        """
        # close current tab
        QShortcut(QKeySequence(QKeySequence.Close), self).activated.connect(lambda: self.removeTab(self.currentIndex()))
        # switch different tab
        QShortcut(QKeySequence("Ctrl+left"), self).activated.connect(lambda: self.switchTab(1))
        QShortcut(QKeySequence("Ctrl+right"), self).activated.connect(lambda: self.switchTab(0))

    def openTab(self, widget: QWidget, widget_type: str, name: str) -> None:
        """
        open widget as a tab
        :param widget:
        :param name: widget's name
        :param widget_type: widget's icon picture path
        :return:
        """
        # widget may has been opened
        index = self.indexOf(widget)
        if index != -1:
            self.setCurrentIndex(index)
        else:
            index = self.addTab(widget, Func.getImageObject(f"widgets/{widget_type}", 1), name)
            self.setCurrentIndex(index)

    def closeTab(self, widget: QWidget) -> None:
        """
        close tab in this tab widget
        :param widget:
        :return:
        """
        index = self.indexOf(widget)
        if index != -1:
            self.removeTab(index)

    def changeTabName(self, widget: QWidget, widget_name: str):
        """
        change tab's name
        :param widget:
        :param widget_name:
        :return:
        """
        index = self.indexOf(widget)
        if index != -1:
            self.setTabText(index, widget_name)

    def switchTab(self, direct: int = 0):
        """
        change tab according to index
        0:right
        1:left
        and loop
        """
        if direct:
            index = self.currentIndex() + 1
            if index >= self.count():
                index = 0
        else:
            index = self.currentIndex() - 1
            if index < 0:
                index = self.count() - 1
        self.setCurrentIndex(index)

    def store(self) -> list:
        """
        store some opening widgets' widget_id
        :return:
        """
        return [self.widget(i).widget_id for i in range(self.count())]

    def restore(self, data: list):
        """
        restore some opening widgets
        :param data:
        :return:
        """
        for widget_id in data:
            widget = Func.getWidget(widget_id)
            widget_type = Func.getWidgetType(widget_id)
            widget_name = Func.getWidgetName(widget_id)
            self.openTab(widget, widget_type, widget_name)
        if self.count():
            self.setCurrentIndex(0)
