from PyQt5.QtCore import QDataStream, QIODevice, pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QScrollArea

from app.func import Func
from app.info import Info
from .timeline_table import TimelineTable


class TimelineArea(QScrollArea):
    """

    """

    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(int, str)
    # item move, emit signal(widget_id, origin index, new index)
    itemMoved = pyqtSignal(int, int, int)

    def __init__(self, parent):
        super(TimelineArea, self).__init__(parent)
        # timeline table
        self.timeline_table = TimelineTable()
        # set container
        container = QFrame()
        # set container's qss id
        container.setObjectName("TimelineArea")
        # set its layout
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.timeline_table, 1)
        layout.addStretch(1)
        container.setLayout(layout)
        # accept drops
        self.setAcceptDrops(True)
        self.setWidget(container)
        self.setAlignment(Qt.AlignCenter)
        self.setWidgetResizable(True)
        # link signals
        self.linkSignals()
        # data
        self.move_col = -1
        self.move_widget_id = -1
        self.move_widget_name = ""

    def linkSignals(self):
        """

        @return:
        """
        self.timeline_table.itemNameChanged.connect(lambda widget_id, text: self.itemNameChanged.emit(widget_id, text))

    def addItem(self, timeline_item, timeline_name_item, index: int) -> int:
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return: final add index
        """
        # left work to timeline table
        return self.timeline_table.addItem(timeline_item, timeline_name_item, index)

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
        elif data_format == Info.MoveInTimeline:
            # move in this timeline
            data = e.mimeData().data(data_format)
            stream = QDataStream(data, QIODevice.ReadOnly)
            self.move_col = stream.readInt()
            # save widget name and widget name
            timeline_item = self.timeline_table.cellWidget(0, self.move_col)
            self.move_widget_id = timeline_item.widget_id
            self.move_widget_name = timeline_item.timeline_name_item.text()
            # delete items
            self.timeline_table.deleteItem(self.move_widget_id)
            e.accept()
        elif data_format == Info.CopyInTimeline:
            # todo copy in this timeline
            print("copy")
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
        # item frame_animation
        self.timeline_table.moveItemAnimation(x)

    def dragLeaveEvent(self, e):
        """

        @param e:
        @return:
        """
        # reset
        self.timeline_table.resetAlignmentAnimation()
        # if move item, we also need reset item in timeline
        if self.move_col != -1:
            # add origin item in timeline
            self.parent().addItem(widget_id=self.move_widget_id, widget_name=self.move_widget_name, index=self.move_col)
            # reset move data
            self.move_col = -1
            self.move_widget_id = -1
            self.move_widget_name = ""
        e.ignore()

    def dropEvent(self, e):
        """

        @param e:
        @return:
        """
        # reset
        self.timeline_table.resetAlignmentAnimation()
        # data format
        data_format = e.mimeData().formats()[0]
        data = e.mimeData().data(data_format)
        if data_format == Info.IconBarToTimeline:
            # simply add a item in timeline
            stream = QDataStream(data, QIODevice.ReadOnly)
            widget_type = stream.readInt()
            index = self.timeline_table.columnAt(e.pos().x())
            widget_id, widget_name, _ = self.parent().addItem(widget_type=widget_type, index=index)
            # create widget
            self.parent().waitStart.emit()
            Func.createWidget(widget_id, widget_name)
            self.parent().waitEnd.emit()
            # accept
            e.accept()
        elif data_format == Info.MoveInTimeline:
            # add origin item in timeline
            index = self.timeline_table.columnAt(e.pos().x())
            _, _, index = self.parent().addItem(widget_id=self.move_widget_id, widget_name=self.move_widget_name,
                                                index=index)
            # emit signal
            if index != self.move_col:
                self.itemMoved.emit(self.move_widget_id, self.move_col, index)
            # reset move data
            self.move_col = -1
            self.move_widget_id = -1
            self.move_widget_name = ""
            # accept
            e.accept()
        else:
            e.ignore()
