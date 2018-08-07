from PyQt5.QtWidgets import QAction, QMainWindow, QInputDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
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

        self.toolbar = self.addToolBar('test')
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.addAction(setting)
        self.toolbar.addAction(addRow)
        self.toolbar.addAction(addRows)
        self.toolbar.addAction(addColumn)
        self.toolbar.addAction(addColumns)

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

        rows, flag = dialog.getInt(self, "Add Rows", "请输入新增行数", 1, 1, 10, 1)
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
                event = Event(parent=None, name="TimeLine", pixmap=".\\.\\image\\timeLine.png")
                self.timelineAdded.emit(self.value, name, event.pixmap(), event.value)
                self.timeLines[row] = event.value
            else:
                name = self.table.item(row, col).text()
                value = self.timeLines[row]
                self.nameChanged.emit(value, name)
