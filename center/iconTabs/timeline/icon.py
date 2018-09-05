from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Icon(QLabel):
    # 判断不同的icon
    OTHER_COUNT = 0
    TIMELINE_COUNT = 0
    # event
    CYCLE_COUNT = 0
    SOUNTOUT_COUNT = 0
    TEXT_COUNT = 0
    IMAGE_COUNT = 0
    VIDEO_COUNT = 0
    # eye tracker
    OPEN_COUNT = 0
    DC_COUNT = 0
    CALIBRATION_COUNT = 0
    ACTION_COUNT = 0
    STARTR_COUNT = 0
    ENDR_COUNT = 0
    CLOSE_COUNT = 0
    # quest
    QUESTINIT_COUNT = 0
    QUESTUPDATA_COUNT = 0
    QUESTGETVALUE_COUNT = 0
    # condition
    IF_ELSE_COUNT = 0
    SWITCH_COUNT = 0

    def __init__(self, parent=None, name="Other", pixmap=None, value=''):
        super(Icon, self).__init__(parent)

        self.setStyleSheet("""
                            QLabel{
                                background-color: transparent;
                            }
                            QLabel:hover{
                                border: 2px solid lightBlue;
                                border-radius: 4px;
                                padding: 2px;
                            }
                            """)
        self.setMouseTracking(True)
        # widget type or name
        self.name = name
        #
        self.setPixmap(QPixmap(pixmap))
        # value
        if not value:
            count = self.getCount(self.name)

            self.value = self.name + "." + str(count)
        else:
            self.value = value

    def setName(self, name):
        self.name = name

    def changeType(self, widget_type):
        self.name = widget_type
        count = self.getCount(widget_type)
        self.value = widget_type + '.' + str(count)

    def getCount(self, widget_type):
        count = 0
        if widget_type == "Cycle":
            count = Icon.CYCLE_COUNT
            Icon.CYCLE_COUNT += 1
        elif widget_type == "Timeline":
            count = Icon.TIMELINE_COUNT
            Icon.TIMELINE_COUNT += 1
        elif widget_type == "SoundOut":
            count = Icon.SOUNTOUT_COUNT
            Icon.SOUNTOUT_COUNT += 1
        elif widget_type == "Text":
            count = Icon.TEXT_COUNT
            Icon.TEXT_COUNT += 1
        elif widget_type == "Image":
            count = Icon.IMAGE_COUNT
            Icon.IMAGE_COUNT += 1
        elif widget_type == "Video":
            count = Icon.VIDEO_COUNT
            Icon.VIDEO_COUNT += 1
        elif widget_type == "Close":
            count = Icon.CLOSE_COUNT
            Icon.CLOSE_COUNT += 1
        elif widget_type == "DC":
            count = Icon.DC_COUNT
            Icon.DC_COUNT += 1
        elif widget_type == "Calibration":
            count = Icon.CALIBRATION_COUNT
            Icon.CALIBRATION_COUNT += 1
        elif widget_type == "EndR":
            count = Icon.ENDR_COUNT
            Icon.ENDR_COUNT += 1
        elif widget_type == "Open":
            count = Icon.OPEN_COUNT
            Icon.OPEN_COUNT += 1
        elif widget_type == "Action":
            count = Icon.ACTION_COUNT
            Icon.ACTION_COUNT += 1
        elif widget_type == "StartR":
            count = Icon.STARTR_COUNT
            Icon.STARTR_COUNT += 1
        elif widget_type == "QuestGetValue":
            count = Icon.QUESTGETVALUE_COUNT
            Icon.QUESTGETVALUE_COUNT += 1
        elif widget_type == "QuestUpdate":
            count = Icon.QUESTUPDATA_COUNT
            Icon.QUESTUPDATA_COUNT += 1
        elif widget_type == "QuestInit":
            count = Icon.QUESTINIT_COUNT
            Icon.QUESTINIT_COUNT += 1
        elif widget_type == "If_else":
            count = Icon.IF_ELSE_COUNT
            Icon.IF_ELSE_COUNT += 1
        elif widget_type == "Switch":
            count = Icon.SWITCH_COUNT
            Icon.SWITCH_COUNT += 1
        else:
            count = Icon.OTHER_COUNT
            Icon.OTHER_COUNT += 1

        return count

    def changeValue(self, value):
        self.value = value