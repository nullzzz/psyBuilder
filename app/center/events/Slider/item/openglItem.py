import math

import OpenGL.GL as gl
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent


class GLItem(QGraphicsItem):

    def __init__(self, item_type="open", item_name: str = "opengel"):
        super(GLItem, self).__init__()

        self.item_type = item_type

        self.item_name = item_name

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        # self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.trolltechGreen = QColor.fromRgb(255, 255, 255, 0)
        self.trolltechPurple = QColor.fromRgb(122, 0, 0, 0)
        self.object = 0

        self.gear1 = 0
        self.gear2 = 0
        self.gear3 = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.gear1Rot = 0

        # self.setPolygon(path)
        self.initializeGL()

    def setPosition(self):
        """
        :get icon properties in scene and send it to info :
        """
        width = self.boundingRect().width()
        height = self.boundingRect().height()

    def getName(self):
        return self.item_name

    def boundingRect(self):
        return QRectF(-100, -100, 200, 200)

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
        print(self.boundingRect())
        painter.drawRoundedRect(self.boundingRect(), 5, 5)
        painter.beginNativePainting()
        ##########
        # gl.glColor3f(0.5, 1.0, 0.2)
        # gl.glBegin(gl.GL_TRIANGLES)
        # gl.glVertex3f(0, -100, 0)
        # gl.glVertex3f(-100, 100.0, 0)
        # gl.glVertex3f(100.0, 100.0, 0)
        # gl.glEnd()
        ################3
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        self.drawGear(self.gear1, -3.0, -2.0, 0.0, self.gear1Rot / 16.0)
        self.drawGear(self.gear2, +3.1, -2.0, 0.0,
                      -2.0 * (self.gear1Rot / 16.0) - 9.0)

        gl.glRotated(+90.0, 1.0, 0.0, 0.0)
        self.drawGear(self.gear3, -3.1, -1.8, -2.2,
                      +2.0 * (self.gear1Rot / 16.0) - 2.0)

        gl.glPopMatrix()
        painter.endNativePainting()

    def drawGear(self, gear, dx, dy, dz, angle):
        gl.glPushMatrix()
        gl.glTranslated(dx, dy, dz)
        gl.glRotated(angle, 0.0, 0.0, 1.0)
        gl.glCallList(gear)
        gl.glPopMatrix()

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        reflectance1 = (0.8, 0.1, 0.0, 1.0)
        reflectance2 = (0.0, 0.8, 0.2, 1.0)
        reflectance3 = (0.2, 0.2, 1.0, 1.0)

        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightPos)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.gear1 = self.makeGear(reflectance1, 1.0, 4.0, 1.0, 0.7, 20)
        self.gear2 = self.makeGear(reflectance2, 0.5, 2.0, 2.0, 0.7, 10)
        self.gear3 = self.makeGear(reflectance3, 1.3, 2.0, 0.5, 0.7, 10)

        gl.glEnable(gl.GL_NORMALIZE)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)

        side = 200

        gl.glViewport(0, 0, 10, 10)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -40.0)

    def getInfo(self):
        return {}

    def setAttributes(self, attributes: list):
        pass

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

    def makeGear(self, reflectance, innerRadius, outerRadius, thickness, toothSize, toothCount):
        list = gl.glGenLists(1)
        gl.glNewList(list, gl.GL_COMPILE)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE,
                        reflectance)

        r0 = innerRadius
        r1 = outerRadius - toothSize / 2.0
        r2 = outerRadius + toothSize / 2.0
        delta = (2.0 * math.pi / toothCount) / 4.0
        z = thickness / 2.0

        gl.glShadeModel(gl.GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            gl.glNormal3d(0.0, 0.0, sign)

            gl.glBegin(gl.GL_QUAD_STRIP)

            for j in range(toothCount + 1):
                angle = 2.0 * math.pi * j / toothCount
                gl.glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                gl.glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                gl.glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                gl.glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            gl.glEnd()

            gl.glBegin(gl.GL_QUADS)

            for j in range(toothCount):
                angle = 2.0 * math.pi * j / toothCount
                gl.glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                gl.glVertex3d(r2 * math.cos(angle + delta), r2 * math.sin(angle + delta), sign * z)
                gl.glVertex3d(r2 * math.cos(angle + 2 * delta), r2 * math.sin(angle + 2 * delta), sign * z)
                gl.glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            gl.glEnd()

        gl.glBegin(gl.GL_QUAD_STRIP)

        for i in range(toothCount):
            for j in range(2):
                angle = 2.0 * math.pi * (i + (j / 2.0)) / toothCount
                s1 = r1
                s2 = r2

                if j == 1:
                    s1, s2 = s2, s1

                gl.glNormal3d(math.cos(angle), math.sin(angle), 0.0)
                gl.glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), +z)
                gl.glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), -z)

                gl.glNormal3d(s2 * math.sin(angle + delta) - s1 * math.sin(angle),
                              s1 * math.cos(angle) - s2 * math.cos(angle + delta), 0.0)
                gl.glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), +z)
                gl.glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), -z)

        gl.glVertex3d(r1, 0.0, +z)
        gl.glVertex3d(r1, 0.0, -z)
        gl.glEnd()

        gl.glShadeModel(gl.GL_SMOOTH)

        gl.glBegin(gl.GL_QUAD_STRIP)

        for i in range(toothCount + 1):
            angle = i * 2.0 * math.pi / toothCount
            gl.glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            gl.glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), +z)
            gl.glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), -z)

        gl.glEnd()

        gl.glEndList()

        return list

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        dx = event.pos().x() - self.lastPos.x()
        dy = event.pos().y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def setXRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.update()

    def setYRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.update()

    def setZRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.update()
