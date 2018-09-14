from PyQt5.QtGui import QIcon, QPixmap


def getImage(widget_type, image_type='icon'):
    path = ''
    if widget_type == "Cycle":
        path = "image/cycle.png"
    elif widget_type == "Timeline":
        path = "image/timeLine.png"
    elif widget_type == "SoundOut":
        path = "image/soundOut.png"
    elif widget_type == "Text":
        path = "image/text.png"
    elif widget_type == "Image":
        path = "image/image.png"
    elif widget_type == "Video":
        path = "image/video.png"
    elif widget_type == "Close":
        path = "image/close_eye.png"
    elif widget_type == "DC":
        path = "image/DC_eye.png"
    elif widget_type == "Calibration":
        path = "image/calibration_eye.png"
    elif widget_type == "EndR":
        path = "image/end_eye.png"
    elif widget_type == "Open":
        path = "image/open_eye.png"
    elif widget_type == "Action":
        path = "image/action_eye.png"
    elif widget_type == "StartR":
        path = "image/start_eye.png"
    elif widget_type == "QuestGetValue":
        path = "image/get_value.png"
    elif widget_type == "QuestUpdate":
        path = "image/update_quest.png"
    elif widget_type == "QuestInit":
        path = "image/start_quest.png"
    elif widget_type == "If_else":
        path = "image/if_else.png"
    elif widget_type == "Switch":
        path = "image/switch.png"
    else:
        pass

    if path:
        if image_type == "pixmap":
            return QPixmap(path)
        elif image_type == "icon":
            return QIcon(path)
        else:
            return None
    return None
