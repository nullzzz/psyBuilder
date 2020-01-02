from PyQt5.QtWidgets import QGraphicsView

from app.info import Info
from .timeline_scene import TimelineScene
from ..timeline_item import TimelineItem


class TimelineArea(QGraphicsView):
    """
    area to place timeline item
    """

    def __init__(self, parent=None):
        super(TimelineArea, self).__init__(parent)
        # set its scene
        self.timeline_scene = TimelineScene()
        self.setScene(self.timeline_scene)
        # set its drag mode
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def addItem(self, widget_type: int = None, widget_id: int = None, widget_name: str = None, index: int = None):
        """
        add timeline item into its scene
        @param widget_type: item's type
        @param widget_id: item' widget id, if it's provided, we need to generate a new one through its widget type
        @param widget_name: like widget id above
        @param index: the index of the item
        @return:
        """
        # generate a timeline item
        timeline_item = TimelineItem(widget_type=widget_type, widget_id=widget_id, widget_name=widget_name)
        # add it to its scene

    def deleteItem(self, widget_id: int):
        """
        delete a timeline item in its scene
        @param widget_id:
        @return:
        """
        # get item's index

        # delete item in scene through its index

    def dragEnterEvent(self, e):
        """
        drag icon into this widget, this widget just accepts several special pattern
        """
        data_format = e.mimeData().formats()[0]
        if data_format == Info.IconBarToTimeline:
            # if drag from icon bar to timeline
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """
        move icon in this widget, we don't need to justify its data format.
        in this function, we should have some feedback such as cartoon.
        """
        # todo some feedback in drag move in timeline area

    def dropEvent(self, e):
        """
        drop icon into this widget, process other procedures
        """
        # todo deal with drop event in timeline area

    def dragLeaveEvent(self, e):
        """
        drag icon leave this widget, ignore this drag
        """
        e.ignore()
