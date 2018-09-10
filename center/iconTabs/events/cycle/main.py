from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QMenu, QApplication, \
    QShortcut

from center.iconTabs.timeline.icon import Icon
from .colAdd import ColAdd
from .colsAdd import ColsAdd
from .properties.property import Property
from .timelineTable import TimelineTable

from structure.main import Structure


class Cycle(QMainWindow):
    # 属性修改 (properties)
    propertiesChange = pyqtSignal(dict)
    # 新增timeline (Cycle.value, name, pixmap, value)
    timelineAdd = pyqtSignal(str, str, QPixmap, str)
    # 某行的timeline名称修改 (parent_value, value, name)
    timelineNameChange = pyqtSignal(str, str, str)
    # 新增attribute (value, name, default_value)
    attributeAdd = pyqtSignal(str, str, str)
    # attribute修改 (value, name, attribute_value)
    attributeChange = pyqtSignal(str, str, str)
    # (value, exist_value)
    timelineWidgetMerge = pyqtSignal(str, str)

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
        self.timeline_count = 0

        self.setCentralWidget(self.timeline_table)

        self.property = Property()
        self.property.setWindowModality(Qt.ApplicationModal)
        # tool bar
        self.setToolbar()
        # right button menu
        self.setMenuAndShortcut()
        # 信号
        self.linkSignals()

    def setToolbar(self):
        setting = QAction(QIcon("image/setting.png"), "Setting", self)
        add_row = QAction(QIcon("image/addRow.png"), "Add Row", self)
        add_rows = QAction(QIcon("image/addRows.png"), "Add Rows", self)
        add_column = QAction(QIcon("image/addColumn.png"), "Add Column", self)
        add_columns = QAction(QIcon("image/addColumns.png"), "Add Columns", self)

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

    def setMenuAndShortcut(self):
        self.right_button_menu = QMenu(self)
        # copy action
        self.copy_data = []
        self.is_copy_disabled = False
        # copy shortcut
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        copy_shortcut.activated.connect(self.mergeForCopy)
        # copy for menu
        self.copy_action = QAction("Copy", self.right_button_menu)
        self.copy_action.triggered.connect(self.copyFromTable)
        self.copy_action.setShortcut(QKeySequence(QKeySequence.Copy))
        self.right_button_menu.addAction(self.copy_action)

        # paste action
        self.is_paste_disabled = True
        self.paste_row = 0
        self.paste_col = 0
        self.paste_data = []
        # paste shortcut
        paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        paste_shortcut.activated.connect(self.mergeForPaste)
        # paste for menu
        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(QKeySequence(QKeySequence.Paste))
        self.paste_action.triggered.connect(self.pasteToTable)
        self.right_button_menu.addAction(self.paste_action)

    def linkSignals(self):
        self.timeline_table.horizontalHeader().sectionDoubleClicked.connect(self.setNameAndValue)
        self.property.ok_bt.clicked.connect(self.savePropertiesClose)
        self.property.apply_bt.clicked.connect(self.saveProperties)
        self.timeline_table.cellChanged.connect(self.addOrChangeTimeline)
        self.timeline_table.cellChanged.connect(self.changeAttribute)

    def addRows(self):
        try:
            dialog = QInputDialog()
            # 不可点击其他界面
            dialog.setModal(True)

            dialog.setWindowFlag(Qt.WindowCloseButtonHint)

            rows, flag = dialog.getInt(self, "Add Rows", "Input rows you want to add.", 1, 1, 10, 1)

            if flag:
                while rows:
                    self.timeline_table.addRow()
                    rows -= 1
        except Exception:
            print("error happens in add row. [cycle/main.py]")

    def addColumn(self):
        dialog = ColAdd(self, exist_name=self.timeline_table.col_header)
        dialog.data.connect(self.getData)
        dialog.exec()

    def addColumns(self):
        dialog = ColsAdd(self, exist_name=self.timeline_table.col_header)
        dialog.data.connect(self.getData)
        dialog.exec()

    def setNameAndValue(self, col):
        try:
            name = self.timeline_table.horizontalHeaderItem(col).text()

            dialog = ColAdd(None, name, self.timeline_table.col_value[col], col)
            dialog.data.connect(self.getData)
            dialog.exec()
        except Exception:
            print("error happens in set col name and default value. [cycle/main.py]")

    def getData(self, data):
        # 新增attributes
        if not len(data) % 2:
            for i in range(0, len(data), 2):
                self.timeline_table.col_header.append(data[i])
                self.timeline_table.col_value.append(data[i + 1])
                self.timeline_table.insertColumn(self.timeline_table.columnCount())
                for row in range(0, self.timeline_table.rowCount()):
                    self.timeline_table.setItem(row, self.timeline_table.columnCount() - 1,
                                                QTableWidgetItem(data[i + 1]))
                # 每次新增一个属性, 给icon tabs发送一个信号, 给此cycle中的timeline增加属性
                self.attributeAdd.emit(self.value, data[i], data[i + 1])
        else:
            col = data[-1]
            default = self.timeline_table.col_value[col]
            self.timeline_table.col_header[col] = data[0]
            self.timeline_table.col_value[col] = data[1]
            for row in range(0, self.timeline_table.rowCount()):
                if self.timeline_table.item(row, col) == None or self.timeline_table.item(row, col).text() in ['',
                                                                                                               default]:
                    self.timeline_table.setItem(row, col, QTableWidgetItem(data[1]))
        self.timeline_table.setHorizontalHeaderLabels(self.timeline_table.col_header)

    def changeAttribute(self, row, col):
        try:
            # col > 1的列才是attribute
            if col > 1:
                # 如果此行存在有效的timeline
                if row in self.row_value:
                    attribute_name = self.timeline_table.col_header[col]
                    attribute_value = self.timeline_table.item(row, col).text()
                    timeline_value = self.row_value[row]
                    self.attributeChange.emit(timeline_value, attribute_name, attribute_value)
        except Exception:
            print("error happens in change timeline attribute. [cycle/main.py]")

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

    def addOrChangeTimeline(self, row, col):
        try:
            if col == 1:
                # new timeline
                item = self.timeline_table.item(row, col)
                if row not in self.row_value:
                    name = item.text()
                    if name:
                        res, exist_value = Structure.checkNameIsValid(name, self.value, 'Timeline.')
                        flag = False
                        mergeFlag = False
                        if res == 0:
                            QMessageBox.information(self, "Warning", "sorry, you can't use this name.")
                            self.timeline_table.setItem(row, col, QTableWidgetItem(''))
                        elif res == 1:
                            flag = True
                        elif res == 2:
                            if QMessageBox.question(self, 'Tips',
                                                    'name has existed in other place, are you sure to change?',
                                                    QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                                flag = True
                                mergeFlag = True
                        if flag:
                            timeline_icon = Icon(parent=None, name="Timeline",
                                                 pixmap="image/timeLine.png")
                            # 相关数据存储
                            self.row_value[row] = timeline_icon.value
                            self.row_name[row] = name
                            self.value_row[timeline_icon.value] = row
                            # 给
                            self.timelineAdd.emit(self.value, name, timeline_icon.pixmap(), timeline_icon.value)
                            self.timeline_count += 1
                            if mergeFlag:
                                self.timelineWidgetMerge.emit(timeline_icon.value, exist_value)
                # change timeline name
                else:
                    name = item.text()
                    value = self.row_value[row]
                    if name:
                        res, exist_value = Structure.checkNameIsValid(name, self.value, value)
                        flag = False
                        if res == 0:
                            QMessageBox.information(self, "Warning", "sorry, you can't use this name.")
                            self.timeline_table.setItem(row, col, QTableWidgetItem(self.row_name[row]))
                        elif res == 1:
                            flag = True
                        elif res == 2:
                            if QMessageBox.question(self, 'Tips',
                                                    'name has existed in other place, are you sure to change?',
                                                    QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                                flag = True
                                self.timelineWidgetMerge.emit(value, exist_value)
                        if flag:
                            self.timelineNameChange.emit(self.value, value, name)
                    else:
                        QMessageBox.information(self, "Tips", "Timeline value can't be none.")
                        self.timeline_table.setItem(row, col, QTableWidgetItem(self.row_name[row]))
        except Exception as e:
            print(f"error {e} happens in add or rename timeline. [cycle/main.py]")


    def deleteTimeline(self, value):
        try:
            row = self.value_row[value]
            self.timeline_table.removeRow(row)
            self.timeline_count -= 1
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

    def changeTimelineName(self, value, name):
        try:
            row = self.value_row[value]
            self.timeline_table.item(row, 1).setText(name)
        except Exception as e:
            print("error {} happens in change timeline name. [cycle/main.py]".format(e))

    def contextMenuEvent(self, e):
        # 判断某些选项是否显示
        self.getDataFromSelection()
        self.pasteSelection()

        self.right_button_menu.exec(self.mapToGlobal(e.pos()))
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
            self.copy_action.setDisabled(True)
        else:
            self.copy_action.setEnabled(True)

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
        self.paste_action.setDisabled(self.is_paste_disabled)

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
