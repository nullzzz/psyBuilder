from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget

from .structureItem import StructureItem
from .structureTree import StructureTree


class Structure(QDockWidget):
    # 打开tab (value, name)
    nodeDoubleClick = pyqtSignal(str, str)
    # 发送到main窗口串联和structure相关及icon tabs串联和tabs相关, 在其中为新增timeline串接信号 (value)
    timelineAdd = pyqtSignal(str)
    # 单击node, 显示properties
    propertiesShow = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)

        # 键为value, 值为StructureItem
        self.value_node = {}

        self.structure_tree = StructureTree()
        # 设置列数、头标签
        self.structure_tree.setColumnCount(1)
        self.structure_tree.setHeaderLabel("E-Object")
        # 隐藏头标签
        self.structure_tree.setHeaderHidden(True)
        root = StructureItem(self.structure_tree, 'Timeline.10001')
        root.setText(0, "Timeline")
        root.setIcon(0, QIcon(".\\image\\timeLine.png"))
        self.value_node['Timeline.10001'] = root
        # 添加根节点
        self.structure_tree.addTopLevelItem(root)
        self.structure_tree.collapseItem(root)

        self.structure_tree.expandAll()

        self.structure_tree.resize(1000, 800)

        self.setWidget(self.structure_tree)

        # 连接信号
        self.linkSignal()

    def linkSignal(self):
        self.structure_tree.doubleClicked.connect(self.openTab)
        self.structure_tree.clicked.connect(lambda :self.propertiesShow.emit(self.structure_tree.currentItem().value))

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

    def addNode(self, parentValue='Timeline.10001', text="node", pixmap=None, value=""):
        if parentValue in self.value_node:
            parent = self.value_node[parentValue]
            node = StructureItem(parent, value)
            node.setText(0, text)
            node.setIcon(0, QIcon(pixmap))
            node.setExpanded(True)
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

    def changeNodeName(self, value, name):
        if value in self.value_node:
            self.value_node[value].setText(0, name)

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
