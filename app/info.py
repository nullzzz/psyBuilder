class Info(object):
    """
    This class is used to store all configuration of this software, without any data.
    The variables in it will not change.
    """

    # image path
    Image_Path = "images"

    # max count of each type of widget
    MaxWidgetCount = 10000

    # widget type
    Timeline = 0
    Cycle = 1

    # widget type name
    WidgetType = {
        Timeline: "Timeline",
        Cycle: "Cycle",
    }

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"
    AttributesToLineEdit = "3"
    StructureMoveToTimeline = "4"
    StructureCopyToTimeline = "5"
    StructureReferToTimeline = "6"

    # signals' origin
    TimelineSignal = 0
    StructureSignal = 1
    CycleSignal = 2

    # name pattern
    widgetPattern = [r"^[a-zA-Z][a-zA-Z0-9_]*$",
                     "Name must start with a letter and contain only letters, numbers and _."]
    weightPattern = ""

    # device type
    INPUT_DEVICE = 0
    OUTPUT_DEVICE = 1

    # 限制输入的正则表达式
    RE_NUMBER = r"\[\w+\]|\d+"
    RE_FLOAT = r"\[\w+\]|\d+\.\d+"
    RE_NUM_PERCENT = r"\[\w+\]|\d+%?|\d+"

    # possible useful in the future
    REF_VALUE_SEPERATOR = "@"

    #
    DEV_NETWORK_PORT = "network_port"
    DEV_SCREEN = "screen"
    DEV_PARALLEL_PORT = "parallel_port"
    DEV_SERIAL_PORT = "serial_port"
    DEV_SOUND = "sound"

    #########################################
    # Variables set for compatibility       #
    # It is best to discard it in later use #
    #########################################
    PLATFORM: str = "linux"
    IMAGE_LOAD_MODE: str = "before_event"
    WID_WIDGET = {}
    WID_NODE: dict = {}
    NAME_WID: dict = {}
    QUEST_INFO: dict = {}
    TRACKER_INFO: dict = {}
    INPUT_DEVICE_INFO: dict = {}
    OUTPUT_DEVICE_INFO: dict = {}
    device_count = None
    SLIDER_COUNT = None
    FILE_NAME = None
