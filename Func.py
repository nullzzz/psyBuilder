from PyQt5.QtGui import QIcon, QPixmap

from Info import Info
from center.iconTabs.condition.ifBranch.main import IfBranch
from center.iconTabs.condition.switchBranch.main import SwitchBranch
from center.iconTabs.events.cycle.main import Cycle
from center.iconTabs.events.image.imageDisplay import ImageDisplay
from center.iconTabs.events.soundOut.soundDisplay import SoundDisplay
from center.iconTabs.events.text.textDisplay import TextDisplay
from center.iconTabs.events.video.videoDisplay import VideoDisplay
from center.iconTabs.eyeTracker.DC import EyeDC
from center.iconTabs.eyeTracker.action import EyeAction
from center.iconTabs.eyeTracker.calibrate import EyeCalibrate
from center.iconTabs.eyeTracker.close import Close
from center.iconTabs.eyeTracker.endR import EndR
from center.iconTabs.eyeTracker.open import Open
from center.iconTabs.eyeTracker.startR import StartR
from center.iconTabs.quest.getvalue import QuestGetValue
from center.iconTabs.quest.start import QuestInit
from center.iconTabs.quest.update import QuestUpdate
from center.iconTabs.timeline.main import Timeline


def getImage(widget_type, image_type='icon'):
    path = ''
    if widget_type == "Cycle":
        path = "image/cycle.png"
    elif widget_type == "Timeline":
        path = "image/timeLine.png"
    elif widget_type == "SoundOut":
        path = "image/soundOut.png"
    elif widget_type == "Text":
        path = "image/text.png"
    elif widget_type == "Image":
        path = "image/image.png"
    elif widget_type == "Video":
        path = "image/video.png"
    elif widget_type == "Close":
        path = "image/close_eye.png"
    elif widget_type == "DC":
        path = "image/DC_eye.png"
    elif widget_type == "Calibration":
        path = "image/calibration_eye.png"
    elif widget_type == "EndR":
        path = "image/end_eye.png"
    elif widget_type == "Open":
        path = "image/open_eye.png"
    elif widget_type == "Action":
        path = "image/action_eye.png"
    elif widget_type == "StartR":
        path = "image/start_eye.png"
    elif widget_type == "QuestGetValue":
        path = "image/get_value.png"
    elif widget_type == "QuestUpdate":
        path = "image/update_quest.png"
    elif widget_type == "QuestInit":
        path = "image/start_quest.png"
    elif widget_type == "If_else":
        path = "image/if_else.png"
    elif widget_type == "Switch":
        path = "image/switch.png"
    else:
        pass

    if path:
        if image_type == "pixmap":
            return QPixmap(path)
        elif image_type == "icon":
            return QIcon(path)
        else:
            return None
    return None


def getAttributes(value: str):
    """
    :param value: 当前widget的value
    :return: 当前widget可用的attributes
    """
    return ["test"]


def getWidget(value: str):
    """
    :param value: widget特征值
    :return: widget
    """
    if value in Info.VALUE_WIDGET.keys():
        return Info.VALUE_WIDGET[value]
    else:
        widget_type = value.split(".")[0]
        if widget_type == "Cycle":
            widget = Cycle(value=value)
        elif widget_type == "Timeline":
            widget = Timeline(value=value)
        elif widget_type == "SoundOut":
            widget = SoundDisplay(value=value)
        elif widget_type == "Text":
            widget = TextDisplay(value=value)
        elif widget_type == "Image":
            widget = ImageDisplay(value=value)
        elif widget_type == "Video":
            widget = VideoDisplay(value=value)
        elif widget_type == "Close":
            widget = Close(value=value)
        elif widget_type == "Action":
            widget = EyeAction(value=value)
        elif widget_type == "Calibration":
            widget = EyeCalibrate(value=value)
        elif widget_type == "EndR":
            widget = EndR(value=value)
        elif widget_type == "Open":
            widget = Open(value=value)
        elif widget_type == "DC":
            widget = EyeDC(value=value)
        elif widget_type == "StartR":
            widget = StartR(value=value)
        elif widget_type == "QuestInit":
            widget = QuestInit(value=value)
        elif widget_type == "QuestUpdate":
            widget = QuestUpdate(value=value)
        elif widget_type == "QuestGetValue":
            widget = QuestGetValue(value=value)
        elif widget_type == "If_else":
            widget = IfBranch(value=value)
        elif widget_type == "Switch":
            widget = SwitchBranch(value=value)
        else:
            widget = "Unknown"
            print(f"Error {widget_type} unknown.[Func/getWidget]")
        # Info.VALUE_WIDGET[value] = widget
        return widget
