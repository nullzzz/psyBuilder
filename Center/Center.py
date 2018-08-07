from PyQt5.QtWidgets import QDockWidget
from .EventTabs.EventTabs import EventTabs


class Center(QDockWidget):
    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # set UI
        self.eventTabs = EventTabs(self)
        self.setWidget(self.eventTabs)
