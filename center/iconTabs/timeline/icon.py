from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Icon(QLabel):
    # 判断不同的icon
    COUNT = 0

    def __init__(self, parent=None, name="", pixmap=None, value=''):
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

        self.name = name
        self.setPixmap(QPixmap(pixmap))
        if not value:
            self.value = name + "." + str(Icon.COUNT)
            Icon.COUNT += 1
        else:
            self.value = value

    def setName(self, name):
        self.name = name
