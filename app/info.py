from PyQt5.QtCore import QSettings


class Info(object):
    """
    info类，主要存放一些配置信息及数据
    """
    # 编译平台：linux\windows\mac
    PLATFORM = None

    IMAGE_LOAD_MODE = None

    # 保存widget_tabs的 (widget_id -> widget)
    WID_WIDGET = None

    # 保存structure的 (widget_id -> node)
    WID_NODE: dict = None

    # 只在structure中进行name的处理，避免失误(name -> [wid1, wid2...]),
    # 必须要保证wid1是所有指向的widget的widget_id！
    NAME_WID: dict = None

    # 输入输出设备
    QUEST_INFO = None
    TRACKER_INFO: dict = {}
    INPUT_DEVICE_INFO: dict = {}
    OUTPUT_DEVICE_INFO: dict = {}
    QUEST_DEVICE_INFO: dict = {}
    TRACKER_DEVICE_INFO: dict = {}
    INPUT_DEVICE = 0
    OUTPUT_DEVICE = 1
    QUEST_DEVICE = 2
    TRACKER_DEVICE = 3
    # 设备id计数
    device_count: dict = {
        "serial_port": 0,
        "parallel_port": 0,
        "network_port": 0,
        "screen": 0,
        "mouse": 0,
        "keyboard": 0,
        "response box": 0,
        "game pad": 0
    }

    # 当前导入导出文件名
    FILE_NAME: str = ""

    CONFIG = QSettings("./operation.ini", QSettings.IniFormat)
    FILE_DIRECTORY: str = CONFIG.value("directory")
    IS_REGISTER: str = CONFIG.value("register")

    # 限制输入的正则表达式
    RE_NUMBER = r"\[\w+\]|\d+"
    RE_FLOAT = r"\[\w+\]|\d+\.\d+"
    RE_NUM_PERCENT = r"\[\w+\]|\d+%?|\d+"

    # possible useful in the future
    REF_VALUE_SEPERATOR = "@"

    # 区分不同的添加情况
    WidgetAdd = 0
    WidgetCopy = 1
    WidgetRefer = 2
    WidgetMove = 3
    # Timeline name
    TimelineNameError = 0
    TimelineTypeError = 1
    TimelineParentError = 2
    TimelineNameRight = 3
    TimelineNameExist = 4

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

    DEV_NETWORK_PORT = "network_port"
    DEV_SCREEN = "screen"
    DEV_PARALLEL_PORT = "parallel_port"
    DEV_SERIAL_PORT = "serial_port"
    DEV_SOUND = "sound"

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
    }

    # 图片保存路径
    IMAGE_SOURCE_PATH = "image"

    ###########################################
    #               new version               #
    ###########################################
    # image path
    Image_Path = "images"

    # widget type
    ERROR_WIDGET_ID = ""

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"
    AttributesToLineEdit = "3"
    AttributesToComboBox = "4"
    StructureMoveToTimeline = "5"
    StructureCopyToTimeline = "6"
    StructureReferToTimeline = "7"

    # sender widget
    TimelineSend = 0
    CycleSend = 1
    StructureSend = 2

    # name pattern
    WidgetPattern = [r"^[a-zA-Z][a-zA-Z0-9_]*$",
                     "Name must start with a letter and contain only letters, numbers and _."]
    WeightPattern = [r"^\+?[1-9][0-9]*$", "Only positive number is enabled."]
