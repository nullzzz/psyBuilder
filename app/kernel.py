from .info import Info


class Kernel(object):
    """
    This Class is used to store main data, without any configuration or function.
    """
    # bind total software to psy
    Psy = None
    FileName = ""
    Platform = "linux"
    ImageLoadMode = "before_event"

    # wid -> widget
    Widgets = {}
    # name -> list of wid
    Names = {}
    # wid -> node
    Nodes = {}

    # wid num of different add_type of widget
    WidgetTypeCount = {
        Info.CYCLE: 0,
        Info.SOUND: 0,
        Info.TEXT: 0,
        Info.IMAGE: 0,
        Info.VIDEO: 0,
        Info.SLIDER: 0,
        Info.BUG: 0,
        Info.OPEN: 0,
        Info.CALIBRATION: 0,
        Info.ACTION: 0,
        Info.STARTR: 0,
        Info.ENDR: 0,
        Info.LOG: 0,
        Info.QUEST_INIT: 0,
        Info.QUEST_UPDATE: 0,
        Info.QUEST_GET_VALUE: 0,
        Info.IF: 0,
        Info.SWITCH: 0,
        Info.TIMELINE: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        Info.CYCLE: 0,
        Info.SOUND: 0,
        Info.TEXT: 0,
        Info.IMAGE: 0,
        Info.VIDEO: 0,
        Info.SLIDER: 0,
        Info.BUG: 0,
        Info.OPEN: 0,
        Info.CALIBRATION: 0,
        Info.ACTION: 0,
        Info.STARTR: 0,
        Info.ENDR: 0,
        Info.LOG: 0,
        Info.QUEST_INIT: 0,
        Info.QUEST_UPDATE: 0,
        Info.QUEST_GET_VALUE: 0,
        Info.IF: 0,
        Info.SWITCH: 0,
        Info.TIMELINE: 0,
    }

    QuestInfo = {}
