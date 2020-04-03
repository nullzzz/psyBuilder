import sys

from PyQt5.QtGui import QOpenGLContext
from PyQt5.QtWidgets import QOpenGLWidget, QApplication


class D(QOpenGLWidget):
    def __init__(self):
        super(D, self).__init__()

    def initializeGL(self):
        f = QOpenGLContext.currentContext().functions()
        f.glClearColor(1.0, 1.0, 1.0, 1.0)

    def resizeGL(self, w, h):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = D()
    t.show()
    sys.exit(app.exec_())
