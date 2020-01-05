from PyQt5.QtCore import QSize, Qt, pyqtSignal, QMimeData, QDataStream, QIODevice, QByteArray, QPoint
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QLabel

from app.func import Func
from app.info import Info


class TimelineItem(QLabel):
    """
    it is widget_type item in timeline.
    """

    # when item clicked, emit its widget id
    clicked = pyqtSignal(int)

    def __init__(self, widget_type: int = None, widget_id: int = None):
        """
        init item
        @param parent:
        @param widget_type: its widget add_type, such as timeline
        @param widget_id: if widget_id has provided, we don't need to generate a new widget_id
        @param widget_name: like widget_id above.
        """
        super(TimelineItem, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineItem")
        # bind timeline name item to it
        self.timeline_name_item = None
        # set data
        self.widget_id = widget_id
        self.widget_type = widget_type
        # if widget_id has provided, widget type may be not provided
        if not widget_type:
            if not widget_id:
                exit()
            self.widget_type = self.widget_id // Info.MaxWidgetCount
        # if not, we need to generate a new widget_id
        if not self.widget_id:
            self.widget_id = Func.generateWidgetId(widget_type)
        # select its widget_type according to its widget type.
        pixmap = Func.getImage(f"widgets/{Info.WidgetType[self.widget_type]}", size=QSize(50, 50))
        # set its pixmap
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)

    def mouseDoubleClickEvent(self, e):
        super(TimelineItem, self).mouseDoubleClickEvent(e)
        self.clicked.emit(self.widget_id)

    def setWidgetId(self, widget_id: int):
        """
        change its widget if
        @param widget_id:
        @return:
        """
        self.widget_id = widget_id

    def mouseMoveEvent(self, e):
        """

        @param e:
        @return:
        """
        if e.modifiers() == Qt.ControlModifier:
            # copy timeline item
            self.copyDrag()
        else:
            # move timeline item
            self.moveDrag()

    def moveDrag(self):
        """
        move widget in this timeline
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(self.timeline_name_item.column())
        mime_data = QMimeData()
        mime_data.setData(Info.MoveInTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(25, 25))
        drag.setPixmap(Func.getImage(f"widgets/{Info.WidgetType[self.widget_type]}", size=QSize(50, 50)))
        drag.exec()

    def copyDrag(self):
        """
        copy widget in this timeline
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeInt(self.widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.CopyInTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(25, 25))
        drag.setPixmap(Func.getImage(f"widgets/{Info.WidgetType[self.widget_type]}", size=QSize(50, 50)))
        drag.exec()
