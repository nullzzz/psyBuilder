import re

from PyQt5.QtCore import pyqtSignal, Qt, QDataStream, QIODevice, QByteArray, QMimeData, QPoint
from PyQt5.QtGui import QDrag, QKeySequence
from PyQt5.QtWidgets import QTreeWidget, QMenu, QShortcut

from app.func import Func
from app.info import Info
from app.kernel import Kernel
from lib import MessageBox
from .structure_node import StructureNode


class StructureTree(QTreeWidget):
    """

    """

    # when node is double clicked, emit signal (widget_id)
    itemDoubleClicked = pyqtSignal(int)
    # when node is double deleted, emit signal (widget_id)
    itemDeleted = pyqtSignal(int)
    # when node is changed, emit(parent_widget_id, widget_id, widget_name)
    itemNameChanged = pyqtSignal(int, int, str)

    def __init__(self):
        super(StructureTree, self).__init__(None)
        # set one column
        self.setColumnCount(1)
        # hide header
        self.setHeaderHidden(True)
        # draggable
        self.setDragEnabled(True)
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.itemChanged.connect(self.dealItemChanged)

    def setMenuAndShortcut(self):
        """

        @return:
        """
        # menu
        self.menu = QMenu()
        self.delete_action = self.menu.addAction(Func.getImage("menu/delete.png", 1), "Delete", self.deleteActionFunc,
                                                 QKeySequence(QKeySequence.Delete))
        self.rename_action = self.menu.addAction(Func.getImage("menu/rename.png", 1), "Rename", self.renameActionFunc,
                                                 QKeySequence("F2"))
        # shortcut
        self.rename_shortcut = QShortcut(QKeySequence('F2'), self)
        self.rename_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.rename_shortcut.activated.connect(self.renameActionFunc)
        self.delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        self.delete_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.delete_shortcut.activated.connect(self.deleteActionFunc)
        self.backspace_shortcut = QShortcut(QKeySequence("Backspace"), self)
        self.backspace_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.backspace_shortcut.activated.connect(self.deleteActionFunc)

    def contextMenuEvent(self, e):
        """

        @param e:
        @return:
        """
        item = self.currentItem()
        if item:
            self.rename_action.setEnabled(False)
            self.delete_action.setEnabled(False)
            if item.widget_id:
                self.delete_action.setEnabled(True)
                if not Func.isWidgetType(item.widget_id, Info.Timeline):
                    self.rename_action.setEnabled(True)
            self.menu.exec(self.mapToGlobal(e.pos()))

    def addNode(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """
        add node to its self
        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # if it has parent node
        if parent_widget_id != -1:
            parent_node: StructureNode = Kernel.Nodes[parent_widget_id]
            node = StructureNode(parent=parent_node, widget_id=widget_id)
            node.setText(0, widget_name)
            # add node
            parent_node.moveChild(index, node)
            # expand node to show its children
            parent_node.setExpanded(True)
        else:
            # create root node
            node: StructureNode = StructureNode(self, widget_id=widget_id)
            node.setText(0, widget_name)
            self.addTopLevelItem(node)
            self.collapseItem(node)
        return node

    def moveNode(self, widget_id: int, index: int):
        """
        move node
        @param widget_id:
        @param index:
        @return:
        """
        node = Kernel.Nodes[widget_id]
        parent = node.parent()
        parent.moveChild(index, node)

    def deleteNode(self, node: StructureNode):
        """

        @return:
        """
        node.parent().removeChild(node)

    def mouseDoubleClickEvent(self, e):
        """

        @param e:
        @return:
        """
        item = self.itemAt(e.pos())
        if item:
            self.itemDoubleClicked.emit(item.widget_id)

    def mouseMoveEvent(self, e):
        """
        drag node to timeline, but we can't move or copy cycle
        @param e:
        @return:
        """
        item = self.itemAt(e.pos())
        if item and item.widget_id:
            widget_id = item.widget_id
            if e.modifiers() == Qt.ControlModifier:
                # ctrl -> copy
                if not Func.isWidgetType(widget_id, Info.Cycle):
                    self.copyDrag(widget_id)
            elif e.modifiers() == Qt.ShiftModifier:
                # todo move to timeline (shift -> move)
                # if not Func.isWidgetType(widget_id, Info.Cycle):
                #     self.moveDrag(widget_id)
                pass
            else:
                # none -> refer
                self.referDrag(widget_id)

    def moveDrag(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeInt(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureMoveToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def copyDrag(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeInt(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureCopyToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def referDrag(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeInt(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureReferToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def dealItemChanged(self, item: StructureNode, index: int):
        """

        @return:
        """
        if item.changed():
            if re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", item.text(0)):
                if Func.checkWidgetNameExisted(item.text(0)):
                    MessageBox.information(self, "warning", "Name existed.")
                    item.redo()
                else:
                    self.itemNameChanged.emit(item.parent().widget_id, item.widget_id, item.text(0))
                    item.save()
            else:
                MessageBox.information(self, "warning",
                                       "Name must start with a letter and contain only letters, numbers and _.")
                item.redo()

    def deleteActionFunc(self):
        """
        delete action
        @return:
        """
        # get current item
        item = self.currentItem()
        if type(item) == StructureNode:
            self.itemDeleted.emit(item.widget_id)

    def renameActionFunc(self):
        """

        @return:
        """
        # get current item
        item = self.currentItem()
        if type(item) == StructureNode and not Func.isWidgetType(item.widget_id, Info.Timeline):
            self.editItem(item, 0)
