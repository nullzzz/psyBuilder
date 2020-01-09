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
    Sound = 2
    Text = 3
    Image = 4
    Video = 5
    Slider = 6

    # widget type name
    WidgetType = {
        Timeline: "Timeline",
        Cycle: "Cycle",
        Sound: "Sound",
        Text: "Text",
        Image: "Image",
        Video: "Video",
        Slider: "Slider"
    }

    # add node type
    AddNode = 0
    CopyNode = 1
    ReferNode = 2
    MoveNode = 3

    # drag type
    IconBarToTimeline = "0"
    CopyInTimeline = "1"
    MoveInTimeline = "2"

    # signals' origin
    TimelineSignal = 0
    StructureSignal = 1
