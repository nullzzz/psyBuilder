from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene

from .timeline_item_widget import TimelineItemWidget


class TimelineArea(QMainWindow):
    """

    """

    def __init__(self, parent=None):
        super(TimelineArea, self).__init__(parent)

        # scene is the real place to put items
        self.scene = QGraphicsScene()
        # view is a widget to contain scene
        self.view = QGraphicsView(self.scene)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        # embed scene into this widget.
        self.setCentralWidget(self.view)

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
