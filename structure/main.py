from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget, QInputDialog, QMessageBox, QLineEdit

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
    # 发送到icon tabs (value, exist_value)
    nodeWidgetMerge = pyqtSignal(str, str)

    name_values = {'Timeline': ['Timeline.10001']}
    value_node = {}
    # name count
    TIMELINE_COUNT = 0
    # event
    CYCLE_COUNT = 0
    SOUNTOUT_COUNT = 0
    TEXT_COUNT = 0
    IMAGE_COUNT = 0
    VIDEO_COUNT = 0
    # eye tracker
    OPEN_COUNT = 0
    DC_COUNT = 0
    CALIBRATION_COUNT = 0
    ACTION_COUNT = 0
    STARTR_COUNT = 0
    ENDR_COUNT = 0
    CLOSE_COUNT = 0
    # quest
    QUESTINIT_COUNT = 0
    QUESTUPDATA_COUNT = 0
    QUESTGETVALUE_COUNT = 0
    # condition
    IF_ELSE_COUNT = 0
    SWITCH_COUNT = 0

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)

        self.structure_tree = StructureTree()
        # 设置列数、头标签
        self.structure_tree.setColumnCount(1)
        self.structure_tree.setHeaderLabel("E-Object")
        self.structure_tree.setHeaderHidden(False)

        self.root = StructureItem(self.structure_tree, 'Timeline.10001')
        self.root.setText(0, "Timeline")
        self.root.setIcon(0, QIcon("image/timeLine.png"))

        Structure.value_node['Timeline.10001'] = self.root
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
        self.structure_tree.itemNameChange.connect(self.renameNode)

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
            Structure.value_node[value] = root

    def addNode(self, parentValue='Timeline.10001', text="node", pixmap=None, value="", properties_window=None):
        if parentValue in Structure.value_node:
            parent = Structure.value_node[parentValue]
            node = StructureItem(parent, value)
            node.setText(0, text)
            node.setIcon(0, QIcon(pixmap))
            parent.setExpanded(True)
            # 往字典中加入
            Structure.value_node[value] = node
            if parent.value.startswith('If_else.'):
                text = text[4:]
            if text in Structure.name_values:
                Structure.name_values[text].append(value)
            else:
                Structure.name_values[text] = [value]
            # count
            self.addCount(value.split('.')[0])

    def removeNode(self, parentValue, value):
        if parentValue in Structure.value_node and value in Structure.value_node:
            parent = Structure.value_node[parentValue]
            node = Structure.value_node[value]
            parent.removeChild(node)

    def moveNode(self, dragCol, targetCol, parentValue, value):
        parent = Structure.value_node[parentValue]
        node = Structure.value_node[value]
        if targetCol != -1:
            if targetCol > parent.childCount():
                targetCol = parent.childCount()
            parent.removeChild(node)
            parent.insertChild(targetCol - 1, node)

    def renameNode(self, item):
        try:
            dialog = QInputDialog()
            dialog.setModal(True)
            dialog.setWindowFlag(Qt.WindowCloseButtonHint)
            name = item.text(0)
            extend = ''
            if item.value != 'Timeline.10001':
                if item.parent().value.startswith('If_else'):
                    extend = name[0:4]
                    name = name[4:]
                text, flag = dialog.getText(None, "Rename", "Rename {} to :".format(name), QLineEdit.Normal, name)
                # 检测rename
                res, exist_value = Structure.checkNameIsValid(text, item.parent().value, item.value)
                whether_change = False
                if res == 0:
                    QMessageBox.information(self, "Warning", "sorry, you can't use this name.")
                elif res == 1:
                    whether_change = True
                elif res == 2:
                    if QMessageBox.question(self, 'Tips', 'name has existed in other place, are you sure to change?',
                                            QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                        whether_change = True
                        self.nodeWidgetMerge.emit(item.value, exist_value)
                if whether_change:
                    if flag and text:
                        text = extend + text
                        self.changeNodeName(item.parent().value, item.value, text)
        except Exception as e:
            print("error {} happens in rename node in structure. [structure/structureTree.py]".format(e))

    def changeNodeName(self, parent_value, value, name):
        try:
            if value in Structure.value_node:
                old_name = Structure.value_node[value].text(0)
                # delete old name
                # if name has many values
                if len(Structure.name_values[old_name]) > 1:
                    Structure.name_values[old_name].remove(value)
                elif len(Structure.name_values[old_name]) == 1:
                    del Structure.name_values[old_name]
                # new name
                if name in Structure.name_values:
                    Structure.name_values[name].append(value)
                else:
                    Structure.name_values[name] = [value]

                Structure.value_node[value].setText(0, name)

                # timeline中icon
                if parent_value.startswith('Timeline.'):
                    self.iconNameChange.emit(parent_value, value, name)
                # cycle中timeline
                elif parent_value.startswith('Cycle.'):
                    self.timelineNameChange.emit(parent_value, value, name)
                # if branch中的icon
                elif parent_value.startswith('If_else.'):
                    self.itemInIfBranchNameChange.emit(parent_value, value, name)
        except Exception as e:
            print("error {} happens in change node name. [structure/main.py]".format(e))

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

    def changeNodeValue(self, old_value, new_value):
        self.value_node[old_value].value = new_value

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
                if child.value.startswith("Cycle.") or child.value.startswith("Timeline.") or child.value.startswith(
                        'If_else.'):
                    grand_child_data = OrderedDict()
                    grand_child_data[child.value] = self.do_getNodeValue(child, [])
                    data.append(grand_child_data)
                else:
                    data.append(child.value)

            return data
        except Exception:
            print("error happens in do get node_value. [structure/main.py]")

    def addCount(self, widget_type):
        if widget_type == "Cycle":
            Structure.CYCLE_COUNT += 1
        elif widget_type == "Timeline":
            Structure.TIMELINE_COUNT += 1
        elif widget_type == "SoundOut":
            Structure.SOUNTOUT_COUNT += 1
        elif widget_type == "Text":
            Structure.TEXT_COUNT += 1
        elif widget_type == "Image":
            Structure.IMAGE_COUNT += 1
        elif widget_type == "Video":
            Structure.VIDEO_COUNT += 1
        elif widget_type == "Close":
            Structure.CLOSE_COUNT += 1
        elif widget_type == "DC":
            Structure.DC_COUNT += 1
        elif widget_type == "Calibration":
            Structure.CALIBRATION_COUNT += 1
        elif widget_type == "EndR":
            Structure.ENDR_COUNT += 1
        elif widget_type == "Open":
            Structure.OPEN_COUNT += 1
        elif widget_type == "Action":
            Structure.ACTION_COUNT += 1
        elif widget_type == "StartR":
            Structure.STARTR_COUNT += 1
        elif widget_type == "QuestGetValue":
            Structure.QUESTGETVALUE_COUNT += 1
        elif widget_type == "QuestUpdate":
            Structure.QUESTUPDATA_COUNT += 1
        elif widget_type == "QuestInit":
            Structure.QUESTINIT_COUNT += 1
        elif widget_type == "If_else":
            Structure.IF_ELSE_COUNT += 1
        elif widget_type == "Switch":
            Structure.SWITCH_COUNT += 1
        else:
            Structure.OTHER_COUNT += 1

    @staticmethod
    def getCount(widget_type):
        if widget_type == "Cycle":
            return Structure.CYCLE_COUNT
        elif widget_type == "Timeline":
            return Structure.TIMELINE_COUNT
        elif widget_type == "SoundOut":
            return Structure.SOUNTOUT_COUNT
        elif widget_type == "Text":
            return Structure.TEXT_COUNT
        elif widget_type == "Image":
            return Structure.IMAGE_COUNT
        elif widget_type == "Video":
            return Structure.VIDEO_COUNT
        elif widget_type == "Close":
            return Structure.CLOSE_COUNT
        elif widget_type == "DC":
            return Structure.DC_COUNT
        elif widget_type == "Calibration":
            return Structure.CALIBRATION_COUNT
        elif widget_type == "EndR":
            return Structure.ENDR_COUNT
        elif widget_type == "Open":
            return Structure.OPEN_COUNT
        elif widget_type == "Action":
            return Structure.ACTION_COUNT
        elif widget_type == "StartR":
            return Structure.STARTR_COUNT
        elif widget_type == "QuestGetValue":
            return Structure.QUESTGETVALUE_COUNT
        elif widget_type == "QuestUpdate":
            return Structure.QUESTUPDATA_COUNT
        elif widget_type == "QuestInit":
            return Structure.QUESTINIT_COUNT
        elif widget_type == "If_else":
            return Structure.IF_ELSE_COUNT
        elif widget_type == "Switch":
            return Structure.SWITCH_COUNT
        else:
            return Structure.OTHER_COUNT

    # get name主要用在drop, copy, branch的自动命名
    @staticmethod
    def getName(value, name, is_copy=False, old_name=''):
        new_name = value.split('.')[0] + '.' + str(Structure.getCount(value.split('.')[0]))
        count = 0
        while True:
            if is_copy:
                new_name = old_name + '.' + str(count)
                count += 1
            if new_name not in Structure.name_values:
                break

        return new_name

    @staticmethod
    def checkNameIsValid(name: str, parent_value='', value=''):
        # 不检查name为空, 在前面部分应该检查掉
        # 0: 完全不能取
        # 1: 可以
        # 2: 可以取但是有重复的, 需要确定
        try:
            # 如果没出现过或者没有改变
            if name not in Structure.name_values or value in Structure.name_values[name]:
                return (1, '')
            else:
                # 如果已存在, 但是不是同类型, 不可以
                if not Structure.name_values[name][0].startswith(value.split('.')[0]):
                    return (0, '')
                else:
                    parent_node = Structure.value_node[parent_value]
                    parent_name = parent_node.text(0)
                    exist_value = Structure.name_values[name][0]
                    # 判断在同一层次是否有同名
                    in_same_level = False
                    for node_value in Structure.name_values[name]:
                        if Structure.value_node[node_value].parent().text(0) == parent_name:
                            in_same_level = True
                    # 如果在同一层次
                    if in_same_level:
                        return (0, '')
                    # 如果是在父节点中
                    else:
                        in_parent = False
                        while parent_node:
                            if name == parent_node.text(0):
                                in_parent = True
                                break
                            parent_node = parent_node.parent()

                        if in_parent:
                            return (0, '')
                        else:
                            return (2, exist_value)
        except Exception as e:
            print(f"error {e} happens in check name is valid. [structure/main.py]")
