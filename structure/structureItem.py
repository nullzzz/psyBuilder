from PyQt5.QtWidgets import QTreeWidgetItem

from getImage import getImage


class StructureItem(QTreeWidgetItem):
    def __init__(self, parent=None, value=''):
        super(StructureItem, self).__init__(parent)

        self.value = value
        widget_type = value.split(".")[0]
        self.setIcon(0, getImage(widget_type))
