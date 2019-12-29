from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsWidget, QGraphicsAnchorLayout

from app.info import Info
from .timeline_item_widget import TimelineItemWidget


class TimelineScene(QGraphicsScene):
    def __init__(self, scene: QGraphicsScene):
        super(TimelineScene, self).__init__(scene)
        # set container to set layout
        container = QGraphicsWidget(None, Qt.Widget)
        container.setPos(0, 0)
        # set container's layout
        layout = QGraphicsAnchorLayout()
        container.setLayout(layout)
        # add container to scene
        self.addItem(container)


class TimelineArea(QGraphicsView):
    """

    """

    def __init__(self, parent=None):
        super(TimelineArea, self).__init__(parent)

        # scene is the real place to put items
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        # view is a widget to contain scene
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def addItem(self, widget_type: int = None, widget_id: int = None) -> None:
        """
        add timeline item into timeline
        :param widget_type: item add_type.
        :param widget_id: if id is provided, we don't need to create new one.
        :return:
        """
        # create new item
        timeline_item = TimelineItemWidget(widget_type=widget_type, widget_id=widget_id)
        # todo add it into scene

    def itemCount(self) -> int:
        """
        count of items
        :return:
        """
        return self.item_count

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
