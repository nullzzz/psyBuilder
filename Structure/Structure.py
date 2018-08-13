from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from .StructureItem import StructureItem
from .StructureTree import StructureTree


class Structure(QDockWidget):
    # 给eventTabs发送信号, 打开新窗口
    sendTabToEventTabs = pyqtSignal(str, str)
    # 后续添加的timeLine
    timeLineAdd = pyqtSignal(str)
    # 给eventTabs发信号
    getProperties = pyqtSignal(str)

    def __init__(self, title="Structure", parent=None):
        super(Structure, self).__init__(title, parent)
        self.setWindowTitle(title)

        # 键为value, 值为StructureItem, 后期考虑字典换成数据库
        self.nodes = {}

        self.structureTree = StructureTree()
        # 设置列数、头标签
        self.structureTree.setColumnCount(1)
        self.structureTree.setHeaderLabel("E-Object")
        # 隐藏头标签
        self.structureTree.setHeaderHidden(True)

        root = StructureItem(self.structureTree, 'TimeLine.10001')
        root.setText(0, "TimeLine")
        root.setIcon(0, QIcon(".\\image\\timeLine.png"))
        self.nodes['TimeLine.10001'] = root
        # 添加根节点
        self.structureTree.addTopLevelItem(root)
        self.structureTree.collapseItem(root)

        self.structureTree.expandAll()

        self.structureTree.resize(1000, 800)

        self.setWidget(self.structureTree)

        # 连接信号
        self.linkSignal()

    def linkSignal(self):
        self.structureTree.doubleClicked.connect(self.openTab)
        self.structureTree.clicked.connect(self.sendValueToTabs)

    def addRoot(self, text="root", pixmap=None, value=""):
        root = StructureItem(self.structureTree, value)
        root.setText(0, text)
        root.setIcon(0, QIcon(pixmap))
        root.setExpanded(True)
        # 添加根节点
        self.structureTree.addTopLevelItem(root)
        self.structureTree.collapseItem(root)
        if value != '':
            # 往字典中加入
            self.nodes[value] = root

    def addNode(self, parentValue='TimeLine.10001', text="node", pixmap=None, value=""):
        if parentValue in self.nodes:
            parent = self.nodes[parentValue]
            node = StructureItem(parent, value)
            node.setText(0, text)
            node.setIcon(0, QIcon(pixmap))
            node.setExpanded(True)
            # self.structureTree.expandAll()
            # 往字典中加入
            self.nodes[value] = node

    def removeNode(self, parentValue, value):
        if parentValue in self.nodes and value in self.nodes:
            parent = self.nodes[parentValue]
            node = self.nodes[value]
            parent.removeChild(node)

    def moveNode(self, dragCol, targetCol, parentValue, value):
        parent = self.nodes[parentValue]
        node = self.nodes[value]
        if targetCol != -1:
            if targetCol > parent.childCount():
                targetCol = parent.childCount()
            parent.removeChild(node)
            parent.insertChild(targetCol - 1, node)

    def openTab(self):
        value = self.structureTree.currentItem().value
        name = self.structureTree.currentItem().text(0)
        self.sendTabToEventTabs.emit(value, name)
        # 新增timeLine 要去连接timeLine 相应信号
        if value!= "TimeLine.10001" and value.startswith('TimeLine'):
            self.timeLineAdd.emit(value)

    def changeEventName(self, value, name):
        if value in self.nodes:
            self.nodes[value].setText(0, name)

    # send Value To Tabs得到properties
    def sendValueToTabs(self):
        value = self.structureTree.currentItem().value
        self.getProperties.emit(value)
