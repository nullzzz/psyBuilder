from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget


class CycleTable(QTableWidget):
    """

    """

    # when widget's name is changed, emit this signal (widget id, widget_name)
    timelineNameChanged = pyqtSignal(int, str)

    def __init__(self):
        super(CycleTable, self).__init__(None)
        self.setColumnCount(10)
        self.setRowCount(10)

    def dealItemChanged(self, item):
        """
        when cell changed, we need to make judgement
        @param item:
        @return:
        """
        # if this item was just added in the table, we ignore it
        if not item.new:
            self.timelineNameChanged.emit(item.widget_id, item.text())
        else:
            item.new = False
