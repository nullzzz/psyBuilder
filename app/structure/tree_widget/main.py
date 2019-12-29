from PyQt5.QtWidgets import QTreeWidget

from app.kernel import Kernel
from .tree_item_widget import TreeItemWidget


class TreeWidget(QTreeWidget):
    """

    """

    def __init__(self):
        super(TreeWidget, self).__init__(None)
        #
        pass

    def addNode(self, parent_widget_id: int, widget_id: int, widget_name: str):
        """
        add node to its self
        :param parent_widget_id:
        :param widget_id:
        :param widget_name:
        :return:
        """
        # if it has parent node
        if parent_widget_id:
            parent_node = Kernel.Nodes[parent_widget_id]
            node = TreeItemWidget(parent=parent_node, widget_id=widget_id)
            node.setText(0, widget_name)
        else:
            # create root node
            node = TreeItemWidget(parent=self, widget_id=widget_id)
            node.setText(0, widget_name)
