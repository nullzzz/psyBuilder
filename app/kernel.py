from .info import Info


class Kernel(object):
    """
    This Class is used to store main data, without any configuration or function.
    """

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
        Info.Sound: 0,
        Info.Text: 0,
        Info.Image: 0,
        Info.Video: 0,
        Info.Slider: 0,
    }

    # it's used to counter the count of widget name should go.
    WidgetNameCount = {
        Info.Timeline: 0,
        Info.Cycle: 0,
        Info.Sound: 0,
        Info.Text: 0,
        Info.Image: 0,
        Info.Video: 0,
        Info.Slider: 0,
    }