from PyQt5.QtWidgets import QVBoxLayout, QFrame, QTableWidgetItem
from PyQt5.QtCore import Qt, QDataStream, QIODevice
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from .iconTable import IconTable
from structure.main import Structure

import time


class IconArea(QFrame):
    # sign显示
    signShow = pyqtSignal(int)
    dragFinish = pyqtSignal()
    # 经过timeline得其value, 后传至structure
    iconAdd = pyqtSignal(str, QPixmap, str)
    iconMove = pyqtSignal(int, int, str)
    iconCopy = pyqtSignal(str, str, str)
    # copy drag finish ()
    copyDragFinish = pyqtSignal()

    def __init__(self, parent=None, timeline_value='Timeline.10001'):
        super(IconArea, self).__init__(parent)
        self.row_height = 0
        self.icon_table = IconTable(timeline_value=timeline_value)
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
        self.copyDragFinish.connect(self.icon_table.copyDragFinish)
        self.icon_table.copyIconToNextCol.connect(self.copyIconToNext)
        self.icon_table.copyDragBegin.connect(self.copyDrag)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("application/IconBar-text-pixmap") or \
                e.mimeData().hasFormat("application/IconTable-col") or \
                e.mimeData().hasFormat("application/IconTable-copy-col"):
            if self.icon_table.is_copy_module:
                self.becomeGray()
            else:
                self.becomeLightGray()

            e.setDropAction(Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        try:
            if e.mimeData().hasFormat("application/IconBar-text-pixmap") or \
                    e.mimeData().hasFormat("application/IconTable-col") or \
                    e.mimeData().hasFormat("application/IconTable-copy-col"):
                # 给iconTable发送x坐标
                self.signShow.emit(e.pos().x())

                e.setDropAction(Qt.CopyAction)
                e.accept()
            else:
                e.ignore()
        except Exception as e:
            print("error {} happens in drop move icon. [icoaArea/main.py]".format(e))

    def dropEvent(self, e):
        # drag from icon bar
        try:
            if e.mimeData().hasFormat("application/IconBar-text-pixmap"):
                data = e.mimeData().data("application/IconBar-text-pixmap")
                stream = QDataStream(data, QIODevice.ReadOnly)
                pixmap = QPixmap(1, 1)
                # 读出数据
                text = stream.readQString()
                stream >> pixmap
                # 保证行高度
                if self.row_height < pixmap.size().height() + 10:
                    self.row_height = pixmap.size().height() + 10
                    self.icon_table.setRowHeight(1, self.row_height)

                # 插入一列
                self.icon_table.insertColumn(self.icon_table.fill_count + 1)
                self.icon_table.setIcon(1, self.icon_table.fill_count, pixmap, text)

                # 给timeLine发射信号
                value = self.icon_table.cellWidget(1, self.icon_table.fill_count).value
                text = Structure.getName(value, text)
                self.iconAdd.emit(text, pixmap, value)
                # 新列名称
                self.icon_table.setText(3, self.icon_table.fill_count, text)

                # 根据鼠标位置进行移动
                drag_col = self.icon_table.fill_count
                target_col = self.icon_table.getColumnForInsert(e.pos().x())

                if target_col != -1:
                    # 往前移动
                    if target_col < drag_col:
                        self.moveToTarget(drag_col, target_col)

                e.setDropAction(Qt.CopyAction)
                e.accept()

                # 发射结束信号
                self.dragFinish.emit()
                # 移动信号
                self.iconMove.emit(drag_col, target_col, value)
                self.becomeWhite()
                self.copyDragFinish.emit()
            # move from icon table
            elif e.mimeData().hasFormat("application/IconTable-col"):
                data = e.mimeData().data("application/IconTable-col")
                stream = QDataStream(data, QIODevice.ReadOnly)
                # 得到被拖拽的控件所在位置
                drag_col = stream.readInt()
                value = self.icon_table.cellWidget(1, drag_col).value
                mouseCol = self.icon_table.columnAt(e.pos().x())
                target_col = -1
                # move to front
                if drag_col > mouseCol and mouseCol != -1:
                    target_col = self.icon_table.getColumnToFront(e.pos().x())
                    self.moveToTarget(drag_col, target_col)
                # move to back
                elif drag_col < mouseCol or mouseCol == -1:
                    target_col = self.icon_table.getColumnToBack(e.pos().x())
                    self.moveToTarget(drag_col, target_col)

                e.setDropAction(Qt.MoveAction)
                e.accept()

                # 发射结束信号
                self.dragFinish.emit()
                # 移动信号
                self.iconMove.emit(drag_col, target_col, value)
                self.becomeWhite()
                self.copyDragFinish.emit()
            # copy from icon table
            elif e.mimeData().hasFormat("application/IconTable-copy-col"):
                data = e.mimeData().data("application/IconTable-copy-col")
                stream = QDataStream(data, QIODevice.ReadOnly)
                # 得到被复制的控件所在位置
                col = stream.readInt()
                old_value = self.icon_table.cellWidget(1, col).value
                pixmap = self.icon_table.cellWidget(1, col).pixmap()
                text = self.icon_table.item(3, col).text()
                # 插入一列
                self.icon_table.insertColumn(self.icon_table.fill_count + 1)
                self.icon_table.setIcon(1, self.icon_table.fill_count, pixmap, text)

                # newValue 由于复制, icon构造函数中, value默认采用text后缀count, 故可能存在错误
                widget_type = old_value.split('.')[0]
                self.icon_table.cellWidget(1, self.icon_table.fill_count).changeType(widget_type)
                new_value = self.icon_table.cellWidget(1, self.icon_table.fill_count).value
                text = Structure.getName(new_value, text, True, text)
                self.icon_table.setText(3, self.icon_table.fill_count, text)
                # 给timeLine发射信号
                self.iconAdd.emit(text, pixmap, new_value)
                # 根据鼠标位置进行移动
                drag_col = self.icon_table.fill_count
                target_col = self.icon_table.getColumnForInsert(e.pos().x())

                if target_col != -1:
                    # 往前移动
                    if target_col < drag_col:
                        self.moveToTarget(drag_col, target_col)

                e.setDropAction(Qt.CopyAction)
                e.accept()

                # 发射结束信号
                self.dragFinish.emit()
                # 移动信号
                self.iconMove.emit(drag_col, target_col, new_value)
                # 给icon tabs发信号, 让new value去复制old value的属性
                self.iconCopy.emit(old_value, new_value, text)

                self.becomeWhite()
                self.copyDragFinish.emit()
            else:
                # 发射结束信号
                self.dragFinish.emit()
                e.ignore()
                self.becomeWhite()
        except Exception as e:
            print("error {} happens in drop icon. [iconArea/main.py]".format(e))

    def dragLeaveEvent(self, e):
        self.dragFinish.emit()
        self.becomeWhite()
        e.ignore()

    def moveToTarget(self, drag_col, target_col):
        try:
            # 将drag_col数据保存
            event = self.icon_table.cellWidget(1, drag_col)
            text = self.icon_table.item(3, drag_col).text()
            # 将drag_col抹掉
            self.icon_table.removeColumn(drag_col)
            # 插入新列
            self.icon_table.insertColumn(target_col)
            self.icon_table.setIcon(row=1, col=target_col, name=event.name, pixmap=event.pixmap(), value=event.value)
            self.icon_table.setText(row=3, col=target_col, text=text)
        except Exception:
            print("error happens in move icon to target. [iconArea/main.py]")

    def becomeWhite(self):
        # pass
        self.setStyleSheet("background-color:rgba(255,255,255)")

        self.icon_table.setPixmap(2, 0, QPixmap("image/line_half.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap("image/line.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap("image/arrow.png"))

    def becomeLightGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211, 0.3)")

        self.icon_table.setPixmap(2, 0, QPixmap("image/line_half_lightGray.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap("image/line_lightGray.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap("image/arrow_lightGray.png"))

    def becomeGray(self):
        # pass
        self.setStyleSheet("background-color:rgba(211,211,211)")

        self.icon_table.setPixmap(2, 0, QPixmap("image/line_half_gray.png"))
        for col in range(1, self.icon_table.columnCount() - 1):
            self.icon_table.setPixmap(2, col, QPixmap("image/line_gray.png"))
        self.icon_table.setPixmap(2, self.icon_table.columnCount() - 1, QPixmap("image/arrow_gray.png"))

    def copyDrag(self):
        # 改变模式
        self.icon_table.is_copy_module = True
        self.becomeGray()

    def copyIconToNext(self, col):
        try:
            # 获取被复制的icon的属性
            old_value = self.icon_table.cellWidget(1, col).value
            pixmap = self.icon_table.cellWidget(1, col).pixmap()
            text = self.icon_table.item(3, col).text()
            # 插入一列
            self.icon_table.insertColumn(col + 1)
            self.icon_table.setIcon(1, col + 1, pixmap, text)

            # newValue 由于复制, icon构造函数中, value默认采用text后缀count, 故可能存在错误
            widget_type = old_value.split('.')[0]
            self.icon_table.cellWidget(1, col + 1).changeType(widget_type)
            new_value = self.icon_table.cellWidget(1, col + 1).value

            # name根据一定规则去命名, 避免重复
            text = Structure.getName(new_value, text, True, text)
            self.icon_table.setText(3, col + 1, text)

            # 给timeLine发射信号
            self.iconAdd.emit(text, pixmap, new_value)
            # 给icon tabs发信号, 让new value去复制old value的属性
            self.iconCopy.emit(old_value, new_value, text)
            # 移动信号
            self.iconMove.emit(self.icon_table.fill_count, col + 1, new_value)
        except Exception as e:
            print("error {} happens in just copy icon. [iconArea/main.py]".format(e))
