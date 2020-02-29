from PyQt5.QtCore import pyqtSignal

from app.info import Info
from app.kernel import Kernel
from lib import DockWidget
from .structure_tree import StructureTree


class Structure(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    # when node is double clicked, emit signal (widget_id)
    itemDoubleClicked = pyqtSignal(str)
    # when node is double deleted, emit signal (sender_widget, widget_id)
    itemDeleted = pyqtSignal(int, str)
    # when node is changed, emit(sender_widget, widget_id, widget_name)
    itemNameChanged = pyqtSignal(int, str, str)

    def __init__(self):
        super(Structure, self).__init__()
        # title
        self.setWindowTitle("Structure")
        self.structure_tree = StructureTree()
        self.setWidget(self.structure_tree)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.structure_tree.itemDoubleClicked.connect(lambda widget_id: self.itemDoubleClicked.emit(widget_id))
        self.structure_tree.itemDeleted.connect(
            lambda widget_id: self.itemDeleted.emit(Info.StructureSend, widget_id))
        self.structure_tree.itemNameChanged.connect(
            lambda widget_id, widget_name: self.itemNameChanged.emit(Info.StructureSend, widget_id, widget_name))

    def addNode(self, parent_widget_id: str, widget_id: str, widget_name: str, index: int):
        """
        add node in structure and Kernel.Nodes
        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # add node in tree
        node = self.structure_tree.addNode(parent_widget_id, widget_id, widget_name, index)
        # change Kernel.Nodes
        Kernel.Nodes[widget_id] = node

    def changeNodeName(self, widget_id: int, widget_name: str):
        """
        change node's widget_name according to widget id
        @param widget_id:
        @param widget_name:
        @return:
        """
        Kernel.Nodes[widget_id].setText(0, widget_name)

    def moveNode(self, widget_id: str, origin_index: int, new_index: int):
        """
        move node in structure
        @param widget_id:
        @param origin_index:
        @param new_index:
        @return:
        """
        self.structure_tree.moveNode(widget_id, new_index)

    def deleteNode(self, widget_id: str):
        """

        @param widget_id:
        @return:
        """
        node = Kernel.Nodes[widget_id]
        self.structure_tree.deleteNode(node)
