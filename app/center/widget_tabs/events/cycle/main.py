from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog

from app.func import Func
from .add_attribute import AddAttributeDialog
from .add_attributes import AddAttributesDialog
from .change_attribute import ChangeAttributeDialog
from .properties.main import Properties
from .timeline_table.main import TimelineTable


class Cycle(QMainWindow):
    # properties发生变化，要告知structure (widget_id -> structure)
    propertiesChange = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(Cycle, self).__init__(parent)
        # data
        self.widget_id = widget_id
        self.current_wid = widget_id
        # widget
        self.timeline_table = TimelineTable(widget_id=self.widget_id)
        self.properties = Properties()
        self.setCentralWidget(self.timeline_table)
        # menu and shortcut
        self.setMenuAndShortcut()
        # toolbar
        self.setToolbar()
        # signals
        self.linkSignals()

    def linkSignals(self):
        self.properties.propertiesChange.connect(lambda: self.propertiesChange.emit(self.widget_id))
        self.timeline_table.horizontalHeader().sectionDoubleClicked.connect(self.changeAttribute)

    def setMenuAndShortcut(self):
        """
        设置菜单和快捷键
        :return:
        """
        pass

    def setToolbar(self):
        setting = QAction(QIcon(Func.getImage("setting.png")), "Setting", self)
        add_row = QAction(QIcon(Func.getImage("add_row.png")), "Add Row", self)
        add_rows = QAction(QIcon(Func.getImage("add_rows.png")), "Add Rows", self)
        delete_rows = QAction(QIcon(Func.getImage("delete_rows.png")), "Delete Rows", self)
        add_column = QAction(QIcon(Func.getImage("add_column.png")), "Add Column", self)
        add_columns = QAction(QIcon(Func.getImage("add_columns.png")), "Add Columns", self)
        delete_columns = QAction(QIcon(Func.getImage("delete_columns.png")), "Delete Columns", self)

        setting.triggered.connect(self.set)
        add_row.triggered.connect(self.addRow)
        add_rows.triggered.connect(self.addRows)
        delete_rows.triggered.connect(self.deleteRows)
        add_column.triggered.connect(self.addAttribute)
        add_columns.triggered.connect(self.addAttributes)
        delete_columns.triggered.connect(self.deleteAttributes)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(setting)
        self.toolbar.addAction(add_row)
        self.toolbar.addAction(add_rows)
        self.toolbar.addAction(delete_rows)
        self.toolbar.addAction(add_column)
        self.toolbar.addAction(add_columns)
        self.toolbar.addAction(delete_columns)

    def set(self):
        self.properties.exec()

    def addRow(self):
        self.timeline_table.addRow()

    def addRows(self):
        try:
            add_rows_dialog = QInputDialog()
            add_rows_dialog.setModal(True)
            add_rows_dialog.setWindowFlag(Qt.WindowCloseButtonHint)

            rows, flag = add_rows_dialog.getInt(self, "Add Rows", "Input rows you want to add.", 1, 1, 100, 1)
            if flag:
                while rows:
                    self.timeline_table.addRow()
                    rows -= 1
        except Exception as e:
            print(f"error {e} happens in add rows. [cycle/main.py]")

    def deleteRows(self):
        try:
            delete_rows = []
            for i in range(len(self.timeline_table.selectedRanges()) - 1, -1, -1):
                selected_range = self.timeline_table.selectedRanges()[i]
                delete_rows.append([selected_range.bottomRow(), selected_range.topRow() - 1])
            # merge rows
            rows = [0 for i in range(self.timeline_table.rowCount())]
            for delete_row_range in delete_rows:
                for row in range(delete_row_range[0], delete_row_range[1], -1):
                    rows[row] = 1
            # delete rows
            for i in range(len(rows) - 1, -1, -1):
                if rows[i]:
                    self.timeline_table.deleteRow(i)
        except Exception as e:
            print(f"error {e} happens in delete rows. [cycle/main.py]")

    def addAttribute(self):
        try:
            dialog = AddAttributeDialog(attributes_exist=Func.getAttributes(self.widget_id))
            dialog.attributeData.connect(self.timeline_table.addAttribute)
            dialog.exec()
        except Exception as e:
            print(f"error {e} happens in add attribute. [cycle/main.py]")

    def changeAttribute(self, col):
        try:
            attribute = self.timeline_table.col_attribute[col]
            value = self.timeline_table.attribute_value[attribute]
            dialog = ChangeAttributeDialog(col=col, attribute=attribute, value=value)
            dialog.attributeData.connect(self.timeline_table.changeAttribute)
            dialog.exec()
        except Exception as e:
            print(f"error {e} happens in change attribute. [cycle/main.py]")

    def addAttributes(self):
        try:
            dialog = AddAttributesDialog(attributes_exist=Func.getAttributes(self.widget_id))
            dialog.attributeData.connect(self.timeline_table.addAttributes)
            dialog.exec()
        except Exception as e:
            print(f"error {e} happens in add attributes. [cycle/main.py]")

    def deleteAttributes(self):
        try:
            delete_cols = []
            for i in range(len(self.timeline_table.selectedRanges()) - 1, -1, -1):
                selected_range = self.timeline_table.selectedRanges()[i]
                delete_cols.append([selected_range.rightColumn(), selected_range.leftColumn() - 1])
            # merge cols
            cols = [0 for i in range(self.timeline_table.columnCount())]
            for delete_col_range in delete_cols:
                for col in range(delete_col_range[0], delete_col_range[1], -1):
                    cols[col] = 1
            # delete cols
            for i in range(len(cols) - 1, -1, -1):
                if cols[i]:
                    self.timeline_table.deleteAttribute(i)
        except Exception as e:
            print(f"error {e} happens in delete attributes. [cycle/main.py]")

    def deleteTimeline(self, timeline_name):
        try:
            row = 0
            while row < self.timeline_table.rowCount():
                if self.timeline_table.item(row, 1).text() == timeline_name:
                    self.timeline_table.removeRow(row)
                else:
                    row += 1
            del self.timeline_table.name_wid[timeline_name]
            del self.timeline_table.name_count[timeline_name]
        except Exception as e:
            print(f"error {e} happens in delete timelines in cycle. [cycle/main.py]")

    def renameTimeline(self, old_name, new_name):
        try:
            # rename
            for row in range(self.timeline_table.rowCount()):
                if self.timeline_table.item(row, 1).text() == old_name:
                    self.timeline_table.item(row, 1).setText(new_name)
            # data
            self.timeline_table.name_wid[new_name] = self.timeline_table.name_wid[old_name]
            self.timeline_table.name_count[new_name] = self.timeline_table.name_count[old_name]
            del self.timeline_table.name_wid[old_name]
            del self.timeline_table.name_count[old_name]
        except Exception as e:
            print(f"error {e} happens in rename timelines in cycle. [cycle/main.py]")

    def getProperties(self):
        return self.properties.getProperties()

    def setProperties(self, properties):
        self.properties.setProperties(properties)

    def changeWidgetId(self, widget_id):
        self.widget_id = widget_id
        self.timeline_table.widget_id = widget_id

    def getInfo(self):
        try:
            info = {}
            info['timeline_table'] = self.timeline_table.getInfo()
            info['properties'] = self.getProperties()
            return info
        except Exception as e:
            print(f"error {e} happens in get info. [cycle/main.py]")

    def restore(self, info: dict):
        """
        读取配置，恢复widget
        :param info:
        :return:
        """
        try:
            self.setProperties(info['properties'])
            self.timeline_table.restore(info['timeline_table'])
        except Exception as e:
            print(f"error {e} happens in restore. [cycle/main.py]")

    def clone(self, copy_wid: str):
        clone_cycle = Cycle(widget_id=copy_wid)
        # timeline table
        self.timeline_table.clone(clone_cycle.timeline_table)
        # properties
        clone_cycle.setProperties(self.getProperties())
        return clone_cycle

    def rowCount(self) -> int:
        """
        返回table共有多少行
        :return:
        """
        return self.timeline_table.rowCount()

    def columnCount(self) -> int:
        """
        返回table共有多少列
        :return:
        """
        return self.timeline_table.columnCount()

    def getHiddenAttribute(self):
        hidden_attr = {
            "cLoop": 0,
            "rowNums": self.timeline_table.rowCount()
        }
        return hidden_attr

    def getTimelines(self) -> list:
        """
        按顺序进行返回所有设置的timeline
        格式为 [ [timeline_name, timeline_widget_id], [], ... ]
        如果某行为空则改行对应的数据为[ '', '']
        :return:
        """
        return self.timeline_table.getTimelines()

    def getAttributes(self, row: int) -> dict:
        """
        按行索引返回该行的数据的一个字典
        格式为{ attribute_name : attribute_value }
        如果属性值未填写则为 ''
        :param row: 行索引
        :return:
        """
        return self.timeline_table.getAttributes(row)

    def getAttributeValues(self, col: int) -> list:
        """
        通过输入的列索引，返回该列对应的attribute的所有value的一个列表
        :param col: 列缩影s
        :return: value的list
        """
        # col有效
        if col < 0 or col >= self.columnCount():
            raise Exception("invalid col index.")
        #
        values = []
        # 遍历每行，将值取出
        for row in range(self.rowCount()):
            values.append(self.item(row, col).text())
        return values

    def getOrder(self) -> str:
        """
        得到设置界面中order的值
        :return:
        """
        return self.getProperties()["order_combo"]

    def getNoRepeatAfter(self) -> str:
        """
        如上类推
        :return:
        """
        return self.getProperties()["no_repeat_after"]

    def getOrderBy(self):
        """
        如上类推
        :return:
        """
        return self.getProperties()["order_by_combo"]
