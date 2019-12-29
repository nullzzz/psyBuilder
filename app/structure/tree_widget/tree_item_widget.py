from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from app.func import Func
from app.info import Info


class TreeItemWidget(QTreeWidgetItem):
    """
    
    """

    def __init__(self, parent=None, widget_id: int = None):
        super(TreeItemWidget, self).__init__(parent)
        self.widget_id = widget_id
        # set its icon
        widget_type = Info.WidgetType[widget_id // Info.MaxWidgetCount]
        self.setIcon(0, Func.getImage(f"widgets/{widget_type}", 1))
        self.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
