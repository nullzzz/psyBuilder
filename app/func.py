import os
import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtWidgets import QDesktopWidget

from app.info import Info
from app.kernel import Kernel


class Func(object):
    """
    存放一些通用函数
    """

    @staticmethod
    def getImagePath(image_name: str) -> str:
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
    def changeCertainDeviceNameWhileUsing(device_id: str, device_name):
        """
        abort at 2019-8-1
        :param device_id:
        :param device_name:
        :return:
        """
        for widget_ids in Info.NAME_WID.values():
            for widget_id in widget_ids:
                widget_type = widget_id.split(".")[0]
                if widget_type in ("Image", "Sound", "Video", "Slider", "Text"):
                    widget = Info.WID_WIDGET[widget_id]
                    widget.pro_window.duration.changeCertainDeviceName(device_id, device_name)
                    widget.apply()

    @staticmethod
    def getProperties(widget_id, is_show: bool = False) -> dict:
        """
        # todo This function is abandoned, It's better to use getWidgetProperties
        按widget_id得到对应widget的属性
        :param widget_id:
        :param is_show: 是否呈现在properties界面
        :return:
        """
        widget = Info.WID_WIDGET[widget_id]
        if widget_id not in Info.WID_NODE.keys():
            return widget.getInfo()
        if hasattr(widget, "refresh"):
            widget.refresh()
        if is_show and hasattr(widget, "getShowProperties"):
            return widget.getShowProperties()
        return widget.getInfo()

    @staticmethod
    def getNameCount(widget_type: str) -> int:
        """
        某个widget type的name的已有count
        :param widget_type:
        :return:
        """
        count = -1
        if widget_type in Kernel.WidgetNameCount:
            count = Kernel.WidgetNameCount[widget_type]
            Kernel.WidgetNameCount[widget_type] += 1
        return count

    @staticmethod
    def generateValidName(widget_id: str) -> str:
        """
        根据widget_id, 生成一个非重复的name
        :param widget_id: 已经生成的widget_id
        :return: 生产的name
        """
        widget_type = widget_id.split('.')[0]
        while True:
            count = Func.getNameCount(widget_type)
            if count == -1:
                raise Exception("fail to generate a valid name, because unknown widget type.")
            name = f"{widget_type}_{count}"
            if name not in Info.NAME_WID:
                break
        return name

    @staticmethod
    def checkNameValidity(name: str) -> (bool, str):
        """
        检查某个name的合法性，首字符为字母且不重复
        :param name: 需要检测的name
        :return: 是否合法
        """
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name):
            return False, "Name must start with a letter and contain only letters, numbers and _"
        return not (name in Info.NAME_WID), 'Name has already existed.'

    @staticmethod
    def isReferName(name: str) -> bool:
        """
        检测name是否对应的widget是否存在引用
        :param name: 需要检测的name
        :return: 是否存在引用
        """
        return len(Info.NAME_WID[name]) > 1

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
    def getAttributes(widget_id) -> dict or list:
        """
        get widget's attributes through its widget id
        """
        # global attributes
        attributes = ["subName", "subNum", "sessionNum", "subSex", "subHandness", "subAge"]
        # attributes about quest
        for key, value in Kernel.QuestInfo.items():
            attributes.append(f"{value.get('Quest Name')}.cValue")
        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Kernel.Nodes[widget_id]
        # do 1.
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.TIMELINE):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.CYCLE):
                    for attribute in Kernel.Widgets[child_node.widget_id].getHiddenAttribute():
                        attributes.append(f"{child_node.text(0)}.{attribute}")
        # do 2. 3.
        first = True
        node = node.parent()
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.CYCLE):
                cycle = Kernel.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes.append(f"{cycle_name}.attr.{attribute}")
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Kernel.Widgets[node.widget_id].getHiddenAttributes()
                    for attribute in first_cycle_hidden_attributes:
                        attributes.append(f"{cycle_name}.{attribute}")
                    first = False
            node = node.parent()
        # return
        return attributes

    @staticmethod
    def getWidgetPosition(widget_id: str) -> int:
        """
        返回一个widget在timeline中的位置索引，从0开始
        如果查询的widget_id不存在位置信息，返回-1
        :param widget_id: 要查询的widget的id
        :return: 位置信息
        """
        # 如果是widget是timeline，不存在位置信息
        if widget_id.startswith(Info.TIMELINE):
            return -1
        #
        try:
            node = Info.WID_NODE[widget_id]
            parent_node = node.parent()
            # if node is if/switch's child node
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                node = parent_node
                parent_node = node.parent()
            return parent_node.indexOfChild(node)
        except:
            print(f"error: widget not founded.")
            return -1

    @staticmethod
    def getNextWidgetId(widget_id: str) -> str or None:
        """
        得到附近下一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if widget_id.startswith(Info.TIMELINE):
            return None
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
                return None
        except:
            print(f"error: widget not founded.")
            return None

    @staticmethod
    def getPreviousWidgetId(widget_id: str) -> str or None:
        """
        得到附近前一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if widget_id.startswith(Info.TIMELINE):
            return None
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
                return None
        except:
            print(f"error: widget not founded.")
            return None

    @staticmethod
    def getWidgetIDInTimeline(timeline_widget_id: str) -> list:
        """
        todo update it
        得到一个timeline中所有的widget的widget_id的list，按顺序放置
        :param timeline_widget_id: timeline的widget_id
        :return:
        """
        try:
            timeline_node = Info.WID_NODE[timeline_widget_id]
            return [timeline_node.child(i).widget_id for i in range(timeline_node.childCount())]
        except:
            print("error: timeline not founded.")
            return []

    @staticmethod
    def isCitingValue(value: str) -> bool:
        # print(f"line 616: {value}")
        if re.fullmatch(r"\[[A-Za-z]+[a-zA-Z\._0-9]*\]", value):
            return True
        return False

    @staticmethod
    def getCurrentScreenRes(screen_id: str) -> tuple:
        resolution = Info.OUTPUT_DEVICE_INFO[screen_id].get('Resolution', "auto")
        # print(f"------------/")
        # print(f"{screen_id}")

        wh = resolution.lower().split('x')

        if len(wh) > 1:
            width = int(wh[0])
            height = int(wh[1])
            # print(f"{width},{height}")
        else:
            scr_rect = QDesktopWidget().screenGeometry()
            width = scr_rect.width()
            height = scr_rect.height()
        #     print(f"{scr_rect}")
        # print(f"------------\\")
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
    def getTrackingPix(text):
        pix = QPixmap(200, 16)
        pix.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pix)
        painter.drawText(0, 0, 200, 16, Qt.TextSingleLine, text)
        return pix

    @staticmethod
    def createDeviceId(device_type: str):
        current_id = Info.device_count[device_type]
        Info.device_count[device_type] = current_id + 1
        return f"{device_type}.{current_id}"

    @staticmethod
    def getScreen() -> list:
        screens = []
        for k, v in Info.OUTPUT_DEVICE_INFO.items():
            if k.startswith("screen"):
                screens.append(v["Device Name"])
        return screens

    @staticmethod
    def getScreenInfo() -> dict:
        info: dict = {}
        for k, v in Info.OUTPUT_DEVICE_INFO.items():
            if k.startswith("screen"):
                info[k] = v["Device Name"]
        return info

    @staticmethod
    def getSoundInfo() -> dict:
        info: dict = {}
        for k, v in Info.OUTPUT_DEVICE_INFO.items():
            if k.startswith("sound"):
                info[k] = v["Device Name"]
        return info

    @staticmethod
    def getSound() -> list:
        sounds = []
        for k, v in Info.OUTPUT_DEVICE_INFO.items():
            if k.startswith("sound"):
                sounds.append(v["Device Name"])
        return sounds

    @staticmethod
    def getDeviceInfoByName(device_name: str) -> dict or None:
        """
        由设备名称获取设备信息
        :param device_name:
        :return: device info dict
        """
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_name == v.get("Device Name"):
                return v
        return

    @staticmethod
    def getDeviceNameById(device_id: str):
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_id == k:
                # print(627)
                # print(v.get("Device Name"))
                return v.get("Device Name")
        return ""

    @staticmethod
    def getDeviceIdByName(device_name: str):
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_name == v.get("Device Name"):
                return k
        return ""

    @staticmethod
    def getQuestInfo():
        info: dict = {}
        for k, v in Info.QUEST_INFO.items():
            info[k] = v.get("Quest Name")
        return info

    @staticmethod
    def getTrackerInfo():
        info: dict = {}
        for k, v in Info.TRACKER_INFO.items():
            info[k] = v.get("Tracker Name")
        return info

    @staticmethod
    def getParentWid(wid: str) -> str:
        """
        根据输入的wid参数，得到他的父节点的wid
        :param wid: 输入的参数
        :return: 父节点的wid， 如果没有父节点返回“”
        """
        try:
            return Info.WID_NODE[wid].parent().widget_id
        except:
            return ""

    @staticmethod
    def getWidLevel(wid: str) -> int:
        """
        通过输入的wid得到该widget所在层级，从0开始累加，即最初始的timeline为0，往后递增
        :param wid: 输入的wid
        :return: 如果wid不存在，返回-1
        """
        try:
            node = Info.WID_NODE[wid]
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
    def getWidgetsTotalLayer(wid: str = f"{Info.TIMELINE}.0") -> int:
        """
        返回最大level，深度优先遍历
        :return:
        """
        node = Info.WID_NODE[wid]
        max_child_count = 0
        for i in range(node.childCount()):
            temp_count = Func.getWidgetsTotalLayer(node.widget_id)
            if temp_count > max_child_count:
                max_child_count = temp_count
        return 1 + max_child_count

    ###############################
    #         new version         #
    ###############################

    @staticmethod
    def getWidget(widget_id: str):
        """
        get widget through its widget id
        """
        return Kernel.Widgets[widget_id]

    @staticmethod
    def getNode(widget_id: str):
        """
        get node through its widget id
        """
        return Kernel.Nodes[widget_id]

    @staticmethod
    def generateWidgetId(widget_type: str) -> str:
        """
        generate a valid widget id
        """
        count = Kernel.WidgetTypeCount[widget_type]
        widget_id = f"{widget_type}.{count}"
        Kernel.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: str) -> str:
        """
        generate a valid widget name
        """
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type}_{Kernel.WidgetNameCount[widget_type]}"
            # inc count of this widget type
            Kernel.WidgetNameCount[widget_type] += 1
            # check name's validity
            if widget_name not in Kernel.Names:
                return widget_name

    @staticmethod
    def checkWidgetNameValidity(widget_name: str) -> (bool, str):
        """
        check the validity of widget name.
        It should be unique, unless it's a reference.
        """
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", widget_name):
            return False, "Name must start with a letter and contain only letters, numbers and _."
        if widget_name in Kernel.Names:
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
        return Kernel.Widgets[widget_id].widget_name

    @staticmethod
    def checkWidgetNameExisted(widget_name: str) -> bool:
        """
        check widget name whether existed
        """
        return widget_name in Kernel.Names

    @staticmethod
    def getWidgetReference(widget_id: str) -> list:
        """
        get list of reference widget's widget id
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        return Kernel.Names[widget_name]

    @staticmethod
    def getWidgetParent(widget_id: str) -> str:
        """
        get parent's widget id
        @param widget_id:
        @return:
        """
        return Kernel.Nodes[widget_id].parent().widget_id

    @staticmethod
    def getWidgetChild(widget_id: str, index: int) -> (str, str):
        """

        @param widget_id:
        @param index:
        @return: child's widget id and widget name
        """
        child = Kernel.Nodes[widget_id].child(index)
        return child.widget_id, child.text(0)

    @staticmethod
    def getWidgetChildren(widget_id: str) -> list:
        """

        @param widget_id:
        @return: list of children's widget id and widget name
        """
        root = Kernel.Nodes[widget_id]
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
            return -1
        node = Kernel.Nodes[widget_id]
        if node.parent():
            return node.parent().indexOfChild(node)
        else:
            return -1

    @staticmethod
    def getWidgetProperties(widget_id: str):
        """
        get widget's properties through its widget id
        """
        widget = Kernel.Widgets[widget_id]
        return widget.getProperties()

    @staticmethod
    def getWidgetAttributes(widget_id: str):
        """
        get widget's attributes through its widget id
        """
        # global attributes
        attributes = ["subName", "subNum", "sessionNum", "subSex", "subHandness", "subAge"]
        # attributes about quest
        for key, value in Kernel.QuestInfo.items():
            attributes.append(f"{value.get('Quest Name')}.cValue")
        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Kernel.Nodes[widget_id]
        # do 1.
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.TIMELINE):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.CYCLE):
                    for attribute in Kernel.Widgets[child_node.widget_id].getHiddenAttribute():
                        attributes.append(f"{child_node.text(0)}.{attribute}")
        # do 2. 3.
        first = True
        node = node.parent()
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.CYCLE):
                cycle = Kernel.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes.append(f"{cycle_name}.attr.{attribute}")
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Kernel.Widgets[node.widget_id].getHiddenAttributes()
                    for attribute in first_cycle_hidden_attributes:
                        attributes.append(f"{cycle_name}.{attribute}")
                    first = False
            node = node.parent()
        # return
        return attributes

    @staticmethod
    def getImage(image_path: str, type: int = 0, size: QSize = None) -> QPixmap or QIcon:
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
        Kernel.Psy.startWait()

    @staticmethod
    def endWait():
        """
        close loading window
        """
        Kernel.Psy.endWait()

    @staticmethod
    def print(information: str, information_type: int = 0):
        """
        print information in output.
        information_type: 0 none
                          1 success
                          2 fail
        """
        Kernel.Psy.output.print(information, information_type)
