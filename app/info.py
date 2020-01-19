class Info(object):
    """
    This class is used to store all configuration of this software, without any data.
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

    # add type
    AddItem = 0
    CopyItem = 1
    ReferItem = 2

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"
    AttributesToLineEdit = "3"

    # signals' origin
    TimelineSignal = 0
    StructureSignal = 1
    CycleSignal = 2
