from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFrame, QLabel

from app.func import Func
from app.info import Info


class TimelineTable(QTableWidget):
    """
    table to place timeline item and timeline name item
    """

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
        self.move_cols = [-2, -2]

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
        temp_label = QLabel()
        temp_label.setPixmap(Func.getImage(image_path))
        self.setCellWidget(1, col, temp_label)

    def addItem(self, timeline_item, timeline_name_item, index: int):
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return:
        """
        # because I init some arrow, So i need to judge if i need to add new arrow line
        # if item count is greater than the initial length, we should add new arrow line
        if self.item_count > Info.InitialArrowLength - 2:
            # add new column
            self.insertColumn(index)
            self.setArrow(index, "timeline/line.png")
        self.setCellWidget(0, index, timeline_item)
        self.setCellWidget(2, index, timeline_name_item)
        # change data
        self.item_count += 1

    def deleteItem(self, widget_id: int):
        """
        delete item in timeline table
        @param widget_id:
        @return:
        """
        # find index of widget_id
        index = -1
        for col in range(self.item_count):
            if widget_id == self.cellWidget(0, col).widget_id:
                index = col
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
            self.cellWidget(2, col).setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.move_cols[1] = col
        else:
            # left
            self.cellWidget(0, col).setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.cellWidget(2, col).setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.move_cols[0] = col

    def resetAlignment(self):
        """

        @return:
        """
        # reset alignment
        for col in self.move_cols:
            if col != -2:
                self.cellWidget(0, col).setAlignment(Qt.AlignCenter)
                self.cellWidget(2, col).setAlignment(Qt.AlignCenter)
        # reset data
        self.move_cols = [-2, -2]

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
        # if excel the range, col will be -1
        if col == -1 or col >= self.item_count:
            # we just need rightest item
            self.setAlignment(self.item_count - 1, 0)
            self.move_cols[0] = self.item_count - 1
        else:
            # we need just mouse in left or right half
            if self.columnAt(x + 50) == col:
                # in the left half
                self.setAlignment(col, 1)
                if col:
                    self.setAlignment(col - 1, 0)
            else:
                # in the right half
                self.setAlignment(col, 0)
                if col + 1 < self.item_count:
                    self.setAlignment(col + 1, 1)
