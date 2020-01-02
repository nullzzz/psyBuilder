from PyQt5.QtWidgets import QGridLayout

from lib import TabItemWidget
from .icon_bar import IconBar
from .timeline_area import TimelineArea


class Timeline(TabItemWidget):
    """
    timeline widget: 1. icon bar to choose item
                     2. area to place item, and this area is graphics view.
    """

    def __init__(self, widget_id: int, widget_name: str):
        super(Timeline, self).__init__(widget_id, widget_name)
        # set its icon bar and timeline area
        self.icon_bar = IconBar()
        self.timeline_area = TimelineArea()
        # set its layout
        grid = QGridLayout(self)
        grid.addWidget(self.icon_bar, 0, 0, 1, 1)
        grid.addWidget(self.timeline_area, 1, 0, 1, 1)
        self.setLayout(grid)

        # todo delete test
        for i in range(1):
            self.addItem(0, i, "timeline_0", i)

    def addItem(self, widget_type: int = None, widget_id: int = None, widget_name: str = None, index: int = None):
        """
        add timeline item into its timeline area
        @param widget_type: item's type
        @param widget_id: item' widget id, if it's provided, we need to generate a new one through its widget type
        @param widget_name: like widget id above
        @param index: the index of the item
        @return:
        """
        # I think it should be left to timeline area
        self.timeline_area.addItem(widget_type, widget_id, widget_name, index)
        # refresh its ui
        self.update()

    def deleteItem(self, widget_id: int):
        """
        delete timeline item in its timeline area through item's widget id
        @param widget_id: item's widget id
        @return:
        """
        # I think it should be left to timeline area
        self.timeline_area.deleteItem(widget_id)

    def itemCount(self):
        """
        the num of timeline items
        @return:
        """
