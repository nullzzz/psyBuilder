from PyQt5.QtWidgets import QDockWidget

from .widget_tabs.main import WidgetTabs


class Center(QDockWidget):
    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # set UI
        self.widget_tabs = WidgetTabs(self)
        self.setWidget(self.widget_tabs)
