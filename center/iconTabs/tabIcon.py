from PyQt5.QtGui import QIcon


class TabIcon(QIcon):
    def __init__(self, tab_type=''):
        if tab_type == "Cycle":
            super().__init__(".\\.\\image\\cycle.png")
        elif tab_type == "Timeline":
            super().__init__(".\\.\\image\\timeLine.png")
        elif tab_type == "SoundOut":
            super().__init__(".\\.\\image\\soundOut.png")
        elif tab_type == "Text":
            super().__init__(".\\.\\image\\text.png")
        elif tab_type == "Image":
            super().__init__(".\\.\\image\\image.png")
        elif tab_type == "Video":
            super().__init__(".\\.\\image\\video.png")
        elif tab_type == "Close":
            super().__init__(".\\.\\image\\close_eye.png")
        elif tab_type == "DC":
            super().__init__(".\\.\\image\\DC_eye.png")
        elif tab_type == "Calibration":
            super().__init__(".\\.\\image\\calibration_eye.png")
        elif tab_type == "EndR":
            super().__init__(".\\.\\image\\end_eye.png")
        elif tab_type == "Open":
            super().__init__(".\\.\\image\\open_eye.png")
        elif tab_type == "Action":
            super().__init__(".\\.\\image\\action_eye.png")
        elif tab_type == "StartR":
            super().__init__(".\\.\\image\\start_eye.png")
        elif tab_type == "QuestGetValue":
            super().__init__(".\\.\\image\\get_value.png")
        elif tab_type == "QuestUpdate":
            super().__init__(".\\.\\image\\update_quest.png")
        elif tab_type == "QuestInit":
            super().__init__(".\\.\\image\\start_quest.png")
        elif tab_type == "If_else":
            super().__init__(".\\.\\image\\if_else.png")
        elif tab_type == "Switch":
            super().__init__(".\\.\\image\\switch.png")
        else:
            pass