from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QMenu, QApplication

from center.iconTabs.timeline.icon import Icon
from .colAdd import ColAdd
from .colsAdd import ColsAdd
from .properties.property import Property
from .timelineTable import TimelineTable


class Cycle(QMainWindow):
    # 属性修改 (properties)
    propertiesChange = pyqtSignal(dict)
    # 新增timeline (Cycle.value, name, pixmap, value)
    timelineAdd = pyqtSignal(str, str, QPixmap, str)
    # 某行的timeline名称修改 (value, name)
    timelineNameChange = pyqtSignal(str, str)

    def __init__(self, parent=None, value=''):
        super(Cycle, self).__init__(parent)

        self.timeline_table = TimelineTable(self)
        # self.properties = {"loadMethod": 0, "fileName": "", "order_combo": 0, "no_repeat_after": 0, "order_by_combo": 0}
        self.properties = {"order_combo": 0, "no_repeat_after": 0, "order_by_combo": 0}
        self.value = value
        # row : value
        self.row_value = {}
        # row : name
        self.row_name = {}
        # value : row
        self.value_row = {}

        self.setCentralWidget(self.timeline_table)

        self.property = Property()
        self.property.setWindowModality(Qt.ApplicationModal)

        setting = QAction(QIcon(".\\.\\image\\setting.png"), "Setting", self)
        add_row = QAction(QIcon(".\\.\\image\\addRow.png"), "Add Row", self)
        add_rows = QAction(QIcon(".\\.\\image\\addRows.png"), "Add Rows", self)
        add_column = QAction(QIcon(".\\.\\image\\addColumn.png"), "Add Column", self)
        add_columns = QAction(QIcon(".\\.\\image\\addColumns.png"), "Add Columns", self)

        setting.triggered.connect(self.setting)
        add_row.triggered.connect(self.timeline_table.addRow)
        add_rows.triggered.connect(self.addRows)
        add_column.triggered.connect(self.addColumn)
        add_columns.triggered.connect(self.addColumns)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(setting)
        self.toolbar.addAction(add_row)
        self.toolbar.addAction(add_rows)
        self.toolbar.addAction(add_column)
        self.toolbar.addAction(add_columns)
        # 菜单
        self.menu = QMenu(self)

        # copy action
        self.copy_data = []
        self.is_copy_disabled = False
        # 在toolbar中设置copy以使用快捷键
        self.copy_toolbar = QAction("&Copy", self)
        self.copy_toolbar.triggered.connect(self.mergeForCopy)
        self.copy_toolbar.setShortcut(QKeySequence(QKeySequence.Copy))
        # self.copyForToolbar.setVisible(False)
        self.toolbar.addAction(self.copy_toolbar)
        # copy for menu
        self.copy_menu = QAction("Copy", self.menu)
        self.copy_menu.triggered.connect(self.copyFromTable)
        self.copy_menu.setShortcut(QKeySequence(QKeySequence.Copy))
        self.menu.addAction(self.copy_menu)

        # paste action
        self.is_paste_disabled = True
        self.paste_row = 0
        self.paste_col = 0
        self.paste_data = []
        # paste for tool bar
        self.paste_toolbar = QAction("Paste", self)
        self.paste_toolbar.setShortcut(QKeySequence(QKeySequence.Paste))
        self.paste_toolbar.triggered.connect(self.mergeForPaste)
        self.toolbar.addAction(self.paste_toolbar)
        # paste for menu
        self.paste_menu = QAction("Paste", self)
        self.paste_menu.setShortcut(QKeySequence(QKeySequence.Paste))
        self.paste_menu.triggered.connect(self.pasteToTable)
        self.menu.addAction(self.paste_menu)

        # 信号
        self.timeline_table.horizontalHeader().sectionDoubleClicked.connect(self.setNameAndValue)
        self.property.ok_bt.clicked.connect(self.savePropertiesClose)
        self.property.apply_bt.clicked.connect(self.saveProperties)
        self.timeline_table.cellChanged.connect(self.addTimeline)

    def addRows(self):
        dialog = QInputDialog()
        # 不可点击其他界面
        dialog.setModal(True)

        dialog.setWindowFlag(Qt.WindowCloseButtonHint)

        rows, flag = dialog.getInt(self, "Add Rows", "Input rows you want to add.", 1, 1, 10, 1)

        if flag:
            while rows:
                self.timeline_table.addRow()
                rows -= 1

    def addColumn(self):
        dialog = ColAdd(self)
        dialog.data.connect(self.getData)
        dialog.exec()

    def addColumns(self):
        dialog = ColsAdd(self)
        dialog.data.connect(self.getData)
        dialog.exec()

    def setNameAndValue(self, col):
        name = self.timeline_table.horizontalHeaderItem(col).text()

        dialog = ColAdd(None, name, self.timeline_table.values[col], col)
        dialog.data.connect(self.getData)
        dialog.exec()

    def getData(self, data):
        if not len(data) % 2:
            for i in range(0, len(data), 2):
                self.timeline_table.headers.append(data[i])
                self.timeline_table.values.append(data[i + 1])
                self.timeline_table.insertColumn(self.timeline_table.columnCount())
                for row in range(0, self.timeline_table.rowCount()):
                    self.timeline_table.setItem(row, self.timeline_table.columnCount() - 1, QTableWidgetItem(data[i + 1]))
        else:
            col = data[-1]
            default = self.timeline_table.values[col]
            self.timeline_table.headers[col] = data[0]
            self.timeline_table.values[col] = data[1]
            for row in range(0, self.timeline_table.rowCount()):
                if self.timeline_table.item(row, col) == None or self.timeline_table.item(row, col).text() in ['', default]:
                    self.timeline_table.setItem(row, col, QTableWidgetItem(data[1]))
        self.timeline_table.setHorizontalHeaderLabels(self.timeline_table.headers)

    def setting(self):
        self.setProperties()
        self.property.exec()

    def setProperties(self):
        # general
        # general = self.property.general
        # general.loadMethod.setCurrentIndex(self.properties["loadMethod"])
        # general.fileName.setText(self.properties["fileName"])
        # selection
        selection = self.property.selection
        selection.order_combo.setCurrentIndex(self.properties["order_combo"])
        selection.no_repeat_after.setCurrentIndex(self.properties["no_repeat_after"])
        selection.order_by_combo.setCurrentIndex(self.properties["order_by_combo"])

    def saveProperties(self):
        # general = self.property.general
        # self.properties["loadMethod"] = general.loadMethod.currentIndex()
        # self.properties["fileName"] = general.fileName.text()

        selection = self.property.selection
        self.properties["order_combo"] = selection.order_combo.currentIndex()
        self.properties["no_repeat_after"] = selection.no_repeat_after.currentIndex()
        self.properties["order_by_combo"] = selection.order_by_combo.currentIndex()

        # 发射信号
        self.propertiesChange.emit(self.getProperties())

    def savePropertiesClose(self):
        self.saveProperties()
        self.property.close()

    def getProperties(self):
        res = {}
        # general = self.property.general
        # res["loadMethod"] = general.loadMethod.currentText()
        # res["fileName"] = general.fileName.text()

        selection = self.property.selection
        res["Order Combo"] = selection.order_combo.currentText()
        res["No Repeat After"] = selection.no_repeat_after.currentText()
        res["Order By Combo"] = selection.order_by_combo.currentText()

        return res

    def addTimeline(self, row, col):
        if col == 1:
            if row not in self.row_value:
                name = self.timeline_table.item(row, col).text()
                if name:
                    event = Icon(parent=None, name="Timeline", pixmap=".\\.\\image\\timeLine.png")
                    self.timelineAdd.emit(self.value, name, event.pixmap(), event.value)
                    self.timeline_table.value_row[event.value] = row
                    # 数据存储
                    self.row_value[row] = event.value
                    self.row_name[row] = name
                    self.value_row[event.value] = row
            else:
                name = self.timeline_table.item(row, col).text()
                if name:
                    value = self.row_value[row]
                    self.timelineNameChange.emit(value, name)
                else:
                    QMessageBox.information(self, "Tips", "Timeline value can't be changed to none.")
                    self.timeline_table.setItem(row, col, QTableWidgetItem(self.row_name[row]))

    def deleteTimeline(self, value):
        try:
            row = self.value_row[value]
            self.timeline_table.removeRow(row)
            # 数据刷新
            del self.value_row[value]
            del self.row_value[row]
            del self.row_name[row]
            # rows: value -> row
            for key in self.value_row:
                if self.value_row[key] > row:
                    self.value_row[key] -= 1
            # timeLines: row -> value
            # timeLineNames: row -> name
            for key in self.row_value:
                if key > row:
                    temp_value = self.row_value[key]
                    temp_name = self.row_name[key]
                    temp_key = key - 1
                    self.row_value[temp_key] = temp_value
                    self.row_name[temp_key] = temp_name
                    del self.row_name[key]
                    del self.row_value[key]
        except Exception:
            print("some errors happen in delete row [main.py]")

    def contextMenuEvent(self, e):
        # 判断某些选项是否显示
        self.getDataFromSelection()
        self.pasteSelection()

        self.menu.exec(self.mapToGlobal(e.pos()))
        # 初始化
        self.copy_data.clear()
        self.is_copy_disabled = False
        self.paste_data.clear()
        self.paste_col = 0
        self.paste_row = 0
        self.is_paste_disabled = False

    def getDataFromSelection(self):
        left_old = -1
        right_old = -1
        # 获取被选择的数据及是否可以被选中
        for select_range in self.timeline_table.selectedRanges():
            top = select_range.topRow()
            bottom = select_range.bottomRow()
            left = select_range.leftColumn()
            right = select_range.rightColumn()
            # 判断被选择数据是否合法
            if (left_old == -1 or left == left_old) and (right_old == -1 or right_old == right):
                left_old = left
                right_old = right
            else:
                self.is_copy_disabled = True
                break
            # 被选中数据
            for row in range(top, bottom + 1):
                temp = []
                for col in range(left, right + 1):
                    try:
                        item = self.timeline_table.item(row, col)
                        temp.append(item.text())
                    except Exception:
                        temp.append("")
                self.copy_data.append(temp)
        # 根据判断结果来决定是否显示copy
        if self.is_copy_disabled or not self.copy_data:
            self.copy_menu.setDisabled(True)
        else:
            self.copy_menu.setEnabled(True)

    def mergeForCopy(self):
        self.getDataFromSelection()
        self.copyFromTable()

    def copyFromTable(self):
        if not self.is_copy_disabled:
            for i in range(0, len(self.copy_data)):
                self.copy_data[i] = '\t'.join(self.copy_data[i])
            text = '\n'.join(self.copy_data)
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
        # 重新初始化
        self.copy_data.clear()
        self.is_copy_disabled = False

    # 复制之前的判断
    def pasteSelection(self):
        # 如果为空或者有多个选择区域, 不能进行粘贴
        if len(self.timeline_table.selectedRanges()) != 1:
            self.is_paste_disabled = True
        else:
            self.paste_row = self.timeline_table.selectedRanges()[0].rowCount()
            self.paste_col = self.timeline_table.selectedRanges()[0].columnCount()
            # 判断选择区域和剪切板中数据是否相同
            clipboard = QApplication.clipboard()
            try:
                text = clipboard.text()
                temp = text.split('\n')
                for i in temp:
                    self.paste_data.append(i.split('\t'))
                if self.paste_col != len(self.paste_data[0]) or self.paste_row != len(self.paste_data):
                    self.is_paste_disabled = True
            except Exception:
                self.is_paste_disabled = True

        # 根据判断结果来决定是否显示paste
        self.paste_menu.setDisabled(self.is_paste_disabled)

    def mergeForPaste(self):
        self.pasteSelection()
        self.pasteToTable()

    def pasteToTable(self):
        try:
            if not self.is_paste_disabled:
                top_row = self.timeline_table.selectedRanges()[0].topRow()
                left_column = self.timeline_table.selectedRanges()[0].leftColumn()
                for row in range(top_row, top_row + self.paste_row):
                    for col in range(left_column, left_column + self.paste_col):
                        self.timeline_table.item(row, col).setText(self.paste_data[row - top_row][col - left_column])
        except Exception:
            print("paste into table error.")

        # 重新初始化
        self.paste_row = 0
        self.paste_col = 0
        self.is_paste_disabled = False
        self.paste_data = []
