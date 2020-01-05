from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from app.info import Info
from .timeline_table import TimelineTable


class TimelineArea(QFrame):
    """

    """

    def __init__(self, parent):
        super(TimelineArea, self).__init__(parent)
        # set its qss id
        self.setObjectName("TimelineArea")
        # timeline table
        self.timeline_table = TimelineTable()
        # set its layout
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.timeline_table, 1)
        layout.addStretch(1)
        self.setLayout(layout)
        # accept drops
        self.setAcceptDrops(True)

    def addItem(self, timeline_item, timeline_name_item, index: int):
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return:
        """
        # left work to timeline table
        self.timeline_table.addItem(timeline_item, timeline_name_item, index)

    def deleteItem(self, widget_id: int):
        """
        delete item in timeline table but I left it to timeline table
        @param widget_id:
        @return:
        """
        self.timeline_table.deleteItem(widget_id)

    def dragEnterEvent(self, e):
        """

        @param e:
        @return:
        """
        data_format = e.mimeData().formats()[0]
        if data_format == Info.IconBarToTimeline:
            # drag from icon bar
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """

        @param e:
        @return:
        """
        # get x
        x = e.pos().x()
        # item animation
        self.timeline_table.moveItemAnimation(x)

    def dragLeaveEvent(self, e):
        """

        @param e:
        @return:
        """
        # reset
        self.timeline_table.resetAlignment()
        e.ignore()

    def dropEvent(self, e):
        """

        @param e:
        @return:
        """
        # reset
        self.timeline_table.resetAlignment()
        # data format
        data_format = e.mimeData().formats()[0]
        data = e.mimeData().data(data_format)
        if data_format == Info.IconBarToTimeline:
            # simply add a item in timeline
            stream = QDataStream(data, QIODevice.ReadOnly)
            widget_type = stream.readInt()
            self.parent().addItem(widget_type=widget_type, index=self.timeline_table.columnAt(e.pos().x()))
            # accept
            e.accept()
        else:
            e.ignore()
