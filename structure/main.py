from collections import OrderedDict

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDockWidget, QInputDialog, QMessageBox, QLineEdit

from center.iconTabs.timeline.icon import Icon
from getImage import getImage
from .structureItem import StructureItem
from .structureTree import StructureTree


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
    itemInSwitchBranchNameChange = pyqtSignal(str, str, str)
    # 单击node, 显示properties
    propertiesShow = pyqtSignal(str)
    # 发送到icon tabs (value, exist_value)
    nodeWidgetMerge = pyqtSignal(str, str)
    # 发送到icon tabs (value, old_exist_value)
    nodeWidgetSplit = pyqtSignal(str, str)
    # (value, exist_value)
    nodeWidgetCopy = pyqtSignal(str, str)
    # 发送到attributes window (attributes)
    timelineAttributesShow = pyqtSignal(dict)
    # 移动节点后将原父节点控件中的子节点进行一个删除
    iconRemove = pyqtSignal(str, str)

    name_values = {'Timeline': ['Timeline.10001']}
    name_value = {'Timeline' : 'Timeline.10001'}
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
        self.structure_tree.nodeDelete.connect(self.removeNode)
        self.nodeWidgetMerge.connect(self.copyNode)

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

    # def addNode(self, parent_value='Timeline.10001', text="node", pixmap=None, value="", properties_window=None):
    #     try:
    #         if parent_value in Structure.value_node:
    #             orgin_text = text
    #             parent = Structure.value_node[parent_value]
    #             # 判断parent_value是否有同名者, 对于同名者也要加入node
    #             for same_name_value in Structure.name_values[parent.text(0)]:
    #                 if same_name_value != parent_value:
    #                     # 对于新增的node，采用不同value，但是指向同一个widget
    #                     temp_parent = Structure.value_node[same_name_value]
    #                     icon_type = value.split('.')[0]
    #                     temp_icon = Icon(None, icon_type, pixmap)
    #                     temp_node = StructureItem(temp_parent, temp_icon.value)
    #                     temp_node.setText(0, text)
    #                     temp_node.setIcon(0, QIcon(pixmap))
    #                     temp_parent.setExpanded(True)
    #                     # 往字典中加入
    #                     Structure.value_node[temp_icon.value] = temp_node
    #                     if temp_parent.value.startswith('If_else.'):
    #                         text = text[4:]
    #                     if text in Structure.name_values:
    #                         Structure.name_values[text].append(temp_icon.value)
    #                     else:
    #                         Structure.name_values[text] = [temp_icon.value]
    #                     # count
    #                     self.addCount(temp_icon.value.split('.')[0])
    #                     # merge
    #                     self.nodeWidgetMerge.emit(temp_icon.value, value)
    #
    #             text = orgin_text
    #             node = StructureItem(parent, value)
    #             node.setText(0, text)
    #             node.setIcon(0, QIcon(pixmap))
    #             parent.setExpanded(True)
    #             # 往字典中加入
    #             Structure.value_node[value] = node
    #             if parent.value.startswith('If_else.'):
    #                 text = text[4:]
    #             if text in Structure.name_values:
    #                 Structure.name_values[text].append(value)
    #             else:
    #                 Structure.name_values[text] = [value]
    #             # count
    #             self.addCount(value.split('.')[0])
    #     except Exception as e:
    #         print(f"error {e} happens in add node in structure. [structure/main.py]")

    def addNode(self, parent_value='Timeline.10001', text="node", pixmap=None, value:str="", properties_window=None, condition_type=''):
        try:
            if parent_value in Structure.value_node:
                parent = Structure.value_node[parent_value]
                node = StructureItem(parent, value)
                name = text
                # TODO 涉及If_else
                if parent_value.startswith('If_else'):
                    name = f'[{condition_type}] ' + text
                node.setText(0, name)
                node.setIcon(0, QIcon(pixmap))
                parent.setExpanded(True)
                # 相关字典数据
                Structure.value_node[value] = node
                Structure.name_value[text] = value
                # 名称计数
                self.addCount(value.split('.')[0])
        except Exception as e:
            print(f"error {e} happens in add node. [structure/main.py]")

    # def removeNode(self, parent_value, value):
    #     try:
    #         # 删除node：
    #         # 1，要删除其子节点
    #         # 2，如果其父亲节点存在同名，其父节点同名者里的此node也要删除，因为其父节点的同名节点应当与其父节点同步
    #         if value in Structure.value_node and parent_value in Structure.value_node:
    #             parent_name = Structure.value_node[parent_value].text(0)
    #             node_name = Structure.value_node[value].text(0)
    #             if parent_value.startswith('If_else'):
    #                 node_name = node_name[4:]
    #             for same_parent_value in Structure.name_values[parent_name]:
    #                 same_node_value = self.getNodeValueByName(same_parent_value, node_name)
    #                 if same_node_value:
    #                      self.removeNodeSimply(same_parent_value, same_node_value)
    #     except Exception as e:
    #         print(f"error {e} happens in remove node in structure. [structure/main.py]")

    # def removeNodeSimply(self, parent_value, value):
    #     try:
    #         # 只删除自身及其子节点
    #         parent = Structure.value_node[parent_value]
    #         node = Structure.value_node[value]
    #         node_name = Structure.value_node[value].text(0)
    #         if parent_value.startswith('If_else'):
    #             node_name = node_name[4:]
    #         # 删除其子节点
    #         while node.childCount():
    #             self.removeNodeSimply(node.value, node.child(0).value)
    #         # 删除自身及相关数据
    #         # 数据包含name_value, value_node
    #         Structure.name_values[node_name].remove(value)
    #         if not Structure.name_values[node_name]:
    #             del Structure.name_values[node_name]
    #         del Structure.value_node[value]
    #         parent.removeChild(node)
    #     except Exception as e:
    #         print(f"error {e} happens in remove node simply. [structure/main.py]")

    def removeNode(self, parent_value, value):
        try:
            parent = Structure.value_node[parent_value]
            node = Structure.value_node[value]
            node_name = node.text(0)
            # TODO 涉及If_else
            if parent_value.startswith('If_else.'):
                node_name = node_name[4:]
            # 先删除其子节点再删除自身
            while node.childCount():
                self.removeNode(value, node.child(0).value)
            # 删除相关数据
            del Structure.value_node[value]
            del Structure.name_value[node_name]
            # 删除节点
            parent.removeChild(node)
        except Exception as e:
            print(f"error {e} happens in remove node. [structure/main.py]")

    def getNodeValueByName(self, parent_value, name):
        parent = Structure.value_node[parent_value]
        for node_value in Structure.name_values[name]:
            if parent.indexOfChild(Structure.value_node[node_value]) != -1:
                return node_value
        return ''

    # def moveNode(self, drag_col, target_col, parent_value, value):
    #     try:
    #         parent_name = Structure.value_node[parent_value].text(0)
    #         child_name = Structure.value_node[value].text(0)
    #         for same_parent_value in Structure.name_values[parent_name]:
    #             parent = Structure.value_node[same_parent_value]
    #             if target_col != -1:
    #                 if target_col > parent.childCount():
    #                     target_col = parent.childCount()
    #                 child_value = self.getNodeValueByName(same_parent_value, child_name)
    #                 child = Structure.value_node[child_value]
    #                 parent.removeChild(child)
    #                 parent.insertChild(target_col - 1, child)
    #     except Exception as e:
    #         print(f"error {e} happens in move node in structure. [structure.main.py]")

    def moveNode(self, drag_col, target_col, parent_value, value):
        try:
            if target_col != -1:
                parent = Structure.value_node[parent_value]
                if target_col > parent.childCount():
                    target_col = parent.childCount()
                child = Structure.value_node[value]
                parent.removeChild(child)
                parent.insertChild(target_col - 1, child)
        except Exception as e:
            print(f"error {e} happens in move node in structure. [structure.main.py]")

    # def renameNode(self, Item):
    #     try:
    #         dialog = QInputDialog()
    #         dialog.setModal(True)
    #         dialog.setWindowFlag(Qt.WindowCloseButtonHint)
    #         name = Item.text(0)
    #         extend = ''
    #         if Item.value != 'Timeline.10001':
    #             if Item.parent().value.startswith('If_else'):
    #                 extend = name[0:4]
    #                 name = name[4:]
    #             text, flag = dialog.getText(None, "Rename", "Rename {} to :".format(name), QLineEdit.Normal, name)
    #             # 检测rename
    #             res, exist_value, old_exist_value = Structure.checkNameIsValid(text, Item.parent().value, Item.value)
    #             whether_change = False
    #             if res == 0:
    #                 QMessageBox.information(self, "Warning", "sorry, you can't use this name.")
    #             elif res == 1:
    #                 whether_change = True
    #             elif res == 2:
    #                 if QMessageBox.question(self, 'Tips', 'name has existed in other place, are you sure to change?',
    #                                         QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
    #                     whether_change = True
    #                     self.nodeWidgetMerge.emit(Item.value, exist_value)
    #             elif res == 3:
    #                 whether_change = True
    #                 self.nodeWidgetSplit.emit(Item.value, old_exist_value)
    #             elif res == 4:
    #                 if QMessageBox.question(self, 'Tips', 'name has existed in other place, are you sure to change?',
    #                                         QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
    #                     whether_change = True
    #                     # 好像不需要去断开之前的连接
    #                     self.nodeWidgetMerge.emit(Item.value, exist_value)
    #             if whether_change:
    #                 if flag and text:
    #                     text = extend + text
    #                     self.changeNodeName(Item.parent().value, Item.value, text)
    #     except Exception as e:
    #         print("error {} happens in rename node in structure. [structure/main.py]".format(e))

    def renameNode(self, item):
        try:
            # 传出去的name也是不带前缀的
            dialog = QInputDialog()
            dialog.setModal(True)
            dialog.setWindowFlag(Qt.WindowCloseButtonHint)
            name = item.text(0)
            if item.value != 'Timeline.10001':
                # TODO 涉及If_else
                if item.parent().value.startswith('If_else'):
                    name = name[4:]
                text, flag = dialog.getText(None, "Rename", "Rename {} to :".format(name), QLineEdit.Normal, name)
                if flag:
                    # name不能为空
                    if text:
                        # 检测name合法性
                        weather_change, tips = Structure.checkNameValidity(text, item.value)
                        if weather_change:
                            self.changeNodeName(item.parent().value, item.value, text)
                        else:
                            QMessageBox.information(self, 'Tips', tips)
                    else:
                        QMessageBox.information(self, 'Tips', "Name can't be none.")
        except Exception as e:
            print(f"error {e} happens in rename node. [structure/main.py]")

    # def changeNodeName(self, parent_value, value, name):
    #     try:
    #         if value in Structure.value_node:
    #             old_name = Structure.value_node[value].text(0)
    #             # delete old name
    #             # if name has many values
    #             if parent_value.startswith('If_else'):
    #                 old_name = old_name[4:]
    #             if len(Structure.name_values[old_name]) > 1:
    #                 Structure.name_values[old_name].remove(value)
    #             elif len(Structure.name_values[old_name]) == 1:
    #                 del Structure.name_values[old_name]
    #             # new name
    #             if name in Structure.name_values:
    #                 Structure.name_values[name].append(value)
    #             else:
    #                 Structure.name_values[name] = [value]
    #
    #             Structure.value_node[value].setText(0, name)
    #
    #             # timeline中icon
    #             if parent_value.startswith('Timeline.'):
    #                 self.iconNameChange.emit(parent_value, value, name)
    #             # cycle中timeline
    #             elif parent_value.startswith('Cycle.'):
    #                 self.timelineNameChange.emit(parent_value, value, name)
    #             # if branch中的icon
    #             elif parent_value.startswith('If_else.'):
    #                 self.itemInIfBranchNameChange.emit(parent_value, value, name)
    #     except Exception as e:
    #         print("error {} happens in change node name. [structure/main.py]".format(e))

    def changeNodeName(self, parent_value, value, name):
        try:
            # 要注意if else，造孽啊，当初搞那玩意加上T，F
            # 此时传进来的name都是不带前缀的
            if value in Structure.value_node:
                old_name = Structure.value_node[value].text(0)
                # delete old name
                # todo 涉及If_else
                prefix = ''
                if parent_value.startswith('If_else'):
                    prefix = old_name[:4]
                    old_name = old_name[4:]
                new_name = prefix + name
                # 删除旧name相关数据
                del Structure.name_value[old_name]
                # new name
                Structure.name_value[name]  = value
                Structure.value_node[value].setText(0, new_name)

                # timeline中icon
                if parent_value.startswith('Timeline.'):
                    self.iconNameChange.emit(parent_value, value, name)
                # cycle中timeline
                elif parent_value.startswith('Cycle.'):
                    self.timelineNameChange.emit(parent_value, value, name)
                # if branch中的icon
                elif parent_value.startswith('If_else.'):
                    # 发出去的是不带前缀的
                    self.itemInIfBranchNameChange.emit(parent_value, value, name)
                elif parent_value.startswith('Switch.'):
                    self.itemInSwitchBranchNameChange.emit(parent_value, value, name)
        except Exception as e:
            print("error {} happens in change node name. [structure/main.py]".format(e))

    # def copyNode(self, value, exist_value):
    #     try:
    #         # 在value所代表的node下增加已有的节点的子节点
    #         if value in Structure.value_node and exist_value in Structure.value_node:
    #             node = Structure.value_node[value]
    #             # 只能简单删除node下所有的子节点
    #             for child_index in range(0, node.childCount()):
    #                 child = node.child(child_index)
    #                 self.removeNodeSimply(node.value, child.value)
    #             # 将exist所有的子节点拷贝过来
    #             self.copyNodeSimply(value, exist_value)
    #     except Exception as e:
    #         print(f"error {e} happens in copy node. [structure/main.py]")
    #
    # # 拷贝子节点
    # def copyNodeSimply(self, value, exist_value):
    #     try:
    #         node = Structure.value_node[value]
    #         exist_node = Structure.value_node[exist_value]
    #         for exist_child_index in range(0, exist_node.childCount()):
    #             exist_child = exist_node.child(exist_child_index)
    #             # 对于新增的node，采用不同value，但是指向同一个widget
    #             icon_type = exist_child.value.split('.')[0]
    #             pixmap = getImage(icon_type, 'pixmap')
    #             child_icon = Icon(None, icon_type, pixmap)
    #             child_node = StructureItem(node, child_icon.value)
    #             child_node.setText(0, exist_child.text(0))
    #             child_node.setIcon(0, QIcon(pixmap))
    #             node.setExpanded(True)
    #             # 往字典中加入
    #             Structure.value_node[child_node.value] = child_node
    #             text = exist_child.text(0)
    #             if exist_value.startswith('If_else.'):
    #                 text = text[4:]
    #             if text in Structure.name_values:
    #                 Structure.name_values[text].append(child_node.value)
    #             else:
    #                 Structure.name_values[text] = [child_node.value]
    #             # count
    #             self.addCount(child_node.value.split('.')[0])
    #             # merge
    #             self.nodeWidgetMerge.emit(child_node.value, exist_child.value)
    #             # 拷贝子节点的子节点
    #             self.copyNodeSimply(child_node.value, exist_child.value)
    #     except Exception as e:
    #         print(f"error {e} happens in copy icon simply. [structure/main.py]")

    def copyNode(self, value, exist_value):
        # 此节点的复制命名，应该已经在前面的步骤完成
        # 在此函数中要完成其子节点的复制命名
        if value in Structure.value_node and exist_value in Structure.value_node:
            # 删除所有原有子节点
            node = Structure.value_node[value]
            while(node.childCount()):
                self.removeNode(value, node.child(0).value)
            # 将被复制的节点的子节点复制过来
            self.copyNodeSimply(value, exist_value)

    def copyNodeSimply(self, value, exist_value):
        node = Structure.value_node[value]
        exist_node = Structure.value_node[exist_value]
        # 复制子节点
        for exist_child_index in range(exist_node.childCount()):
            exist_child = exist_node.child(exist_child_index)
            icon_type = exist_child.value.split('.')[0]
            pixmap = getImage(icon_type, 'pixmap')
            child_icon = Icon(None, icon_type, pixmap)
            child_node = StructureItem(node, child_icon.value)
            child_node.setText(0, Structure.getValidName(child_node.value, True, exist_child.text(0)))
            child_node.setIcon(0, QIcon(pixmap))
            node.setExpanded(True)
            # 往字典中加入
            Structure.value_node[child_node.value] = child_node
            text = child_node.text(0)
            # TODO 涉及If_else
            if exist_value.startswith('If_else.'):
                text = text[4:]
            Structure.name_value[text] = child_node.value
            # count
            self.addCount(child_node.value.split('.')[0])
            # 拷贝子节点的子节点
            self.copyNodeSimply(child_node.value, exist_child.value)
            # copy widget
            self.nodeWidgetCopy.emit(exist_child.value, child_node.value)

    def changeNode(self, new_parent_value, value):
        # 将一个节点及其所有子节点移动到新的parent下
        child = Structure.value_node[value]
        old_parent = child.parent()
        old_parent.removeChild(child)
        new_parent:StructureItem = Structure.value_node[new_parent_value]
        new_parent.addChild(child)
        # 将原父节点控件中的子节点图标删除
        self.iconRemove.emit(old_parent.value, value)

    def openTab(self):
        try:
            child = self.structure_tree.currentItem()
            value = child.value
            name = child.text(0)
            # TODO 涉及If_else
            try:
                if child.parent().value.startswith('If_else'):
                    name = name[4:]
            except Exception:
                pass
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
                        'If_else.') or child.value.startswith("Switch."):
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
    def getValidName(value, is_copy=False, old_name=''):
        try:
            value_type = value.split('.')[0]
            name = f"{value_type}.{Structure.getCount(value_type)}"

            count = 0
            while True:
                if is_copy:
                    name = f"{old_name}.{count}"
                if name not in Structure.name_value:
                    break
                count += 1

            return name
        except Exception as e:
            print(f"error {e} happens in get valid name. [structure/main.py]")

    @staticmethod
    def checkNameIsValid(name: str, parent_value='', value=''):
        # 不检查name为空, 在前面部分应该检查掉
        # 0: 完全不能取
        # 1: 可以
        # 2: 可以取但是有重复的, 需要确定
        # 3：改名断开连接
        # 4：改名断开连接后，新名字为重复值
        # 5: 重复进行复制
        # 返回值type，exist_value，old_value
        try:
            if name[0].isalpha():
                # 如果new name没出现过或者没有改变
                if name not in Structure.name_values or value in Structure.name_values[name]:
                    # 如果有old name且是有同名的，改成没有出现过的new name则是断开原有连接
                    if value in Structure.value_node:
                        old_name = Structure.value_node[value].text(0)
                        if parent_value.startswith('If_else.'):
                            old_name = old_name[4:]
                        if len(Structure.name_values[old_name]) > 1:
                            old_exist_value = ''
                            for temp_value in Structure.name_values[old_name]:
                                if temp_value != value:
                                    old_exist_value = temp_value
                                    break
                            return 3, '', old_exist_value
                        else:
                            return 1, '', ''
                    else:
                        return 1, '', ''
                else:
                    # 如果已存在, 但是不是同类型, 不可以
                    if not Structure.name_values[name][0].startswith(value.split('.')[0]):
                        return 0, '', ''
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
                            return 0, '', ''
                        # 如果是在父节点中
                        else:
                            in_parent = False
                            while parent_node:
                                if name == parent_node.text(0):
                                    in_parent = True
                                    break
                                parent_node = parent_node.parent()

                            if in_parent:
                                return 0, '', ''
                            else:
                                if value in Structure.value_node:
                                    old_name = Structure.value_node[value].text(0)
                                    if len(Structure.name_values[old_name]) > 1:
                                        old_exist_value = ''
                                        for temp_value in Structure.name_values[old_name]:
                                            if temp_value != value:
                                                old_exist_value = temp_value
                                                break
                                        return 4, exist_value, old_exist_value
                                    else:
                                        return 2, exist_value, ''
                                else:
                                    return 2, exist_value, ''
            else:
                return 0, '', ''
        except Exception as e:
            print(f"error {e} happens in check name is valid or not. [structure/main.py]")

    @staticmethod
    def checkNameValidity(name: str, value='', delete_names=[]):
        try:
            # name不为空，空的情况应该在之前就排除
            # return: bool, tips
            # 先检测是否重名
            if not name in Structure.name_value or value == Structure.name_value[name]:
                # 检测开头必须是字母
                if name[0].isalpha():
                    return True, ''
                else:
                    return False, "Name must start with letter."
            else:
                if name in delete_names:
                    return True, ''
                return False, "You can't use existed name."
        except Exception as e:
            print(f"error {e} happens in check name's validity. [structure/main.py]")

    def showTimelineAttributes(self, value):
        self.timelineAttributesShow.emit(self.getTimelineAttributes(value))

    def getTimelineAttributes(self, value):
        # todo 得到timeline的attributes
        return {"error" : "can't get attributes"}

    @staticmethod
    def getValueBySameAndParent(same_value, parent_value):
        try:
            name = Structure.value_node[same_value].text(0)
            for value in Structure.name_values[name]:
                if Structure.value_node[value].parent().value == parent_value:
                    return value
            return ''
        except Exception as e:
            print(f"error {e} happens in get value. [structure/main.py]")

    @staticmethod
    def getNameAndValueByParent(parent_value, index):
        try:
            parent = Structure.value_node[parent_value]
            child = parent.child(index)
            return child.text(0), child.value
        except Exception as e:
            print(f"error {e} happens in get name and value. [structure/main.py]")

    @staticmethod
    def getNameAndValueByOldAndParent(old_name, old_parent_value, parent_value):
        try:
            old_parent = Structure.value_node[old_parent_value]
            index = -1
            for i in range(old_parent.childCount()):
                if old_parent.child(i).text(0) == old_name:
                    index = i
            parent = Structure.value_node[parent_value]
            child = parent.child(index)
            return child.text(0), child.value
        except Exception as e:
            print(f'error {e} happens in get name and value. [structure/main.py]')

    @staticmethod
    def getNameAndValueInIfBranchByParent(parent_value, condition_type):
        try:
            parent = Structure.value_node[parent_value]
            for i in range(parent.childCount()):
                child:StructureItem = parent.child(i)
                if child.text(0).startswith(f"[{condition_type}]"):
                    return ' '.join(child.text(0).split(' ')[1:]), child.value
        except Exception as e:
            print(f"error {e} happens in get name and value of item in if. [structure/main.py]")

    @staticmethod
    def getNameAndValueInSwitchBranchByParent(old_parent_value, old_case_value, new_parent_value):
        try:
            old_parent = Structure.value_node[old_parent_value]
            index = 0
            for i in range(old_parent.childCount()):
                if old_parent.child(i).value == old_case_value:
                    index = i
            new_parent = Structure.value_node[new_parent_value]
            child = new_parent.child(index)
            return child.text(0), child.value
        except Exception as e:
            print(f"error {e} happens in get name and value of item in switch. [structure/main.py]")

    @staticmethod
    def getParentValue(value):
        if value != 'Timeline.10001':
            return Structure.value_node[value].parent().value
        return ''

    @staticmethod
    def getTimelineValues(value):
        try:
            values = []
            while True:
                if value.startswith('Timeline.'):
                    values.append(value)
                try:
                    value = Structure.value_node[value].parent().value
                except Exception:
                    break
            return values
        except Exception as e:
            print(f"error {e} happens in get timeline value list. [structure/main.py]")

    @staticmethod
    def checkDragValidity(value):
        # 里面的var choose的检测，父节点检测
        # 父节点检测先做
        pass
