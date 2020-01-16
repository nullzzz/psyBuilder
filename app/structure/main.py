from app.info import Info
from app.kernel import Kernel
from lib import DockWidget
from .structure_tree import StructureTree


class Structure(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)
        self.structure_tree = StructureTree()
        self.setWidget(self.structure_tree)

    def addNode(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int, add_type: int = 0) -> None:
        """
        add a node to its tree widget, not just add, we should consider few conditions as follow.
        0. simple add (default)
        1. copy other
        2. refer other
        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @param add_type:
        @return:
        """
        # discern different type
        if add_type == Info.AddItem:
            self.addNodeAdd(parent_widget_id, widget_id, widget_name, index)
        elif add_type == Info.CopyItem:
            self.addNodeCopy(parent_widget_id, widget_id, widget_name, index)
        elif add_type == Info.ReferItem:
            self.addNodeRefer(parent_widget_id, widget_id, widget_name, index)

    def addNodeAdd(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # todo add node add
        node = self.structure_tree.addNode(parent_widget_id, widget_id, widget_name, index)
        # add it to kernel
        Kernel.Nodes[widget_id] = node

    def addNodeCopy(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # todo add node copy

    def addNodeRefer(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # todo add node refer

    def changeNodeName(self, widget_id: int, widget_name: str):
        """
        change node's widget_name in all related nodes according to widget id
        @param widget_id:
        @param widget_name:
        @return:
        """
        # todo change node's widget_name in all related nodes

    def moveNode(self, widget_id: int, origin_index: int, new_index: int):
        """
        move node in structure
        @param widget_id:
        @param origin_index:
        @param new_index:
        @return:
        """
        # todo move node in structure
