from PyQt5.QtWidgets import QTreeWidget, QMenu, QAction, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal


class StructureTree(QTreeWidget):
    itemDeleted = pyqtSignal(str)
    timeLineDeleted = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(StructureTree, self).__init__(parent)

    def contextMenuEvent(self, e):
        item = self.itemAt(e.pos())
        if item and item.value != "TimeLine.10001":
            menu = QMenu()
            delete = QAction("delete", menu)
            delete.triggered.connect(lambda : self.deleteItem(item))
            menu.addAction(delete)
            menu.exec(self.mapToGlobal(e.pos()))

    def deleteItem(self, item):
        parent = item.parent()
        value = item.value
        if isinstance(parent, QTreeWidgetItem):
            parent.removeChild(item)
            self.itemDeleted.emit(value)
            try:
                # 如果时timeLine被删除要包括删除其所在cycle中的那一行
                if value.startswith("TimeLine."):
                    self.timeLineDeleted.emit(parent.value, value)
            except Exception:
                print("some errors happen in getting tree item's parent value.")
