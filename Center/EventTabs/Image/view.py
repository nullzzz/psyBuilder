from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QDialog


class Preview(QDialog):
    def __init__(
            self,
            pix_file=None,
            start_x=0,
            start_y=0,
            width=100,
            height=100):
        super(Preview, self).__init__()
        self.file = pix_file
        self.start_x = start_x
        self.start_y = start_y
        self.width_factor = width / 100
        self.height_factor = height / 100

    def setTransparent(self, transparent_value=10):
        self.setWindowOpacity(transparent_value / 100)

    def setStartPos(self, x, y):
        self.start_x = x
        self.start_y = y

    def paintEvent(self, e):
        painter = QPainter(self)
        pix = QPixmap()
        pix.load(".\\.\\image\\preview_tip")
        painter.drawPixmap(
            self.start_x,
            self.start_y,
            self.width() * self.width_factor,
            self.height() * self.height_factor,
            self.file)
        painter.drawPixmap(0, 0, 400, 150, pix)

