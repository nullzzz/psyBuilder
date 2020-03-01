from PyQt5.QtCore import QDataStream, QIODevice, pyqtSignal, QByteArray
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from app.func import Func
from app.info import Info
from .timeline_table import TimelineTable


class TimelineArea(QFrame):
    """

    """

    # item clicked and double clicked (widget_id)
    itemClicked = pyqtSignal(str)
    itemDoubleClicked = pyqtSignal(str)
    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(str, str)
    # item add, emit signal (widget_id, widget_name, index)
    itemAdded = pyqtSignal(str, str, int)
    # item copied, emit signal (origin_widget_id, new_widget_id, new_widget_name, index)
    itemCopied = pyqtSignal(str, str, str, int)
    # item referenced, emit signal (origin_widget_id, new_widget_id, index)
    itemReferenced = pyqtSignal(str, str, int)
    # item move, emit signal(origin_timeline, widget_id, origin index, new index)
    itemMoved = pyqtSignal(str, str, int, int)
    # item delete, emit signal(widget_id)
    itemDeleted = pyqtSignal(str)

    def __init__(self, parent):
        super(TimelineArea, self).__init__(parent)
        # timeline table
        self.timeline_table = TimelineTable()
        # set its qss id
        self.setObjectName("TimelineArea")
        # set its layout
        layout = QVBoxLayout()
        layout.addWidget(self.timeline_table, 1)
        self.setLayout(layout)
        # accept drops
        self.setAcceptDrops(True)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """

        @return:
        """
        self.timeline_table.itemClicked.connect(lambda widget_id: self.itemClicked.emit(widget_id))
        self.timeline_table.itemDoubleClicked.connect(lambda widget_id: self.itemDoubleClicked.emit(widget_id))
        self.timeline_table.itemNameChanged.connect(lambda widget_id, text: self.itemNameChanged.emit(widget_id, text))
        self.timeline_table.itemDeleted.connect(lambda widget_id: self.itemDeleted.emit(widget_id))

    def addItem(self, widget_type: str = None, widget_id: str = None, widget_name: str = None, index: int = 0) -> (
            str, str, int):
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return: final add index
        """
        # left work to timeline table
        return self.timeline_table.addItem(widget_type, widget_id, widget_name, index)

    def deleteItem(self, widget_id: str):
        """
        delete item in timeline table but I left it to timeline table
        @param widget_id:
        @return:
        """
        self.timeline_table.deleteItem(widget_id)

    def moveItem(self, origin_index: int, dest_index: int) -> (str, int):
        """
        remove item
        return: widget id and new index
        """
        return self.timeline_table.moveItem(origin_index, dest_index)

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
        return self.timeline_table.itemWidgetId(widget_name)

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
            e.accept()
        elif data_format == Info.StructureMoveToTimeline or data_format == Info.StructureReferToTimeline:
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
            self.handleAddDrag(data, index)
            # accept
            e.accept()
        elif data_format == Info.MoveInTimeline:
            # move item in timeline, we have deleted item above, now we add item.
            self.handleMoveDrag(data, index)
            # accept
            e.accept()
        elif data_format == Info.CopyInTimeline:
            # copy item in timeline
            self.handleCopyDrag(data, index)
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

    def handleAddDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
        # simply add a item in timeline
        stream = QDataStream(data, QIODevice.ReadOnly)
        widget_type = stream.readQString()
        widget_id, widget_name, index = self.addItem(widget_type=widget_type, index=index)
        # emit signal
        self.itemAdded.emit(widget_id, widget_name, index)

    def handleMoveDrag(self, data: QByteArray, dest_index: int):
        """

        """
        # emit signal
        stream = QDataStream(data, QIODevice.ReadOnly)
        origin_index = stream.readInt()
        if dest_index != origin_index:
            # move item
            widget_id, dest_index = self.moveItem(origin_index, dest_index)
            self.itemMoved.emit(self.parent().widget_id, widget_id, origin_index, dest_index)

    def handleCopyDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
        # simply add a item in timeline
        stream = QDataStream(data, QIODevice.ReadOnly)
        origin_widget_id = stream.readQString()
        widget_type = Func.getWidgetType(origin_widget_id)
        new_widget_id, new_widget_name, index = self.addItem(widget_type=widget_type, index=index)
        # emit signal
        self.itemCopied.emit(origin_widget_id, new_widget_id, new_widget_name, index)

    def handleReferDrag(self, data: QByteArray, index: int):
        """

        @param data:
        @param index:
        @return:
        """
