from PyQt5.QtWidgets import QItemDelegate, QStyle
from PyQt5.QtGui import QPen


class NoDash(QItemDelegate):
    def __init__(self):
        super(NoDash, self).__init__()

    def drawFocus(self, painter, option, rect):
        if option.state and QStyle.State_HasFocus:
            pen = QPen()
            pen.setWidth(0)
            painter.setPen(pen)
