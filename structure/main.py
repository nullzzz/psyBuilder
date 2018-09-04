from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget

from .structureItem import StructureItem
from .structureTree import StructureTree

from collections import OrderedDict


class Structure(QDockWidget):
    # 打开tab (value, name)
    nodeDoubleClick = pyqtSignal(str, str)
    # 发送到main窗口串联和structure相关及icon tabs串联和tabs相关, 在其中为新增timeline串接信号 (value)
    timelineAdd = pyqtSignal(str)
    # 发送到main (parent_value, value, name)
    timelineNameChange = pyqtSignal(str, str, str)
    # 发送到icon tabs (parent_value, value, name)
    iconNameChange = pyqtSignal(str, str, str)
    #
    itemInIfBranchNameChange = pyqtSignal(str, str, str)
    # 单击node, 显示properties
    propertiesShow = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)

        # 键为value, 值为StructureItem
        self.value_node = {}
        self.data = OrderedDict()

        self.structure_tree = StructureTree()
        # 设置列数、头标签
        self.structure_tree.setColumnCount(1)
        self.structure_tree.setHeaderLabel("E-Object")
        self.structure_tree.setHeaderHidden(False)

        self.root = StructureItem(self.structure_tree, 'Timeline.10001')
        self.root.setText(0, "Timeline")
        self.root.setIcon(0, QIcon(".\\image\\timeLine.png"))

        self.value_node['Timeline.10001'] = self.root
        # 添加根节点
        self.structure_tree.addTopLevelItem(self.root)
        self.structure_tree.collapseItem(self.root)

        self.structure_tree.expandAll()

        self.structure_tree.resize(1000, 800)

        self.setWidget(self.structure_tree)

        # 连接信号
        self.linkSignal()

    def linkSignal(self):
        self.structure_tree.doubleClicked.connect(self.openTab)
        self.structure_tree.clicked.connect(lambda: self.propertiesShow.emit(self.structure_tree.currentItem().value))
        self.structure_tree.itemNameChange.connect(self.changeNodeName)

    def addRoot(self, text="root", pixmap=None, value=""):
        root = StructureItem(self.structure_tree, value)
        root.setText(0, text)
        root.setIcon(0, QIcon(pixmap))
        root.setExpanded(True)
        # 添加根节点
        self.structure_tree.addTopLevelItem(root)
        self.structure_tree.collapseItem(root)
        if value != '':
            # 往字典中加入
            self.value_node[value] = root

    def addNode(self, parentValue='Timeline.10001', text="node", pixmap=None, value="", properties_window=None):
        if parentValue in self.value_node:
            parent = self.value_node[parentValue]
            node = StructureItem(parent, value)
            node.setText(0, text)
            node.setIcon(0, QIcon(pixmap))
            parent.setExpanded(True)
            # 往字典中加入
            self.value_node[value] = node

    def removeNode(self, parentValue, value):
        if parentValue in self.value_node and value in self.value_node:
            parent = self.value_node[parentValue]
            node = self.value_node[value]
            parent.removeChild(node)

    def moveNode(self, dragCol, targetCol, parentValue, value):
        parent = self.value_node[parentValue]
        node = self.value_node[value]
        if targetCol != -1:
            if targetCol > parent.childCount():
                targetCol = parent.childCount()
            parent.removeChild(node)
            parent.insertChild(targetCol - 1, node)

    def changeNodeName(self, parent_value, value, name):
        if value in self.value_node:
            self.value_node[value].setText(0, name)
            # timeline中icon
            if parent_value.startswith('Timeline.'):
                self.iconNameChange.emit(parent_value, value, name)
            # cycle中timeline
            elif parent_value.startswith('Cycle.'):
                self.timelineNameChange.emit(parent_value, value, name)
            # if branch中的icon
            elif parent_value.startswith('If_else.'):
                self.itemInIfBranchNameChange.emit(parent_value, value, name)

    def openTab(self):
        try:
            value = self.structure_tree.currentItem().value
            name = self.structure_tree.currentItem().text(0)
            self.nodeDoubleClick.emit(value, name)
            # cycle新增timeline, 只能通过structure打开, 故此时去连接timeline相应信号
            if value != "Timeline.10001" and value.startswith('Timeline'):
                self.timelineAdd.emit(value)
        except Exception:
            print("error happens in open tab. [structure/main.py]")

    def getNodeValue(self):
        try:
            # 深度优先遍历
            node_value = OrderedDict()
            for i in range(0, self.structure_tree.topLevelItemCount()):
                root = self.structure_tree.topLevelItem(i)
                node_value[root.value] = self.do_getNodeValue(root, [])

            return node_value
        except Exception:
            print("error happens in get node_value. [structure/main.py]")

    def do_getNodeValue(self, node: StructureItem, data: list):
        try:
            for i in range(0, node.childCount()):
                child = node.child(i)
                if child.value.startswith("Cycle.") or child.value.startswith("Timeline.") or child.value.startswith('If_else.'):
                    grand_child_data = OrderedDict()
                    grand_child_data[child.value] = self.do_getNodeValue(child, [])
                    data.append(grand_child_data)
                else:
                    data.append(child.value)

            return data
        except Exception:
            print("error happens in do get node_value. [structure/main.py]")

    @staticmethod
    def getName(old_name):
        name = old_name
        print("I am producing a valid name.")
        return name

    @staticmethod
    def nameIsValid(name):
        return True
