from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from .colAdd import ColAdd
from noDash import NoDash


class TimelineTable(QTableWidget):
    def __init__(self, parent=None):
        super(TimelineTable, self).__init__(parent)
        # 保存name及其默认值
        self.col_header = ["Weight", "Timeline"]
        self.col_value = ["", ""]
        # 其余组件
        self.dialog = ColAdd()
        # 隐藏竖直表头
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(NoDash())
        # 初始化为1行4列
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.col_header)
        self.addRow()

    def addRow(self):
        self.insertRow(self.rowCount())
        for col in range(0, len(self.col_value)):
            self.setItem(self.rowCount() - 1, col, QTableWidgetItem(self.col_value[col]))

    def addColumn(self, name):
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount() - 1, QTableWidgetItem(name))
