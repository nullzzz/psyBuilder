import copy

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from noDash import NoDash
from .colAdd import ColAdd


class TimelineTable(QTableWidget):
    canEmit = pyqtSignal(bool)

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

        # Alt仿excel复制
        self.is_copying = False
        self.selected_text = ""

        # self.mouseGrabber()
        self.cellClicked.connect(self.selectCell)
        self.itemDoubleClicked.connect(lambda: print("double click"))
        # todo: bug need fixing, table 监听键盘事件会覆盖item的键盘事件
        self.grabKeyboard()

    def addRow(self):
        self.insertRow(self.rowCount())
        for col in range(0, len(self.col_value)):
            self.setItem(self.rowCount() - 1, col, QTableWidgetItem(self.col_value[col]))

    def addColumn(self, name):
        self.insertColumn(self.columnCount())
        self.setHorizontalHeaderItem(self.columnCount() - 1, QTableWidgetItem(name))

    def copy(self, timeline_table, row_name):
        try:
            timeline_table.col_header = copy.deepcopy(self.col_header)
            timeline_table.col_value = copy.deepcopy(self.col_value)
            timeline_table.setColumnCount(self.columnCount())
            timeline_table.setHorizontalHeaderLabels(self.col_header)
            # 得到name
            for row in range(self.rowCount()):
                if row < timeline_table.rowCount():
                    for col in range(self.columnCount()):
                        text = self.item(row, col).text()
                        if col == 1:
                            if text:
                                timeline_table.setItem(row, col, QTableWidgetItem(row_name[row]))
                        else:
                            timeline_table.setItem(row, col, QTableWidgetItem(text))
                else:
                    timeline_table.insertRow(timeline_table.rowCount())
                    for col in range(self.columnCount()):
                        text = self.item(row, col).text()
                        if col == 1:
                            if text:
                                timeline_table.setItem(row, col, QTableWidgetItem(row_name[row]))
                        else:
                            timeline_table.setItem(row, col, QTableWidgetItem(text))
        except Exception as e:
            print(f'error {e} happens in copy timeline table. [cycle/timelineTable.py]')

    def save(self):
        try:
            data = {}
            data['col_header'] = self.col_header
            data['col_value'] = self.col_value
            data['timeline'] = []
            # 列表中的值
            for row in range(self.rowCount()):
                timeline_data = []
                for col in range(self.columnCount()):
                    timeline_data.append(self.item(row, col).text())
                data['timeline'].append(timeline_data)
            return data
        except Exception as e:
            print(f"error {e} happens in copy cycle. [cycle/timelineTable.py]")

    def restore(self, data: dict):
        try:
            self.col_header = data['col_header']
            self.col_value = data['col_value']
            self.setColumnCount(len(self.col_header))
            self.setHorizontalHeaderLabels(self.col_header)
            # 还原timeline table
            print(data['timeline'])
            for row in range(len(data['timeline'])):
                timeline_data = data['timeline'][row]
                if row < self.rowCount():
                    for col in range(len(timeline_data)):
                        if col == 1:
                            try:
                                timeline_name = timeline_data[col]
                                if timeline_name:
                                    self.canEmit.emit(False)
                                    self.setItem(row, col, QTableWidgetItem(timeline_name))
                                    self.canEmit.emit(True)
                            except Exception:
                                pass
                        else:
                            try:
                                self.setItem(row, col, QTableWidgetItem(timeline_data[col]))
                            except Exception:
                                pass
                else:
                    self.insertRow(self.rowCount())
                    for col in range(len(timeline_data)):
                        if col == 1:
                            try:
                                timeline_name = timeline_data[col]
                                if timeline_name:
                                    self.canEmit.emit(False)
                                    self.setItem(row, col, QTableWidgetItem(timeline_name))
                                    self.canEmit.emit(True)
                            except Exception:
                                pass
                        else:
                            try:
                                self.setItem(row, col, QTableWidgetItem(timeline_data[col]))
                            except Exception:
                                pass
        except Exception as e:
            print(f"error {e} happens in copy cycle. [cycle/timelineTable.py]")

    def selectCell(self, row: int, column: int):
        item: QTableWidgetItem = self.item(row, column)
        self.selected_text = item.text()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.is_copying = True
            # todo: 复制时候的光标样式等有空找个好看的吧
            self.setCursor(Qt.SplitVCursor)
        QTableWidget.keyPressEvent(self, e)

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.is_copying = False
            self.unsetCursor()
        QTableWidget.keyReleaseEvent(self, e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.is_copying:
            items = self.selectedItems()
            for item in items:
                item.setText(self.selected_text)
        QTableWidget.mouseReleaseEvent(self, e)
