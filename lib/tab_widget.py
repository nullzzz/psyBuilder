from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTabWidget, QWidget, QShortcut

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
        self.tabCloseRequested.connect(self.removeTab)
        # set short and menu
        self.setMenuAndShortcut()

    def setMenuAndShortcut(self):
        """

        :return:
        """
        # close current tab
        self.close_shortcut = QShortcut(QKeySequence(QKeySequence.Close), self)
        self.close_shortcut.activated.connect(lambda: self.removeTab(self.currentIndex()))

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
            index = self.addTab(widget, Func.getImage(f"widgets/{widget_type}", 1), name)
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
