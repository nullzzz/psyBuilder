from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem

from app.func import Func
from app.info import Info


class StructureNode(QTreeWidgetItem):
    """

    """

    def __init__(self, parent=None, widget_id: int = None):
        super(StructureNode, self).__init__(parent)
        self.old_text = ""
        self.widget_id = widget_id
        # set its icon
        widget_type = Info.WidgetType[Func.getWidgetType(widget_id)]
        self.setIcon(0, Func.getImage(f"widgets/{widget_type}", 1))
        if widget_id:
            self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        else:
            self.setFlags(Qt.NoItemFlags | Qt.ItemIsSelectable | Qt.ItemIsEnabled)


    def moveChild(self, index: int, node: QTreeWidgetItem):
        """
        move child
        @param index:
        @param node:
        @return:
        """
        self.removeChild(node)
        self.insertChild(index, node)

    def setText(self, p_int, p_str):
        """
        save text as old_text
        @param p_int:
        @param p_str:
        @return:
        """
        self.old_text = p_str
        super(StructureNode, self).setText(p_int, p_str)

    def save(self):
        """

        @return:
        """
        self.old_text = self.text(0)

    def redo(self):
        """

        @return:
        """
        self.setText(0, self.old_text)

    def changed(self):
        """

        @return:
        """
        return self.old_text != self.text(0)
