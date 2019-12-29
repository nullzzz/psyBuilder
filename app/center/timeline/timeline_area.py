from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene

from app.info import Info
from .timeline_item_widget import TimelineItemWidget


class TimelineView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene):
        super(TimelineView, self).__init__(scene)

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


class TimelineArea(QMainWindow):
    """

    """

    def __init__(self, parent=None):
        super(TimelineArea, self).__init__(parent)

        # scene is the real place to put items
        self.scene = QGraphicsScene()
        # view is a widget to contain scene
        self.view = TimelineView(self.scene)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        # embed scene into this widget.
        self.setCentralWidget(self.view)
        # set it can drop
        self.setAcceptDrops(True)

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
