from PyQt5.QtWidgets import QTreeWidget

from app.kernel import Kernel
from .structure_node import StructureNode


class StructureTree(QTreeWidget):
    """

    """

    def __init__(self):
        super(StructureTree, self).__init__(None)
        # set one column
        self.setColumnCount(1)
        # hide header
        self.setHeaderHidden(True)
        # draggable
        self.setDragEnabled(True)

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
            parent_node.removeChild(node)
            parent_node.insertChild(index, node)
            # expand node to show its children
            parent_node.setExpanded(True)
        else:
            # create root node
            node: StructureNode = StructureNode(self, widget_id=widget_id)
            node.setText(0, widget_name)
            self.addTopLevelItem(node)
            self.collapseItem(node)
        return node
