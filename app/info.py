import os

from PyQt5.QtCore import QSettings


class Info(object):
    """
    info类，主要存放一些配置信息及数据
    """

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
    OPEN = "Open"
    DC = "DC"
    CALIBRATION = "Calibration"
    ACTION = "Action"
    STARTR = "StartR"
    ENDR = "EndR"
    CLOSE = "Close"
    QUEST_INIT = "QuestInit"
    QUEST_UPDATE = "QuestUpdate"
    QUEST_GET_VALUE = "QuestGetValue"
    IF = "If"
    SWITCH = "Switch"
    TIMELINE = "Timeline"

    # 图片保存路径
    IMAGE_SOURCE_PATH = "image"
    # widget不同类型对应图片
    WIDGET_TYPE_IMAGE_PATH = {
        CYCLE: os.path.join(IMAGE_SOURCE_PATH, "cycle.png"),
        SOUND: os.path.join(IMAGE_SOURCE_PATH, "soundOut.png"),
        TEXT: os.path.join(IMAGE_SOURCE_PATH, "text.png"),
        IMAGE: os.path.join(IMAGE_SOURCE_PATH, "image.png"),
        VIDEO: os.path.join(IMAGE_SOURCE_PATH, "video.png"),
        SLIDER: os.path.join(IMAGE_SOURCE_PATH, "slider.png"),
        OPEN: os.path.join(IMAGE_SOURCE_PATH, "open_eye.png"),
        DC: os.path.join(IMAGE_SOURCE_PATH, "DC_eye.png"),
        CALIBRATION: os.path.join(IMAGE_SOURCE_PATH, "calibration_eye.png"),
        ACTION: os.path.join(IMAGE_SOURCE_PATH, "action_eye.png"),
        STARTR: os.path.join(IMAGE_SOURCE_PATH, "start_eye.png"),
        ENDR: os.path.join(IMAGE_SOURCE_PATH, "end_eye.png"),
        CLOSE: os.path.join(IMAGE_SOURCE_PATH, "close_eye.png"),
        QUEST_INIT: os.path.join(IMAGE_SOURCE_PATH, "start_quest.png"),
        QUEST_UPDATE: os.path.join(IMAGE_SOURCE_PATH, "update_quest.png"),
        QUEST_GET_VALUE: os.path.join(IMAGE_SOURCE_PATH, "get_value.png"),
        IF: os.path.join(IMAGE_SOURCE_PATH, "if.png"),
        SWITCH: os.path.join(IMAGE_SOURCE_PATH, "switch.png"),
        TIMELINE: os.path.join(IMAGE_SOURCE_PATH, "timeline.png"),
    }

    # widget不同类型名称的对应数
    WIDGET_TYPE_NAME_COUNT = {
        CYCLE: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        SLIDER: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        CLOSE: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 1,
    }

    # widget不同类型id对应数
    WIDGET_TYPE_ID_COUNT = {
        CYCLE: 0,
        SOUND: 0,
        TEXT: 0,
        IMAGE: 0,
        VIDEO: 0,
        SLIDER: 0,
        OPEN: 0,
        DC: 0,
        CALIBRATION: 0,
        ACTION: 0,
        STARTR: 0,
        ENDR: 0,
        CLOSE: 0,
        QUEST_INIT: 0,
        QUEST_UPDATE: 0,
        QUEST_GET_VALUE: 0,
        IF: 0,
        SWITCH: 0,
        TIMELINE: 1,
    }

    # drag
    FromAttributeToLineEdit = "attributes/move-attribute"
