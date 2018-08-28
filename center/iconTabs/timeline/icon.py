from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Icon(QLabel):
    # 判断不同的icon
    COUNT = 0

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
            self.value = self.name + "." + str(Icon.COUNT)
            Icon.COUNT += 1
        else:
            self.value = value

    def setName(self, name):
        self.name = name

    def changeType(self, widgetType):
        self.name = widgetType
        self.value = widgetType + '.'+ self.value.split('.')[-1]
