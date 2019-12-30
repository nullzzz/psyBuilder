from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsWidget, QGraphicsAnchorLayout

from app.info import Info
from .timeline_item import TimelineItem


class TimelineScene(QGraphicsScene):
    def __init__(self):
        super(TimelineScene, self).__init__(None)
        # data
        self.item_count = 0
        # set container to set layout
        self.container = QGraphicsWidget(None, Qt.Widget)
        self.container.setPos(0, 0)
        # set container's layout
        self.layout = QGraphicsAnchorLayout()
        self.container.setLayout(self.layout)
        # add container to scene
        self.addItem(self.container)

    def addTimelineItem(self, item: TimelineItem, index: int) -> None:
        """
        add timeline item in this scene
        @param item:
        @param index: the index of item which starts from 0
        @return:
        """

    def deleteTimelineItem(self, index: int) -> None:
        """
        delete timeline item in this scene
        @param index: the index of item which starts from 0
        @return:
        """


class TimelineArea(QGraphicsView):
    """

    """

    def __init__(self, parent=None):
        super(TimelineArea, self).__init__(parent)

        # scene is the real place to put items
        self.scene = TimelineScene()
        self.setScene(self.scene)
        # view is a widget to contain scene
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def addTimelineItem(self, widget_type: int = None, widget_id: int = None, index: int = 0) -> None:
        """
        add timeline item into timeline
        @param widget_type: item add_type.
        @param widget_id: if id is provided, we don't need to create new one.
        @param index: index of item
        @return:
        """
        # create new item
        timeline_item = TimelineItem(widget_type=widget_type, widget_id=widget_id)
        # todo add it into scene
        self.scene.addTimelineItem(timeline_item, index)

    def deleteTimelineItem(self, index: int):
        """
        delete in this area
        @param index:
        @return:
        """

    def itemCount(self) -> int:
        """
        count of items
        @return:
        """
        return self.scene.item_count

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
