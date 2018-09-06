from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QInputDialog, QLineEdit, QShortcut, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence
from .structureItem import StructureItem


class StructureTree(QTreeWidget):
    # (value)
    itemDelete = pyqtSignal(str)
    # 发送到main(parent.value, value)
    timelineDelete = pyqtSignal(str, str)
    itemInIfBranchDelete = pyqtSignal(str, str)
    # (item)
    itemNameChange = pyqtSignal(StructureItem)

    def __init__(self, parent=None):
        super(StructureTree, self).__init__(parent)
        # 菜单
        self.right_button_menu = QMenu()
        self.delete_action = QAction("delete", self.right_button_menu)
        self.rename_action = QAction("rename", self.right_button_menu)
        self.right_button_menu.addAction(self.delete_action)
        self.right_button_menu.addAction(self.rename_action)
        # 快捷键
        self.rename_shortcut = QShortcut(QKeySequence('F2'), self)
        self.rename_shortcut.activated.connect(lambda : self.renameItem(self.currentItem()))

    def contextMenuEvent(self, e):
        item = self.itemAt(e.pos())
        if item and item.value != "Timeline.10001":
            self.delete_action.disconnect()
            self.delete_action.triggered.connect(lambda: self.deleteItem(item))
            self.rename_action.disconnect()
            self.rename_action.triggered.connect(lambda: self.renameItem(item))

            self.right_button_menu.exec(self.mapToGlobal(e.pos()))

    def deleteItem(self, item):
        try:
            parent = item.parent()
            if isinstance(parent, StructureItem):
                parent.removeChild(item)
                self.itemDelete.emit(item.value)
                if item.value.startswith("Timeline"):
                    self.timelineDelete.emit(parent.value, item.value)
                if parent.value.startswith('If_else'):
                    self.itemInIfBranchDelete.emit(parent.value, item.value)
        except Exception:
            print("some errors happen in delete structure item. (structureTree.py)")

    def renameItem(self, item: StructureItem):
        self.itemNameChange.emit(item)
