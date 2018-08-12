from PyQt5.QtWidgets import QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QDataStream, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from .EventTable import EventTable


class EventArea(QFrame):
    # sign显示
    pos = pyqtSignal(int)
    finish = pyqtSignal()
    # 先给SessionProc传递新增event, 后传至structure
    addEvent = pyqtSignal(str, QPixmap, str)
    eventMove = pyqtSignal(int, int, str)
    eventCopy = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super(EventArea, self).__init__(parent)
        self.rowHeight = 0
        self.eventTable = EventTable()
        # ui
        self.setFrameStyle(QFrame.StyledPanel)
        # 设置布局
        self.vBox = QVBoxLayout(self)
        self.vBox.addWidget(self.eventTable)
        self.setLayout(self.vBox)
        self.becomeWhite()
        # 允许放置
        self.setAcceptDrops(True)
        # 连接信号
        self.pos.connect(self.eventTable.sendPos)
        self.finish.connect(self.eventTable.sendFinish)
        self.eventTable.copyDragStart.connect(self.copyDrag)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("application/EventList-text-pixmap") or \
                e.mimeData().hasFormat("application/EventAreaTable-col") or \
                e.mimeData().hasFormat("application/EventAreaTable-copy-col"):
            if not self.eventTable.copy:
                self.becomeLightGray()
            else:
                self.becomeGray()
            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasFormat("application/EventList-text-pixmap") or \
                e.mimeData().hasFormat("application/EventAreaTable-col") or \
                e.mimeData().hasFormat("application/EventAreaTable-copy-col"):
            # 给sign发送x
            self.pos.emit(e.pos().x())

            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasFormat("application/EventList-text-pixmap"):
            data = e.mimeData().data("application/EventList-text-pixmap")
            stream = QDataStream(data, QIODevice.ReadOnly)
            pixmap = QPixmap(1, 1)
            # 读出数据
            text = stream.readQString()
            stream >> pixmap
            # 保证行高度
            if self.rowHeight < pixmap.size().height():
                self.rowHeight = pixmap.size().height()
                self.eventTable.setRowHeight(1, self.rowHeight)

            # 插入一列
            self.eventTable.insertColumn(self.eventTable.fillCount + 1)
            self.eventTable.setEvent(1, self.eventTable.fillCount, pixmap, text)
            self.eventTable.setText(3, self.eventTable.fillCount, text)

            # 给timeLine发射信号
            value = self.eventTable.cellWidget(1, self.eventTable.fillCount).value
            self.addEvent.emit(text, pixmap, value)

            # 根据鼠标位置进行移动
            dragCol = self.eventTable.fillCount
            targetCol = self.eventTable.getColumnForInsert(e.pos().x())

            if targetCol != -1:
                # 往前移动
                if targetCol < dragCol:
                    self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.CopyAction)
            e.accept()

            # 发射结束信号
            self.finish.emit()
            # 移动信号
            self.eventMove.emit(dragCol, targetCol, value)
            self.becomeWhite()
        elif e.mimeData().hasFormat("application/EventAreaTable-col"):
            data = e.mimeData().data("application/EventAreaTable-col")
            stream = QDataStream(data, QIODevice.ReadOnly)
            # 得到被拖拽的控件所在位置
            dragCol = stream.readInt()
            value = self.eventTable.cellWidget(1, dragCol).value
            mouseCol = self.eventTable.columnAt(e.pos().x())
            targetCol = -1
            # move to front
            if dragCol > mouseCol and mouseCol != -1:
                targetCol = self.eventTable.getColumnToFront(e.pos().x())
                self.moveToTarget(dragCol, targetCol)
            # move to back
            elif dragCol < mouseCol or mouseCol == -1:
                targetCol = self.eventTable.getColumnToBack(e.pos().x())
                self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.MoveAction)
            e.accept()

            # 发射结束信号
            self.finish.emit()
            # 移动信号
            self.eventMove.emit(dragCol, targetCol, value)
            self.becomeWhite()
        elif e.mimeData().hasFormat("application/EventAreaTable-copy-col"):
            data = e.mimeData().data("application/EventAreaTable-copy-col")
            stream = QDataStream(data, QIODevice.ReadOnly)
            # 得到被复制的控件所在位置
            col = stream.readInt()
            oldValue = self.eventTable.cellWidget(1, col).value
            pixmap = self.eventTable.cellWidget(1, col).pixmap()
            text = self.eventTable.item(3, col).text()
            # 插入一列
            self.eventTable.insertColumn(self.eventTable.fillCount + 1)
            self.eventTable.setEvent(1, self.eventTable.fillCount, pixmap, text)
            self.eventTable.setText(3, self.eventTable.fillCount, text)
            # 给timeLine发射信号
            newValue = self.eventTable.cellWidget(1, self.eventTable.fillCount).value
            self.addEvent.emit(text, pixmap, newValue)
            # 根据鼠标位置进行移动
            dragCol = self.eventTable.fillCount
            targetCol = self.eventTable.getColumnForInsert(e.pos().x())

            if targetCol != -1:
                # 往前移动
                if targetCol < dragCol:
                    self.moveToTarget(dragCol, targetCol)

            e.setDropAction(Qt.CopyAction)
            e.accept()

            # 发射结束信号
            self.finish.emit()
            # 移动信号
            self.eventMove.emit(dragCol, targetCol, newValue)
            # 给event tabs发信号, 让newValue去复制oldValue的属性
            self.eventCopy.emit(oldValue, newValue, text)

            self.becomeWhite()
            self.eventTable.copy = False
        else:
            # 发射结束信号
            self.finish.emit()
            e.ignore()
            self.becomeWhite()

    def dragLeaveEvent(self, e):
        self.finish.emit()
        self.becomeWhite()
        e.ignore()

    def moveToTarget(self, dragCol, targetCol):
        # 将dragCol数据保存
        event = self.eventTable.cellWidget(1, dragCol)
        text = self.eventTable.item(3, dragCol).text()
        # 将dragCol抹掉
        self.eventTable.removeColumn(dragCol)
        # 插入新列
        self.eventTable.insertColumn(targetCol)
        self.eventTable.setEvent(row=1, col=targetCol, name=event.name, pixmap=event.pixmap(), value=event.value)
        self.eventTable.setText(row=3, col=targetCol, text=text)

    def becomeWhite(self):
        # pass
        self.setStyleSheet("background-color:rgba(255,255,255)")

        self.eventTable.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half.png"))
        for col in range(1, self.eventTable.columnCount() - 1):
            self.eventTable.setPixmap(2, col, QPixmap(".\\.\\image\\line.png"))
        self.eventTable.setPixmap(2, self.eventTable.columnCount() - 1, QPixmap(".\\.\\image\\arrow.png"))

    def becomeLightGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211, 0.3)")

        self.eventTable.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half_lightGray.png"))
        for col in range(1, self.eventTable.columnCount() - 1):
            self.eventTable.setPixmap(2, col, QPixmap(".\\.\\image\\line_lightGray.png"))
        self.eventTable.setPixmap(2, self.eventTable.columnCount() - 1, QPixmap(".\\.\\image\\arrow_lightGray.png"))

    def becomeGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211)")

        self.eventTable.setPixmap(2, 0, QPixmap(".\\.\\image\\line_half_gray.png"))
        for col in range(1, self.eventTable.columnCount() - 1):
            self.eventTable.setPixmap(2, col, QPixmap(".\\.\\image\\line_gray.png"))
        self.eventTable.setPixmap(2, self.eventTable.columnCount() - 1, QPixmap(".\\.\\image\\arrow_gray.png"))

    def copyDrag(self):
        # 改变模式
        self.eventTable.copy = True
        self.becomeGray()

    def keyPressEvent(self, e):
        if self.eventTable.copy:
            if e.key() == Qt.Key_Escape:
                self.eventTable.copy = False
                self.becomeWhite()
