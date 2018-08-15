from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QDataStream, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from .iconTable import IconTable


class IconArea(QFrame):
    # sign显示
    signShow = pyqtSignal(int)
    dragFinish = pyqtSignal()
    # 经过timeline得其value, 后传至structure
    iconAdd = pyqtSignal(str, QPixmap, str)
    iconMove = pyqtSignal(int, int, str)
    iconCopy = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super(IconArea, self).__init__(parent)
        self.row_height = 0
        self.icon_table = IconTable()
        # ui
        self.setFrameStyle(QFrame.StyledPanel)
        # 设置布局
        self.vBox = QVBoxLayout(self)
        self.vBox.addWidget(self.icon_table)
        self.setLayout(self.vBox)
        self.becomeWhite()
        # 允许放置
        self.setAcceptDrops(True)
        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        self.signShow.connect(self.icon_table.showSign)
        self.dragFinish.connect(lambda : self.icon_table.signHide.emit())
        self.icon_table.copyDragBegin.connect(self.copyDrag)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("application/IconBar-text-pixmap") or \
                e.mimeData().hasFormat("application/IconTable-col") or \
                e.mimeData().hasFormat("application/IconTable-copy-col"):
            if not self.icon_table.is_copy:
                self.becomeLightGray()
            else:
                self.becomeGray()
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasFormat("application/IconBar-text-pixmap") or \
                e.mimeData().hasFormat("application/IconTable-col") or \
                e.mimeData().hasFormat("application/IconTable-copy-col"):
            # 给iconTable发送x坐标
            self.signShow.emit(e.pos().x())

            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        # drag from icon bar
        if e.mimeData().hasFormat("application/IconBar-text-pixmap"):
            data = e.mimeData().data("application/IconBar-text-pixmap")
            stream = QDataStream(data, QIODevice.ReadOnly)
            pixmap = QPixmap(1, 1)
            # 读出数据
            text = stream.readQString()
            stream >> pixmap
            # 保证行高度
            if self.row_height < pixmap.size().height():
                self.row_height = pixmap.size().height()
                self.icon_table.setRowHeight(1, self.row_height)

            # 插入一列
            self.icon_table.insertColumn(self.icon_table.fill_count + 1)
            self.icon_table.setIcon(1, self.icon_table.fill_count, pixmap, text)
            self.icon_table.setText(3, self.icon_table.fill_count, text)

            # 给timeLine发射信号
            value = self.icon_table.cellWidget(1, self.icon_table.fill_count).value
            self.iconAdd.emit(text, pixmap, value)

            # 根据鼠标位置进行移动
            dragCol = self.icon_table.fill_count
            targetCol = self.icon_table.getColumnForInsert(e.pos().x())

            if targetCol != -1:
                # 往前移动
                if targetCol < dragCol:
                    self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.CopyAction)
            e.accept()

            # 发射结束信号
            self.dragFinish.emit()
            # 移动信号
            self.iconMove.emit(dragCol, targetCol, value)
            self.becomeWhite()
        # move from icon table
        elif e.mimeData().hasFormat("application/IconTable-col"):
            data = e.mimeData().data("application/IconTable-col")
            stream = QDataStream(data, QIODevice.ReadOnly)
            # 得到被拖拽的控件所在位置
            dragCol = stream.readInt()
            value = self.icon_table.cellWidget(1, dragCol).value
            mouseCol = self.icon_table.columnAt(e.pos().x())
            targetCol = -1
            # move to front
            if dragCol > mouseCol and mouseCol != -1:
                targetCol = self.icon_table.getColumnToFront(e.pos().x())
                self.moveToTarget(dragCol, targetCol)
            # move to back
            elif dragCol < mouseCol or mouseCol == -1:
                targetCol = self.icon_table.getColumnToBack(e.pos().x())
                self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.MoveAction)
            e.accept()

            # 发射结束信号
            self.dragFinish.emit()
            # 移动信号
            self.iconMove.emit(dragCol, targetCol, value)
            self.becomeWhite()
        # copy from icon table
        elif e.mimeData().hasFormat("application/IconTable-copy-col"):
            data = e.mimeData().data("application/IconTable-copy-col")
            stream = QDataStream(data, QIODevice.ReadOnly)
            # 得到被复制的控件所在位置
            col = stream.readInt()
            oldValue = self.icon_table.cellWidget(1, col).value
            pixmap = self.icon_table.cellWidget(1, col).pixmap()
            text = self.icon_table.item(3, col).text()
            # 插入一列
            self.icon_table.insertColumn(self.icon_table.fill_count + 1)
            self.icon_table.setIcon(1, self.icon_table.fill_count, pixmap, text)
            self.icon_table.setText(3, self.icon_table.fill_count, text)

            # newValue 由于复制, icon构造函数中, value默认采用text后缀count, 故可能存在错误
            newValue = self.icon_table.cellWidget(1, self.icon_table.fill_count).value
            widget_type = oldValue.split('.')[0]
            value_count = newValue.split('.')[1]
            self.icon_table.cellWidget(1, self.icon_table.fill_count).value = widget_type + '.' + value_count
            newValue = self.icon_table.cellWidget(1, self.icon_table.fill_count).value

            # 给timeLine发射信号
            self.iconAdd.emit(text, pixmap, newValue)
            # 根据鼠标位置进行移动
            dragCol = self.icon_table.fill_count
            targetCol = self.icon_table.getColumnForInsert(e.pos().x())

            if targetCol != -1:
                # 往前移动
                if targetCol < dragCol:
                    self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.CopyAction)
            e.accept()

            # 发射结束信号
            self.dragFinish.emit()
            # 移动信号
            self.iconMove.emit(dragCol, targetCol, newValue)
            # 给event tabs发信号, 让newValue去复制oldValue的属性
            self.iconCopy.emit(oldValue, newValue, text)

            self.becomeWhite()
            self.icon_table.is_copy = False
        else:
            # 发射结束信号
            self.dragFinish.emit()
            e.ignore()
            self.becomeWhite()

    def dragLeaveEvent(self, e):
        self.dragFinish.emit()
        self.becomeWhite()
        e.ignore()

    def moveToTarget(self, dragCol, targetCol):
        # 将dragCol数据保存
        event = self.icon_table.cellWidget(1, dragCol)
        text = self.icon_table.item(3, dragCol).text()
        # 将dragCol抹掉
        self.icon_table.removeColumn(dragCol)
        # 插入新列
        self.icon_table.insertColumn(targetCol)
        self.icon_table.setIcon(row=1, col=targetCol, name=event.name, pixmap=event.pixmap(), value=event.value)
        self.icon_table.setText(row=3, col=targetCol, text=text)

    def becomeWhite(self):
        # pass
        self.setStyleSheet("background-color:rgba(255,255,255)")

        self.icon_table.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap(".\\.\\image\\arrow.png"))

    def becomeLightGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211, 0.3)")

        self.icon_table.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half_lightGray.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap(".\\.\\image\\line_lightGray.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap(".\\.\\image\\arrow_lightGray.png"))

    def becomeGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211)")

        self.icon_table.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half_gray.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap(".\\.\\image\\line_gray.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap(".\\.\\image\\arrow_gray.png"))

    def copyDrag(self):
        # 改变模式
        self.icon_table.is_copy = True
        self.becomeGray()

    def keyPressEvent(self, e):
        if self.icon_table.is_copy:
            if e.key() == Qt.Key_Escape:
                self.icon_table.is_copy = False
                self.becomeWhite()
