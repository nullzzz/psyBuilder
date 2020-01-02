from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsGridLayout, QGraphicsWidget

from ..timeline_item import TimelineItem


class TimelineScene(QGraphicsScene):
    """
    real place to place items
    """

    def __init__(self):
        super(TimelineScene, self).__init__(None)
        # layout
        self.layout = QGraphicsGridLayout()
        self.layout.setRowFixedHeight(0, 100)
        # set a container widget to set layout
        self.container = QGraphicsWidget(None, Qt.Widget)
        self.container.setObjectName("Test")
        # set container's pos, namely top left.
        self.container.setPos(0, 0)
        self.container.setLayout(self.layout)
        # add container to itself
        self.addItem(self.container)

    def addTimelineItem(self, timeline_item: TimelineItem, index: int):
        """
        add a item in its layout
        @param timeline_item:
        @param index:
        @return:
        """
        # add timeline item
        col = index * 2 + 1
        self.layout.setColumnFixedWidth(col, 100)
        self.layout.addItem(timeline_item, 0, col, Qt.AlignCenter)
        # add text item
        item_name = timeline_item.widget_name

    def deleteTimelineItem(self, index: int):
        """
        delete a item through its index
        @param index:
        @return:
        """
