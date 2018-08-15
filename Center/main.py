from PyQt5.QtWidgets import QDockWidget
from .iconTabs.main import IconTabs


class Center(QDockWidget):
    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # set UI
        self.icon_tabs = IconTabs(self)
        self.setWidget(self.icon_tabs)
