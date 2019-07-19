import copy
import os
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor
from PyQt5.QtWidgets import QWidget

from app.info import Info


class Func(object):
    """
    存放一些通用函数
    """

    @staticmethod
    def getWidgetImage(widget_type: str, type: str = 'icon') -> QPixmap or QIcon:
        """
        返回widget_type对应的图片
        :param widget_type: widget类型
        :param type: 返回图片类型
        :return: 
        """
        # 得到图片路径
        if widget_type in Info.WIDGET_TYPE_IMAGE_PATH:
            path = Info.WIDGET_TYPE_IMAGE_PATH[widget_type]
            if type == "icon":
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
    def changeCertainDeviceNameWhileUsing(device_id: str, device_name):
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
    def getProperties(widget_id) -> dict:
        """
        按widget_id得到对应widget的属性
        :param widget_id:
        :return:
        """
        widget = Info.WID_WIDGET[widget_id]
        return widget.getProperties()

    @staticmethod
    def getWidgetName(widget_id: str) -> str:
        """
        根据widget_id得到对应widget的name
        :param widget_id:
        :return:
        """
        if widget_id in Info.WID_NODE:
            return Info.WID_NODE[widget_id].text(0)
        raise Exception("fail to get widget name. [func.py]")

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
        if not re.match(r"^[a-zA-Z].*$", name):
            return False, 'The name must start with a letter.'
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
            del Info.WID_WIDGET[widget_id]
        except KeyError:
            pass

    @staticmethod
    def createWidget(widget_id: str) -> QWidget:
        """
        根据widget_id创建对应类型的widget
        :param widget_id:
        :return:
        """
        widget_type = widget_id.split('.')[0]
        if widget_type == Info.TIMELINE:
            from app.center.widget_tabs.timeline.main import Timeline
            widget = Timeline(widget_id=widget_id)
        # condition
        elif widget_type == Info.IF:
            from app.center.widget_tabs.condition.ifBranch.main import IfBranch
            widget = IfBranch(widget_id=widget_id)
        elif widget_type == Info.SWITCH:
            from app.center.widget_tabs.condition.switch.main import Switch
            widget = Switch(widget_id=widget_id)
        # event
        elif widget_type == Info.CYCLE:
            from app.center.widget_tabs.events.cycle.main import Cycle
            widget = Cycle(widget_id=widget_id)
        elif widget_type == Info.IMAGE:
            from app.center.widget_tabs.events.image.imageDisplay import ImageDisplay
            widget = ImageDisplay(widget_id=widget_id)
        elif widget_type == Info.VIDEO:
            from app.center.widget_tabs.events.video.videoDisplay import VideoDisplay
            widget = VideoDisplay(widget_id=widget_id)
        elif widget_type == Info.TEXT:
            from app.center.widget_tabs.events.text.textDisplay import TextDisplay
            widget = TextDisplay(widget_id=widget_id)
        elif widget_type == Info.SOUND:
            from app.center.widget_tabs.events.soundOut.soundDisplay import SoundDisplay
            widget = SoundDisplay(widget_id=widget_id)
        elif widget_type == Info.SLIDER:
            from app.center.widget_tabs.events.slider.Slider import Slider
            widget = Slider(widget_id=widget_id)
        # eye tracker
        elif widget_type == Info.ACTION:
            from app.center.widget_tabs.eye_tracker.action import EyeAction
            widget = EyeAction(widget_id=widget_id)
        elif widget_type == Info.CALIBRATION:
            from app.center.widget_tabs.eye_tracker.calibrate import EyeCalibrate
            widget = EyeCalibrate(widget_id=widget_id)
        elif widget_type == Info.ENDR:
            from app.center.widget_tabs.eye_tracker.endR import EndR
            widget = EndR(widget_id=widget_id)
        elif widget_type == Info.OPEN:
            from app.center.widget_tabs.eye_tracker.open import Open
            widget = Open(widget_id=widget_id)
        elif widget_type == Info.DC:
            from app.center.widget_tabs.eye_tracker.DC import EyeDC
            widget = EyeDC(widget_id=widget_id)
        elif widget_type == Info.STARTR:
            from app.center.widget_tabs.eye_tracker.startR import StartR
            widget = StartR(widget_id=widget_id)
        elif widget_type == Info.CLOSE:
            from app.center.widget_tabs.eye_tracker.close import Close
            widget = Close(widget_id=widget_id)
        elif widget_type == Info.QUEST_INIT:
            from app.center.widget_tabs.quest.start import QuestInit
            widget = QuestInit(widget_id=widget_id)
        elif widget_type == Info.QUEST_UPDATE:
            from app.center.widget_tabs.quest.update import QuestUpdate
            widget = QuestUpdate(widget_id=widget_id)
        elif widget_type == Info.QUEST_GET_VALUE:
            from app.center.widget_tabs.quest.getvalue import QuestGetValue
            widget = QuestGetValue(widget_id=widget_id)
        else:
            widget = None
        # 如果未生成实体，报错
        if not widget:
            raise Exception("fail to create widget, because unknown widget type. [func.py]")
        # 将新生成的widget存储到wid_widget中
        Info.WID_WIDGET[widget_id] = widget
        return widget

    @staticmethod
    def copyWidget(new_widget_id, old_widget_id) -> None:
        """
        复制widget
        :param new_widget_id: 新widget的widget id
        :param old_widget_id: 被复制的widget的widget_id
        :return: None
        """
        # 调用widget中实现的clone函数
        Info.WID_WIDGET[new_widget_id] = Info.WID_WIDGET[old_widget_id].clone(new_widget_id)

    @staticmethod
    def referWidget(new_widget_id, old_widget_id) -> None:
        """
        引用widget，不同widget_id指向同一个widget，变成引用效果
        :param new_widget_id:
        :param old_widget_id:
        :return:
        """
        # 这样做有一个问题，当源widget脱离后，其余的widget_id仍指向这个widget，
        # 而这个widget内部绑定的widget_id是源widget的id
        # 所以脱离时要进行一个检测：是否存在引用，是否是源widget_id
        Info.WID_WIDGET[new_widget_id] = Info.WID_WIDGET[old_widget_id]

    @staticmethod
    def getReferWidgetIds(widget_id) -> list:
        """
        用来得到widget_id同引用的其他widget_id
        :param widget_id:
        :return:
        """
        try:
            widget_ids: list = copy.deepcopy(Info.NAME_WID[Info.WID_NODE[widget_id].text(0)])
            widget_ids.remove(widget_id)
            return widget_ids
        except Exception as e:
            print(f"error {e} happens in get refer widget ids. [func.py]")
            return []

    @staticmethod
    def getAttributes(widget_id, need_detail=False) -> dict or list:
        """
        根据某个节点的wid得到它的属性，根据属性返回是否需要详细信息，
        :param widget_id:
        :param need_detail: 是否需要详细的信息即属性的值
        :return:
        """
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subSex": 0, "subHandness": 0, "subAge": 0}
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
    def getWidgetId(parent_widget_id, child_name) -> str:
        """
        通过parent的widget_id和自身name可以得到自身的widget_id
        :param parent_widget_id: 父节点的widget_id
        :param child_name: 自身name
        :return:
        """
        parent_node = Info.WID_NODE[parent_widget_id]
        for i in range(parent_node.childCount()):
            if parent_node.child(i).text(0) == child_name:
                return parent_node.child(i).widget_id
        raise Exception("fail to get widget id.")

    @staticmethod
    def deleteItemInWidget(widget_id) -> None:
        """
        删除widget中的item，只有cycle和timeline中存在
        :param widget_id:
        :return:
        """
        try:
            parent_wid: str = Info.WID_NODE[widget_id].parent().widget_id
            name = Info.WID_NODE[widget_id].text(0)
            if parent_wid.startswith(Info.TIMELINE):
                Func.deleteWidgetIconInTimeline(parent_wid, name)
            elif parent_wid.startswith(Info.CYCLE):
                Func.deleteTimelineInCycle(parent_wid, name)
        except Exception as e:
            print(f"error {e} happens in delete widget icon in timeline. [func.py]")

    @staticmethod
    def deleteWidgetIconInTimeline(timeline_wid, icon_name) -> None:
        """
        删除timeline中的widget
        :param timeline_wid: timeline的id
        :param icon_name: 需要删除的item的name
        :return:
        """
        try:
            timeline = Info.WID_WIDGET[timeline_wid]
            for col in range(1, timeline.widget_icon_area.widget_icon_table.widget_icon_count + 1):
                if icon_name == timeline.widget_icon_area.widget_icon_table.item(3, col).text():
                    timeline.widget_icon_area.widget_icon_table.removeColumn(col)
                    return None
            raise Exception('fail to delete widget icon in timeline, because no found.')
        except Exception as e:
            print(f"error {e} happens in delete widget icon in timeline. [func.py]")

    @staticmethod
    def deleteTimelineInCycle(cycle_wid, timeline_name):
        try:
            cycle = Info.WID_WIDGET[cycle_wid]
            cycle.deleteTimeline(timeline_name)
        except Exception as e:
            print(f"error {e} happens in delete timeline in cycle. [func.py]")

    @staticmethod
    def renameItemInWidget(widget_id, new_name):
        try:
            parent_wid: str = Info.WID_NODE[widget_id].parent().widget_id
            name = Info.WID_NODE[widget_id].text(0)
            if parent_wid.startswith(Info.TIMELINE):
                Func.renameWidgetIconInTimeline(parent_wid, name, new_name)
            elif parent_wid.startswith(Info.CYCLE):
                Func.renameTimelineInCycle(parent_wid, name, new_name)
        except Exception as e:
            print(f"error {e} happens in delete widget icon in timeline. [func.py]")

    @staticmethod
    def renameWidgetIconInTimeline(timeline_wid, icon_name, new_name):
        try:
            timeline = Info.WID_WIDGET[timeline_wid]
            for col in range(1, timeline.widget_icon_area.widget_icon_table.widget_icon_count + 1):
                if icon_name == timeline.widget_icon_area.widget_icon_table.item(3, col).text():
                    timeline.widget_icon_area.widget_icon_table.setWidgetName(col, new_name)
                    return None
            raise Exception('fail to rename widget icon in timeline, because no found.')
        except Exception as e:
            print(f"error {e} happens in rename widget icon in timeline. [func.py]")

    @staticmethod
    def renameTimelineInCycle(cycle_wid, timeline_name, new_name):
        try:
            Info.WID_WIDGET[cycle_wid].renameTimeline(timeline_name, new_name)
        except Exception as e:
            print(f"error {e} happens in rename timeline in cycle. [func.py]")

    @staticmethod
    def checkDragValidityFromStructure(target_timeline_wid: str, widget_id: str) -> bool:
        """
        当从structure中拖拽至timeline时，
        对于cycle的拖拽，因其下面挂着timeline，如果不进行处理，会导致类似死锁。
        :param target_timeline_wid: 目标的timeline的wid
        :param widget_id: 被拖拽的wid
        :return: 合法性
        """
        try:
            # 需求要求引用只局限于一个同一个cycle下的timeline，说不定哪天让我改回来，现将下方代码注释
            # # 只需检测cycle
            # if Func.isWidgetType(widget_id, Info.CYCLE):
            #     # 检测目标的timeline的自身包括引用节点上面有没有父节点name是cycle的name
            #     cycle_name = Info.WID_NODE[widget_id].text(0)
            #     timeline_name = Info.WID_NODE[target_timeline_wid].text(0)
            #     for timeline_wid in Info.NAME_WID[timeline_name]:
            #         node = Info.WID_NODE[timeline_wid].parent()
            #         while node:
            #             if node.text(0) == cycle_name:
            #                 return False
            #             node = node.parent()
            #     return True
            # return True

            # 先确定被拖拽的widget所属的cycle是否与target的timeline所属的cycle是否为同一个
            # target_timeline不能是第一层timeline，因为它没有父cycle
            if target_timeline_wid == f"{Info.TIMELINE}.0":
                return False
            cycle_1_wid = Info.WID_NODE[target_timeline_wid].parent().widget_id
            # 根据widget得到父timeline
            node = Info.WID_NODE[widget_id]
            parent_timeline = node.parent()
            # 如果是父亲为第一层timeline，其没有父cycle
            if parent_timeline.widget_id == f"{Info.TIMELINE}.0":
                return False
            cycle_2_wid = parent_timeline.parent().widget_id
            # 父cycle是否相同
            if cycle_1_wid == cycle_2_wid:
                return True
            return False
        except Exception as e:
            print(f"error {e} happens in check validity of drag from structure. [func.py]")

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

    # 控制台输出信息
    @staticmethod
    def log(text, error=False, timer=True):
        pass
