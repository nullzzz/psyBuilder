from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog, QTableWidgetItem, QMessageBox, QMenu, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal
from .TimeLineTable import TimeLineTable
from .ColumnDialog import ColumnDialog
from .ColumnsDialog import ColumnsDialog
from .Properties.Property import Property
from ..TimeLine.Event import Event


class Cycle(QMainWindow):
    propertiesChanged = pyqtSignal(dict)
    timelineAdded = pyqtSignal(str, str, QPixmap, str)
    nameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None, value=''):
        super(Cycle, self).__init__(parent)

        self.table = TimeLineTable(self)
        self.properties = {"loadMethod": 0, "fileName": "", "orderCombo": 0, "noRepeatAfter": 0, "orderByCombo": 0}
        self.value = value
        # row : value
        self.timeLines = {}
        # row : name
        self.timeLineNames = {}
        # value : row
        self.rows = {}

        self.setCentralWidget(self.table)

        self.property = Property()
        self.property.setWindowModality(Qt.ApplicationModal)

        setting = QAction(QIcon(".\\.\\image\\setting.png"), "Setting", self)
        addRow = QAction(QIcon(".\\.\\image\\addRow.png"), "Add Row", self)
        addRows = QAction(QIcon(".\\.\\image\\addRows.png"), "Add Rows", self)
        addColumn = QAction(QIcon(".\\.\\image\\addColumn.png"), "Add Column", self)
        addColumns = QAction(QIcon(".\\.\\image\\addColumns.png"), "Add Columns", self)

        setting.triggered.connect(self.setting)
        addRow.triggered.connect(self.table.addRow)
        addRows.triggered.connect(self.addRows)
        addColumn.triggered.connect(self.addColumn)
        addColumns.triggered.connect(self.addColumns)

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(setting)
        self.toolbar.addAction(addRow)
        self.toolbar.addAction(addRows)
        self.toolbar.addAction(addColumn)
        self.toolbar.addAction(addColumns)
        # 菜单
        self.menu = QMenu(self)

        # copy action
        self.copyData = []
        self.copyDisabled = False
        # 在toolbar中设置copy以使用快捷键
        self.copyForToolbar = QAction("&Copy", self)
        self.copyForToolbar.triggered.connect(self.mergeForCopy)
        self.copyForToolbar.setShortcut(QKeySequence(QKeySequence.Copy))
        # self.copyForToolbar.setVisible(False)
        self.toolbar.addAction(self.copyForToolbar)
        # copy for menu
        self.copyForMenu = QAction("Copy", self.menu)
        self.copyForMenu.triggered.connect(self.copyFromTable)
        self.copyForMenu.setShortcut(QKeySequence(QKeySequence.Copy))
        self.menu.addAction(self.copyForMenu)

        # paste action
        self.pasteDisabled = True
        self.pasteRow = 0
        self.pasteCol = 0
        self.pasteData = []
        # paste for tool bar
        self.pasteForToolbar = QAction("Paste", self)
        self.pasteForToolbar.setShortcut(QKeySequence(QKeySequence.Paste))
        self.pasteForToolbar.triggered.connect(self.mergeForPaste)
        self.toolbar.addAction(self.pasteForToolbar)
        # paste for menu
        self.pasteForMenu = QAction("Paste", self)
        self.pasteForMenu.setShortcut(QKeySequence(QKeySequence.Paste))
        self.pasteForMenu.triggered.connect(self.pasteToTable)
        self.menu.addAction(self.pasteForMenu)

        # 信号
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.setNameAndValue)
        self.property.ok_bt.clicked.connect(self.savePropertiesClose)
        self.property.apply_bt.clicked.connect(self.saveProperties)
        self.table.cellChanged.connect(self.addTimeline)

    def addRows(self):
        dialog = QInputDialog()
        # 不可点击其他界面
        dialog.setModal(True)

        dialog.setWindowFlag(Qt.WindowCloseButtonHint)

        rows, flag = dialog.getInt(self, "Add Rows", "Input rows you want to add.", 1, 1, 10, 1)

        if flag:
            while rows:
                self.table.addRow()
                rows -= 1

    def addColumn(self):
        dialog = ColumnDialog(self)
        dialog.data.connect(self.getData)
        dialog.exec()

    def addColumns(self):
        dialog = ColumnsDialog(self)
        dialog.data.connect(self.getData)
        dialog.exec()

    def setNameAndValue(self, col):
        name = self.table.horizontalHeaderItem(col).text()

        dialog = ColumnDialog(None, name, self.table.values[col], col)
        dialog.data.connect(self.getData)
        dialog.exec()

    def getData(self, data):
        if not len(data) % 2:
            for i in range(0, len(data), 2):
                self.table.headers.append(data[i])
                self.table.values.append(data[i + 1])
                self.table.insertColumn(self.table.columnCount())
                for row in range(0, self.table.rowCount()):
                    self.table.setItem(row, self.table.columnCount() - 1, QTableWidgetItem(data[i + 1]))
        else:
            col = data[-1]
            default = self.table.values[col]
            self.table.headers[col] = data[0]
            self.table.values[col] = data[1]
            for row in range(0, self.table.rowCount()):
                if self.table.item(row, col) == None or self.table.item(row, col).text() in ['', default]:
                    self.table.setItem(row, col, QTableWidgetItem(data[1]))
        self.table.setHorizontalHeaderLabels(self.table.headers)

    def setting(self):
        self.setProperties()
        self.property.exec()

    def setProperties(self):
        # general
        general = self.property.tab.widget(0)
        general.loadMethod.setCurrentIndex(self.properties["loadMethod"])
        general.fileName.setText(self.properties["fileName"])
        # selection
        selection = self.property.tab.widget(1)
        selection.orderCombo.setCurrentIndex(self.properties["orderCombo"])
        selection.noRepeatAfter.setCurrentIndex(self.properties["noRepeatAfter"])
        selection.orderByCombo.setCurrentIndex(self.properties["orderByCombo"])

    def saveProperties(self):
        general = self.property.tab.widget(0)
        self.properties["loadMethod"] = general.loadMethod.currentIndex()
        self.properties["fileName"] = general.fileName.text()
        selection = self.property.tab.widget(1)
        self.properties["orderCombo"] = selection.orderCombo.currentIndex()
        self.properties["noRepeatAfter"] = selection.noRepeatAfter.currentIndex()
        self.properties["orderByCombo"] = selection.orderByCombo.currentIndex()

        # 发射信号
        self.propertiesChanged.emit(self.getProperties())

    def savePropertiesClose(self):
        self.saveProperties()
        self.property.close()

    def getProperties(self):
        general = self.property.tab.widget(0)
        res = {}
        res["loadMethod"] = general.loadMethod.currentText()
        res["fileName"] = general.fileName.text()

        selection = self.property.tab.widget(1)
        res["orderCombo"] = selection.orderCombo.currentText()
        res["noRepeatAfter"] = selection.noRepeatAfter.currentText()
        res["orderByCombo"] = selection.orderByCombo.currentText()

        return res

    def addTimeline(self, row, col):
        if col == 1:
            if row not in self.timeLines:
                name = self.table.item(row, col).text()
                if name:
                    event = Event(parent=None, name="TimeLine", pixmap=".\\.\\image\\timeLine.png")
                    self.timelineAdded.emit(self.value, name, event.pixmap(), event.value)
                    self.table.rows[event.value] = row
                    # 数据存储
                    self.timeLines[row] = event.value
                    self.timeLineNames[row] = name
                    self.rows[event.value] = row
            else:
                name = self.table.item(row, col).text()
                if name:
                    value = self.timeLines[row]
                    self.nameChanged.emit(value, name)
                else:
                    QMessageBox.information(self, "Tips", "TimeLine value can't be changed to none.")
                    self.table.setItem(row, col, QTableWidgetItem(self.timeLineNames[row]))

    def deleteTimeLine(self, value):
        try:
            row = self.rows[value]
            self.table.removeRow(row)
            # 数据刷新
            del self.rows[value]
            del self.timeLines[row]
            del self.timeLineNames[row]
            # rows: value -> row
            for key in self.rows:
                if self.rows[key] > row:
                    self.rows[key] -= 1
            # timeLines: row -> value
            # timeLineNames: row -> name
            for key in self.timeLines:
                if key > row:
                    tempValue = self.timeLines[key]
                    tempName = self.timeLineNames[key]
                    tempKey = key - 1
                    self.timeLines[tempKey] = tempValue
                    self.timeLineNames[tempKey] = tempName
                    del self.timeLineNames[key]
                    del self.timeLines[key]
        except Exception:
            print("some errors happen in delete row (Cycle.py)")

    def contextMenuEvent(self, e):
        # 判断某些选项是否显示
        self.getDataFromSelection()
        self.pasteSelection()

        self.menu.exec(self.mapToGlobal(e.pos()))
        # 初始化
        self.copyData.clear()
        self.copyDisabled = False
        self.pasteData.clear()
        self.pasteCol = 0
        self.pasteRow = 0
        self.pasteDisabled = False

    def getDataFromSelection(self):
        leftOld = -1
        rightOld = -1
        # 获取被选择的数据及是否可以被选中
        for selectRange in self.table.selectedRanges():
            top = selectRange.topRow()
            bottom = selectRange.bottomRow()
            left = selectRange.leftColumn()
            right = selectRange.rightColumn()
            # 判断被选择数据是否合法
            if (leftOld == -1 or left == leftOld) and (rightOld == -1 or rightOld == right):
                leftOld = left
                rightOld = right
            else:
                self.copyDisabled = True
                break
            # 被选中数据
            for row in range(top, bottom + 1):
                temp = []
                for col in range(left, right + 1):
                    try:
                        item = self.table.item(row, col)
                        temp.append(item.text())
                    except Exception:
                        temp.append("")
                self.copyData.append(temp)
        # 根据判断结果来决定是否显示copy
        if self.copyDisabled or not self.copyData:
            self.copyForMenu.setDisabled(True)
        else:
            self.copyForMenu.setEnabled(True)

    def mergeForCopy(self):
        self.getDataFromSelection()
        self.copyFromTable()

    def copyFromTable(self):
        if not self.copyDisabled:
            for i in range(0, len(self.copyData)):
                self.copyData[i] = '\t'.join(self.copyData[i])
            text = '\n'.join(self.copyData)
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
        # 重新初始化
        self.copyData.clear()
        self.copyDisabled = False

    # 复制之前的判断
    def pasteSelection(self):
        # 如果为空或者有多个选择区域, 不能进行粘贴
        if len(self.table.selectedRanges()) != 1:
            self.pasteDisabled = True
        else:
            self.pasteRow = self.table.selectedRanges()[0].rowCount()
            self.pasteCol = self.table.selectedRanges()[0].columnCount()
            # 判断选择区域和剪切板中数据是否相同
            clipboard = QApplication.clipboard()
            try:
                text = clipboard.text()
                temp = text.split('\n')
                for i in temp:
                    self.pasteData.append(i.split('\t'))
                if self.pasteCol != len(self.pasteData[0]) or self.pasteRow != len(self.pasteData):
                    self.pasteDisabled = True
            except Exception:
                self.pasteDisabled = True

        # 根据判断结果来决定是否显示paste
        self.pasteForMenu.setDisabled(self.pasteDisabled)

    def mergeForPaste(self):
        self.pasteSelection()
        self.pasteToTable()

    def pasteToTable(self):
        try:
            if not self.pasteDisabled:
                topRow = self.table.selectedRanges()[0].topRow()
                leftColumn = self.table.selectedRanges()[0].leftColumn()
                for row in range(topRow, topRow + self.pasteRow):
                    for col in range(leftColumn, leftColumn + self.pasteCol):
                        self.table.item(row, col).setText(self.pasteData[row - topRow][col - leftColumn])
        except Exception:
            print("paste into table error.")

        # 重新初始化
        self.pasteRow = 0
        self.pasteCol = 0
        self.pasteDisabled = False
        self.pasteData = []
