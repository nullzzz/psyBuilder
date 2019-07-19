from PyQt5.QtCore import pyqtSignal, Qt, QDataStream, QIODevice, QByteArray, QMimeData, QPoint
from PyQt5.QtGui import QKeySequence, QDrag
from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QShortcut, QMessageBox

from app.func import Func
from app.info import Info
from .structure_node import StructureNode


# 此中函数一般只发信号而不做实际行动
class StructureTree(QTreeWidget):
    # 节点删除会影响到widget_tabs中的tab，和该节点所处widget (widget_id, sender -> widget_tabs, structure)
    nodeDelete = pyqtSignal(str, str)
    # 新增加一个sender表示是structure tree发送的(widget_id, name, str -> widget_tabs, structure)
    nodeNameChange = pyqtSignal(str, str, str)
    # 双击节点打开widget (widget_id -> widget_tabs)
    widgetOpen = pyqtSignal(str)

    def __init__(self, parent=None):
        super(StructureTree, self).__init__(parent=parent)
        # 初始化
        self.setDragEnabled(True)
        self.setColumnCount(1)
        # self.setHeaderLabel("E-Object")
        self.setHeaderHidden(True)
        timeline_node = StructureNode(self, f'{Info.TIMELINE}.0')
        timeline_node.setText(0, Info.TIMELINE)
        self.addTopLevelItem(timeline_node)
        self.collapseItem(timeline_node)
        self.expandAll()
        # data
        Info.WID_NODE[f"{Info.TIMELINE}.0"] = timeline_node
        Info.NAME_WID[Info.TIMELINE] = [f'{Info.TIMELINE}.0']
        self.edit_wid = ''
        self.focus = False
        #
        self.setMenuAndShortcut()
        #
        self.linkSignals()

    def linkSignals(self):
        self.itemChanged.connect(self.renameNode)

    def setMenuAndShortcut(self):
        # 菜单
        self.right_button_menu = QMenu()
        self.delete_action = QAction("Delete", self.right_button_menu)
        self.rename_action = QAction("Rename", self.right_button_menu)
        self.delete_action.triggered.connect(self.deleteNode)
        self.rename_action.triggered.connect(self.editNode)
        self.right_button_menu.addAction(self.delete_action)
        self.right_button_menu.addAction(self.rename_action)
        # 快捷键
        self.rename_shortcut = QShortcut(QKeySequence('F2'), self)
        self.rename_shortcut.activated.connect(self.editNode)

    def contextMenuEvent(self, e):
        node = self.itemAt(e.pos())
        if node and node.widget_id != f"{Info.TIMELINE}.0":
            self.rename_action.setEnabled(True)
            if node.widget_id.startswith(Info.TIMELINE):
                self.rename_action.setEnabled(False)
            self.right_button_menu.exec(self.mapToGlobal(e.pos()))

    def editNode(self, node: StructureNode = None):
        try:
            # 必须在当前窗口中
            if self.focus:
                # 保证node非None
                if not node:
                    node: StructureNode = self.currentItem()
                if node:
                    # 初始timeline不可修改
                    if node.widget_id != f'{Info.TIMELINE}.0':
                        self.old_name = node.text(0)
                        self.edit_wid = node.widget_id
                        self.editItem(node, 0)
        except Exception as e:
            print(f"error {e} happens in edit node. [structure/structure_tree.py]")
            Func.log(e, True)

    def renameNode(self, node: StructureNode, index):
        try:
            if node.widget_id == self.edit_wid:
                # 检测new_name的合法性
                new_name = node.text(0)
                # 在这里timeline的name也不可以是引用的值
                if new_name:
                    validity, tips = Func.checkNameValidity(name=new_name)
                    if validity:
                        # 先将
                        self.edit_wid = ''
                        node.setText(0, self.old_name)
                        self.old_name = ''
                        self.nodeNameChange.emit(node.widget_id, new_name, 'structure_tree')
                    else:
                        QMessageBox.information(self, 'Warning', tips)
                        # 复原至初始状态重来
                        self.edit_wid = ''
                        node.setText(0, self.old_name)
                        self.old_name = ''
                else:
                    QMessageBox.information(self, 'Warning', "Name can't be none.")
                    # 复原至初始状态重来
                    self.edit_wid = ''
                    node.setText(0, self.old_name)
                    self.old_name = ''
        except Exception as e:
            print(f"error {e} happens in rename node. [structure/structure_tree.py]")
            Func.log(e, True)

    def focusInEvent(self, QFocusEvent):
        """
        设置focus参数，在当前窗口中，快捷键才能使用
        :param QFocusEvent:
        :return:
        """
        super(StructureTree, self).focusInEvent(QFocusEvent)
        # 设置参数，在当前窗口中，快捷键才能使用
        self.focus = True

    def focusOutEvent(self, QFocusEvent):
        """
        改变focus参数
        :param QFocusEvent:
        :return:
        """
        super(StructureTree, self).focusOutEvent(QFocusEvent)
        self.focus = False

    def deleteNode(self):
        try:
            node: StructureNode = self.currentItem()
            # 初始timeline不可删除
            if node and node.widget_id != f'{Info.TIMELINE}.0':
                self.nodeDelete.emit(node.widget_id, 'structure_tree')
        except Exception as e:
            print(f"delete node error. [structure_tree.py]")

    def mouseDoubleClickEvent(self, e):
        # super(StructureTree, self).mouseDoubleClickEvent(e)
        if self.currentItem():
            self.widgetOpen.emit(self.currentItem().widget_id)

    def mouseMoveEvent(self, e):
        try:
            node: StructureNode = self.itemAt(e.pos())
            if node:
                widget_id = node.widget_id
                if not widget_id.startswith(Info.TIMELINE):
                    # copy
                    if e.modifiers() == Qt.ControlModifier:
                        self.copyDrag(widget_id)
                    # move
                    elif e.modifiers() == Qt.ShiftModifier:
                        self.moveDrag(widget_id)
                    # refer
                    else:
                        self.referDrag(widget_id)
        except Exception as e:
            print(f"error {e} happens in mouse move event. [structure/structure_tree.py]")
            Func.log(e, True)

    def moveDrag(self, widget_id):
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData("structure_tree/move-wid", data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def copyDrag(self, widget_id):
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData('structure_tree/copy-wid', data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def referDrag(self, widget_id):
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData('structure_tree/refer-wid', data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()
