from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QDialog, QDesktopWidget

from app.func import Func


class Preview(QDialog):
    def __init__(self, file: str = "", pix_file=None, start_x: str = "0", start_y: str = "0", width: str = "100",
                 height: str = "100"):
        super(Preview, self).__init__()
        self.file = file
        self.pix = pix_file
        screen = QDesktopWidget().screenGeometry()
        if "%" in start_x:
            self.start_x = int(start_x[0:-1]) * screen.width() / 100
        else:
            self.start_x = int(start_x)
        if "%" in start_y:
            self.start_y = int(start_y[0:-1]) * screen.height() / 100
        else:
            self.start_y = int(start_y)
        if "%" in width:
            self.width_factor = int(width[0:-1]) * screen.width() / 100
        else:
            self.width_factor = int(width)
        if "%" in height:
            self.height_factor = int(height[0:-1]) * screen.height() / 100
        else:
            self.height_factor = int(height)

    def setTransparent(self, transparent_value=80):
        self.setWindowOpacity(1 - transparent_value / 100)

    def setStartPos(self, x, y):
        self.start_x = x
        self.start_y = y

    def paintEvent(self, e):
        painter = QPainter(self)
        pix = QPixmap()
        pix.load(Func.getImagePath("preview_tip"))
        painter.drawPixmap(
            self.start_x,
            self.start_y,
            self.width_factor,
            self.height_factor,
            self.pix)
        painter.drawPixmap(0, 0, 400, 150, pix)
