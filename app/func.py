import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter
from PyQt5.QtWidgets import QDesktopWidget

from .info import Info
from .kernel import Kernel


class Func(object):
    """
    This class is used to store all common function.
    """

    @staticmethod
    def generateWidgetId(widget_type: int) -> int:
        """
        it' used to generate widget id which is used to discern different widget.
        @param widget_type: the add_type of widget, such as timeline.
        @return: new widget id
        """
        # get the current num of this add_type which has been created.
        count = Kernel.WidgetTypeCount[widget_type]
        # widget id = widget_type * 10000 + count
        widget_id = widget_type * Info.MaxWidgetCount + count
        # inc count of this widget type
        Kernel.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: int) -> str:
        """
        it' used to generate widget id which is used to discern different widget.
        @param widget_type: the add_type of widget, such as timeline.
        @return: new widget id
        """
        widget_type_name = Info.WidgetType[widget_type]
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type_name}_{Kernel.WidgetNameCount[widget_type]}"
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
        @param widget_name:
        @return: validity
        """
        # name should start with a letter
        if not re.match(r"^[a-zA-Z].*$", widget_name):
            return False, "Name should start with a letter."
        # name should be unique.
        if widget_name not in Kernel.Names:
            return True, ""
        return False, "Name already exists."

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
    def print(information: str, information_type: int = 0) -> None:
        """
        print information in output.
        @param information:
        @param information_type: 0 none
                                 1 success
                                 2 fail
        @return:
        """
        Kernel.Psy.output.print(information, information_type)

    @staticmethod
    def getTrackingPix(text: str) -> QPixmap:
        """
        generate pixmap from text
        @param text:
        @return:
        """
        pix = QPixmap(200, 16)
        pix.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pix)
        painter.drawText(0, 0, 200, 16, Qt.TextSingleLine, text)
        return pix

    @staticmethod
    def getWidgetAttributes(widget_id: int) -> dict:
        """
        get widget's attributes and attributes' layer
        @param widget_id:
        @return: {attribute: layer}
        """
        # global attributes
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subSex": 0, "subHandness": 0, "subAge": 0}
        return attributes
        # todo attributes about quest, I don't know what they are.
        pass

        # get widget's hidden attributes
        hidden_attributes = Kernel.Widgets[widget_id].getHiddenAttributes()

        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Kernel.Nodes[widget_id]
        depth = -1
        temp_node = node
        while temp_node:
            depth += 1
            temp_node = temp_node.parent()
        # do 1.
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.Timeline):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.Cycle):
                    for attribute in Kernel.Widgets[child_node.widget_id].getHiddenAttribute():
                        attributes[f"{child_node.text(0)}.{attribute}"] = depth
        # do 2. 3.
        first = True
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.Cycle):
                cycle = Kernel.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes[f"{cycle_name}.attr.{attribute}"] = depth
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Kernel.Widgets[node.widget_id].getHiddenAttribute()
                    for attribute in first_cycle_hidden_attributes:
                        attributes[f"{cycle_name}.{attribute}"] = depth
                    first = False
            depth -= 1
            node = node.parent()
        # return
        return attributes

    @staticmethod
    def getWidgetProperties(widget_id: int) -> dict:
        """
        get widget's properties
        @param widget_id:
        @return:
        """
        widget = Kernel.Widgets[widget_id]
        return widget.getProperties()

    @staticmethod
    def getWidgetName(widget_id: int):
        """
        get widget's name
        @param widget_id:
        @return:
        """
        return Kernel.Widgets[widget_id].widget_name

    @staticmethod
    def getWidgetType(widget_id: int) -> int:
        """
        get widget's type
        @param widget_id:
        @return:
        """
        return widget_id // Info.MaxWidgetCount

    @staticmethod
    def isWidgetType(widget_id: int, widget_type: int) -> bool:
        """
        judge widget_id's widget type
        @param self:
        @param widget_id:
        @param widget_type:
        @return:
        """
        return Func.getWidgetType(widget_id) == widget_type

    @staticmethod
    def checkReferValidity(target_timeline: int, widget_id: int):
        """
        when refer widget, we should check validity
        @param target_timeline: target timeline's widget id
        @param widget_id: widget which we want to refer
        @return:
        """
        # todo check refer validity

    @staticmethod
    def getWidgetReference(widget_id: int) -> list:
        """
        get list of reference widget's widget id
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        return Kernel.Names[widget_name]

    @staticmethod
    def checkWidgetNameExisted(widget_name: str) -> bool:
        """

        @param widget_name:
        @return:
        """
        return widget_name in Kernel.Names

    @staticmethod
    def getWidgetParent(widget_id: int) -> int:
        """
        get parent's widget id
        @param widget_id:
        @return:
        """
        return Kernel.Nodes[widget_id].parent().widget_id

    @staticmethod
    def getWidgetChild(widget_id: int, index: int) -> (int, str):
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
    def getWidgetIndex(widget_id: int) -> int:
        """
        get widget's index in timeline
        @param widget_id:
        @return:
        """
        if Func.isWidgetType(widget_id, Info.Timeline):
            return -1
        node = Kernel.Nodes[widget_id]
        if node.parent():
            return node.parent().indexOfChild(node)
        else:
            return -1

    @staticmethod
    def getWidgetLevel(widget_id: int) -> int:
        """
        get the depth from this widget id to the root node(initial timeline)
        @param widget_id:
        @return:
        """
        depth = 0
        node = Kernel.Nodes[widget_id].parent()
        while node:
            node = node.parent()
            depth += 1
        return depth

    @staticmethod
    def getWidgetHeight(widget_id: int) -> int:
        """
        get the height of the tree with this widget id as the root node
        @param widget_id:
        @return:
        """
        node = Kernel.Nodes[widget_id]
        max_height = 0
        for i in range(node.childCount()):
            child = node.child(i)
            height = Func.getWidgetHeight(child.widget_id)
            if height > max_height:
                max_height = height
        return max_height + 1

    @staticmethod
    def getNextWidget(widget_id: int) -> int:
        """
        get its next widget's widget id in timeline
        @param widget_id:
        @return:
        """
        index = Func.getWidgetIndex(widget_id)
        if index != -1:
            try:
                node = Kernel.Nodes[widget_id]
                return node.parent().child(index + 1).widget_id
            except:
                return -1
        else:
            return -1

    @staticmethod
    def getPreviousWidget(widget_id: int) -> int:
        """
        get its previous widget's widget id in timeline
        @param widget_id:
        @return:
        """
        index = Func.getWidgetIndex(widget_id)
        if index != -1 and index != 0:
            try:
                node = Kernel.Nodes[widget_id]
                return node.parent().child(index - 1).widget_id
            except:
                return -1
        else:
            return -1

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

    #########################################
    # Variables set for compatibility       #
    # It is best to discard it in later use #
    #########################################

    @staticmethod
    def getWidgetPosition(widget_id: int) -> int:
        return Func.getWidgetIndex(widget_id)

    @staticmethod
    def getNextWidgetId(widget_id: int) -> int:
        return Func.getNextWidget(widget_id)

    @staticmethod
    def getPreviousWidgetId(widget_id: int) -> int:
        return Func.getPreviousWidget(widget_id)

    @staticmethod
    def getWidgetIDInTimeline(timeline_widget_id: int) -> list:
        return Func.getWidgetChildren(timeline_widget_id)

    @staticmethod
    def getParentWid(widget_id: int) -> int:
        return Func.getWidgetParent(widget_id)

    @staticmethod
    def log(text, error=False, timer=True):
        if error:
            Func.print(text, 2)
        else:
            Func.print(text)

    @staticmethod
    def getWidLevel(widget_id: int) -> int:
        return Func.getWidgetLevel(widget_id)

    @staticmethod
    def getWidgetsTotalLayer(widget_id: int) -> int:
        return Func.getWidgetHeight(widget_id)
