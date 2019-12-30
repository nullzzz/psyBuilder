from app.info import Info
from lib import DockWidget
from .tree_widget import TreeWidget


class Structure(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)
        self.tree_widget = TreeWidget()

    def addNode(self, parent_widget_id: int, widget_id: int, widget_name: str, add_type: int = 0) -> None:
        """
        add a node to its tree widget, not just add, we should consider few conditions as follow.
        0. simple add (default) 
        1. copy other
        2. refer other
        3. move other
        @param parent_widget_id: its parent
        @param widget_id: its id
        @param widget_name: its name
        @param add_type: add type
        @return: 
        """
        # discern different type
        if add_type == Info.AddNode:
            self.addNodeAdd(parent_widget_id, widget_id, widget_name)
        elif add_type == Info.CopyNode:
            self.addNodeCopy(parent_widget_id, widget_id, widget_name)
        elif add_type == Info.ReferNode:
            self.addNodeRefer(parent_widget_id, widget_id, widget_name)
        elif add_type == Info.MoveNode:
            self.addNodeMove(parent_widget_id, widget_id, widget_name)
        else:
            exit()

    def addNodeAdd(self, parent_widget_id: int, widget_id: int, widget_name: str):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @return:
        """
        # todo add node add

    def addNodeCopy(self, parent_widget_id: int, widget_id: int, widget_name: str):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @return:
        """
        # todo add node copy

    def addNodeRefer(self, parent_widget_id: int, widget_id: int, widget_name: str):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @return:
        """
        # todo add node refer

    def addNodeMove(self, parent_widget_id: int, widget_id: int, widget_name: str):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @return:
        """
        # todo add node move
