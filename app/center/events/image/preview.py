from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtWidgets import QDialog

from app.func import Func


class Preview(QDialog):
    def __init__(self, info: dict):
        super(Preview, self).__init__()
        self.general: dict = info.get("General")
        self.frame: dict = info.get("Frame")
        self.file_name = ""

    def setTransparent(self, transparent_value=80):
        self.setWindowOpacity(1 - transparent_value / 100)

    def setStartPos(self, x, y):
        self.start_x = x
        self.start_y = y

    def paintEvent(self, e):
        painter = QPainter(self)
        pix = QPixmap()
        pix.load(Func.getImage("preview_tip"))
        painter.drawPixmap(
            self.start_x,
            self.start_y,
            self.width_factor,
            self.height_factor,
            self.pix)
        painter.drawPixmap(0, 0, 400, 150, pix)

    def parseProperties(self):
        self.file = self.general.get("File name", "")
        if self.isRefer(self.file):
            self.file = ""

        self.is_UD = self.general.get("Mirror Up/Down", False)
        self.is_LR = self.general.get("Mirror Mirror Left/Right", False)
        self.rotate = self.general.get("Rotate")
        if self.isRefer(self.rotate):
            self.ratate = 0

        self.is_stretch = self.general.get("Stretch")
        self.stretch_mode = self.general.get("Stretch Mode")

        self.x_pos = self.frame.get("Center X", "50%")
        self.y_pos = self.frame.get("Center Y", "50%")
        self.w_size = self.frame.get("Width", "100%")
        self.h_size = self.frame.get("Height", "100%")
        if self.isRefer(self.x_pos):
            self.x_pos = "50%"
        if self.isRefer(self.y_pos):
            self.y_pos = "50%"
        if self.isRefer(self.w_size):
            self.w_size = "100%"
        if self.isRefer(self.h_size):
            self.h_size = "100%"

        self.frame_fill_color = self.frame.get("Frame")
        self.transparent_value = self.pro_window.general.transparent.text()

    def isRefer(self, var: str):
        return var.startswith("[") and var.endswith("]")

    def setImage(self):
        img = QImage(self.file)
        image = img.mirrored(self.isLR, self.isUD)
        pix = QPixmap.fromImage(image)
        self.pix = pix
        # 图片反转
        if self.is_stretch:
            mode = self.pro_window.general.stretch_mode.currentText()
            w = self.label.size().width()
            h = self.label.size().height()
            if mode == "Both":
                new_pix = pix.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            elif mode == "LeftRight":
                new_pix = pix.scaledToWidth(w, Qt.FastTransformation)
            else:
                new_pix = pix.scaledToHeight(h, Qt.FastTransformation)
            self.label.setPixmap(new_pix)
        else:
            self.label.setPixmap(pix)
