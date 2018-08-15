from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal
from .structureItem import StructureItem


class StructureTree(QTreeWidget):
    #
    itemDelete = pyqtSignal(str)
    timelineDelete = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(StructureTree, self).__init__(parent)

    def contextMenuEvent(self, e):
        item = self.itemAt(e.pos())
        if item and item.value != "Timeline.10001":
            menu = QMenu()
            delete = QAction("delete", menu)
            delete.triggered.connect(lambda: self.deleteItem(item))
            menu.addAction(delete)
            menu.exec(self.mapToGlobal(e.pos()))

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



