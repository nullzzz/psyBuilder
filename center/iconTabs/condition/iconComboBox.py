from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox


class IconComboBox(QComboBox):
    def __init__(self, parent=None):
        super(IconComboBox, self).__init__(parent)

        self.setStyleSheet("""
            QComboBox {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 200px;
                max-width: 100px;
                min-height: 50px;
            }
            
            QComboBox:editable {
                background: white;
            }
            
            QComboBox:!editable, QComboBox::drop-down:editable {
                 background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                             stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                             stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
            }
            
            /* QComboBox gets the "on" state when the popup is open */
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                            stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
            }
            
            QComboBox:on { /* shift the text when the popup opens */
                padding-top: 3px;
                padding-left: 4px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
            
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }
            
            QComboBox::down-arrow {
                image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
            }
            
            QComboBox::down-arrow:on { /* shift the arrow when popup is open */
                top: 1px;
                left: 1px;
            }""")

        self.addItem("None")
        self.addIcon("Timeline")
        self.addIcon("Cycle")
        self.addIcon("SoundOut")
        self.addIcon("Text")
        self.addIcon("Image")
        self.addIcon("Video")
        self.addIcon("Close")
        self.addIcon("DC")
        self.addIcon("Calibration")
        self.addIcon("EndR")
        self.addIcon("Open")
        self.addIcon("Action")
        self.addIcon("StartR")
        self.addIcon("QuestGetValue")
        self.addIcon("QuestUpdate")
        self.addIcon("IfElse")
        self.addIcon("Switch")

    def addIcon(self, widget_type):
        tab_icon = None
        if widget_type == "Cycle":
            tab_icon = QIcon(".\\.\\image\\cycle.png")
        elif widget_type == "Timeline":
            tab_icon = QIcon(".\\.\\image\\timeLine.png")
        elif widget_type == "SoundOut":
            tab_icon = QIcon(".\\.\\image\\soundOut.png")
        elif widget_type == "Text":
            tab_icon = QIcon(".\\.\\image\\text.png")
        elif widget_type == "Image":
            tab_icon = QIcon(".\\.\\image\\image.png")
        elif widget_type == "Video":
            tab_icon = QIcon(".\\.\\image\\video.png")
        elif widget_type == "Close":
            tab_icon = QIcon(".\\.\\image\\close_eye.png")
        elif widget_type == "DC":
            tab_icon = QIcon(".\\.\\image\\DC_eye.png")
        elif widget_type == "Calibration":
            tab_icon = QIcon(".\\.\\image\\calibration_eye.png")
        elif widget_type == "EndR":
            tab_icon = QIcon(".\\.\\image\\end_eye.png")
        elif widget_type == "Open":
            tab_icon = QIcon(".\\.\\image\\open_eye.png")
        elif widget_type == "Action":
            tab_icon = QIcon(".\\.\\image\\action_eye.png")
        elif widget_type == "StartR":
            tab_icon = QIcon(".\\.\\image\\start_eye.png")
        elif widget_type == "QuestGetValue":
            tab_icon = QIcon(".\\.\\image\\get_value.png")
        elif widget_type == "QuestUpdate":
            tab_icon = QIcon(".\\.\\image\\update_quest.png")
        elif widget_type == "IfElse":
            tab_icon = QIcon(".\\.\\image\\if_else.png")
        elif widget_type == "Switch":
            tab_icon = QIcon(".\\.\\image\\switch.png")
        else:
            pass

        self.addItem(tab_icon, widget_type)