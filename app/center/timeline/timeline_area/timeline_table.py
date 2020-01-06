from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFrame, QLabel

from app.func import Func
from app.info import Info
from ..timeline_name_item import TimelineNameItem


class TimelineTable(QTableWidget):
    """
    table to place timeline item and timeline name item
    """

    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(int, str)

    def __init__(self):
        super(TimelineTable, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineTable")
        # hide its scroll bar
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # hide its grid lines
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        # init table
        self.initTable()
        # data
        self.item_count = 0
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.itemChanged.connect(self.dealCellChanged)

    def initTable(self):
        """
        init table: 1. arrow
                    2. three row
        @return:
        """
        # 3 rows and 10 columns
        self.setRowCount(3)
        self.setRowHeight(0, 100)
        self.setColumnCount(10)
        # set initial arrow
        for col in range(Info.InitialArrowLength - 1):
            self.setUnselectableItem(0, col)
            self.setArrow(col, "timeline/line.png")
            self.setUnselectableItem(2, col)
        self.setUnselectableItem(0, Info.InitialArrowLength - 1)
        self.setArrow(Info.InitialArrowLength - 1, "timeline/arrow.png", 50)
        self.setUnselectableItem(2, Info.InitialArrowLength - 1)

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

    def setArrow(self, col: int, image_path: str, width: int = 100):
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
        self.setCellWidget(1, col, label)

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
        self.insertColumn(index)
        self.setArrow(index, "timeline/line.png")
        self.setCellWidget(0, index, timeline_item)
        self.setItem(2, index, timeline_name_item)
        # change data
        self.item_count += 1
        # if initial length is not full, we should delete one column
        if self.item_count < Info.InitialArrowLength - 1:
            self.removeColumn(Info.InitialArrowLength - 2)
        return index

    def deleteItem(self, widget_id: int):
        """
        delete item in timeline table
        @param widget_id:
        @return:
        """
        # find index of widget_id
        index = self.itemColumn(widget_id)
        # delete
        if index != -1:
            # if item count is greater than the initial length, we should delete arrow line
            if self.item_count > Info.InitialArrowLength - 2:
                self.removeColumn(index)
            else:
                self.insertColumn(Info.InitialArrowLength - 2)
                self.setUnselectableItem(0, Info.InitialArrowLength - 1)
                self.setArrow(Info.InitialArrowLength - 2, "timeline/line.png")
                self.setUnselectableItem(2, Info.InitialArrowLength - 2)
                self.removeColumn(index)
            # change data
            self.item_count -= 1

    def itemColumn(self, widget_id: int):
        """
        find item's col according to its widget id
        @param widget_id:
        @return:
        """
        for col in range(self.item_count):
            if widget_id == self.cellWidget(0, col).widget_id:
                return col
        return -1

    def setAlignment(self, col: int, direction: int = 0):
        """
        set alignment of item in table
        @param col:
        @param direction: 0. left
                          1. right
        @return:
        """
        if direction:
            # right
            self.cellWidget(0, col).setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            # self.move_cols[1] = col
        else:
            # left
            self.cellWidget(0, col).setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            # self.move_cols[0] = col

    def resetAlignment(self):
        """

        @return:
        """
        # reset alignment
        for col in range(self.item_count):
            self.cellWidget(0, col).setAlignment(Qt.AlignCenter)

    def moveItemAnimation(self, x: int):
        """
        show animation according to horizontal coordinate
        @param x: horizontal coordinate
        @return:
        """
        # reset alignment
        self.resetAlignment()
        # get the column corresponding to the x coordinate
        col = self.columnAt(x)
        # show animation according to col
        if self.item_count:
            # if excel the range, col will be -1
            if col == -1 or col >= self.item_count:
                # all items left
                for i in range(self.item_count):
                    self.setAlignment(i, 0)
            else:
                # we need judge mouse in left or right half
                if self.columnAt(x + 50) == col:
                    # in the left half
                    for i in range(col):
                        self.setAlignment(i, 0)
                    for i in range(col, self.item_count):
                        self.setAlignment(i, 1)
                else:
                    # in the right half
                    for i in range(col + 1):
                        self.setAlignment(i, 0)
                    for i in range(col + 1, self.item_count):
                        self.setAlignment(i, 1)

    def dealCellChanged(self, item):
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
