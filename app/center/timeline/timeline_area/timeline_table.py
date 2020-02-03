from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidgetItem, QFrame, QLabel, QAbstractItemView, QMenu

from app.func import Func
from app.info import Info
from lib import TableWidget
from ..timeline_item import TimelineItem
from ..timeline_name_item import TimelineNameItem


class TimelineTable(TableWidget):
    """
    table to place timeline item and timeline name item
    """

    # timeline initial length of arrow
    InitialArrowLength = 10
    Height = 100
    Width = 100
    #
    top_row = 0
    item_row = 1
    arrow_row = 2
    name_row = 3

    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(int, str)

    def __init__(self):
        super(TimelineTable, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineTable")
        # hide its scroll bar
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setAutoScroll(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # hide its grid lines
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        # init table
        self.initTable()
        # data
        self.item_count = 0
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.itemChanged.connect(self.dealItemChanged)

    def setMenuAndShortcut(self):
        """
        set menu and shortcut
        @return:
        """
        self.menu = QMenu()
        # copy action
        self.copy_action = self.menu.addAction(Func.getImage("menu/copy.png", 1), "Copy", self.copyActionFunc,
                                               QKeySequence(QKeySequence.Copy))

    def contextMenuEvent(self, e):
        """

        @param e:
        @return:
        """
        col = self.columnAt(e.pos().x())
        row = self.rowAt(e.pos().y())
        if row == self.item_row and col <= self.item_count:
            widget = self.cellWidget(row, col)
            if widget:
                widget_id = widget.widget_id
                if Func.isWidgetType(widget_id, Info.Cycle):
                    self.copy_action.setEnabled(False)
                self.menu.exec(self.mapToGlobal(e.pos()))

    def copyActionFunc(self):
        """

        @return:
        """
        print("copy")

    def deleteActionFunc(self):
        """

        @return:
        """
        print("delete")

    def initTable(self):
        """
        init table: 1. arrow
                    2. three row
        @return:
        """
        # 5 rows and 10 columns
        self.setRowCount(5)
        self.setRowHeight(self.item_row, TimelineTable.Height)
        self.setColumnCount(10)
        # set initial arrow
        for col in range(TimelineTable.InitialArrowLength - 1):
            self.setUnselectableItem(self.top_row, col)
            self.setUnselectableItem(self.item_row, col)
            self.setArrow(col, "timeline/line.png")
            self.setUnselectableItem(self.name_row, col)
        self.setUnselectableItem(self.top_row, TimelineTable.InitialArrowLength - 1)
        self.setUnselectableItem(self.item_row, TimelineTable.InitialArrowLength - 1)
        self.setArrow(TimelineTable.InitialArrowLength - 1, "timeline/arrow.png", 50)
        self.setUnselectableItem(self.name_row, TimelineTable.InitialArrowLength - 1)

    def setUnselectableItem(self, row: int, col: int):
        """
        set unselectable item in table
        @param row:
        @param col:
        @return:
        """
        item = QTableWidgetItem("")
        item.setFlags(Qt.ItemIsSelectable)
        self.setItem(row, col, item)

    def setArrow(self, col: int, image_path: str, width: int = Width):
        """
        set arrow pixmap in table
        @param image_path:
        @return:
        """
        # set column width
        self.setColumnWidth(col, width)
        # set pixmap
        label = QLabel()
        label.setPixmap(Func.getImage(image_path))
        label.setFocusPolicy(Qt.NoFocus)
        self.setCellWidget(self.arrow_row, col, label)

    def addItem(self, timeline_item, timeline_name_item, index: int) -> int:
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return: add index
        """
        # no matter what, insert a column first
        if index > self.item_count or index == -1:
            index = self.item_count

        # we need animation, you can cancel it.
        # self.startMoveToNextAnimation(index)

        # insert new column to add new item
        self.insertColumn(index)
        self.setArrow(index, "timeline/line.png")
        self.setUnselectableItem(self.top_row, index)
        self.setCellWidget(self.item_row, index, timeline_item)
        self.setItem(self.name_row, index, timeline_name_item)
        # change data
        self.item_count += 1
        # if initial length is not full, we should delete one column
        if self.item_count < TimelineTable.InitialArrowLength - 1:
            self.removeColumn(TimelineTable.InitialArrowLength - 2)
        return index

    def deleteItem(self, widget_id: int):
        """
        delete item in timeline table
        @param widget_id:
        @return:
        """
        # find index of widget_id
        index = self.itemIndex(widget_id)
        # delete
        if index != -1:
            # we need animation, you can cancel it.
            # if index != self.item_count - 1:
            #     self.startMoveToPreAnimation(index + 1)

            # if item count is greater than the initial length, we should delete arrow line
            if self.item_count > TimelineTable.InitialArrowLength - 2:
                self.removeColumn(index)
            else:
                self.insertColumn(TimelineTable.InitialArrowLength - 2)
                self.setUnselectableItem(self.top_row, TimelineTable.InitialArrowLength - 1)
                self.setUnselectableItem(self.item_row, TimelineTable.InitialArrowLength - 1)
                self.setArrow(TimelineTable.InitialArrowLength - 2, "timeline/line.png")
                self.setUnselectableItem(self.name_row, TimelineTable.InitialArrowLength - 2)
                self.removeColumn(index)
            # change data
            self.item_count -= 1

    def renameItem(self, origin_widget_name: str, new_widget_name: str):
        """
        change item's name.
        @param origin_widget_name:
        @param new_widget_name:
        @return:
        """
        for col in range(self.item_count):
            item = self.item(self.name_row, col)
            if item.text() == origin_widget_name:
                item.setText(new_widget_name)
                break

    def itemIndex(self, widget_id: int) -> int:
        """
        find item's col according to its widget id
        @param widget_id:
        @return:
        """
        for col in range(self.item_count):
            if widget_id == self.cellWidget(self.item_row, col).widget_id:
                return col
        return -1

    def itemExist(self, widget_id: int) -> int:
        """
        if item or its reference exist in this timeline, return its index, else -1
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        for col in range(self.item_count):
            if widget_name == self.cellWidget(self.name_row, col).text():
                return col
        return -1

    def startItemAnimation(self, x: int):
        """
        show items' animation according to horizontal coordinate
        @param x: horizontal coordinate
        @return:
        """
        # get the column corresponding to the x coordinate
        col = self.columnAt(x)
        # show frame_animation according to col
        if self.item_count:
            # if excel the range, col will be -1
            if col == -1 or col >= self.item_count:
                # all items left
                for i in range(self.item_count):
                    self.startAlignmentAnimation(i, 0)
            else:
                # we need judge mouse in left or right half
                if self.columnAt(x + 50) == col:
                    # in the left half
                    for i in range(col):
                        self.startAlignmentAnimation(i, 0)
                    for i in range(col, self.item_count):
                        self.startAlignmentAnimation(i, 1)
                else:
                    # in the right half
                    for i in range(col + 1):
                        self.startAlignmentAnimation(i, 0)
                    for i in range(col + 1, self.item_count):
                        self.startAlignmentAnimation(i, 1)

    def startAlignmentAnimation(self, col: int, direction: int = 0):
        """
        set alignment of item in table in form of animation
        @param col:
        @param direction: 0. left
                          1. right
        @return:
        """
        widget: TimelineItem = self.cellWidget(self.item_row, col)
        if direction:
            # right
            x = TimelineTable.Width - TimelineItem.IconSize
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
        else:
            # left
            x = 0
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
        frame_rect = QRect(x, y, TimelineItem.IconSize, TimelineItem.IconSize)
        widget.startFrameAnimation(frame_rect)

    def resetAlignmentAnimation(self):
        """
        reset alignment of item in table in form of animation
        @return:
        """
        # reset alignment
        for col in range(self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            x = (TimelineTable.Width - TimelineItem.IconSize) / 2
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
            frame_rect = QRect(x, y, TimelineItem.IconSize, TimelineItem.IconSize)
            widget.startFrameAnimation(frame_rect)

    def startMoveToNextAnimation(self, start_col: int):
        """
        too many bugs.
        move to next pos animation and it starts form col provided.
        @return:
        """
        for col in range(start_col, self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            geometry = widget.geometry()
            x = geometry.x() + TimelineTable.Width
            y = geometry.y()
            width = geometry.width()
            height = geometry.height()
            rect = QRect(x, y, width, height)
            widget.startGeometryAnimation(rect)

    def startMoveToPreAnimation(self, start_col: int):
        """
        too many bugs.
        move to pre pos animation and it starts form col provided.
        @return:
        """
        for col in range(start_col, self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            geometry = widget.geometry()
            x = geometry.x() - TimelineTable.Width
            y = geometry.y()
            width = geometry.width()
            height = geometry.height()
            rect = QRect(x, y, width, height)
            widget.startGeometryAnimation(rect)

    def dealItemChanged(self, item):
        """
        when cell changed, we need to make judgement
        @param item:
        @return:
        """
        # we just deal this type
        if type(item) == TimelineNameItem:
            # if this item was just added in the table, we ignore it
            if not item.new:
                self.itemNameChanged.emit(item.widget_id, item.text())
            else:
                item.new = False
