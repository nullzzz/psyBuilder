from PyQt5.QtWidgets import QGraphicsScene

from ..timeline_item import TimelineItem


class TimelineScene(QGraphicsScene):
    """
    real place to place items
    """

    def __init__(self):
        super(TimelineScene, self).__init__(None)

    def addTimelineItem(self, timeline_item: TimelineItem, index: int):
        """
        add a item in itself
        @param timeline_item:
        @param index:
        @return:
        """

    def deleteTimelineItem(self, index: int):
        """
        delete a item through its index
        @param index:
        @return:
        """
