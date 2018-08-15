from PyQt5.QtWidgets import QTreeWidgetItem


class StructureItem(QTreeWidgetItem):
    def __init__(self, parent=None, value=''):
        super(StructureItem, self).__init__(parent)

        self.value = value
