import os
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
    def getWidgetImage(widget_type: str, image_type: str = 'icon') -> QPixmap or QIcon:
        """
        todo update
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
    def getWidgetType(widget_id: str):
        """
        get widget's type through its widget id
        """
        return widget_id.split('.')[0]

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
    def restore(widget_id: str, properties: dict) -> None:
        """
        复原控件属性
        :param widget_id: 控件id
        :param properties: 控件属性
        :return:
        """
        widget = Info.WID_WIDGET.get(widget_id, None)
        if widget:
            widget.restore(properties)
        else:
            print("No such widget")

    @staticmethod
    def getProperties(widget_id, is_show: bool = False) -> dict:
        """
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
    def getWidgetName(widget_id: str) -> str:
        """
        根据widget_id得到对应widget的name
        :param widget_id:
        :return:
        """
        if widget_id in Info.WID_NODE:
            return Info.WID_NODE[widget_id].text(0)
        raise Exception(f"fail to get widget name for {widget_id}. [func.py]")

    @staticmethod
    def getNameCount(widget_type: str) -> int:
        """
        某个widget type的name的已有count
        :param widget_type:
        :return:
        """
        count = -1
        if widget_type in Info.WIDGET_TYPE_NAME_COUNT:
            count = Info.WIDGET_TYPE_NAME_COUNT[widget_type]
            Info.WIDGET_TYPE_NAME_COUNT[widget_type] += 1
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
    def generateWidgetId(widget_type) -> str:
        """
        生成一个合法的widget_id
        :param widget_type: widget的类型
        :return: 生成的widget_id
        """
        if widget_type in Info.WIDGET_TYPE_ID_COUNT:
            count = Info.WIDGET_TYPE_ID_COUNT[widget_type]
            Info.WIDGET_TYPE_ID_COUNT[widget_type] += 1
            return f"{widget_type}.{count}"
        raise Exception('fail to generate widget id, because unknown widget type.')

    @staticmethod
    def checkTimelineNameValidity(name: str, cycle_widget_id: str) -> (int, str):
        """
        检测timeline的name的合法性，检测是否类似死锁等等
        :param name: 要检测的name
        :param cycle_widget_id: timeline所属的cycle
        :return: 检测结果类型，及对应提示
        """
        if name not in Info.NAME_WID:
            if not name:
                return Info.TimelineNameError, ''
            if re.match(r"^[a-zA-Z][a-zA-Z_0-9]*$", name):
                return Info.TimelineNameRight, ''
            return Info.TimelineNameError, ''
        else:
            # 如果已经存在，且为同一个cycle下的timeline，则返回正确，否则返回出错
            cycle_node = Info.WID_NODE[cycle_widget_id]
            # 因为timeline已经不允许引用了，所以不会出现父节点为不同的cycle，所以直接判断cycle下是否有那个name即可
            try:
                for index in range(cycle_node.childCount()):
                    if cycle_node.child(index).text(0) == name:
                        return Info.TimelineNameRight, ""
            except Exception as e:
                print(e)
            return Info.TimelineParentError, ""
            # 需求要求timeline不能引用，说不定哪天让我改回来，现将下方代码注释
            # widget_id = Info.NAME_WID[name][0]
            # # 类型
            # if widget_id.split('.')[0] == Info.TIMELINE:
            #     # 是否存在于父节点
            #     # 对于判断想引用的timeline是不是cycle的父节点,
            #     # 要确认所有引用的cycle的父节点timeline是不是在name的引用，比较繁琐啊
            #     parent_timeline_list = []
            #     for cycle_wid in Info.NAME_WID[Info.WID_NODE[cycle_widget_id].text(0)]:
            #         node = Info.WID_NODE[cycle_wid].parent()
            #         while node:
            #             if node.widget_id.startswith(Info.TIMELINE):
            #                 parent_timeline_list.append(node.widget_id)
            #             node = node.parent()
            #     for timeline_wid in parent_timeline_list:
            #         if timeline_wid in Info.NAME_WID[name]:
            #             return Info.TimelineParentError, ''
            #     return Info.TimelineNameExist, widget_id
            # return Info.TimelineTypeError, ''

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
    def getAttributes(widget_id, need_detail=False) -> dict or list:
        """
        根据某个节点的wid得到它的属性，根据属性返回是否需要详细信息，
        :param widget_id:
        :param need_detail: 是否需要详细的信息即属性的值
        :return:
        """
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subSex": 0, "subHandness": 0, "subAge": 0}

        # 添加quest设备全局参数
        for k, v in Info.QUEST_INFO.items():
            v: dict
            quest_name = v.get("Quest Name")
            attributes[f"{quest_name}.cValue"] = ""
        node = Info.WID_NODE[widget_id]
        node_parent = node.parent()
        # 得到到第0层一共多少层
        layer_count = -1
        while node:
            layer_count += 1
            node = node.parent()
        # 如果挂在timeline下要得到在其前面的兄弟节点的一些隐藏属性
        if node_parent and node_parent.widget_id.startswith(Info.TIMELINE):
            for i in range(node_parent.childCount()):
                child_node = node_parent.child(i)
                if child_node.widget_id == widget_id:
                    break
                # cycle不要
                if Func.isWidgetType(child_node.widget_id, Info.CYCLE):
                    continue
                for attribute in Info.WID_WIDGET[child_node.widget_id].getHiddenAttribute():
                    attributes[f"{child_node.text(0)}.{attribute}"] = layer_count
        # 其第一次父cycle的hide属性也要
        # 往上递归
        first_parent = True
        node = Info.WID_NODE[widget_id].parent()
        layer_count -= 1
        while node:
            # 每逢cycle要获得一次属性，且格式特殊
            if Func.isWidgetType(node.widget_id, Info.CYCLE):
                cycle = Info.WID_WIDGET[node.widget_id]
                cycle_name = node.text(0)
                for attribute in cycle.timeline_table.col_attribute:
                    # # 去重，只保留最近的值
                    # if attribute not in attributes:
                    #     attributes[f"{cycle_name}.attr.{attribute}"] = layer_count
                    attributes[f"{cycle_name}.attr.{attribute}"] = layer_count
                #
                if first_parent:
                    for attribute in Info.WID_WIDGET[node.widget_id].getHiddenAttribute():
                        attributes[f"{node.text(0)}.{attribute}"] = layer_count
                    first_parent = False
            layer_count -= 1
            node = node.parent()
        # 是否需要详细信息
        if need_detail:
            return attributes
        else:
            return attributes.keys()

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

    # 控制台输出信息
    @staticmethod
    def log(text, error=False, timer=True):
        pass

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
    def getWidgetChildren(widget_id: int) -> list:
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

    @staticmethod
    def getWidgetAttributes(widget_id: str):
        """
        get widget's attributes through its widget id
        """

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
