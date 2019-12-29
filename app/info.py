class Info(object):
    """
    This class is used to store all configuration of this software, without any data.
    """
    # image path
    Image_Path = "images"

    # max count of each add_type of widget
    MaxWidgetCount = 10000

    # widget add_type
    Timeline = 0
    Cycle = 1
    Sound = 2
    Text = 3
    Image = 4
    Video = 5
    Slider = 6

    # widget add_type name
    WidgetType = {
        Timeline: "Timeline",
        Cycle: "Cycle",
        Sound: "Sound",
        Text: "Text",
        Image: "Image",
        Video: "Video",
        Slider: "Slider"
    }

    # add node add_type
    AddNode = 0
    CopyNode = 1
    ReferNode = 2
    MoveNode = 3

    # drag type
    IconBarToTimeline = "0"
