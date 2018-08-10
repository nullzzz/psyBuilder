from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QFrame, QAction, QLabel
from PyQt5.QtCore import Qt, QDataStream, QIODevice, QByteArray, QPoint, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import pyqtSignal
from ..Event import Event
from .Sign import Sign
from NoDashDelegate import NoDashDelegate


class EventTable(QTableWidget):
    col = pyqtSignal(int)
    finish = pyqtSignal()
    # 给structure传递修改name
    eventNameChanged = pyqtSignal(str, str)
    # 打开新页面
    openTab = pyqtSignal(str, str)
    # 新增timeLine
    timeLineAdd = pyqtSignal(str)
    # 给timeLine发删除信号
    eventRemove = pyqtSignal(str)
    # 和properties窗口关联, 先发送到tabs, 看是否创建过, 没有则返回默认值
    properties = pyqtSignal(str)

    # icon固定宽度
    width = 50

    def __init__(self, parent=None):
        super(EventTable, self).__init__(parent)

        self.upSign = Sign(icon="arrowUp.png")
        self.downSign = Sign(icon="arrowDown.png")
        self.fillCount = 0
        self.filled = False
        self.editing = False

        # 隐藏表头
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QFrame.NoFrame)
        # 隐藏网格
        self.setShowGrid(False)
        self.setItemDelegate(NoDashDelegate())
        # 设置行数
        self.setRowCount(5)
        # 设置10列及其宽度
        self.setColumnCount(10)
        self.setColumnWidth(0, self.width)
        for i in range(1, 9):
            self.setColumnWidth(i, self.width * 2)
        self.setColumnWidth(9, self.width)
        # 0, 4: sign
        self.setSpan(0, 0, 1, 10)
        self.setSpan(4, 0, 1, 10)

        self.setCellWidget(4, 0, self.upSign)
        self.setCellWidget(0, 0, self.downSign)

        self.upSign.setColumnCount(9)
        self.downSign.setColumnCount(9)

        for i in range(0, 9):
            self.upSign.setColumnWidth(i, self.width * 2)
        for i in range(0, 9):
            self.downSign.setColumnWidth(i, self.width * 2)

        self.setRowHeight(0, 80)
        self.setRowHeight(4, 80)

        # 3: line arrow
        for col in range(0, 10):
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable)
            self.setItem(1, col, item)
            item1 = QTableWidgetItem("")
            item1.setFlags(Qt.ItemIsSelectable)
            self.setItem(3, col, item1)

        self.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half.png"))
        for col in range(1, 9):
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
        self.setPixmap(2, 9, QPixmap(".\\.\\image\\arrow.png"))

        self.setMinimumHeight(400)

        self.lastPos = [-1, -1]

        self.setDragEnabled(True)

        # 连接信号
        self.linkSignal()

    def linkSignal(self):
        # 箭头相关
        self.col.connect(self.upSign.showIcon)
        self.col.connect(self.downSign.showIcon)
        self.finish.connect(self.upSign.hideIcon)
        self.finish.connect(self.downSign.hideIcon)

        # 名称修改
        self.itemChanged.connect(self.changEventName)
        # 双击打开tab
        self.cellDoubleClicked.connect(self.getValueName)
        # 点击和properties窗口串联
        self.cellClicked.connect(self.getProperties)

    def mouseMoveEvent(self, e):
        if self.columnAt(e.pos().x()) in range(1, self.fillCount + 1) and self.rowAt(e.pos().y()) in (1, 3):
            self.startDrag(Qt.MoveAction)

    def startDrag(self, dropActions):
        # 获得拖拽的控件的column
        dragCol = self.currentColumn()
        if dragCol >= 1 and dragCol < self.fillCount + 1:
            # 将col传过去
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeInt(dragCol)
            mimeData = QMimeData()
            mimeData.setData("application/EventAreaTable-col", data)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec(Qt.MoveAction)

    def setText(self, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, col, item)

    def setEvent(self, row, col, pixmap, name, value=''):
        event = Event(name=name, pixmap=pixmap, value=value)
        event.setAlignment(Qt.AlignCenter)
        self.setCellWidget(row, col, event)
        self.setColumnWidth(col, self.width * 2)

    def setPixmap(self, row, col, pixmap):
        label = QLabel()
        label.setPixmap(pixmap)
        label.setFocusPolicy(Qt.NoFocus)
        self.setCellWidget(row, col, label)

    def setColumnCount(self, count):
        super().setColumnCount(count)
        # 设置sign
        self.setSpan(0, 0, 1, self.columnCount())
        self.setSpan(4, 0, 1, self.columnCount())

        self.upSign.setColumnCount(self.columnCount() - 1)
        self.downSign.setColumnCount(self.columnCount() - 1)

        for i in range(0, self.upSign.columnCount()):
            self.upSign.setColumnWidth(i, self.width * 2)
        for i in range(0, self.downSign.columnCount()):
            self.downSign.setColumnWidth(i, self.width * 2)

    def removeColumn(self, col, sendFlag=False):
        if sendFlag:
            value = self.cellWidget(1, col).value
            self.eventRemove.emit(value)
        if self.fillCount > 8:
            super().removeColumn(col)
            self.upSign.removeColumn(self.columnCount() - 1)
            self.downSign.removeColumn(self.columnCount() - 1)
        else:
            super().insertColumn(9)
            self.setPixmap(2, 9, QPixmap(".\\.\\image\\line.png"))
            self.setColumnWidth(9, self.width * 2)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable)
            self.setItem(1, 9, item)
            item1 = QTableWidgetItem("")
            item1.setFlags(Qt.ItemIsSelectable)
            self.setItem(3, 9, item1)
            super().removeColumn(col)
        self.fillCount -= 1
        if self.fillCount < 8:
            self.filled = False

    def insertColumn(self, col):
        if self.fillCount >= 8:
            super().insertColumn(col)
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
            self.upSign.insertColumn(self.upSign.columnCount())
            self.upSign.setColumnWidth(self.upSign.columnCount() - 1, self.width * 2)
            self.downSign.insertColumn(self.downSign.columnCount())
            self.downSign.setColumnWidth(self.downSign.columnCount() - 1, self.width * 2)
        else:
            super().removeColumn(8)
            super().insertColumn(col)
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))

        self.fillCount += 1

        if self.fillCount >= 8:
            self.filled = True

    # 只会存在moveToFront, return -1即无需移动
    def getColumnForInsert(self, x):
        col = self.columnAt(x)

        if col == 0:
            return 1
        if col != -1:
            tempCol = self.columnAt(x + self.width)
            if tempCol > col:
                return tempCol
            if tempCol == col:
                return col
            if tempCol == -1:
                return -1
        else:
            return -1

    # col != -1 and col < dragCol
    def getColumnToFront(self, x):
        col = self.columnAt(x)
        # 鼠标指向首末列
        if col == 0:
            return 1
        # 鼠标指向其他列
        tempCol = self.columnAt(x + self.width)
        return tempCol

    # col > dragCol
    def getColumnToBack(self, x):
        col = self.columnAt(x)
        # 在末尾
        if col == self.columnCount() - 1:
            return self.fillCount
        if col != -1:
            colTemp = self.columnAt(x - self.width)
            if not self.filled and colTemp > self.fillCount:
                return self.fillCount
            return colTemp
        else:
            return self.fillCount

    # 接受x坐标, 给sign发送应当显示的col
    def sendPos(self, x):
        col = self.columnAt(x)
        iconCol = col
        # 未满时
        if not self.filled:
            if col == 0:
                iconCol = 0
            elif col > self.fillCount or col == -1:
                iconCol = self.fillCount
            else:
                colTemp = self.columnAt(x + self.width)
                if colTemp == col:
                    iconCol = col - 1
        else:
            if col == self.columnCount() - 1 or col == -1:
                iconCol = self.upSign.columnCount() - 1
            elif col == 0:
                iconCol = 0
            else:
                colTemp = self.columnAt(x + self.width)
                if colTemp == -1:
                    iconCol = self.fillCount
                if colTemp > col:
                    pass
                elif col == colTemp:
                    iconCol = col - 1
        self.col.emit(iconCol)

    # 给sign发送消除信号
    def sendFinish(self):
        self.finish.emit()

    # 右键菜单
    def contextMenuEvent(self, e):
        column = self.columnAt(e.pos().x())
        row = self.rowAt(e.pos().y())
        if column in range(0, self.fillCount + 1) and row == 1:
            menu = QMenu(self)
            delete = QAction("删除", menu)
            menu.addAction(delete)
            delete.triggered.connect(lambda: self.removeColumn(column, True))
            menu.popup(self.mapToGlobal(e.pos()))

    def mouseDoubleClickEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())

            # event
            if row == 1 and col in range(1, self.fillCount + 1):
                self.cellDoubleClicked.emit(row, col)
            # text
            elif row == 3 and col in range(1, self.fillCount + 1):
                self.setFocus()
                self.editItem(self.item(row, col))
                self.editing = True

    # 接受row, col
    def getValueName(self, row, col):
        name = self.item(row + 2, col).text()
        value = self.cellWidget(row, col).value
        # 给eventTabs发
        self.openTab.emit(value, name)
        # 如果是timeLine要串事件, 包括双击打开tab, 后加event添加至structure, name修改要同步
        if value.startswith('TimeLine'):
            self.timeLineAdd.emit(value)

    # 更改event name
    def changEventName(self, item):
        if self.editing:
            self.cellWidget(1, item.column()).setName(item.text())
            # 发送value和更改后的name
            self.eventNameChanged.emit(self.cellWidget(1, item.column()).value, item.text())
            self.editing = False

    def getProperties(self, row, col):
        if row in (1, 3) and col in range(0, self.fillCount + 1):
            value = self.cellWidget(1, col).value
            self.properties.emit(value)

    def removeEvent(self, value):
        index = -1
        for col in range(1, self.fillCount + 1):
            if self.cellWidget(1, col).value == value:
                index = col
                break

        if index != -1:
            self.removeColumn(index, False)