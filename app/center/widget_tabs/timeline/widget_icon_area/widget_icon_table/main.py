from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFrame, QLabel, QMenu, QAction, \
    QAbstractItemView

from app.func import Func
from app.lib import NoDash
from lib.psy_message_box import PsyMessageBox as QMessageBox
from .sign_table import SignTable
from ...widget_icon import WidgetIcon


class WidgetIconTable(QTableWidget):
    # 单击时将widget icon所指widget的properties显示到properties, 发送widget id去info中获取 (widget_id -> properties)
    propertiesShow = pyqtSignal(str)
    # 和上一个信号相似 (widget_id -> attributes)
    attributesShow = pyqtSignal(str)
    # 双击打开一个tab (widget_id, widget_name -> widget_tabs)
    widgetOpen = pyqtSignal(str, str)
    # widget icon name的变化 (widget_id, widget_name -> structure, widget_tabs)
    widgetIconNameChange = pyqtSignal(str, str)
    # widget icon在widget icon table中被删除 (widget_id -> structure, widget_tabs)
    widgetIconDelete = pyqtSignal(str)

    # data
    # 固定高宽
    WIDTH = 50
    HEIGHT = WidgetIcon.SIZE + 10
    #
    Initial_Length = 10

    def __init__(self, parent=None, widget_id=''):
        super(WidgetIconTable, self).__init__(parent)
        # 美化（隐藏表头之类）
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        self.setItemDelegate(NoDash())
        self.setStyleSheet("""
            QMenu {
    background-color: white;
    border: 0px solid;
    border-radius: 2px;
    margin: 2px;
    min-width: 78px;
}

QMenu::Item {
    padding: 2px 25px 2px 20px;
}

QMenu::Item:selected {
    border-color: transparent;
    background: rgb(153,196,244);
}

QMenu::Item:!enabled {
    border-color: transparent;
    background: rgb(211,211,211);
}

QMenu::icon:checked {
    background: rgb(210,210,210);
    border: 0.5px inset rgb(210,210,210);
    position: absolute;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 13px;
    height: 13px;
}
        """)
        # 数据
        self.widget_id = widget_id
        self.widget_icon_count = 0
        self.edit_row_col = [-1, -1]
        self.is_fill = False
        self.old_name = ''
        self.up_sign = SignTable(sign="timeline/arrow_up.png")
        self.down_sign = SignTable(sign="timeline/arrow_down.png")
        self.focus = False
        # 初始化
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        # 行
        self.setRowCount(5)
        self.setRowHeight(1, WidgetIconTable.HEIGHT)
        # 列
        self.setColumnCount(WidgetIconTable.Initial_Length)
        self.setColumnWidth(0, WidgetIconTable.WIDTH)
        for i in range(1, WidgetIconTable.Initial_Length - 1):
            self.setColumnWidth(i, WidgetIconTable.WIDTH * 2)
        self.setColumnWidth(9, WidgetIconTable.WIDTH)

        # 第0，4行：sign table
        self.setSpan(0, 0, 1, WidgetIconTable.Initial_Length)
        self.setCellWidget(0, 0, self.down_sign)
        self.setSpan(4, 0, 1, WidgetIconTable.Initial_Length)
        self.setCellWidget(4, 0, self.up_sign)
        self.up_sign.setColumnCount(WidgetIconTable.Initial_Length - 1)
        self.down_sign.setColumnCount(WidgetIconTable.Initial_Length - 1)

        for i in range(0, WidgetIconTable.Initial_Length - 1):
            self.up_sign.setColumnWidth(i, WidgetIconTable.WIDTH * 2)
        for i in range(0, WidgetIconTable.Initial_Length - 1):
            self.down_sign.setColumnWidth(i, WidgetIconTable.WIDTH * 2)

        self.setRowHeight(0, 100)
        self.setRowHeight(4, 100)

        # 第3行：arrow line
        for col in range(0, WidgetIconTable.Initial_Length - 1):
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsSelectable)
            self.setItem(1, col, item)
            item_1 = QTableWidgetItem("")
            item_1.setFlags(Qt.ItemIsSelectable)
            self.setItem(3, col, item_1)

        self.setPixmap(2, 0, QPixmap(Func.getImage("line_half.png")))
        for col in range(1, WidgetIconTable.Initial_Length - 1):
            self.setPixmap(2, col, QPixmap(Func.getImage("line.png")))
        self.setPixmap(2, WidgetIconTable.Initial_Length - 1, QPixmap(Func.getImage("arrow.png")))

        # 可拖拽
        self.setDragEnabled(True)
        # 连接信号
        self.linkSignals()
        # menu and shortcut
        self.setMenuAndShortcut()

    def linkSignals(self):
        self.itemChanged.connect(self.changeWidgetName)

    def setMenuAndShortcut(self):
        self.right_button_menu = QMenu(self)
        # delete action
        self.delete_action = QAction("Delete", self.right_button_menu)
        # copy action
        # self.copy_action = QAction("copy", self.right_button_menu)

        self.right_button_menu.addAction(self.delete_action)
        # short cut
        # self.backspace_shortcut = QShortcut(QKeySequence("BackSpace"), self)
        # self.backspace_shortcut.activated.connect(self.deleteWidgetIcon)

    def contextMenuEvent(self, e):
        try:
            col = self.columnAt(e.pos().x())
            row = self.rowAt(e.pos().y())
            if col in range(1, self.widget_icon_count + 1) and row == 1:
                # delete action
                self.delete_action.disconnect()
                self.delete_action.triggered.connect(lambda: self.removeColumn(col, True))
                # copy action
                self.right_button_menu.popup(self.mapToGlobal(e.pos()))
        except Exception as e:
            print(f"error {e} happens in generate menu. [widget_icon_table/main.py]")
            Func.log(e, True)

    def setWidgetIcon(self, col, widget_type, widget_id=''):
        widget_icon = WidgetIcon(widget_type=widget_type, widget_id=widget_id)
        widget_icon.setAlignment(Qt.AlignCenter)
        self.setCellWidget(1, col, widget_icon)
        return widget_icon.widget_id

    def setWidgetName(self, col, name):
        item = QTableWidgetItem(name)
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(3, col, item)

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

    def removeColumn(self, col, send_signal=False):
        try:
            # 如果是删除了widget icon需要发送信号
            if send_signal:
                self.widgetIconDelete.emit(self.cellWidget(1, col).widget_id)
            # remove, 如果没有满要保证最短长度
            if self.widget_icon_count > WidgetIconTable.Initial_Length - 2:
                super().removeColumn(col)
                self.up_sign.removeColumn(self.columnCount() - 1)
                self.down_sign.removeColumn(self.columnCount() - 1)
            else:
                # 保证长度要先在末尾加上一列
                super().insertColumn(WidgetIconTable.Initial_Length - 1)
                self.setPixmap(2, WidgetIconTable.Initial_Length - 1, QPixmap(Func.getImage("line.png")))
                self.setColumnWidth(WidgetIconTable.Initial_Length - 1, self.WIDTH * 2)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsSelectable)
                self.setItem(1, WidgetIconTable.Initial_Length - 1, item)
                item1 = QTableWidgetItem("")
                item1.setFlags(Qt.ItemIsSelectable)
                self.setItem(3, WidgetIconTable.Initial_Length - 1, item1)
                #
                super().removeColumn(col)
            # data,
            self.widget_icon_count -= 1
            if self.widget_icon_count < WidgetIconTable.Initial_Length - 2:
                self.is_fill = False
        except Exception as e:
            print(f"error {e} happens in remove column. [widget_icon_table/main.py]")
            Func.log(e, True)

    def insertColumn(self, col):
        try:
            if self.widget_icon_count >= WidgetIconTable.Initial_Length - 2:
                super().insertColumn(col)
                self.setPixmap(2, col, QPixmap(Func.getImage("line.png")))
                self.setColumnWidth(col, WidgetIconTable.WIDTH * 2)
                self.up_sign.insertColumn(self.up_sign.columnCount())
                self.up_sign.setColumnWidth(self.up_sign.columnCount() - 1, self.WIDTH * 2)
                self.down_sign.insertColumn(self.down_sign.columnCount())
                self.down_sign.setColumnWidth(self.down_sign.columnCount() - 1, self.WIDTH * 2)
            else:
                # 如果没有满，只是假的insert，实际是把那一列变成可用列
                super().removeColumn(WidgetIconTable.Initial_Length - 2)
                super().insertColumn(col)
                self.setPixmap(2, col, QPixmap(Func.getImage("line.png")))
                self.setColumnWidth(col, WidgetIconTable.WIDTH * 2)
            # data
            self.widget_icon_count += 1
            if self.widget_icon_count >= WidgetIconTable.Initial_Length - 2:
                self.is_fill = True
        except Exception as e:
            print(f"error {e} happens in insert column. [widget_icon_table/main.py]")
            Func.log(e, True)

    def mouseMoveEvent(self, e):
        try:
            # 合法可拖动区域
            if self.columnAt(e.pos().x()) in range(1, self.widget_icon_count + 1) and \
                    self.rowAt(e.pos().y()) in range(1, 3):
                if e.modifiers() == Qt.ControlModifier:
                    # copy模式
                    self.copyDrag()
                else:
                    # move模式
                    self.moveDrag()
        except Exception as e:
            print(f"error {e} happens in mouse move event. [widget_icon_table/main.py]")
            Func.log(e, True)

    def moveDrag(self):
        col = self.currentColumn()
        # 有效列才能拖动
        if 1 <= col <= self.widget_icon_count:
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeInt(col)
            mime_data = QMimeData()
            mime_data.setData("widget_icon_table/move-col", data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec()

    def copyDrag(self):
        col = self.currentColumn()
        if 1 <= col <= self.widget_icon_count:
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeInt(col)
            mime_data = QMimeData()
            mime_data.setData("widget_icon_table/copy-col", data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec()

    # 只会存在moveToFront, return -1即无需移动
    def getColumnForInsert(self, x):
        col = self.columnAt(x)

        if col == 0:
            return 1
        if col != -1:
            temp_col = self.columnAt(x + WidgetIconTable.WIDTH)
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
        temp_col = self.columnAt(x + WidgetIconTable.WIDTH)
        return temp_col

    # col > dragCol
    def getColumnToBack(self, x):
        col = self.columnAt(x)
        # 在末尾
        if col == self.columnCount() - 1:
            return self.widget_icon_count
        if col != -1:
            col_temp = self.columnAt(x - self.WIDTH)
            if not self.is_fill and col_temp > self.widget_icon_count:
                return self.widget_icon_count
            return col_temp
        else:
            return self.widget_icon_count

    def showSign(self, x):
        try:
            col = self.columnAt(x)
            icon_col = col

            if not self.is_fill:
                if col == 0:
                    icon_col = 0
                elif col > self.widget_icon_count or col == -1:
                    icon_col = self.widget_icon_count
                else:
                    col_temp = self.columnAt(x + WidgetIconTable.WIDTH)
                    if col_temp == col:
                        icon_col = col - 1
            else:
                if col == self.columnCount() - 1 or col == -1:
                    icon_col = self.up_sign.columnCount() - 1
                elif col == 0:
                    icon_col = 0
                else:
                    col_temp = self.columnAt(x + WidgetIconTable.WIDTH)
                    if col_temp == -1:
                        icon_col = self.widget_icon_count
                    if col_temp > col:
                        pass
                    elif col == col_temp:
                        icon_col = col - 1
            # 显示sign
            self.up_sign.showSign(icon_col)
            self.down_sign.showSign(icon_col)
        except Exception as e:
            print(f"error {e} happens in show sign. [widget_icon_table/main.py]")
            Func.log(e, True)

    def hideSign(self):
        self.up_sign.hideSign()
        self.down_sign.hideSign()

    def moveWidgetIcon(self, drag_col, target_col):
        try:
            if drag_col != target_col:
                # 将drag_col数据保存
                widget_id = self.cellWidget(1, drag_col).widget_id
                widget_name = self.item(3, drag_col).text()
                # 将drag_col抹掉
                self.removeColumn(drag_col)
                # 插入新列
                self.insertColumn(target_col)
                self.setWidgetIcon(target_col, widget_id.split('.')[0], widget_id)
                self.setWidgetName(target_col, widget_name)
        except Exception as e:
            print("error happens in move icon to target. [widget_icon_table/main.py]")
            Func.log(e, True)

    def mouseDoubleClickEvent(self, e):
        # 只支持鼠标左键双击
        if e.buttons() == Qt.LeftButton:
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())
            # 有效列
            if col in range(1, self.widget_icon_count + 1):
                if row == 1:
                    # icon
                    widget_id = self.cellWidget(row, col).widget_id
                    widget_name = self.item(3, col).text()
                    self.widgetOpen.emit(widget_id, widget_name)
                elif row == 3:
                    # 修改widget name
                    self.setFocus()
                    self.old_name = self.item(row, col).text()
                    self.editItem(self.item(row, col))
                    self.edit_row_col = [row, col]

    def changeWidgetName(self, item: QTableWidgetItem):
        # 保证是name的修改，而不是其他的变化
        if self.edit_row_col[0] == item.row() and self.edit_row_col[1] == item.column() and item.text():
            name = item.text()
            self.edit_row_col = [-1, -1]
            validity, tips = Func.checkNameValidity(name)
            if validity:
                self.widgetIconNameChange.emit(self.cellWidget(1, item.column()).widget_id, item.text())
            else:
                QMessageBox.information(self, 'Warning', tips)
                item.setText(self.old_name)
            self.old_name = ''

    def getProperties(self, row, col):
        if row in (1, 3) and col in range(0, self.fill_count + 1):
            value = self.cellWidget(1, col).value
            self.propertiesShow.emit(value)

    def deleteWidgetIcon(self):
        try:
            if self.currentColumn() in range(1, self.widget_icon_count + 1):
                self.removeColumn(self.currentColumn(), True)
        except Exception as e:
            print(f"error {e} happens in delete icon. [widget_icon_table/main.py]")
            Func.log(e, True)

    def mousePressEvent(self, e):
        try:
            super(WidgetIconTable, self).mousePressEvent(e)
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())
            if row in range(1, 4) and col in range(1, self.widget_icon_count + 1):
                self.propertiesShow.emit(self.cellWidget(1, col).widget_id)
                self.attributesShow.emit(self.cellWidget(1, col).widget_id)
        except Exception as e:
            print(f"error {e} happens in show icon properties. [widget_icon_table/main.py]")
            Func.log(e, True)

    def getInfo(self):
        info = {
            'widget_icon_count': self.widget_icon_count,
            'is_fill': self.is_fill,
            'widget_icons': []
        }
        for col in range(1, self.widget_icon_count + 1):
            info['widget_icons'].append([self.cellWidget(1, col).widget_id, self.item(3, col).text()])
        return info

    def restore(self, info):
        try:
            # 先将timeline中的数据清除, 即删除所有的widget
            total_count = self.widget_icon_count + 1
            for i in range(1, total_count):
                self.removeColumn(1, True)
            # 再往其中添加
            widget_icon_count = info['widget_icon_count']
            self.is_fill = info['is_fill']
            for i in range(1, widget_icon_count + 1):
                widget_id = info['widget_icons'][i - 1][0]
                name = info['widget_icons'][i - 1][1]
                self.insertColumn(self.widget_icon_count + 1)
                self.setWidgetIcon(self.widget_icon_count, widget_id.split('.')[0],
                                   widget_id)
                self.setWidgetName(self.widget_icon_count, name)
        except Exception as e:
            print(f"error {e} happens in restore. [widget_icon_table/main.py]")
            Func.log(e, True)

    def focusInEvent(self, QFocusEvent):
        """
        得到焦点进行记录
        :param QFocusEvent:
        :return:
        """
        super(WidgetIconTable, self).focusInEvent(QFocusEvent)
        self.focus = True

    def focusOutEvent(self, QFocusEvent):
        """
        在失去焦点时进行记录
        :param QFocusEvent:
        :return:
        """
        super(WidgetIconTable, self).focusOutEvent(QFocusEvent)
        self.focus = False

    def deleteShortcut(self):
        """
        删除快捷键对应功能函数
        :return:
        """
        try:
            col = self.currentColumn()
            # 如果col有效
            if col in range(1, self.widget_icon_count + 1):
                self.removeColumn(col, True)
        except:
            pass
