from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsProxyWidget, QSizePolicy, QLabel

from app.func import Func
from app.info import Info


class TimelineLabel(QLabel):
    """
    timeline label
    """

    def __init__(self, pixmap):
        super(TimelineLabel, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineLabel")
        # set its pixmap
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)


class TimelineItem(QGraphicsProxyWidget):
    """
    it is widget_type item in timeline.
    """

    # when item clicked, emit its widget id
    clicked = pyqtSignal(int)

    def __init__(self, parent=None, widget_type: int = None, widget_id: int = None, widget_name: str = ""):
        """
        init item
        @param parent:
        @param widget_type: its widget add_type, such as timeline
        @param widget_id: if widget_id has provided, we don't need to generate a new widget_id
        @param widget_name: like widget_id above.
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
        label = TimelineLabel(Func.getImage(f"widgets/{Info.WidgetType[widget_type]}", size=QSize(50, 50)))
        self.setWidget(label)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def mouseDoubleClickEvent(self, e):
        super(TimelineItem, self).mouseDoubleClickEvent(e)
        self.clicked.emit(self.widget_id)
