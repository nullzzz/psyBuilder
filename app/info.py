import os


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

    INPUT_DEVICE = 0
    OUTPUT_DEVICE = 1
    QUEST_DEVICE = 2
    TRACKER_DEVICE = 3

    # 当前导入导出文件名
    FILE_NAME = ""
    FILE_DIRECTORY = ""

    # possible useful in the future
    REF_VALUE_SEPERATOR = "@"

    # widget type
    CYCLE = "Cycle"
    SOUND = "Sound"
    TEXT = "Text"
    IMAGE = "Image"
    VIDEO = "Video"
    SLIDER = "Slider"
    BUG = "Bug"

    OPEN = "Open"
    DC = "DC"
    CALIBRATION = "Calibration"
    ACTION = "Action"
    STARTR = "StartR"
    ENDR = "EndR"
    LOG = "Log"
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
    DEV_EYE_ACTION = "action"

    # 设备id计数
    device_count: dict = {
        DEV_SERIAL_PORT: 0,
        DEV_PARALLEL_PORT: 0,
        DEV_NETWORK_PORT: 0,
        DEV_SCREEN: 0,
        DEV_MOUSE: 0,
        DEV_KEYBOARD: 0,
        DEV_RESPONSE_BOX: 0,
        DEV_GAMEPAD: 0,
        DEV_EYE_ACTION: 0
    }

    # FOR SLIDER ITEMS:
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

    SLIDER_COUNT: dict = {
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
    IMAGE_SOURCE_PATH = "image"
    # widget不同类型对应图片
    WIDGET_TYPE_IMAGE_PATH = {
        CYCLE: os.path.join(IMAGE_SOURCE_PATH, "cycle.png"),
        SOUND: os.path.join(IMAGE_SOURCE_PATH, "sound.png"),
        TEXT: os.path.join(IMAGE_SOURCE_PATH, "text.png"),
        IMAGE: os.path.join(IMAGE_SOURCE_PATH, "image.png"),
        VIDEO: os.path.join(IMAGE_SOURCE_PATH, "video.png"),
        SLIDER: os.path.join(IMAGE_SOURCE_PATH, "slider.png"),
        BUG: os.path.join(IMAGE_SOURCE_PATH, "bug.png"),
        OPEN: os.path.join(IMAGE_SOURCE_PATH, "open_eye.png"),
        DC: os.path.join(IMAGE_SOURCE_PATH, "DC_eye.png"),
        CALIBRATION: os.path.join(IMAGE_SOURCE_PATH, "calibration_eye.png"),
        ACTION: os.path.join(IMAGE_SOURCE_PATH, "action_eye.png"),
        STARTR: os.path.join(IMAGE_SOURCE_PATH, "start_eye.png"),
        ENDR: os.path.join(IMAGE_SOURCE_PATH, "end_eye.png"),
        LOG: os.path.join(IMAGE_SOURCE_PATH, "close_eye.png"),
        QUEST_INIT: os.path.join(IMAGE_SOURCE_PATH, "start_quest.png"),
        QUEST_UPDATE: os.path.join(IMAGE_SOURCE_PATH, "update_quest.png"),
        QUEST_GET_VALUE: os.path.join(IMAGE_SOURCE_PATH, "get_value.png"),
        IF: os.path.join(IMAGE_SOURCE_PATH, "if.png"),
        SWITCH: os.path.join(IMAGE_SOURCE_PATH, "switch.png"),
        TIMELINE: os.path.join(IMAGE_SOURCE_PATH, "timeline.png"),
    }

    ###########################################
    #           new version info              #
    ###########################################
    # init file
    VarEnvFile = "var_env.ini"
    TempFile = "temp.ini"

    # image path
    ImagePath = "source/images"

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
                     "Name must start with a letter and contain only letters, numbers and _."]
    WeightPattern = [r"^\+?[1-9][0-9]*$", "Only positive number is enabled."]

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
        CYCLE: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        SLIDER: 0,
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
        CYCLE: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        SLIDER: 0,
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
