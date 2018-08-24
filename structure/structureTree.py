from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from .structureItem import StructureItem


class StructureTree(QTreeWidget):
    #
    itemDelete = pyqtSignal(str)
    timelineDelete = pyqtSignal(str, str)
    # (value, name)
    itemNameChange = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(StructureTree, self).__init__(parent)
        # 菜单
        self.right_button_menu = QMenu()
        self.delete_action = QAction("delete", self.right_button_menu)
        self.rename_action = QAction("rename", self.right_button_menu)
        self.right_button_menu.addAction(self.delete_action)
        self.right_button_menu.addAction(self.rename_action)

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
        except Exception:
            print("some errors happen in delete structure item. (structureTree.py)")

    def renameItem(self, item: StructureItem):
        dialog = QInputDialog()
        dialog.setModal(True)
        dialog.setWindowFlag(Qt.WindowCloseButtonHint)
        text, flag = dialog.getText(None, "Rename", "Rename {} to :".format(item.text(0)), QLineEdit.Normal, item.text(0))
        if flag and text:
            self.itemNameChange.emit(item.value, text)
