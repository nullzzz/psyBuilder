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
        Info.Timeline: 0,
        Info.Cycle: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        Info.Timeline: 0,
        Info.Cycle: 0,
    }

    # device
    QuestInfo = {}
    TrackerInfo = {}
    InputDeviceInfo = {}
    OutputDeviceInfo = {}

    # device id counter
    DeviceCount = {
        "serial_port": 0,
        "parallel_port": 0,
        "network_port": 0,
        "screen": 0,
        "mouse": 0,
        "keyboard": 0,
        "response box": 0,
        "game pad": 0
    }

    SliderCount = {
        "polygon": 0,
        "arc": 0,
        "rect": 0,
        "circle": 0,
        "image": 0,
        "text": 0,
        "video": 0,
        "sound": 0,
        "snow": 0,
        "gabor": 0,
        "line": 0,
    }
