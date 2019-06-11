from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import Qt

from app.func import Func


class StructureNode(QTreeWidgetItem):
    def __init__(self, parent=None, widget_id=''):
        super(StructureNode, self).__init__(parent)

        self.widget_id = widget_id
        widget_type = widget_id.split(".")[0]
        self.setIcon(0, Func.getWidgetImage(widget_type))
        self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
