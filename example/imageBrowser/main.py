from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPaintEvent, QImage, QTransform, QColor, QPen
from PyQt5.QtWidgets import QScrollArea, QMainWindow, QApplication, QLabel, QFrame

borderColor = QColor(Qt.red)
borderWidth = 10
rotation = 45


class ImageContainer(QLabel):
    def __init__(self):
        super(ImageContainer, self).__init__()

        self.cx = 960
        self.cy = 540

        self.back_color: str = "0,0,0"
        self.image_width = 564
        self.image_height = 432
        img = QImage(r"D:\新建文件夹\摸鱼.png")

        self.pix = QPixmap.fromImage(img)
        self.border_color: str = "255,0,0"
        self.border_width = 1
        self.rotate = 45

    def setCenter(self, x: int, y: int):
        self.cx = x
        self.cy = y

    def paintEvent(self, a0: QPaintEvent) -> None:
        super(QFrame, self).paintEvent(a0)
        painter = QPainter(self)

        rect = QRect(- self.image_width // 2,
                     - self.image_height // 2,
                     self.image_width,
                     self.image_height)

        painter.translate(self.cx, self.cy)
        painter.rotate(45)
        painter.drawPixmap(rect,
                           self.pix)

        painter.setPen(QPen(Qt.red, 12))
        painter.drawRect(rect)


class ImageBrowser(QScrollArea):
    def __init__(self):
        super(ImageBrowser, self).__init__()

        self.setMaximumSize(1920, 1080)
        # self.image = ImageContainer()
        self.image = QLabel()
        self.image.setMaximumSize(1920, 1080)

        self.setPix()

        self.setWidget(self.image)

    def setPix(self):
        img = QImage(r"D:\新建文件夹\摸鱼.png")
        matrix = QTransform()
        matrix.rotate(45)
        img2 = img.transformed(matrix)
        self.image.setPixmap(QPixmap.fromImage(img2))


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.browser = ImageBrowser()
        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = ImageContainer()
    form.show()
    sys.exit(app.exec_())
