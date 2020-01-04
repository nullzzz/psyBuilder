from PyQt5.QtWidgets import QTableWidget, QFrame, QLabel

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
        # hide its grid lines
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        # init table
        self.initTable()
        # data
        self.count = 0

    def initTable(self):
        """
        init table: 1. arrow
                    2. three row
        @return:
        """
        # 3 rows and 10 columns
        self.setRowCount(3)
        self.setColumnCount(10)
        # set initial arrow
        for col in range(Info.InitialArrowLength - 1):
            self.setArrow(col, "timeline/line.png")
        self.setArrow(Info.InitialArrowLength - 1, "timeline/arrow.png", 50)

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

    def deleteItem(self, widget_id: int):
        """
        delete item in timeline table
        @param widget_id:
        @return:
        """
        # find index of widget_id
        # delete
