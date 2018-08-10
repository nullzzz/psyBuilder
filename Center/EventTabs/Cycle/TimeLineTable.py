from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from .ColumnDialog import ColumnDialog
from NoDashDelegate import NoDashDelegate


class TimeLineTable(QTableWidget):
    def __init__(self, parent=None):
        super(TimeLineTable, self).__init__(parent)
        # 保存name及其默认值
        self.headers = ["Weight", "TimeLine"]
        self.values = ["", ""]
        # 其余组件
        self.dialog = ColumnDialog()
        # 隐藏竖直表头
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(NoDashDelegate())
        # 初始化为1行4列
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.headers)
        self.addRow()


    def addRow(self):
        self.insertRow(self.rowCount())
        for col in range(0, len(self.values)):
            self.setItem(self.rowCount() - 1, col, QTableWidgetItem(self.values[col]))

    def addColumn(self, name):
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount() - 1, QTableWidgetItem(name))
