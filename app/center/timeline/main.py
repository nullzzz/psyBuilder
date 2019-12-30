from PyQt5.QtWidgets import QGridLayout

from lib import TabItemWidget
from .timeline_area import TimelineArea
from .timeline_bar import WidgetIconBar


class TimelineWidget(TabItemWidget):
    def __init__(self, widget_id: int, widget_name: str):
        super(TimelineWidget, self).__init__(widget_id, widget_name)
        # widget icon bar
        self.widget_icon_bar = WidgetIconBar()
        # timeline area
        self.timeline_area = TimelineArea()
        # set layout
        grid = QGridLayout(self)
        grid.addWidget(self.widget_icon_bar, 0, 0, 1, 1)
        grid.addWidget(self.timeline_area, 1, 0, 1, 1)
        self.setLayout(grid)

    def itemCount(self) -> int:
        """
        count of items
        :return:
        """
        return self.timeline_area.itemCount()

    def addItem(self, widget_type: str = None, widget_id: int = None, widget_name: str = None):
        """
        @p@return widget_type: 
        @p@return widget_id: 
        @p@return widget_name: 
        @return: 
        """
