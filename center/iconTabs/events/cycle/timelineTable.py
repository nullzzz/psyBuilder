from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from .colAdd import ColAdd
from noDash import NoDash

import copy


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

    def copy(self, timeline_table):
        try:
            timeline_table.col_header = copy.deepcopy(self.col_header)
            timeline_table.col_value = copy.deepcopy(self.col_value)
            timeline_table.setColumnCount(self.columnCount())
            timeline_table.setHorizontalHeaderLabels(self.col_header)
            for row in range(self.rowCount()):
                if row < timeline_table.rowCount():
                    for col in range(self.columnCount()):
                        text = self.item(row, col).text()
                        if col == 1 and not text:
                            pass
                        else:
                            timeline_table.setItem(row, col, QTableWidgetItem(text))
                else:
                    timeline_table.insertRow(timeline_table.rowCount())
                    for col in range(self.columnCount()):
                        text = self.item(row, col).text()
                        if col == 1 and not text:
                            pass
                        else:
                            timeline_table.setItem(row, col, QTableWidgetItem(text))
        except Exception as e:
            print(f'error {e} happens in copy timeline table. [cycle/timelineTable.py]')
