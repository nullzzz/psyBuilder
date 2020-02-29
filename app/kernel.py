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
        Info.TIMELINE: 0,
        Info.CYCLE: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        Info.TIMELINE: 0,
        Info.CYCLE: 0,
    }
