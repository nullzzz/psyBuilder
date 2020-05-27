import os
import sys


class Info(object):
    """
    info类，主要存放一些配置信息及数据
    """
    ###########################################
    #           old info/data                 #
    ###########################################
    # 编译平台：linux\windows\mac
    PLATFORM: str = "linux"

    IMAGE_LOAD_MODE: str = "before_event"

    # 保存widget_tabs的 (widget_id -> widget)
    WID_WIDGET = {}

    # 保存structure的 (widget_id -> node)
    WID_NODE: dict = {}

    # 只在structure中进行name的处理，避免失误(name -> [wid1, wid2...]),
    # 必须要保证wid1是所有指向的widget的widget_id！
    NAME_WID: dict = {}

    # 输入输出设备
    INPUT_DEVICE_INFO: dict = {}
    OUTPUT_DEVICE_INFO: dict = {}
    QUEST_DEVICE_INFO: dict = {}
    TRACKER_DEVICE_INFO: dict = {}

    # 当前导入导出文件名
    FILE_NAME = ""
    FILE_DIRECTORY = ""

    # possible useful in the future
    REF_VALUE_SEPERATOR = "@"

    # widget type
    LOOP = "Loop"
    IMAGE = "Image"
    TEXT = "Text"
    SOUND = "Sound"
    VIDEO = "Video"
    COMBO = "Scene"
    BUG = "Bug"

    OPEN = "Open"
    DC = "DC"
    CALIBRATION = "Calibration"
    ACTION = "EyeAction"
    STARTR = "StartR"
    ENDR = "EndR"
    LOG = "Logging"
    QUEST_INIT = "QuestInit"
    QUEST_UPDATE = "QuestUpdate"
    QUEST_GET_VALUE = "QuestGetValue"
    IF = "If"
    SWITCH = "Switch"
    TIMELINE = "Timeline"

    DEV_NETWORK_PORT = "network port"
    DEV_SCREEN = "screen"
    DEV_PARALLEL_PORT = "parallel port"
    DEV_SERIAL_PORT = "serial port"
    DEV_SOUND = "sound"
    DEV_TRACKER = "tracker"
    DEV_QUEST = "quest"

    DEV_KEYBOARD = "keyboard"
    DEV_MOUSE = "mouse"
    DEV_RESPONSE_BOX = "response box"
    DEV_GAMEPAD = "game pad"
    DEV_EYE_ACTION = "eye action"

    # FOR COMBO ITEMS:
    ITEM_POLYGON = "polygon"
    ITEM_ARC = "arc"
    ITEM_RECT = "rect"
    ITEM_CIRCLE = "circle"
    ITEM_IMAGE = "image"
    ITEM_TEXT = "text"
    ITEM_VIDEO = "video"
    ITEM_SOUND = "sound"
    ITEM_SNOW = "snow"
    ITEM_GABOR = "gabor"
    ITEM_LINE = "line"
    ITEM_DOT_MOTION = "dot motion"

    COMBO_COUNT: dict = {
        ITEM_POLYGON: 0,
        ITEM_ARC: 0,
        ITEM_RECT: 0,
        ITEM_CIRCLE: 0,
        ITEM_IMAGE: 0,
        ITEM_TEXT: 0,
        ITEM_VIDEO: 0,
        ITEM_SOUND: 0,
        ITEM_SNOW: 0,
        ITEM_GABOR: 0,
        ITEM_LINE: 0,
        ITEM_DOT_MOTION: 0,
    }

    # 图片保存路径
    # if getattr(sys, 'frozen', False): # we are running in a |PyInstaller| bundle
    #     BasePath = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname("run.py")))
    # else: # we are running in a normal Python environment
    BasePath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # IMAGE_SOURCE_PATH = os.path.join(BasePath, "source", "image")
    # widget不同类型对应图片

    ###########################################
    #           new version info              #
    ###########################################
    # init file
    VarEnvFile = "var_env.ini"
    TempFile = "temp.ini"

    # image path
    ImagePath = os.path.join(BasePath, "source", "images")
    # ImagePath = "source/images"

    # widget type
    ERROR_WIDGET_ID = ""

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"
    AttributesToWidget = "3"
    StructureMoveToTimeline = "4"
    StructureCopyToTimeline = "5"
    StructureReferToTimeline = "6"

    # sender widget
    TimelineSend = 0
    CycleSend = 1
    StructureSend = 2
    ConditionSend = 3

    # name pattern
    WidgetPattern = [r"^[a-zA-Z][a-zA-Z0-9_]*$",
                     "Name must start with a letter and contain only letters, numbers, and _."]
    RepetitionsPattern = [r"^\+?[1-9][0-9]*$", "Only positive number is allowed."]

    ###########################################
    #           new version data              #
    ###########################################
    Psy = None
    # wid -> widget
    Widgets = WID_WIDGET
    # name -> list of wid
    Names = NAME_WID
    # wid -> node
    Nodes = WID_NODE

    # wid num of different add_type of widget
    WidgetTypeCount = {
        LOOP: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        COMBO: 0,
        BUG: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        LOG: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        LOOP: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        COMBO: 0,
        BUG: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        LOG: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 0,
    }
