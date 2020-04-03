import math

import OpenGL.GL as gl
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsItem


class GLItem(QGraphicsItem):

    def __init__(self, item_type, item_name: str = "opengel"):
        super(GLItem, self).__init__()

        self.item_type = item_type

        self.item_name = item_name

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.trolltechGreen = QColor.fromRgb(255, 255, 255, 0)
        self.trolltechPurple = QColor.fromRgb(122, 0, 0, 0)
        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

    def setPosition(self):
        """
        :get icon properties in scene and send it to info :
        """
        width = self.boundingRect().width()
        height = self.boundingRect().height()

    def getName(self):
        return self.item_name

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.beginNativePainting()

        # self.setClearColor(self.trolltechPurple.darker())
        # self.object = self.makeObject()
        # gl.glShadeModel(gl.GL_FLAT)
        # gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glEnable(gl.GL_CULL_FACE)
        # gl.glClear(
        #     gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # gl.glLoadIdentity()
        # gl.glTranslated(0.0, 0.0, -10.0)
        # gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        # gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        # gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        # gl.glCallList(self.object)
        gl.glColor3f(0.5, 1.0, 0.2)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex3f(100.0, 100.0, -100.0)
        gl.glVertex3f(150.0, 300.0, -500.0)
        gl.glVertex3f(200.0, 700.0, -200.0)
        gl.glEnd()
        painter.endNativePainting()

    def getInfo(self):
        return {}

    def setAttributes(self, attributes: list):
        pass

    # def boundingRect(self):
    #     return QRectF(20, 20, 200, 200)

    def openPro(self):
        pass

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBegin(gl.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        gl.glEnd()
        gl.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        gl.glVertex3d(x1, y1, -0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x3, y3, -0.05)
        gl.glVertex3d(x4, y4, -0.05)

        gl.glVertex3d(x4, y4, +0.05)
        gl.glVertex3d(x3, y3, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        gl.glVertex3d(x1, y1, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print("ddddd")
