from PyQt5.QtCore import QDataStream, QIODevice, pyqtSignal, Qt, QByteArray
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QScrollArea

from app.func import Func
from app.info import Info
from .timeline_table import TimelineTable


class TimelineArea(QScrollArea):
    """

    """

    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(int, str)
    # item add, emit signal (widget_id, widget_name, index)
    itemAdded = pyqtSignal(int, str, int)
    # item copied, emit signal (origin_widget_id, new_widget_id, new_widget_name, index)
    itemCopied = pyqtSignal(int, int, str, int)
    # item copied, emit signal (origin_widget_id, new_widget_id, index)
    itemReferenced = pyqtSignal(int, int, int)
    # item move, emit signal(widget_id, origin index, new index)
    itemMoved = pyqtSignal(int, int, int)
    # item delete, emit signal(widget_id)
    itemDeleted = pyqtSignal(int)

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
        layout.addWidget(self.timeline_table, 1)
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
        self.timeline_table.itemDeleted.connect(lambda widget_id: self.itemDeleted.emit(widget_id))

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

    def deleteItem(self, widget_name: str):
        """
        delete item in timeline table but I left it to timeline table
        @param widget_id:
        @return:
        """
        self.timeline_table.deleteItem(widget_name)

    def renameItem(self, origin_widget_name: str, new_widget_name: str):
        """
        change item's name.
        @param origin_widget_name:
        @param new_widget_name:
        @return:
        """
        self.timeline_table.renameItem(origin_widget_name, new_widget_name)

    def itemWidgetId(self, widget_name: str):
        """
        get item's widget id through its widget name
        @param widget_name:
        @return:
        """
        self.timeline_table.itemWidgetId(widget_name)

    def dragEnterEvent(self, e):
        """

        @param e:
        @return:
        """
        data_format = e.mimeData().formats()[0]
        data = e.mimeData().data(data_format)
        stream = QDataStream(data, QIODevice.ReadOnly)
        if data_format == Info.IconBarToTimeline or data_format == Info.CopyInTimeline or data_format == Info.StructureCopyToTimeline:
            # drag from icon bar or copy
            e.accept()
        elif data_format == Info.MoveInTimeline:
            # move item in timeline
            self.move_col = stream.readInt()
            # save widget name and widget name
            timeline_item = self.timeline_table.cellWidget(TimelineTable.item_row, self.move_col)
            self.move_widget_id = timeline_item.widget_id
            self.move_widget_name = timeline_item.timeline_name_item.text()
            # delete items
            self.timeline_table.deleteItem(self.move_widget_id)
            e.accept()
        elif data_format == Info.StructureMoveToTimeline or data_format == Info.StructureReferToTimeline:
            # get widget id
            widget_id = stream.readInt()
            self.move_col = self.timeline_table.itemExist(widget_id)
            # if exist in this timeline, it just move in timeline
            if self.move_col != -1:
                # save widget id and widget name
                timeline_item = self.timeline_table.cellWidget(TimelineTable.item_row, self.move_col)
                self.move_widget_id = timeline_item.widget_id
                self.move_widget_name = timeline_item.timeline_name_item.text()
                # delete items
                self.timeline_table.deleteItem(self.move_widget_id)
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
        self.timeline_table.startItemAnimation(x)
        e.accept()

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
        index = self.timeline_table.columnAt(e.pos().x())
        if data_format == Info.IconBarToTimeline:
            # add item in timeline simply
            self.dealAddDrag(data, index)
            # accept
            e.accept()
        elif data_format == Info.MoveInTimeline:
            # move item in timeline, we have deleted item above, now we add item.
            self.dealMoveDrag(data, index)
            # accept
            e.accept()
        elif data_format == Info.CopyInTimeline:
            # copy item in timeline
            self.dealCopyDrag(data, index)
            # accept
            e.accept()
        elif data_format == Info.StructureMoveToTimeline:
            # move item in different timeline
            if self.move_col != -1:
                # if item exist in this timeline, it just move item in timeline
                pass
            else:
                # we add item in this timeline and delete it in other timeline
                pass
            # accept
            e.accept()
        elif data_format == Info.StructureReferToTimeline:
            if self.move_col != -1:
                # if item exist in timeline, it just move item in timeline
                pass
            else:
                # we refer item in this timeline
                pass
            # accept
            e.accept()
        else:
            e.ignore()

    def dealAddDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
        # simply add a item in timeline
        stream = QDataStream(data, QIODevice.ReadOnly)
        widget_type = stream.readInt()
        widget_id, widget_name, index = self.parent().addItem(widget_type=widget_type, index=index)
        # emit signal
        self.itemAdded.emit(widget_id, widget_name, index)

    def dealMoveDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
        _, _, index = self.parent().addItem(widget_id=self.move_widget_id, widget_name=self.move_widget_name,
                                            index=index)
        # emit signal
        if index != self.move_col:
            self.itemMoved.emit(self.move_widget_id, self.move_col, index)
        # reset move data
        self.move_col = -1
        self.move_widget_id = -1
        self.move_widget_name = ""

    def dealCopyDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
        # simply add a item in timeline
        stream = QDataStream(data, QIODevice.ReadOnly)
        origin_widget_id = stream.readInt()
        widget_type = Func.getWidgetType(origin_widget_id)
        new_widget_id, new_widget_name, index = self.parent().addItem(widget_type=widget_type, index=index)
        # emit signal
        self.itemCopied.emit(origin_widget_id, new_widget_id, new_widget_name, index)

    def dealReferDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
