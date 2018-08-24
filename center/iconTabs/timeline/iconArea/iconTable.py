from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QFrame, QAction, QLabel
from PyQt5.QtCore import Qt, QDataStream, QIODevice, QByteArray, QPoint, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtCore import pyqtSignal
from ..icon import Icon
from .signTable import SignTable
from noDash import NoDash


class IconTable(QTableWidget):
    # 给signTable发送此时显示的column (col)
    signShow = pyqtSignal(int)
    signHide = pyqtSignal()
    # name被修改 (value, name)
    iconNameChange = pyqtSignal(str, str)
    # icon被remove, 先发送给timeline获取icon的parent value (value)
    iconRemove = pyqtSignal(str)
    # 双击icon打开tab (value, name)
    iconDoubleClicked = pyqtSignal(str, str)
    # copy模式启动 ()
    copyDragBegin = pyqtSignal()
    # 单击得properties, 给icon tabs发送信号 (value)
    propertiesShow = pyqtSignal(str)

    # icon固定宽度
    WIDTH = 50

    def __init__(self, parent=None):
        super(IconTable, self).__init__(parent)
        # sign table
        self.up_sign = SignTable(sign="arrow_up.png")
        self.down_sign = SignTable(sign="arrow_down.png")
        # 当前icon count
        self.fill_count = 0
        # 当前icon count 是否 >= 8
        self.is_fill = False
        # text是否可以被编辑
        self.is_edit = False
        # 是否是copy模式
        self.is_copy_module = False
        # 可以被复制的列
        self.can_copy_col = -1

        # 隐藏表头
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QFrame.NoFrame)
        # 隐藏网格
        self.setShowGrid(False)
        self.setItemDelegate(NoDash())
        # 设置行数
        self.setRowCount(5)
        # 设置10列及其宽度
        self.setColumnCount(10)
        self.setColumnWidth(0, IconTable.WIDTH)
        for i in range(1, 9):
            self.setColumnWidth(i, IconTable.WIDTH * 2)
        self.setColumnWidth(9, IconTable.WIDTH)
        # 0, 4: sign
        self.setSpan(0, 0, 1, 10)
        self.setCellWidget(0, 0, self.down_sign)
        self.setSpan(4, 0, 1, 10)
        self.setCellWidget(4, 0, self.up_sign)

        self.up_sign.setColumnCount(9)
        self.down_sign.setColumnCount(9)

        for i in range(0, 9):
            self.up_sign.setColumnWidth(i, IconTable.WIDTH * 2)
        for i in range(0, 9):
            self.down_sign.setColumnWidth(i, IconTable.WIDTH * 2)

        self.setRowHeight(0, 100)
        self.setRowHeight(4, 100)

        # 3: arrow line
        for col in range(0, 10):
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable)
            self.setItem(1, col, item)
            item_1 = QTableWidgetItem("")
            item_1.setFlags(Qt.ItemIsSelectable)
            self.setItem(3, col, item_1)

        self.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half.png"))
        for col in range(1, 9):
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
        self.setPixmap(2, 9, QPixmap(".\\.\\image\\arrow.png"))

        self.setMinimumHeight(400)

        self.lastPos = [-1, -1]

        self.setDragEnabled(True)

        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # 显示sign
        self.signShow.connect(self.up_sign.showSign)
        self.signShow.connect(self.down_sign.showSign)
        # 隐藏sign
        self.signHide.connect(self.up_sign.hideSign)
        self.signHide.connect(self.down_sign.hideSign)
        # icon name改变同步到structure, iconTabs
        self.itemChanged.connect(self.changIconName)
        # 双击打开tab
        self.cellDoubleClicked.connect(self.openTab)
        # 单击显示properties
        self.cellClicked.connect(self.getProperties)

    def setText(self, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, col, item)

    def setIcon(self, row, col, pixmap, name, value=''):
        icon = Icon(name=name, pixmap=pixmap, value=value)
        icon.setAlignment(Qt.AlignCenter)
        self.setCellWidget(row, col, icon)
        self.setColumnWidth(col, self.WIDTH * 2)

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

        self.up_sign.setColumnCount(self.columnCount() - 1)
        self.down_sign.setColumnCount(self.columnCount() - 1)

        for i in range(0, self.up_sign.columnCount()):
            self.up_sign.setColumnWidth(i, self.WIDTH * 2)
        for i in range(0, self.down_sign.columnCount()):
            self.down_sign.setColumnWidth(i, self.WIDTH * 2)

    def removeColumn(self, col, sendFlag=False):
        if sendFlag:
            value = self.cellWidget(1, col).value
            self.iconRemove.emit(value)
        if self.fill_count > 8:
            super().removeColumn(col)
            self.up_sign.removeColumn(self.columnCount() - 1)
            self.down_sign.removeColumn(self.columnCount() - 1)
        else:
            super().insertColumn(9)
            self.setPixmap(2, 9, QPixmap(".\\.\\image\\line.png"))
            self.setColumnWidth(9, self.WIDTH * 2)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable)
            self.setItem(1, 9, item)
            item1 = QTableWidgetItem("")
            item1.setFlags(Qt.ItemIsSelectable)
            self.setItem(3, 9, item1)
            super().removeColumn(col)
        self.fill_count -= 1
        if self.fill_count < 8:
            self.is_fill = False

    def insertColumn(self, col):
        if self.fill_count >= 8:
            super().insertColumn(col)
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
            self.up_sign.insertColumn(self.up_sign.columnCount())
            self.up_sign.setColumnWidth(self.up_sign.columnCount() - 1, self.WIDTH * 2)
            self.down_sign.insertColumn(self.down_sign.columnCount())
            self.down_sign.setColumnWidth(self.down_sign.columnCount() - 1, self.WIDTH * 2)
        else:
            super().removeColumn(8)
            super().insertColumn(col)
            self.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))

        self.fill_count += 1

        if self.fill_count >= 8:
            self.is_fill = True

    def mouseMoveEvent(self, e):
        if self.columnAt(e.pos().x()) in range(1, self.fill_count + 1) and self.rowAt(e.pos().y()) in (1, 3):
            # move模式
            if not self.is_copy_module:
                self.moveDrag(Qt.MoveAction)
            # copy模式
            else:
                if self.can_copy_col != -1 and self.columnAt(e.pos().x()) == self.can_copy_col:
                    self.copyDrag()

    def moveDrag(self, dropActions):
        drag_col = self.currentColumn()
        if drag_col >= 1 and drag_col < self.fill_count + 1:
            # 将col传过去
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeInt(drag_col)
            mime_data = QMimeData()
            mime_data.setData("application/IconTable-col", data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec(dropActions)

    def copyDrag(self):
        col = self.currentColumn()
        if col >= 1 and col < self.fill_count + 1 and col == self.can_copy_col:
            # 将col传过去
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeInt(col)
            mime_data = QMimeData()
            mime_data.setData("application/IconTable-copy-col", data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec(Qt.CopyAction)

    # 只会存在moveToFront, return -1即无需移动
    def getColumnForInsert(self, x):
        col = self.columnAt(x)

        if col == 0:
            return 1
        if col != -1:
            temp_col = self.columnAt(x + self.WIDTH)
            if temp_col > col:
                return temp_col
            if temp_col == col:
                return col
            if temp_col == -1:
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
        temp_col = self.columnAt(x + self.WIDTH)
        return temp_col

    # col > dragCol
    def getColumnToBack(self, x):
        col = self.columnAt(x)
        # 在末尾
        if col == self.columnCount() - 1:
            return self.fill_count
        if col != -1:
            col_temp = self.columnAt(x - self.WIDTH)
            if not self.is_fill and col_temp > self.fill_count:
                return self.fill_count
            return col_temp
        else:
            return self.fill_count

    # 接收x坐标, 给signTable发送应当显示的col
    def showSign(self, x):
        col = self.columnAt(x)
        icon_col = col

        if not self.is_fill:
            if col == 0:
                icon_col = 0
            elif col > self.fill_count or col == -1:
                icon_col = self.fill_count
            else:
                col_temp = self.columnAt(x + self.WIDTH)
                if col_temp == col:
                    icon_col = col - 1
        else:
            if col == self.columnCount() - 1 or col == -1:
                icon_col = self.up_sign.columnCount() - 1
            elif col == 0:
                icon_col = 0
            else:
                col_temp = self.columnAt(x + self.WIDTH)
                if col_temp == -1:
                    icon_col = self.fill_count
                if col_temp > col:
                    pass
                elif col == col_temp:
                    icon_col = col - 1

        self.signShow.emit(icon_col)

    # 给sign发送消除信号
    def sendFinish(self):
        self.dragFinish.emit()

    # 右键菜单
    def contextMenuEvent(self, e):
        try:
            column = self.columnAt(e.pos().x())
            row = self.rowAt(e.pos().y())
            if column in range(0, self.fill_count + 1) and row == 1:
                menu = QMenu(self)
                if not self.is_copy_module:
                    # delete action
                    delete = QAction("delete", menu)
                    delete.triggered.connect(lambda : self.removeColumn(column, True))
                    menu.addAction(delete)
                    # copy action
                    copy = QAction("copy", menu)
                    copy.triggered.connect(lambda :self.copyDragStart(column))
                    item_value = self.cellWidget(row, column).value
                    if item_value.startswith("Cycle"):
                        copy.setDisabled(True)
                    menu.addAction(copy)
                else:
                    pass
                menu.popup(self.mapToGlobal(e.pos()))
        except Exception:
            print("error happens in generate menu. [iconTable.py]")

    def mouseDoubleClickEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())

            # event
            if row == 1 and col in range(1, self.fill_count + 1):
                self.cellDoubleClicked.emit(row, col)
            # text
            elif row == 3 and col in range(1, self.fill_count + 1):
                self.setFocus()
                self.editItem(self.item(row, col))
                self.is_edit = True

    def openTab(self, row, col):
        name = self.item(row + 2, col).text()
        value = self.cellWidget(row, col).value
        # 发送给icon tabs
        self.iconDoubleClicked.emit(value, name)

    # 更改event name
    def changIconName(self, item):
        if self.is_edit:
            self.cellWidget(1, item.column()).setName(item.text())
            # 发送value和更改后的name
            self.iconNameChange.emit(self.cellWidget(1, item.column()).value, item.text())
            self.is_edit = False

    def getProperties(self, row, col):
        if row in (1, 3) and col in range(0, self.fill_count + 1):
            value = self.cellWidget(1, col).value
            self.propertiesShow.emit(value)

    def removeIcon(self, value):
        index = -1
        for col in range(1, self.fill_count + 1):
            if self.cellWidget(1, col).value == value:
                index = col
                break

        if index != -1:
            self.removeColumn(index)

    def copyDragStart(self, col):
        self.copyDragBegin.emit()
        self.can_copy_col = col

    def copyDragFinish(self):
        self.can_copy_col = -1
        self.is_copy_module = False

