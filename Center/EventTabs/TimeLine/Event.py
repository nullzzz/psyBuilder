from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class Event(QLabel):
    # 用以区分不同的event
    count = 0
    def __init__(self, parent=None, name="", pixmap=None, value=''):
        super(Event, self).__init__(parent)

        self.setStyleSheet("background-color:transparent;")

        self.name = name
        self.setPixmap(QPixmap(pixmap))
        if not value:
            self.value = name + "." + str(Event.count)
            Event.count += 1
        else:
            self.value = value


    def setName(self, name):
        self.name = name
