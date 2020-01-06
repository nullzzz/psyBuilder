from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout

from app.info import Info
from lib import TabItemWidget
from .icon_bar import IconBar
from .timeline_area import TimelineArea
from .timeline_item import TimelineItem
from .timeline_name_item import TimelineNameItem


class Timeline(TabItemWidget):
    """
    timeline widget: 1. icon bar to choose item
                     2. area to place item, and this area is graphics view.
    """

    # when item's name changed, emit its widget id. (Info.TimelineSignal, widget_id, new_text)
    itemNameChanged = pyqtSignal(int, int, str)
    # when item clicked, emit its widget id. (widget_id)
    itemClicked = pyqtSignal(int)
    itemDoubleClicked = pyqtSignal(int)

    def __init__(self, widget_id: int, widget_name: str):
        super(Timeline, self).__init__(widget_id, widget_name)
        # set its qss id
        self.setObjectName("Timeline")
        # set its icon bar and timeline area
        self.icon_bar = IconBar()
        self.timeline_area = TimelineArea(self)
        # set its layout
        grid = QGridLayout(self)
        grid.addWidget(self.icon_bar, 0, 0, 1, 1)
        grid.addWidget(self.timeline_area, 1, 0, 1, 1)
        self.setLayout(grid)

        # link signals
        self.linkSignals()

    def linkSignals(self) -> None:
        """
        link signals
        @return:
        """
        self.timeline_area.itemNameChanged.connect(
            lambda widget_id, text: self.itemNameChanged.emit(Info.TimelineSignal, widget_id, text))

    def addItem(self, widget_type: int = None, widget_id: int = None, widget_name: str = None, index: int = 0):
        """
        add timeline item into its timeline area
        @param widget_type: item's type
        @param widget_id: item' widget id, if it's provided, we need to generate a new one through its widget type
        @param widget_name: like widget id above
        @param index: the index of the item
        @return:
        """
        # generate a timeline item and timeline name item
        timeline_item = TimelineItem(widget_type, widget_id)
        timeline_name_item = TimelineNameItem(timeline_item.widget_type, timeline_item.widget_id, widget_name)
        # bind timeline name item to timeline item
        timeline_item.timeline_name_item = timeline_name_item
        # link items' signals
        timeline_item.clicked.connect(lambda widget_id: self.itemClicked.emit(widget_id))
        timeline_item.doubleClicked.connect(lambda widget_id: self.itemDoubleClicked.emit(widget_id))
        # later work should be left to timeline table
        self.timeline_area.addItem(timeline_item, timeline_name_item, index)
        # refresh its ui
        self.update()
        # return valid widget_id, widget_name
        return timeline_item.widget_id, timeline_name_item.text()

    def deleteItem(self, widget_id: int):
        """
        delete timeline item in its timeline area through item's widget id
        @param widget_id: item's widget id
        @return:
        """
        # it should be left to timeline area
        self.timeline_area.deleteItem(widget_id)

    def itemCount(self):
        """
        the num of timeline items
        @return:
        """
