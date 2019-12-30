from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsLayoutItem

from app.func import Func
from app.info import Info


class TimelineItem(QGraphicsLayoutItem):
    """
    it is widget_type item in timeline.
    """

    def __init__(self, parent=None, widget_type: int = None, widget_id: int = None, widget_name: str = ""):
        """
        init item
        :param parent:
        :param widget_type: its widget add_type, such as timeline
        :param widget_id: if widget_id has provided, we don't need to generate a new widget_id
        :param widget_name: like widget_id above.
        """
        super(TimelineItem, self).__init__(parent)
        # if widget_id/widget_name has provided
        self.widget_id = widget_id
        self.widget_name = widget_name
        # if not, we need to generate a new widget_id/widget_name
        if not self.widget_id:
            self.widget_id = Func.generateWidgetId(widget_type)
        if not self.widget_name:
            self.widget_name = Func.generateWidgetName(widget_type)
        # select its widget_type according to its widget type.
        self.pixmap_item = QGraphicsPixmapItem()
        self.pixmap_item.setPixmap(Func.getImage(f"widgets/{Info.WidgetType[widget_type]}"))
        self.setGraphicsItem(self.pixmap_item)
