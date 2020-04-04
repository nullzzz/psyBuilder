import os
import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget

from app.info import Info


class Func(object):
    """
    This class stores some common functions
    """

    ###########################################
    #           old version func              #
    ###########################################
    @staticmethod
    def getWidgetImage(widget_type: str, image_type: str = 'icon') -> QPixmap or QIcon:
        """
        返回widget_type对应的图片
        :param widget_type: widget类型
        :param image_type: 返回图片类型
        :return:
        """
        # 得到图片路径
        if widget_type in Info.WIDGET_TYPE_IMAGE_PATH:
            path = Info.WIDGET_TYPE_IMAGE_PATH[widget_type]
            if image_type == "icon":
                return QIcon(path)
            else:
                return QPixmap(path)
        raise Exception("unknown widget type.")

    @staticmethod
    def getImage(image_name: str) -> str:
        """
        返回指定name的图片路径
        :param image_name:
        :return:
        """
        return os.path.join(Info.IMAGE_SOURCE_PATH, image_name)

    @staticmethod
    def getPsyIconPath() -> str:
        return os.path.join(Info.IMAGE_SOURCE_PATH, "psy.ico")

    @staticmethod
    def getIOType(device_type: str) -> int:
        device_type = device_type.split(".")[0]
        if device_type in ("network_port", "parallel_port", "serial_port", "screen", "sound"):
            return Info.OUTPUT_DEVICE
        return Info.INPUT_DEVICE

    @staticmethod
    def getProperties(widget_id) -> dict:
        """
        按widget_id得到对应widget的属性
        :param widget_id:
        :return:
        """
        return Func.getWidgetProperties(widget_id)

    @staticmethod
    def delWidget(widget_id: str) -> None:
        """
        删除widget，几乎没用，python不支持主动的内存回收
        :param widget_id:
        :return:
        """
        try:
            if widget_id.startswith("If") or widget_id.startswith("Switch"):
                sub_wid = Info.WID_WIDGET[widget_id].getSubWidgetId()
                for wid in sub_wid:
                    Info.WID_WIDGET.pop(wid)
            Info.WID_WIDGET.pop(widget_id)
        except KeyError:
            pass

    @staticmethod
    def createWidget(widget_id: str, visible: bool = True):
        raise Exception("Deprecated functions")

    @staticmethod
    def getAttributes(widget_id, detail=False) -> dict or list:
        return Func.getWidgetAttributes(widget_id, detail)

    @staticmethod
    def getWidgetPosition(widget_id: str) -> int:
        return Func.getWidgetIndex(widget_id)

    @staticmethod
    def getNextWidgetId(widget_id: str) -> str:
        """
        得到附近下一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            return Info.ERROR_WIDGET_ID
        #
        try:
            node = Info.WID_NODE[widget_id]
            parent_node = node.parent()
            # if node is if/switch's child node
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                node = parent_node
                parent_node = node.parent()
            index = parent_node.indexOfChild(node)
            try:
                return parent_node.child(index + 1).widget_id
            except:
                return Info.ERROR_WIDGET_ID
        except:
            return Info.ERROR_WIDGET_ID

    @staticmethod
    def getPreviousWidgetId(widget_id: str) -> str:
        """
        得到附近前一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            return Info.ERROR_WIDGET_ID
        #
        try:
            node = Info.WID_NODE[widget_id]
            parent_node = node.parent()
            # if node is if/switch's child node
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                node = parent_node
                parent_node = node.parent()
            index = parent_node.indexOfChild(node)
            try:
                return parent_node.child(index - 1).widget_id
            except:
                return Info.ERROR_WIDGET_ID
        except:
            return Info.ERROR_WIDGET_ID

    @staticmethod
    def getWidgetIDInTimeline(widget_id: str) -> list:
        """
        得到一个timeline中所有的widget的widget_id的list，按顺序放置
        :param widget_id: timeline的widget_id
        :return:
        """
        return Func.getWidgetChildren(widget_id)

    @staticmethod
    def isCitingValue(value: str) -> bool:
        # print(f"line 616: {value}")
        if re.fullmatch(r"\[[A-Za-z]+[a-zA-Z\._0-9]*\]", value):
            return True
        return False

    @staticmethod
    def getCurrentScreenRes(screen_id: str) -> tuple:
        resolution = Info.OUTPUT_DEVICE_INFO[screen_id].get('Resolution', "auto")
        wh = resolution.lower().split('x')

        if len(wh) > 1:
            width = int(wh[0])
            height = int(wh[1])
        else:
            scr_rect = QDesktopWidget().screenGeometry()
            width = scr_rect.width()
            height = scr_rect.height()
        return width, height

    @staticmethod
    def isRGBStr(RGBStr: str):
        if re.fullmatch("^\d+,\d+,\d+$", RGBStr):
            output = RGBStr.split(',')
            return output

        return False

    @staticmethod
    def isWidgetType(widget_id: str, widget_type: str):
        """
        根据输入的widget_id来判断是不是输入的类型
        :param widget_id: 需要判断的id
        :param widget_type: 需要确定的类型
        :return:
        """
        try:
            return widget_id.split('.')[0] == widget_type
        except:
            return False

    @staticmethod
    def createDeviceId(device_type: str):
        current_id = Info.device_count[device_type]
        Info.device_count[device_type] = current_id + 1
        return f"{device_type}.{current_id}"

    @staticmethod
    def getDeviceInfo(device_type: str) -> dict:
        """
        for each widget which has device information such as screen or sound.
        :param device_type: screen or sound, and maybe more in the future.
        :return:
        """
        devices = {}
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.QUEST_DEVICE_INFO, **Info.TRACKER_DEVICE_INFO}.items():
            if k.startswith(device_type):
                devices[k] = v["Device Name"]
        return devices

    @staticmethod
    def getDeviceNameById(device_id: str) -> str:
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_id == k:
                return v.get("Device Name")
        return ""

    @staticmethod
    def getDeviceIdByName(device_name: str):
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_name == v.get("Device Name"):
                return k
        return ""

    @staticmethod
    def log(text, error=False, timer=True):
        Func.print(text)

    @staticmethod
    def getParentWid(widget_id: str) -> str:
        return Func.getWidgetParent(widget_id)

    @staticmethod
    def getWidLevel(widget_id: str) -> int:
        """
        通过输入的wid得到该widget所在层级，从0开始累加，即最初始的timeline为0，往后递增
        :param widget_id: 输入的wid
        :return: 如果wid不存在，返回-1
        """
        try:
            node = Info.WID_NODE[widget_id]
        except:
            return -1
        # 不断迭代，直至父结点为空
        level = 0
        node = node.parent()
        while node:
            node = node.parent()
            level += 1
        return level

    @staticmethod
    def getWidgetsTotalLayer(widget_id: str = f"{Info.TIMELINE}.0") -> int:
        """
        返回最大level，深度优先遍历
        :return:
        """
        node = Info.WID_NODE[widget_id]
        max_child_count = 0
        for i in range(node.childCount()):
            temp_count = Func.getWidgetsTotalLayer(node.widget_id)
            if temp_count > max_child_count:
                max_child_count = temp_count
        return 1 + max_child_count

    ###########################################
    #           new version func              #
    ###########################################
    @staticmethod
    def getWidget(widget_id: str):
        """
        get widget through its widget id
        """
        return Info.Widgets[widget_id]

    @staticmethod
    def getNode(widget_id: str):
        """
        get node through its widget id
        """
        return Info.Nodes[widget_id]

    @staticmethod
    def generateWidgetId(widget_type: str) -> str:
        """
        generate a valid widget id
        """
        count = Info.WidgetTypeCount[widget_type]
        widget_id = f"{widget_type}.{count}"
        Info.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: str) -> str:
        """
        generate a valid widget name
        """
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type}_{Info.WidgetNameCount[widget_type]}"
            # inc count of this widget type
            Info.WidgetNameCount[widget_type] += 1
            # check name's validity
            if widget_name not in Info.Names:
                return widget_name

    @staticmethod
    def checkWidgetNameValidity(widget_name: str) -> (bool, str):
        """
        check the validity of widget name.
        It should be unique, unless it's a reference.
        """
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", widget_name):
            return False, "Name must start with a letter and contain only letters, numbers and _."
        if widget_name in Info.Names:
            return False, "Name already exists."
        return True, ""

    @staticmethod
    def getWidgetType(widget_id: str):
        """
        get widget's type through its widget id
        """
        return widget_id.split('.')[0]

    @staticmethod
    def getWidgetName(widget_id: str):
        """
        get widget's name
        """
        return Info.Widgets[widget_id].widget_name

    @staticmethod
    def checkWidgetNameExisted(widget_name: str) -> bool:
        """
        check widget name whether existed
        """
        return widget_name in Info.Names

    @staticmethod
    def getWidgetReference(widget_id: str) -> list:
        """
        get list of reference widget's widget id
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        return Info.Names[widget_name]

    @staticmethod
    def getWidgetParent(widget_id: str) -> str:
        """
        get parent's widget id
        @param widget_id:
        @return:
        """
        return Info.Nodes[widget_id].parent().widget_id

    @staticmethod
    def getWidgetChild(widget_id: str, index: int) -> (str, str):
        """

        @param widget_id:
        @param index:
        @return: child's widget id and widget name
        """
        child = Info.Nodes[widget_id].child(index)
        return child.widget_id, child.text(0)

    @staticmethod
    def getWidgetChildren(widget_id: str) -> list:
        """
        get its children
        @param widget_id:
        @return: list of children's widget id and widget name
        """
        root = Info.Nodes[widget_id]
        children = []
        for i in range(root.childCount()):
            child = root.child(i)
            children.append((child.widget_id, child.text(0)))
        return children

    @staticmethod
    def getWidgetIndex(widget_id: str) -> int:
        """
        get widget's index in timeline
        @param widget_id:
        @return:
        """
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            # we ignore timeline'pos
            return -1
        node = Info.Nodes[widget_id]
        parent_node = node.parent()
        if parent_node:
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                # if widget is child of if/switch, its pos is its parent's pos
                node = parent_node
                parent_node = node.parent()
            return parent_node.indexOfChild(node)
        else:
            return -1

    @staticmethod
    def getWidgetProperties(widget_id: str) -> dict:
        """
        get widget's properties through its widget id
        """
        widget = Info.Widgets[widget_id]
        return widget.getProperties()

    @staticmethod
    def getWidgetAttributes(widget_id: str, detail: bool = False):
        """
        get widget's attributes through its widget id

        """
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subSex": 0, "subHandness": 0, "subAge": 0}

        # 添加quest设备全局参数
        if len(Info.QUEST_DEVICE_INFO.items()) > 1:
            attributes["questRandValue"] = ""
        for k, v in Info.QUEST_DEVICE_INFO.items():
            v: dict
            quest_name = v.get("Device Name")
            attributes[f"{quest_name}.cValue"] = ""

        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Info.Nodes[widget_id]
        depth = -1
        while node:
            depth += 1
            node = node.parent()
        # do 1.
        node = Info.Nodes[widget_id]
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.TIMELINE):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.CYCLE):
                    for attribute in Info.Widgets[child_node.widget_id].getHiddenAttributes():
                        attributes[f"{child_node.text(0)}.{attribute}"] = depth
        # do 2. 3.
        first = True
        node = node.parent()
        depth -= 1
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.CYCLE):
                cycle = Info.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes[f"{cycle_name}.attr.{attribute}"] = depth
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Info.Widgets[node.widget_id].getHiddenAttributes()
                    for attribute in first_cycle_hidden_attributes:
                        attributes[f"{cycle_name}.{attribute}"] = depth
                    first = False
            node = node.parent()
            depth -= 1

        # ********* untested ************
        # 是否需要详细信息
        return attributes if detail else attributes.keys()

    @staticmethod
    def getImageObject(image_path: str, type: int = 0, size: QSize = None) -> QPixmap or QIcon:
        """
        get image from its relative path, return qt image object, include QPixmap or QIcon.
        @param image_path: its relative path
        @param type: 0: pixmap (default),
                     1: icon
        @return: Qt image object
        """
        path = os.path.join(Info.Image_Path, image_path)
        if not type:
            if size:
                return QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation)
            return QPixmap(path)
        return QIcon(path)

    @staticmethod
    def startWait():
        """
        show loading window
        """
        Info.Psy.startWait()

    @staticmethod
    def endWait():
        """
        close loading window
        """
        Info.Psy.endWait()

    @staticmethod
    def print(information: str, information_type: int = 0):
        """
        print information in output.
        information_type: 0 none
                          1 success
                          2 fail
        """
        Info.Psy.output.print(str(information), information_type)

    @staticmethod
    def checkReferValidity(target_timeline_widget_id: str, widget_id: str) -> bool:
        """
        当从structure中拖拽至timeline时，
        :param target_timeline_widget_id: 目标的timeline的wid
        :param widget_id: 被拖拽的wid
        :return: 合法性
        """
        target_timeline_node = Info.Nodes[target_timeline_widget_id]
        widget_name = Func.getWidgetName(widget_id)
        # 先确定被拖拽的widget所属的cycle是否与target的timeline所属的cycle是否为同一个
        # target_timeline不能是第一层timeline，因为它没有父cycle
        if target_timeline_widget_id == f"{Info.TIMELINE}.0":
            return False
        cycle_1_wid = target_timeline_node.parent().widget_id
        # 根据widget得到父timeline
        parent_timeline_node = Info.Nodes[Func.getWidgetParent(widget_id)]
        # 如果是父亲为第一层timeline，其没有父cycle
        if parent_timeline_node.widget_id == f"{Info.TIMELINE}.0":
            return False
        cycle_2_wid = parent_timeline_node.parent().widget_id
        # 父cycle是否相同
        if cycle_1_wid == cycle_2_wid:
            return True
        return False
