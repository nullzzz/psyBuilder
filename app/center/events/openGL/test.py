import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtOpenGL import QGLFormat, QGLWidget, QGL
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QApplication

from app.center.events.Slider.item.openglItem import GLItem


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        opengl = QGLWidget(QGLFormat(QGL.SampleBuffers))
        opengl.makeCurrent()
        self.view.setViewport(opengl)

        width, height = 1920, 1080
        #
        self.view.setMaximumSize(width, height)
        self.scene.setSceneRect(0, 0, width, height)
        self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)
        self.setCentralWidget(self.view)

        item1 = GLItem()
        item2 = GLItem()
        item1.setPos(400, 400)
        item2.setPos(700, 700)
        item2.setFlag(1, False)
        self.scene.addItem(item1)
        self.scene.addItem(item2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = Win()
    w.show()
    app.exec()
