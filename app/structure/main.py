import copy

from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QDockWidget, QApplication

from app.center.widget_tabs.timeline.widget_icon import WidgetIcon
from app.func import Func
from app.info import Info
from app.lib import SizeContainerWidget
from .structure_node import StructureNode
from .structure_tree import StructureTree
from .wid_tree.main import WidTree


# 在这层改动一般不会发送什么信号
# 基本在structure中完成了大部分的数据操作
# name_wid, wid_node
class Structure(QDockWidget):
    # 在这里发送信号到main去创建连接信号 (widget_id -> main)
    widgetSignalsLink = pyqtSignal(str)
    # 在创建widget时有一个转圈圈 (none -> main)
    widgetCreatStart = pyqtSignal()
    widgetCreatEnd = pyqtSignal()
    # 当某个widget被彻底删除，即无任何widget指向它后，要关闭tab
    widgetDelete = pyqtSignal(str)
    # 当有widget发生修改（新增、删除、重命名）时，在修改完成后，发送一个刷新attributes的信号
    widgetModify = pyqtSignal()

    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)
        self.structure_tree = StructureTree(self)
        size_container = SizeContainerWidget()
        size_container.setWidget(self.structure_tree)
        self.setWidget(size_container)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        self.structure_tree.nodeNameChange.connect(self.renameNode)
        self.structure_tree.nodeDelete.connect(self.deleteNode)

    def addNode(self, parent_widget_id, widget_id, name, flag, old_widget_id='', refresh=True):
        """
        flag 0 直接添加 flag 1 复制 flag 2 引用
        直接添加，父节点存在引用，则引用节点下也要添加节点 (父节点只可能是timeline, cycle)
        分两步走，第一步先直接在parent_widget_id节点下增加, 这一步就要区分新增节点的添加方式
        第二步，refer_parent_widget_id节点下增加引用
        timeline只要引用，不存在复制，cycle的复制，但是下面timeline子节点是引用, cycle的引用更是全都是引用
        复制过来的，多出一个复制过程，本节点的复制, 如果是cycle，多出来一个子节点引用
        引用过来的，多出一个引用过程，本节点的引用，如果是cycle，多出来一个子节点引用
        :param parent_widget_id:
        :param widget_id:
        :param name:
        :param flag:
        :param old_widget_id:
        :return:
        """
        # 发送开始创建信号，开始转圈圈
        self.widgetCreatStart.emit()
        if refresh:
            QApplication.processEvents()
        # 按类型进行
        if flag == Info.WidgetAdd:
            self.addNodeForAdd(parent_widget_id, widget_id, name)
        elif flag == Info.WidgetCopy:
            self.addNodeForCopy(parent_widget_id, widget_id, name, old_widget_id)
        elif flag == Info.WidgetRefer:
            self.addNodeForRefer(parent_widget_id, widget_id, name, old_widget_id)
        elif flag == Info.WidgetMove:
            self.addNodeForMove(parent_widget_id, widget_id, name)
        # 发送创建结束信号，结束转圈圈
        self.widgetCreatEnd.emit()
        if refresh:
            QApplication.processEvents()
        # modify
        self.widgetModify.emit()

    def addNodeForAdd(self, parent_widget_id, widget_id, name):
        """
        单纯添加最好做，注意父节点引用即可
        因为是单纯新增，且用户来命名，名字不可以重复，所以必定是新名字，这是在命名时就应该检测好的
        由于可能存在引用，但是此时并没有生成好一个widget，所以要发送信号到widget_tabs来创建widget
        :param parent_widget_id:
        :param widget_id:
        :param name:
        :return:
        """
        try:
            # 先在源节点下添加
            parent_node = Info.WID_NODE[parent_widget_id]
            node = StructureNode(parent_node, widget_id)
            node.setText(0, name)
            parent_node.setExpanded(True)
            # data
            Info.WID_NODE[widget_id] = node
            Info.NAME_WID[name] = [widget_id]
            # 创建控件, 连接信号
            Func.createWidget(widget_id)
            self.widgetSignalsLink.emit(widget_id)
            # 父节点引用
            widget_type = widget_id.split('.')[0]
            refer_parent_wids = Func.getReferWidgetIds(parent_widget_id)
            for refer_parent_wid in refer_parent_wids:
                refer_parent_node = Info.WID_NODE[refer_parent_wid]
                # 要为新增节点搞一个widget_id啊
                refer_child_wid = WidgetIcon(widget_type=widget_type).widget_id
                refer_child_node = StructureNode(refer_parent_node, refer_child_wid)
                refer_child_node.setText(0, name)
                refer_parent_node.setExpanded(True)
                # data
                Info.WID_NODE[refer_child_wid] = refer_child_node
                Info.NAME_WID[name].append(refer_child_wid)
                Info.WID_WIDGET[refer_child_wid] = Info.WID_WIDGET[widget_id]
        except Exception as e:
            print(f"error {e} happens in add node for add. [structure/main.py]")
            Func.log(str(e), True)

    def addNodeForCopy(self, parent_widget_id, widget_id, name, old_widget_id):
        try:
            # copy过来的先在源节点下进行copy好了
            parent_node = Info.WID_NODE[parent_widget_id]
            node = StructureNode(parent_node, widget_id)
            node.setText(0, name)
            parent_node.setExpanded(True)
            # data
            Info.WID_NODE[widget_id] = node
            Info.NAME_WID[name] = [widget_id]
            # 复制如果原节点存在子节点timeline/cycle，复制的节点下面的子节点也是引用
            self.referChildrenNodes(widget_id, old_widget_id)
            # 复制控件
            Func.copyWidget(widget_id, old_widget_id)
            self.widgetSignalsLink.emit(widget_id)

            # 父节点引用下，也要增加一个源节点下复制的引用
            refer_parent_wids = Func.getReferWidgetIds(parent_widget_id)
            widget_type = widget_id.split('.')[0]
            for refer_parent_wid in refer_parent_wids:
                refer_parent_node = Info.WID_NODE[refer_parent_wid]
                # 要为新增节点搞一个widget_id啊
                refer_child_wid = WidgetIcon(widget_type=widget_type).widget_id
                refer_child_node = StructureNode(refer_parent_node, refer_child_wid)
                refer_child_node.setText(0, name)
                refer_parent_node.setExpanded(True)
                # data
                Info.WID_NODE[refer_child_wid] = refer_child_node
                Info.NAME_WID[name].append(refer_child_wid)
                Info.WID_WIDGET[refer_child_wid] = Info.WID_WIDGET[widget_id]
                # 子节点是引用
                self.referChildrenNodes(refer_child_wid, widget_id)
        except Exception as e:
            print(f"error {e} happens in add node for copy. [structure/main.py]")
            Func.log(str(e), True)

    def addNodeForRefer(self, parent_widget_id, widget_id, name, old_widget_id):
        try:
            # 源父节点
            parent_node = Info.WID_NODE[parent_widget_id]
            node = StructureNode(parent_node, widget_id)
            node.setText(0, name)
            parent_node.setExpanded(True)
            # data
            Info.WID_NODE[widget_id] = node
            Func.referWidget(widget_id, old_widget_id)
            Info.NAME_WID[name].append(widget_id)
            # 子节点
            self.referChildrenNodes(widget_id, old_widget_id)

            # 父节点引用
            refer_parent_wids = Func.getReferWidgetIds(parent_widget_id)
            widget_type = widget_id.split('.')[0]
            for refer_parent_wid in refer_parent_wids:
                refer_parent_node = Info.WID_NODE[refer_parent_wid]
                # 要为新增节点搞一个widget_id啊
                refer_child_wid = WidgetIcon(widget_type=widget_type).widget_id
                refer_child_node = StructureNode(refer_parent_node, refer_child_wid)
                refer_child_node.setText(0, name)
                refer_parent_node.setExpanded(True)
                # data
                Info.WID_NODE[refer_child_wid] = refer_child_node
                Info.NAME_WID[name].append(refer_child_wid)
                Info.WID_WIDGET[refer_child_wid] = Info.WID_WIDGET[widget_id]
                # 子节点是引用
                self.referChildrenNodes(refer_child_wid, widget_id)
        except Exception as e:
            print(f"error {e} happens in add node for refer. [structure/main.py]")
            Func.log(str(e), True)

    def addNodeForMove(self, parent_wid, widget_id, name):
        # 用来应付一个widget在非引用的timeline之间移动，在新的timeline中添加icon，并且从旧的timeline中删除
        # 切记注意引用
        # 现在的环境是目标timeline中已经加入了一个wid为被拖拽的node的wid的icon，现在这边要做的就是先删除原有节点，再新增一个节点
        try:
            # 先删除原节点端一切
            # 保留一下widget，可能有用哈
            widget = Info.WID_WIDGET[widget_id]
            self.deleteNode(widget_id)

            # 增加新节点，借助部分addNodeForAdd代码段
            # 先在源节点下添加
            parent_node = Info.WID_NODE[parent_wid]
            node = StructureNode(parent_node, widget_id)
            node.setText(0, name)
            parent_node.setExpanded(True)
            # data
            Info.WID_NODE[widget_id] = node
            if name in Info.NAME_WID:
                # 删除节点时没有被全部删除
                Info.NAME_WID[name].append(widget_id)
                Info.WID_WIDGET[widget_id] = Info.WID_WIDGET[Info.NAME_WID[name][0]]
            else:
                # 删除节点时被全部删除掉了
                Info.NAME_WID[name] = [widget_id]
                # 原有的widget改变一下widget_id，才能适用于新情况
                widget.changeWidgetId(widget_id)
                Info.WID_WIDGET[widget_id] = widget

            # 父节点引用
            widget_type = widget_id.split('.')[0]
            refer_parent_wids = Func.getReferWidgetIds(parent_wid)
            for refer_parent_wid in refer_parent_wids:
                refer_parent_node = Info.WID_NODE[refer_parent_wid]
                # 要为新增节点搞一个widget_id啊
                refer_child_wid = WidgetIcon(widget_type=widget_type).widget_id
                refer_child_node = StructureNode(refer_parent_node, refer_child_wid)
                refer_child_node.setText(0, name)
                refer_parent_node.setExpanded(True)
                # data
                Info.WID_NODE[refer_child_wid] = refer_child_node
                Info.NAME_WID[name].append(refer_child_wid)
                Info.WID_WIDGET[refer_child_wid] = Info.WID_WIDGET[widget_id]
        except Exception as e:
            print(f"error {e} happens in add node for move. [structure/main.py]")
            Func.log(str(e), True)

    def referChildrenNodes(self, widget_id, old_widget_id):
        try:
            # 此函数只用来copy节点下的所有子节点，不包括根节点，似乎都是引用啊
            widget_type = widget_id.split('.')[0]
            if widget_type == 'Cycle' or widget_type == 'Timeline':
                # 其下面所有节点都是引用
                node: StructureNode = Info.WID_NODE[widget_id]
                old_node: StructureNode = Info.WID_NODE[old_widget_id]
                for i in range(old_node.childCount()):
                    old_child_node = old_node.child(i)
                    old_child_wid = old_child_node.widget_id
                    # 生成新widget_id进行引用
                    new_child_wid = WidgetIcon(widget_type=old_child_wid.split('.')[0]).widget_id
                    # 新增节点
                    new_child_node = StructureNode(node, new_child_wid)
                    new_child_node.setText(0, old_child_node.text(0))
                    # data
                    Info.WID_WIDGET[new_child_wid] = Info.WID_WIDGET[old_child_wid]
                    Info.WID_NODE[new_child_wid] = new_child_node
                    Info.NAME_WID[old_child_node.text(0)].append(new_child_wid)

                    self.referChildrenNodes(new_child_wid, old_child_wid)
                node.setExpanded(True)
        except Exception as e:
            print(f"error {e} happen in refer children node. [structure/main.py]")
            Func.log(str(e), True)

    # 在这里只修改而不发送信号，只是接收外部的信号来进行rename
    def renameNode(self, widget_id, name, sender=''):
        try:
            # timeline的name的修改是不存在脱离，是直接全部修改掉
            if not widget_id.startswith('Timeline.'):
                # 如果是structure发送信号过来，要改变在timeline中icon或者cycle中timeline的name
                if sender == 'structure_tree':
                    Func.renameItemInWidget(widget_id, name)
                # 普通的rename
                node = Info.WID_NODE[widget_id]
                old_name = node.text(0)
                if not Func.isReferName(old_name):
                    # 普通的rename只存在于其父节点不是引用，且其自身也不是引用
                    node.setText(0, name)
                    Info.NAME_WID[name] = Info.NAME_WID[old_name]
                    del Info.NAME_WID[old_name]
                # 之前是引用现在要分离的rename
                else:
                    # 引用存在的可能很多
                    parent_node: StructureNode = node.parent()
                    # 1：父节点不是引用，但自己是引用
                    if not Func.isReferName(parent_node.text(0)):
                        # 此时要去断开连接，指向的控件变成原有指向的复制
                        # 如果是源控件脱离引用呢？
                        if widget_id == Info.NAME_WID[old_name][0]:
                            # 按下一个widget_id生成一个拷贝，给其余所有widget_id
                            widget_copy = Info.WID_WIDGET[widget_id].clone(Info.NAME_WID[old_name][1])
                            for i in range(1, len(Info.NAME_WID[old_name])):
                                Info.WID_WIDGET[Info.NAME_WID[old_name][i]] = widget_copy
                        else:
                            Info.WID_WIDGET[widget_id] = Info.WID_WIDGET[widget_id].clone(widget_id)
                        # name_wid：从原来的list中删除，并新建一个list
                        Info.NAME_WID[old_name].remove(widget_id)
                        Info.NAME_WID[name] = [widget_id]
                        # 修改节点name
                        node.setText(0, name)
                    else:
                        # 找出非父节点引用导致的引用的其他引用节点
                        same_parent = []
                        different_parent = []
                        for wid in Info.NAME_WID[old_name]:
                            if Info.WID_NODE[wid].parent().text(0) == parent_node.text(0):
                                same_parent.append(wid)
                            else:
                                different_parent.append(wid)
                        # 2：父节点是引用导致的引用，且没有其他的引用
                        if len(different_parent) == 0:
                            for wid in same_parent:
                                Info.WID_NODE[wid].setText(0, name)
                            Info.NAME_WID[name] = Info.NAME_WID[old_name]
                            del Info.NAME_WID[old_name]
                        # 3：父节点是引用，且在其他节点下也有引用
                        else:
                            # 先生成一个源widget的拷贝
                            # 如果是源widget是在父节点引用下的
                            if Info.WID_WIDGET[widget_id].widget_id in same_parent:
                                # 需要找到一个不是父节点引用的节点，来创建新的widget
                                widget_copy = Info.WID_WIDGET[widget_id].clone(different_parent[0])
                                name_wid: list = copy.deepcopy(Info.NAME_WID[old_name])
                                # 修改name，name_wid
                                for wid in same_parent:
                                    # 从原来的name_wid删除掉
                                    Info.NAME_WID[old_name].remove(wid)
                                    Info.WID_NODE[wid].setText(0, name)
                                # 修改wid_widget
                                for wid in different_parent:
                                    Info.WID_WIDGET[wid] = widget_copy
                                    name_wid.remove(wid)
                                Info.NAME_WID[name] = name_wid
                            else:
                                widget_copy = Info.WID_WIDGET[widget_id].clone(same_parent[0])
                                name_wid: list = copy.deepcopy(Info.NAME_WID[old_name])
                                # name，name_wid, wid_widget
                                for wid in same_parent:
                                    Info.WID_WIDGET[wid] = widget_copy
                                    Info.WID_NODE[wid].setText(0, name)
                                    Info.NAME_WID[old_name].remove(wid)
                                # 不需要修改
                                for wid in different_parent:
                                    name_wid.remove(wid)
                                Info.NAME_WID[name] = name_wid
            else:
                # 是把所有的timeline的名字都改掉，而不是脱离引用,
                # 这边骚的是所有的都要改，所以要跑到每一个有这个timeline的去改
                old_name = Info.WID_NODE[widget_id].text(0)
                has_changed = []
                for timeline_wid in Info.NAME_WID[old_name]:
                    node = Info.WID_NODE[timeline_wid]
                    # renameItemInWidget的机制是输入widget_id，然后根据wid去获取父节点的widget，然后修改
                    # 由于可能存在重复，所以要去重
                    parent_name = node.parent().text(0)
                    if parent_name not in has_changed:
                        Func.renameItemInWidget(timeline_wid, name)
                        has_changed.append(parent_name)
                    node.setText(0, name)
                # data
                Info.NAME_WID[name] = Info.NAME_WID[old_name]
                del Info.NAME_WID[old_name]
            # 发送widget修改信号
            self.widgetModify.emit()
        except Exception as e:
            print(f"error {e} happens in rename node. [structure/main.py]")
            Func.log(str(e), True)

    def deleteNode(self, widget_id, sender=''):
        """
        只删除而不发送信号，只是接收外部的信号来进行delete
        删除节点，也要删除数据
        删除节点要注意父节点引用下的节点也要删除，其余应该没了
        关闭widget_tabs已经没有任何wid指向的widget的tab
        """
        try:
            # 先删除icon或者在cycle中的表格的timeline
            if sender == 'structure_tree':
                Func.deleteItemInWidget(widget_id)
            # 先递归删除子节点

            node = Info.WID_NODE[widget_id]
            children = []
            self.getChild(node, children, False)
            for child in children:
                self.deleteNode(child[1])
            #
            delete_wid = [widget_id]
            # 源节点
            name = node.text(0)
            parent_node: StructureNode = node.parent()
            parent_node.removeChild(node)
            # data
            del Info.WID_NODE[widget_id]
            del Info.WID_WIDGET[widget_id]
            Info.NAME_WID[name].remove(widget_id)
            # 引用父节点
            for refer_parent_wid in Func.getReferWidgetIds(parent_node.widget_id):
                refer_parent_node: StructureNode = Info.WID_NODE[refer_parent_wid]
                refer_node = None
                refer_node_wid = ''
                for i in range(refer_parent_node.childCount()):
                    refer_node = refer_parent_node.child(i)
                    refer_node_wid = refer_node.widget_id
                    if refer_node_wid in Info.NAME_WID[node.text(0)]:
                        break
                if refer_node:
                    refer_parent_node.removeChild(refer_node)
                    del Info.WID_NODE[refer_node_wid]
                    del Info.WID_WIDGET[refer_node_wid]
                    Info.NAME_WID[name].remove(refer_node_wid)
                    delete_wid.append(refer_node_wid)
                else:
                    raise Exception("fail to find refer node in refer parent.")
            # 如果这个引用被清空了，删除相应数据
            if not len(Info.NAME_WID[name]):
                # 删除显示的tab
                # 如果是timeline或者cycle
                self.widgetDelete.emit(widget_id)
                del Info.NAME_WID[name]
            else:
                # 有一个可能，被删除的节点是源节点，所以要改变源widget的widget_id啊
                widget = Info.WID_WIDGET[Info.NAME_WID[name][0]]
                if widget.widget_id in delete_wid:
                    widget.changeWidgetId(Info.NAME_WID[name][0])

            # modify
            self.widgetModify.emit()
        except Exception as e:
            print(f"error {e} happens in delete node. [structure/main.py]")
            Func.log(str(e), True)

    def moveNode(self, widget_id, drag_col, target_col):
        try:
            if target_col != -1:
                node = Info.WID_NODE[widget_id]
                parent_node: StructureNode = node.parent()
                if target_col > parent_node.childCount():
                    target_col = parent_node.childCount()
                parent_node.removeChild(node)
                parent_node.insertChild(target_col - 1, node)

                refer_parent_wids = Func.getReferWidgetIds(parent_node.widget_id)
                for refer_parent_wid in refer_parent_wids:
                    refer_parent_node: StructureNode = Info.WID_NODE[refer_parent_wid]
                    refer_node = None
                    for i in range(refer_parent_node.childCount()):
                        refer_node = refer_parent_node.child(i)
                        if refer_node.text(0) == node.text(0):
                            break
                    if refer_node:
                        refer_parent_node.removeChild(refer_node)
                        refer_parent_node.insertChild(target_col - 1, refer_node)
                    else:
                        raise Exception("fail to find refer node in refer parent.")
        except Exception as e:
            print(f"error {e} happens in move node in structure. [structure.main.py]")
            Func.log(str(e), True)

    def getStructure(self, requester=None):
        """
        广度优先遍历, 得到一整颗树的结构
        :type requester: 调用者
        :return:
        """
        structure_tree: list = []
        for i in range(self.structure_tree.topLevelItemCount()):
            sub_tree: list = []
            root: StructureNode = self.structure_tree.topLevelItem(i)
            sub_tree.append((root.text(0), root.widget_id))
            self.getChild(root, sub_tree)
            structure_tree.append(sub_tree)
        if requester:
            if len(structure_tree) == 1:
                return structure_tree[0]
            else:
                return structure_tree
        return WidTree(structure_tree[0])

    def getChild(self, root: StructureNode, sub_tree: list, recursive: bool = True):
        """
        广度优先遍历递归得到所有的子节点
        :param root:
        :param sub_tree: 作为载体
        :return:
        """
        if recursive:
            for i in range(root.childCount()):
                child: StructureNode = root.child(i)
                if child.widget_id.startswith(Info.CYCLE):
                    child_tree: list = [(child.text(0), child.widget_id)]
                    self.getChild(child, child_tree)
                    sub_tree.append(child_tree)
                elif child.widget_id.startswith(Info.TIMELINE):
                    child_tree: list = [(child.text(0), child.widget_id)]
                    self.getChild(child, child_tree)
                    sub_tree.append(child_tree)
                else:
                    key: tuple = (child.text(0), child.widget_id)
                    sub_tree.append(key)
        else:
            for i in range(root.childCount()):
                child: StructureNode = root.child(i)
                key: tuple = (child.text(0), child.widget_id)
                sub_tree.append(key)

    def loadStructure(self, tree: list):
        """
        从文件加载structure
        :param tree: 树结构
        :return:
        """
        parent_widget_id = tree[0][1]
        for subtree in tree[1:]:
            if isinstance(subtree, list):
                name, widget_id = subtree[0]
                self.loadWidgetAndNode(parent_widget_id, widget_name=name, widget_id=widget_id)
                self.loadStructure(subtree)
            elif isinstance(subtree, tuple):
                name, widget_id = subtree
                self.loadWidgetAndNode(parent_widget_id, widget_name=name, widget_id=widget_id)

    def loadWidgetAndNode(self, parent_widget_id: str, widget_name: str, widget_id: str):
        """
        先在structure中创建node，然后适时创建widget
        :param parent_widget_id: 父控件的widget_id
        :param widget_name: 控件名
        :param widget_id: 待复原控件的widget_id
        :return:
        """
        # 判断父节点是否在
        if parent_widget_id in Info.WID_NODE:
            # 添加节点
            parent = Info.WID_NODE[parent_widget_id]
            node = StructureNode(parent, widget_id)
            node.setText(0, widget_name)
            parent.setExpanded(True)

            # wid_node
            Info.WID_NODE[widget_id] = node

            # 如果为源widget(wid_name的值的第一个wid), 创建控件
            origin_wid = Info.NAME_WID[widget_name][0]
            if widget_id == origin_wid:
                # 可能在创建被引用节点时已经创建
                if widget_id not in Info.WID_WIDGET:
                    Func.createWidget(widget_id)
                    setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
                    properties = setting.value(widget_id)
                    if properties:
                        Func.restore(widget_id, properties)
                    # 连接信号
                    self.widgetSignalsLink.emit(widget_id)
            else:
                # 有可能被引用的节点先于源节点复原
                if origin_wid not in Info.WID_WIDGET:
                    # 创建源
                    Func.createWidget(origin_wid)
                    setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
                    properties = setting.value(origin_wid)
                    if properties:
                        Func.restore(origin_wid, properties)
                    # 连接信号
                    self.widgetSignalsLink.emit(origin_wid)
                # 要链接过去
                Info.WID_WIDGET[widget_id] = Info.WID_WIDGET[origin_wid]

    def isFocused(self) -> int:
        """
        返回当前窗口是否为焦点
        :return:
        """
        if self.structure_tree.focus:
            return Info.StructureFocused
        return Info.NotFocused
