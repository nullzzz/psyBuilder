import numpy as np
import qimage2ndarray
from PyQt5.QtCore import (pyqtSignal, QLineF, QPointF, QRect, QRectF, QSize, QPoint, Qt, QByteArray, QDataStream,
                          QIODevice, QMimeData)
from PyQt5.QtGui import (QBrush, QColor, QFont, QIcon, QIntValidator, QPainter,
                         QPainterPath, QPen, QPixmap, QDrag)
from PyQt5.QtWidgets import (QAction, QButtonGroup, QComboBox, QFontComboBox, QGraphicsItem,
                             QGraphicsLineItem, QGraphicsPolygonItem,
                             QGraphicsScene, QGraphicsTextItem, QGraphicsView, QGridLayout, QGraphicsPixmapItem,
                             QHBoxLayout, QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QToolBox, QToolButton,
                             QWidget, QPushButton, QColorDialog, QDesktopWidget)

from app.center.widget_tabs.events.slider.item.diaItem import DiaItem
from app.center.widget_tabs.events.slider.item.diagramTextItem import DiagramTextItem
from app.center.widget_tabs.events.slider.item.pixItem import PixItem

from app.center.widget_tabs.events.slider.property import SliderProperty
from app.center.widget_tabs.events.slider.scene import Scene
from app.func import Func
from lib.psy_message_box import PsyMessageBox as QMessageBox


class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        icon = self.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()

"""
class DiagramTextItem(QGraphicsTextItem):
    lostFocus = pyqtSignal(QGraphicsTextItem)
    selectedChange = pyqtSignal(QGraphicsItem)

    def __init__(self, parent=None, scene=None):
        super(DiagramTextItem, self).__init__()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.default_properties = {
            'name': 'text',
            'family': 'SimSun',
            'size': 1,
            'B': False,
            'I': False,
            'U': False,
            'color': self.defaultTextColor(),
            'text': 'text',
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1
        }

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        super(DiagramTextItem, self).focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
        super(DiagramTextItem, self).mouseDoubleClickEvent(event)

    def setProperties(self):
        self.default_properties['family'] = self.font().family()
        self.default_properties['size'] = self.font().pointSize()
        self.default_properties['B'] = self.font().bold()
        self.default_properties['I'] = self.font().italic()
        self.default_properties['U'] = self.font().underline()
        self.default_properties['color'] = self.defaultTextColor().name()
        self.default_properties['text'] = self.toPlainText()
        self.default_properties['z'] = self.zValue()
        self.default_properties['x_pos'] = self.scenePos().x()
        self.default_properties['y_pos'] = self.scenePos().y()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        font = QFont()
        font.setFamily(self.default_properties['family'])
        font.setPointSize(self.default_properties['size'])
        font.setBold(self.default_properties['B'])
        font.setItalic(self.default_properties['I'])
        font.setUnderline(self.default_properties['U'])

        self.setFont(font)
        self.setDefaultTextColor(QColor(self.default_properties['color']))
        self.setPlainText(self.default_properties['text'])

    def clone(self):
        item = DiagramTextItem()
        self.setProperties()
        item.restore(self.default_properties)
        item.setZValue(self.zValue())

        return item

class PixItem(QGraphicsPixmapItem):
    Video, Picture, Sound, Snow, Gabor = 5, 6, 7, 8, 9

    def __init__(self, diagramType, contextMenu, attributes=None, parent=None):
        super(PixItem, self).__init__(parent)

        self.diagramType = diagramType
        self.contextMenu = contextMenu
        self.attributes = attributes

        if self.diagramType == self.Video:
            self.pro_window = VideoProperty()
            self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(100, 100))

        elif self.diagramType == self.Sound:
            self.pro_window = SoundProperty()
            self.setPixmap(QPixmap(Func.getImage("music.png")).scaled(100, 100))

        elif self.diagramType == self.Snow:
            self.pro_window = snowProperty()
            self.setPixmap(QPixmap(Func.getImage("snow.png")))

        elif self.diagramType == self.Gabor:
            self.pro_window = GaborProperty()
            self.setPixmap(QPixmap(Func.getImage("Gabor.png")))

        else:
            self.pro_window = ImageProperty()
            self.setPixmap(QPixmap(Func.getImage("Picture.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.resizingFlag = False
        self.arbitrary_resize = False
        self.keep_resize = False

        self.default_properties = {
            'name': self.diagramType,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties
        }

    def mousePressEvent(self, mouseEvent):
        if self.diagramType < 8:
            if mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.AltModifier:
                self.arbitrary_resize = True
                self.setCursor(Qt.SizeAllCursor)
            elif mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.ShiftModifier:
                self.keep_resize = True
                self.setCursor(Qt.SizeAllCursor)
            else:
                super(PixItem, self).mousePressEvent(mouseEvent)
        else:
            super(PixItem, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()
        if self.diagramType > 7:
            self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
        if self.arbitrary_resize:
            self.resizingFlag = True
        if self.keep_resize:
            self.resizingFlag = True
            if x > y:
                x = y
            else:
                y = x
        if self.resizingFlag:
            pass
            # if self.diagramType == self.Video:
            #     self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(x, y))
            # elif self.diagramType == self.Sound:
            #     self.setPixmap(QPixmap(Func.getImage("music.png")).scaled(x, y))
            # else:
            #     self.setPixmap(QPixmap(Func.getImage("Picture.png")).scaled(x, y))
            # self.update()
        else:
            super(PixItem, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.arbitrary_resize = False
        self.keep_resize = False
        self.resizingFlag = False
        super(PixItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttributes(self.attributes)
        if self.diagramType == self.Snow:
            self.default_properties['Center X'] = str(int(self.scenePos().x()))
            self.default_properties['Center Y'] = str(int(self.scenePos().y()))
        elif self.diagramType == self.Gabor:
            self.default_properties['Center X'] = str(int(self.scenePos().x()))
            self.default_properties['Center Y'] = str(int(self.scenePos().y()))
        try:
            self.pro_window.setProperties(self.default_properties)
        except Exception as e:
            print(e)
        self.pro_window.show()

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        # Here is a bug, Fuck you!
        # self.myContextMenu.exec_(event.screenPos())
        self.contextMenu.exec_(event.screenPos())

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # load previous default_properties
        self.pro_window.loadSetting()

    def apply(self):
        # 将deafult_properties设置成当前各个输入框的内容
        self.pro_window.getInfo()
        self.default_properties = {
            'name': self.diagramType,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties}

        if self.diagramType == self.Snow:
            try:
                snowPixSize = int(self.default_properties["Scale"])
                snowStim    = Snow(int(int(self.default_properties["Width"])/snowPixSize),
                                   int(int(self.default_properties["Height"])/snowPixSize))
                snowStim    = snowStim.astype(np.uint8)

                pix = QPixmap(qimage2ndarray.array2qimage(snowStim))
                pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))

                self.setPos(QPoint(float(self.pro_window.frame.default_properties["Center X"]),
                                   float(self.pro_window.frame.default_properties["Center Y"])))

                self.setPixmap(pix)
                x = self.boundingRect().center().x()
                y = self.boundingRect().center().y()

                self.setTransformOriginPoint(x, y)
                self.setRotation(int(self.default_properties["Rotation"]))
                # self.setScale(float(self.default_properties["Scale"]))
                self.update()
            except Exception as e:
                print(e)
                
        if self.diagramType == self.Gabor:
            try:
                spFreq      = float(self.default_properties['spatialFreq(cycles/pixel)'])
                Contrast    = float(self.default_properties['Contrast'])
                phase       = float(self.default_properties['phase'])
                orientation = float(self.default_properties['orientation'])

                rgbValue = self.default_properties['bkColor'].split(',')
                sdx      = float(self.default_properties['SDx(pixels)'])
                sdy      = float(self.default_properties['SDy(pixels)'])
                width    = int(self.default_properties["Width"])
                height   = int(self.default_properties["Height"])
                bkColor  = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))

                stim  = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                  bkColor, width, height, sdx, sdy)
                stim  = stim.astype(np.uint8)
                pix   = QPixmap(qimage2ndarray.array2qimage(stim))
                pix  = pix.scaled(int(self.default_properties['Width']),
                                 int(self.default_properties['Height']),
                                 Qt.KeepAspectRatio)

                self.setPos(QPoint(float(self.pro_window.frame.default_properties["Center X"]),
                                   float(self.pro_window.frame.default_properties["Center Y"])))
                self.setPixmap(pix)

                x = self.boundingRect().center().x()
                y = self.boundingRect().center().y()

                self.setTransformOriginPoint(x, y)
                self.setRotation(int(self.default_properties["rotation"]))
                self.update()
            except Exception as e:
                print(e)

        self.default_properties = {
            'name': self.diagramType,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties}

    def setProperties(self):
        self.default_properties['x_pos'] = self.scenePos().x()
        self.default_properties['y_pos'] = self.scenePos().y()

    def restore(self, properties: dict):
        if properties:
            self.pro_window.setProperties(properties)
            if self.diagramType == self.Snow:
                try:
                    snowStim = Snow(int(properties["Width"]), int(properties["Height"]))
                    snowStim = snowStim.astype(np.uint8)
                    pix = QPixmap(qimage2ndarray.array2qimage(snowStim))

                    pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
                    self.setPixmap(pix)

                    x = self.boundingRect().center().x()
                    y = self.boundingRect().center().y()

                    self.setTransformOriginPoint(x, y)
                    self.setRotation(int(properties["Rotation"]))
                    self.update()
                except Exception as e:
                    print(e)


            if self.diagramType == self.Gabor:
                try:
                    spFreq      = float(self.default_properties['spatialFreq(cycles/pixel)'])
                    Contrast    = float(self.default_properties['Contrast'])
                    phase       = float(self.default_properties['phase'])
                    orientation = float(self.default_properties['orientation'])
                    rgbValue    = self.default_properties['bkColor'].split(',')
                    sdx     = float(self.default_properties['SDx(pixels)'])
                    sdy     = float(self.default_properties['SDy(pixels)'])
                    width   = int(self.default_properties["Width"])
                    height  = int(self.default_properties["Height"])
                    bkColor = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))

                    stim = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                         bkColor, width, height, sdx, sdy)

                    stim = stim.astype(np.uint8)
                    pix  = QPixmap(qimage2ndarray.array2qimage(stim))

                    pix  = pix.scaled(int(self.default_properties['Width']),
                                     int(self.default_properties['Height']),
                                     Qt.KeepAspectRatio)

                    self.setPixmap(pix)
                    x = self.boundingRect().center().x()
                    y = self.boundingRect().center().y()
                    self.setTransformOriginPoint(x, y)
                    self.setRotation(int(properties["rotation"]))
                    self.update()
                except Exception as e:
                    print(e)

    def clone(self):
        new = PixItem(self.diagramType, self.contextMenu, self.attributes)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        new.setPixmap(self.pixmap())
        new.setZValue(self.zValue())

        return new

class DiaItem(QGraphicsPolygonItem):
    PolygonStim, Arc, Circle, Rectangle, Line = range(5)

    def __init__(self, diagramType, contextMenu, attributes=None, p1=None, p2=None, parent=None,
                 scene=None):
        super(DiaItem, self).__init__()
        self.diagramType = diagramType
        self.contextMenu = contextMenu
        self.attributes = attributes

        self.default_properties = {
            "name": self.diagramType,
            "Type": self.diagramType,
            "Center X": "0",
            "Center Y": "0",
            "P1 X": "0",
            "P1 Y": "0",
            "P2 X": "0",
            "P2 Y": "0",
            "Point": [['0', '0'], ['0', '0'], ['0', '0']],  # added by yang
            "Start angle": "0",
            "Angle length": "270",
            "Width": "200",
            "Height": "200",
            "Border color": "black",
            "Border width": 1,
            "Fill color": "white",
            'z': self.zValue()
        }
        self.p1 = p1
        self.p2 = p2

        path = QPainterPath()
        # circle
        if self.diagramType == self.Circle:
            path.addEllipse(QRectF(-100, -100, 200, 200))
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('circle')

        #  reactange
        elif self.diagramType == self.Rectangle:
            path.addRect(QRectF(-100, -100, 200, 200))
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('rectangle')

        # arc
        elif self.diagramType == self.Arc:
            path.arcTo(QRectF(-100, -100, 200, 200), 0, 270)
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('arc')

        # polygon
        elif self.diagramType == self.PolygonStim:
            # added by yang to plot the triangle
            nVertices = 3
            verticesXY = []
            for iVertex in range(nVertices):
                verticesXY.append([int(100 * np.cos(np.pi / 2 - iVertex * 2 * np.pi / nVertices)),
                                   int(100 * np.sin(iVertex * 2 * np.pi / nVertices - np.pi / 2))])
                if iVertex == 0:
                    path.moveTo(verticesXY[iVertex][0], verticesXY[iVertex][1])
                else:
                    path.lineTo(verticesXY[iVertex][0], verticesXY[iVertex][1])

            path.lineTo(verticesXY[0][0], verticesXY[0][1])
            #
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('polygonStim')

        elif self.diagramType == self.Line:
            path.moveTo(p1.x(), p1.y())
            path.lineTo(p2.x(), p2.y())
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('line')

        else:
            raise Exception("diagramType should be of 'Arc','Line','rectangle', or 'circle' !!")

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setPolygon(self.mPolygon)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.arbitrary_resize = False
        self.keep_resize = False
        self.resizingFlag = False
        # self.flag1 = False
        self.center = QPointF(0, 0)
        self.ItemColor = 'white'
        self.LineColor = 'black'
        self.LineWidth = 1

    def setItemColor(self, color):
        self.ItemColor = color

    def setLineColor(self, color):
        self.LineColor = color

    def setLineWidth(self, width):
        self.LineWidth = width
        # self.polygon

    def boundingRect(self):
        return self.polygon().boundingRect().adjusted(-self.pen().width(),
                                                      -self.pen().width(),
                                                      self.pen().width(),
                                                      self.pen().width())

    def mouseMoveEvent(self, mouseEvent):
        # step 1: updating the default_properties of frame
        self.getProperties()
        self.pro_window.frame.setProperties(self.default_properties)

        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()

        rect0 = self.polygon().boundingRect()

        cHeight = rect0.height()
        cWidth  = rect0.width()

        # 非等比例
        if self.arbitrary_resize and self.diagramType < 4:
            self.resizingFlag = True
        # 等比例
        if self.keep_resize and self.diagramType < 4:
            self.resizingFlag = True

            if cHeight < 5:
                cHeight = 5

            if cWidth < 5:
                cWidth = 5

            # make sure the zoom in/out ratio equal for h and w
            ratio = cHeight / cWidth

            if (y - cHeight) / (x - cWidth) > ratio:
                y = ratio * (x - cWidth) + cHeight
            else:
                x = (y - cHeight) / ratio + cWidth

        if self.resizingFlag:
            x0 = rect0.left()
            y0 = rect0.top()

            path  = QPainterPath()

            newWidth  = x - x0
            newHeight = y - y0

            cRect = QRectF(x0 - (newWidth - cWidth)/2, y0 - (newHeight - cHeight)/2, newWidth, newHeight)

            if self.diagramType == self.Circle:
                path.addEllipse(cRect)

            elif self.diagramType == self.Arc:
                path.moveTo(cRect.center())
                path.arcTo(cRect, float(self.pro_window.frame.default_properties["Start angle"]),
                           float(self.pro_window.frame.default_properties["Angle length"]))

            elif self.diagramType == self.Rectangle:
                path.addRect(cRect)

            elif self.diagramType == self.PolygonStim:

                hRatio = (x - x0) / cWidth
                vRatio = (y - y0) / cHeight

                if self.keep_resize:
                    if hRatio > vRatio:
                        vRatio = hRatio
                    else:
                        hRatio = vRatio

                for iVertex in range(len(self.polygon())):
                    cX = self.polygon().value(iVertex).x() * hRatio
                    cY = self.polygon().value(iVertex).y() * vRatio

                    if iVertex == 0:
                        path.moveTo(cX, cY)
                    else:
                        path.lineTo(cX, cY)


            else:
                raise Exception("diagramType should be of 'Arc','rectangle', or 'circle' !!")

            self.mPolygon = path.toFillPolygon()
            self.setPolygon(self.mPolygon)
            self.update()

            cBoundRect = self.polygon().boundingRect()
            self.center = cBoundRect.center()

            # print(f"scenePos: {self.scenePos().x()},{self.scenePos().y()}")

            self.getProperties()
            self.pro_window.frame.setProperties(self.default_properties)

        else:
            super(DiaItem, self).mouseMoveEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.AltModifier:
            self.arbitrary_resize = True
            self.setCursor(Qt.SizeAllCursor)

        elif mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.ShiftModifier:
            self.keep_resize = True
            self.setCursor(Qt.SizeAllCursor)

        else:
            super(DiaItem, self).mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.flag1 = False  # what does this for ????
        self.resizingFlag = False

        self.arbitrary_resize = False
        self.keep_resize = False
        super(DiaItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        self.getProperties()

        self.pro_window.frame.setProperties(self.default_properties)
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttributes(self.attributes)
        self.pro_window.show()

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def image(self):
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.mPolygon)
        return pixmap

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self.contextMenu.exec_(event.screenPos())

    def setPolygonFillColor(self):
        rgbValue = Func.isRGBStr(self.ItemColor)
        if rgbValue:
            self.setBrush(QColor(int(rgbValue[0]), int(rgbValue[1]), int(rgbValue[2]) ))
        else:
            self.setBrush(QColor(self.ItemColor))

    def setOutlineColorAndWidth(self):
        rgbValue = Func.isRGBStr(self.LineColor)

        pen = self.pen()
        pen.setWidth(self.LineWidth)

        if rgbValue:
            pen.setColor(QColor(int(rgbValue[0]), int(rgbValue[1]), int(rgbValue[2]) ))
        else:
            pen.setColor(QColor(self.LineColor))

        self.setPen(pen)


    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的deafult_properties
        self.pro_window.frame.loadSetting()

    def apply(self):

        self.pro_window.frame.getInfo()
        cx = int(self.pro_window.frame.default_properties["Center X"])
        cy = int(self.pro_window.frame.default_properties["Center Y"])

        self.ItemColor = self.pro_window.frame.default_properties["Fill color"]
        self.LineColor = self.pro_window.frame.default_properties["Border color"]
        self.LineWidth = int(self.pro_window.frame.default_properties["Border width"])

        self.setPolygonFillColor()
        self.setOutlineColorAndWidth()

        path = QPainterPath()

        if self.diagramType == self.Circle:
            rect = QRectF(-int(self.pro_window.frame.default_properties["Width"]) / 2,
                          -int(self.pro_window.frame.default_properties["Height"]) / 2,
                          int(self.pro_window.frame.default_properties["Width"]),
                          int(self.pro_window.frame.default_properties["Height"]))
            path.addEllipse(rect)

        elif self.diagramType == self.Arc:
            rect = QRectF(-int(self.pro_window.frame.default_properties["Width"]) / 2,
                          -int(self.pro_window.frame.default_properties["Height"]) / 2,
                          int(self.pro_window.frame.default_properties["Width"]),
                          int(self.pro_window.frame.default_properties["Height"]))

            path.arcTo(rect, float(self.pro_window.frame.default_properties["Start angle"]),
                       float(self.pro_window.frame.default_properties["Angle length"]))

        elif self.diagramType == self.Rectangle:
            rect = QRectF(-int(self.pro_window.frame.default_properties["Width"]) / 2,
                          -int(self.pro_window.frame.default_properties["Height"]) / 2,
                          int(self.pro_window.frame.default_properties["Width"]),
                          int(self.pro_window.frame.default_properties["Height"]))
            path.addRect(rect)

        elif self.diagramType == self.Line:
            path.moveTo(int(self.pro_window.frame.default_properties["P1 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P1 Y"]) - cy)
            path.lineTo(int(self.pro_window.frame.default_properties["P2 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P2 Y"]) - cy)

        elif self.diagramType == self.PolygonStim:
            verticesXY = self.pro_window.frame.default_properties["Point"]
            # added by yang to plot the m-polygon
            for iVertex in range(len(verticesXY)):
                if iVertex == 0:
                    path.moveTo(int(verticesXY[iVertex][0]) - cx, int(verticesXY[iVertex][1]) - cy)
                else:
                    path.lineTo(int(verticesXY[iVertex][0]) - cx, int(verticesXY[iVertex][1]) - cy)
            path.lineTo(int(verticesXY[0][0]) - cx, int(verticesXY[0][1]) - cy)

        self.setPos(QPoint(int(self.pro_window.frame.default_properties["Center X"]),
                           int(self.pro_window.frame.default_properties["Center Y"])))

        self.mPolygon = path.toFillPolygon()
        self.setPolygon(self.mPolygon)
        self.update()


    def getProperties(self):
        item_center_x = int(self.scenePos().x())
        item_center_y = int(self.scenePos().y())
        # print(f"cx: {item_center_x},{item_center_y}")
        self.default_properties["Center X"] = str(item_center_x)
        self.default_properties["Center Y"] = str(item_center_y)

        if self.diagramType == self.Line:
            self.default_properties["P1 X"] = str(int(self.p1.x()) + item_center_x)
            self.default_properties["P1 Y"] = str(int(self.p1.y()) + item_center_y)
            self.default_properties["P2 X"] = str(int(self.p2.x()) + item_center_x)
            self.default_properties["P2 Y"] = str(int(self.p2.y()) + item_center_y)

        elif self.diagramType == self.Rectangle:
            self.default_properties["Height"] = str(int(self.polygon().boundingRect().height()))
            self.default_properties["Width"] = str(int(self.polygon().boundingRect().width()))
        elif self.diagramType == self.Arc:
            self.default_properties["Height"] = str(int(self.polygon().boundingRect().height()))
            self.default_properties["Width"] = str(int(self.polygon().boundingRect().width()))

            self.default_properties["Start angle"] = self.pro_window.frame.default_properties["Start angle"]
            self.default_properties["Angle length"] = self.pro_window.frame.default_properties["Angle length"]

        elif self.diagramType == self.Circle:
            self.default_properties["Height"] = str(int(self.polygon().boundingRect().height()))
            self.default_properties["Width"] = str(int(self.polygon().boundingRect().width()))

        elif self.diagramType == self.PolygonStim:
            verticesXY = []
            for iVertex in range(len(self.polygon()) - 1):
                verticesXY.append([str(int(self.polygon()[iVertex].x()) + item_center_x),
                                   str(int(self.polygon()[iVertex].y()) + item_center_y)])

            self.default_properties["Point"] = verticesXY

        self.default_properties["Border color"] = self.LineColor
        self.default_properties["Border width"] = str(self.LineWidth)
        self.default_properties["Fill color"]   = self.ItemColor
        self.default_properties["z"]            = self.zValue()

        return self.default_properties


    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.frame.setProperties(self.default_properties)
            self.apply()

    def clone(self):
        if self.diagramType == self.Line:
            item = DiaItem(self.diagramType, self.contextMenu, self.attributes, self.p1, self.p2)
        else:
            item = DiaItem(self.diagramType, self.contextMenu, self.attributes)
        item.setPolygon(self.polygon())
        item.setLineWidth(self.LineWidth)
        item.setLineColor(self.LineColor)
        item.setItemColor(self.ItemColor)
        item.setBrush(QColor(self.ItemColor))
        item.setPen(self.pen())

        return item

class Scene(QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem = range(4)

    itemInserted = pyqtSignal(DiaItem)
    textInserted = pyqtSignal(QGraphicsTextItem)
    itemSelected = pyqtSignal(QGraphicsItem)
    pixitemInserted = pyqtSignal(QGraphicsPixmapItem)
    DitemSelected = pyqtSignal(dict)

    def __init__(self, itemMenu, attributes, parent=None):
        super(Scene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.myItemType = DiaItem.PolygonStim
        self.attributes = attributes
        self.line = None
        self.textItem = None
        self.myItemColor = Qt.white
        self.myTextColor = Qt.black
        self.myLineColor = Qt.black
        self.myFont = QFont()
        self.myLineWidth = 1

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            # 添加图形
            if self.myMode == self.InsertItem:
                if self.myItemType < 4:
                    # 参数：图形的形状，右键菜单
                    item = DiaItem(self.myItemType, self.myItemMenu, self.attributes)
                    pen = item.pen()
                    pen.setColor(self.myLineColor)
                    pen.setWidth(self.myLineWidth)
                    item.setBrush(self.myItemColor)
                    item.setPen(pen)
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self.itemInserted.emit(item)
                    self.update()
                # 添加图片
                else:
                    item = PixItem(self.myItemType, self.myItemMenu, self.attributes)
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self.pixitemInserted.emit(item)
                    self.update()
            elif self.myMode == self.InsertText:
                textItem = DiagramTextItem()
                textItem.setFont(self.myFont)
                textItem.setPlainText('Text')
                textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
                textItem.setZValue(1000.0)  # a possible reason why text is always on the front
                textItem.lostFocus.connect(self.editorLostFocus)
                textItem.selectedChange.connect(self.itemSelected)
                self.addItem(textItem)
                textItem.setDefaultTextColor(self.myTextColor)
                textItem.setPos(event.scenePos())
                self.textInserted.emit(textItem)

            action = Qt.MoveAction
            event.setDropAction(action)
            event.accept()
        else:
            event.ignore()

    def setLineColor(self, color):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            pen = item.pen()
            pen.setColor(color)
            item.setPen(pen)
            item.setLineColor(color.name())

    def setLineWidth(self, size):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            pen = item.pen()
            pen.setWidth(size)
            item.setPen(pen)
            item.setLineWidth(size)
            self.update()

    def setTextColor(self, color):
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(color)

    def setItemColor(self, color):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            item.setBrush(color)
            item.setItemColor(color.name())

    def setFont(self, font):
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setFont(font)

    def setMode(self, mode):
        self.myMode = mode

    def setItemType(self, type):
        self.myItemType = type

    def editorLostFocus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        # BUG
        # if item.toPlainText():
        if not item.toPlainText():
            self.removeItem(item)
            item.deleteLater()

    def mousePressEvent(self, mouseEvent):
        d = {'itemcolor': 'white',
             'linecolor': 'black',
             'linewidth': 1}
        if self.selectedItems() and self.isItemChange(DiaItem):
            it = self.selectedItems()[0]
            d = {'itemcolor': it.ItemColor,
                 'linecolor': it.LineColor,
                 'linewidth': it.LineWidth}
            self.DitemSelected.emit(d)

        if (mouseEvent.button() != Qt.LeftButton):
            return

        if self.myMode == self.InsertLine:
            self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(),
                                                 mouseEvent.scenePos()))
            self.line.setPen(QPen(self.myLineColor, 2))
            self.addItem(self.line)

        self.DitemSelected.emit(d)
        super(Scene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.InsertLine and self.line:
            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            self.update()
            super(Scene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.myMode == self.InsertLine:
            p1 = self.line.line().p1()
            p2 = self.line.line().p2()
            p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
            p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
            center = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
            item = DiaItem(DiaItem.Line, self.myItemMenu, self.attributes, p3, p4)
            self.addItem(item)
            item.setPos(center)
            self.update()
            self.removeItem(self.line)
            self.line = None

        self.line = None
        super(Scene, self).mouseReleaseEvent(mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False
"""

class Slider(QMainWindow):
    propertiesChange = pyqtSignal(str)
    InsertTextButton = 10

    def __init__(self, widget_id):
        super(Slider, self).__init__()
        self.widget_id = widget_id
        self.current_wid = widget_id
        self.attributes = []
        try:
            self.attributes = Func.getAttributes(self.widget_id)
        except KeyError:
            # condition下的slider在此出错
            pass

        self.createActions()
        self.createMenus()
        self.createToolBox()

        self.scene = Scene(self.itemMenu, self.attributes)

        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.pixItemInserted.connect(self.pixitemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.itemSelected.connect(self.itemSelected)
        self.scene.DitemSelected.connect(self.DitemSelected)

        self.createToolbars()

        layout = QHBoxLayout()
        layout.addWidget(self.toolBox)
        self.view = QGraphicsView(self.scene)
        scr_Rect = QDesktopWidget().screenGeometry()

        print(f"screen: {scr_Rect}")

        self.scene.setSceneRect(0, 0, scr_Rect.width(), scr_Rect.height())
        self.view.fitInView(0,0, scr_Rect.width()/2,scr_Rect.height()/2, Qt.KeepAspectRatio)

        layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Slider")

        self.pro_window = SliderProperty()
        self.setAttributes(self.attributes)
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def getProperties(self):
        return {'none': 'none'}

    def getHiddenAttribute(self):
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt": 0
        }
        return hidden_attr

    def DitemSelected(self, d):
        self.fillColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"), QColor(d['itemcolor'])))
        self.lineColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"), QColor(d['linecolor'])))
        self.lineWidthCombo.setCurrentText(str(d['linewidth']))

    # 左边工具栏按钮事件
    def buttonGroupPressed(self, id):
        self.pointerTypeGroup.button(3).setChecked(False)
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)

        if id == self.InsertTextButton:
            self.scene.setMode(Scene.InsertText)
        else:
            self.scene.setItemType(id)
            self.scene.setMode(Scene.InsertItem)

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if item.zValue() >= zValue and (isinstance(item, DiaItem) or isinstance(item, PixItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and (isinstance(item, DiaItem) or isinstance(item, PixItem))):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.pointerTypeGroup.button(Scene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def pixitemInserted(self, item):
        self.pointerTypeGroup.button(Scene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def textInserted(self, item):
        self.buttonGroup.button(self.InsertTextButton).setChecked(False)
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def currentFontChanged(self, font):
        self.handleFontChange()

    def fontSizeChanged(self, font):
        self.handleFontChange()

    def textColorChanged(self):
        self.textAction = self.sender()
        if self.textAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fontColorToolButton.setIcon(
                    self.createColorToolButtonIcon(Func.getImage("textpointer.png"), color))
                self.scene.setTextColor(color)
        else:
            self.fontColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("textpointer.png"),
                                               QColor(self.textAction.data())))
            self.textButtonTriggered()

    def itemColorChanged(self):
        self.fillAction = self.sender()
        if self.fillAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fillColorToolButton.setIcon(
                    self.createColorToolButtonIcon(Func.getImage("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fillColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("floodfill.png"),
                                               QColor(self.fillAction.data())))
            self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        if self.lineAction.data() == 'More..':
            color = QColorDialog.getColor()
            self.lineColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.lineColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage('linecolor.png'),
                                               QColor(self.lineAction.data())))
            self.lineButtonTriggered()

    def lineWidthChanged(self):
        self.scene.setLineWidth(int(self.lineWidthCombo.currentText()))

    def backChanged(self):
        self.backAction = self.sender()
        if self.backAction.data() == '1':
            self.backToolButton.setIcon(QIcon(Func.getImage("background1.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background1.png"))))
        elif self.backAction.data() == '2':
            self.backToolButton.setIcon(QIcon(Func.getImage("background2.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background2.png"))))
        elif self.backAction.data() == '3':
            self.backToolButton.setIcon(QIcon(Func.getImage("background3.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background3.png"))))
        elif self.backAction.data() == '4':
            self.backToolButton.setIcon(QIcon(Func.getImage("background4.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background4.png"))))
        self.scene.update()
        self.view.update()

    def textButtonTriggered(self):
        # print(2)
        self.scene.setTextColor(QColor(self.textAction.data()))

    def fillButtonTriggered(self):
        self.scene.setItemColor(QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QColor(self.lineAction.data()))

    def handleFontChange(self):
        font = self.fontCombo.currentFont()
        # BUG
        # font.setPointSize(self.fontSizeCombo.currentText().toInt()[0])
        font.setPointSize(int(self.fontSizeCombo.currentText()))
        if self.boldAction.isChecked():
            font.setWeight(QFont.Bold)
        else:
            font.setWeight(QFont.Normal)
        font.setItalic(self.italicAction.isChecked())
        font.setUnderline(self.underlineAction.isChecked())

        self.scene.setFont(font)

    def itemSelected(self, item):
        font = item.font()
        color = item.defaultTextColor()
        self.fontCombo.setCurrentFont(font)
        self.fontSizeCombo.setEditText(str(font.pointSize()))
        self.boldAction.setChecked(font.weight() == QFont.Bold)
        self.italicAction.setChecked(font.italic())
        self.underlineAction.setChecked(font.underline())

    def about(self):
        QMessageBox.about(self, "About Diagram Scene",
                          "The <b>Diagram Scene</b> example shows use of the graphics framework.")

    def openPro(self):
        try:
            self.attributes = Func.getAttributes(self.widget_id)
            self.setAttributes(self.attributes)
        except KeyError as e:
            # condition下的slider在这里出错
            pass
        screen_devices = Func.getScreen()
        self.pro_window.general.setScreen(screen_devices)

        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        try:
            self.pro_window.setAttributes(format_attributes)
        except Exception as e:
            print(e)

    # 视图左边的工具栏
    def createToolBox(self):
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(False)
        self.buttonGroup.buttonPressed[int].connect(self.buttonGroupPressed)

        layout = QGridLayout()
        layout.addWidget(self.createCellWidget("Polygon", DiaItem.PolygonStim), 0, 0)
        layout.addWidget(self.createCellWidget("Circle", DiaItem.Circle), 1, 0)
        layout.addWidget(self.createCellWidget("Arc", DiaItem.Arc), 2, 0)
        layout.addWidget(self.createCellWidget("Rectangle", DiaItem.Rectangle), 3, 0)

        # layout.addWidget(self.createCellWidget("Conditional", DiagramItem.Conditional), 0, 0)
        # layout.addWidget(self.createCellWidget("Polygon", DiagramItem.Step), 2, 0)
        # layout.addWidget(self.createCellWidget("Circle", DiagramItem.Circle), 2, 0)
        # layout.addWidget(self.createCellWidget("Input/Output", DiagramItem.Io), 3, 0)

        textButton = Button()
        self.buttonGroup.addButton(textButton, self.InsertTextButton)
        textButton.setIcon(QIcon(QPixmap(Func.getImage("textpointer.png")).scaled(50, 50)))
        textButton.setIconSize(QSize(50, 50))
        videoButton = Button()
        self.buttonGroup.addButton(videoButton, PixItem.Video)
        videoButton.setIcon(QIcon(QPixmap(Func.getImage("video.png")).scaled(50, 50)))
        videoButton.setIconSize(QSize(50, 50))
        pictureButton = Button()
        self.buttonGroup.addButton(pictureButton, PixItem.Picture)
        pictureButton.setIcon(QIcon(QPixmap(Func.getImage("Picture.png")).scaled(50, 50)))
        pictureButton.setIconSize(QSize(50, 50))
        soundButton = Button()
        self.buttonGroup.addButton(soundButton, PixItem.Sound)
        soundButton.setIcon(QIcon(QPixmap(Func.getImage("music.png")).scaled(50, 50)))
        soundButton.setIconSize(QSize(50, 50))
        snowButton = Button()
        self.buttonGroup.addButton(snowButton, PixItem.Snow)
        snowButton.setIcon(QIcon(QPixmap(Func.getImage("snow.png")).scaled(50, 50)))
        snowButton.setIconSize(QSize(50, 50))
        gaborButton = Button()
        self.buttonGroup.addButton(gaborButton, PixItem.Gabor)
        gaborButton.setIcon(QIcon(QPixmap(Func.getImage("Gabor.png")).scaled(50, 50)))
        gaborButton.setIconSize(QSize(50, 50))

        textLayout = QGridLayout()
        videoLayout = QGridLayout()
        pictureLayout = QGridLayout()
        soundLayout = QGridLayout()
        snowLayout = QGridLayout()
        gaborLayout = QGridLayout()

        textLayout.addWidget(textButton, 0, 0, Qt.AlignHCenter)
        textLayout.addWidget(QLabel("Text"), 1, 0, Qt.AlignCenter)
        videoLayout.addWidget(videoButton, 0, 0, Qt.AlignHCenter)
        videoLayout.addWidget(QLabel("Video"), 1, 0, Qt.AlignCenter)
        pictureLayout.addWidget(pictureButton, 0, 0, Qt.AlignHCenter)
        pictureLayout.addWidget(QLabel("Picture"), 1, 0, Qt.AlignCenter)
        soundLayout.addWidget(soundButton, 0, 0, Qt.AlignHCenter)
        soundLayout.addWidget(QLabel("Sound"), 1, 0, Qt.AlignCenter)
        snowLayout.addWidget(snowButton, 0, 0, Qt.AlignHCenter)
        snowLayout.addWidget(QLabel("Snow"), 1, 0, Qt.AlignCenter)
        gaborLayout.addWidget(gaborButton, 0, 0, Qt.AlignHCenter)
        gaborLayout.addWidget(QLabel("Gabor"), 1, 0, Qt.AlignCenter)

        textWidget = QWidget()
        textWidget.setLayout(textLayout)
        videoWidget = QWidget()
        videoWidget.setLayout(videoLayout)
        pictureWidget = QWidget()
        pictureWidget.setLayout(pictureLayout)
        soundWidget = QWidget()
        soundWidget.setLayout(soundLayout)
        snowWidget = QWidget()
        snowWidget.setLayout(snowLayout)
        gaborWidget = QWidget()
        gaborWidget.setLayout(gaborLayout)

        layout.setRowStretch(5, 10)

        itemWidget = QWidget()
        itemWidget.setLayout(layout)

        # self.backgroundButtonGroup = QButtonGroup()
        # self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

        backgroundLayout = QGridLayout()
        backgroundLayout.addWidget(textWidget, 0, 0)
        backgroundLayout.addWidget(videoWidget, 1, 0)
        backgroundLayout.addWidget(pictureWidget, 2, 0)
        backgroundLayout.addWidget(soundWidget, 3, 0)
        backgroundLayout.addWidget(snowWidget, 4, 0)
        backgroundLayout.addWidget(gaborWidget, 5, 0)

        backgroundLayout.setRowStretch(6, 10)

        backgroundWidget = QWidget()
        backgroundWidget.setLayout(backgroundLayout)

        self.toolBox = QToolBox()
        self.toolBox.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))
        self.toolBox.setMinimumWidth(itemWidget.sizeHint().width())
        self.toolBox.addItem(itemWidget, "Basic Geometries")
        self.toolBox.addItem(backgroundWidget, "Stimuli")

    def createActions(self):
        self.toFrontAction = QAction(QIcon(Func.getImage("sendtoback.png")), "Bringto & Front", self, shortcut="Ctrl+F",
                                     statusTip="Bring item to front", triggered=self.bringToFront)

        self.sendBackAction = QAction(QIcon(Func.getImage("bringtofront.png")), "Sendto & Back", self,
                                      shortcut="Ctrl+B", statusTip="Send item to back", triggered=self.sendToBack)

        self.deleteAction = QAction(QIcon(Func.getImage("delete.png")), "&Delete", self, shortcut="Ctrl+Delete",
                                    statusTip="Delete item from diagram", triggered=self.deleteItem)

        self.exitAction = QAction("E&xit", self, shortcut="Ctrl+X",
                                  statusTip="Quit Scenediagram example", triggered=self.close)

        self.boldAction = QAction(QIcon(Func.getImage("bold.png")),
                                  "Bold", self, checkable=True, shortcut="Ctrl+B",
                                  triggered=self.handleFontChange)

        self.italicAction = QAction(QIcon(Func.getImage("italic.png")),
                                    "Italic", self, checkable=True, shortcut="Ctrl+I",
                                    triggered=self.handleFontChange)

        self.underlineAction = QAction(
            QIcon(Func.getImage("underline.png")), "Underline", self,
            checkable=True, shortcut="Ctrl+U",
            triggered=self.handleFontChange)

        self.aboutAction = QAction("A&bout", self, shortcut="Ctrl+B",
                                   triggered=self.about)
        self.open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self, triggered=self.openPro)

        # 工具栏删除，顶层底层

    def createMenus(self):
        self.itemMenu = QMenu()
        self.itemMenu.addAction(self.deleteAction)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.toFrontAction)
        self.itemMenu.addAction(self.sendBackAction)

    # 上方工具栏
    def createToolbars(self):
        self.settingToolBar = self.addToolBar('Setting')
        self.settingToolBar.addAction(self.open_pro)

        # self.editToolBar = self.addToolBar("Edit")
        self.settingToolBar.addAction(self.deleteAction)
        self.settingToolBar.addAction(self.toFrontAction)
        self.settingToolBar.addAction(self.sendBackAction)

        self.fontCombo = QFontComboBox()
        self.fontCombo.currentFontChanged.connect(self.currentFontChanged)

        # 字体大小
        self.fontSizeCombo = QComboBox()
        self.fontSizeCombo.setEditable(True)
        for iFontSize in range(8, 30, 2):
            self.fontSizeCombo.addItem(str(iFontSize))

        validator = QIntValidator(2, 64, self)

        self.fontSizeCombo.setValidator(validator)
        self.fontSizeCombo.currentIndexChanged.connect(self.fontSizeChanged)

        # 边框宽度
        self.lineWidthCombo = QComboBox()
        self.lineWidthCombo.setEditable(True)
        for iLineWidth in range(2, 20, 2):
            self.lineWidthCombo.addItem(str(iLineWidth))

        validator = QIntValidator(0, 20, self)
        self.lineWidthCombo.setValidator(validator)
        self.lineWidthCombo.currentIndexChanged.connect(self.lineWidthChanged)

        # 字体颜色
        self.fontColorToolButton = QToolButton()
        self.fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.fontColorToolButton.setMenu(
            self.createColorMenu(self.textColorChanged, Qt.black))
        self.textAction = self.fontColorToolButton.menu().defaultAction()
        self.fontColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("textpointer.png"),
                                           Qt.black))
        # self.fontColorToolButton.setAutoFillBackground(True)
        try:
            self.fontColorToolButton.clicked.connect(self.textButtonTriggered)
        except Exception as e:
            print(e)

        self.fillColorToolButton = QToolButton()
        self.fillColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.fillColorToolButton.setMenu(
            self.createColorMenu(self.itemColorChanged, Qt.white))
        self.fillAction = self.fillColorToolButton.menu().defaultAction()
        self.fillColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"), Qt.white))
        self.fillColorToolButton.clicked.connect(self.fillButtonTriggered)

        self.lineColorToolButton = QToolButton()
        self.lineColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.lineColorToolButton.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.lineAction = self.lineColorToolButton.menu().defaultAction()
        self.lineColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"), Qt.black))
        self.lineColorToolButton.clicked.connect(self.lineButtonTriggered)

        # ?
        # self.textToolBar = self.addToolBar("Font")
        self.settingToolBar.addWidget(self.fontCombo)
        self.settingToolBar.addWidget(self.fontSizeCombo)
        self.settingToolBar.addAction(self.boldAction)
        self.settingToolBar.addAction(self.italicAction)
        self.settingToolBar.addAction(self.underlineAction)

        # self.colorToolBar = self.addToolBar("Color")
        self.settingToolBar.addWidget(self.fontColorToolButton)
        self.settingToolBar.addWidget(self.fillColorToolButton)
        self.settingToolBar.addWidget(self.lineColorToolButton)
        self.settingToolBar.addWidget(self.lineWidthCombo)

        pointerButton = QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QIcon(Func.getImage("pointer.png")))
        linePointerButton = QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QIcon(Func.getImage("linepointer.png")))

        self.pointerTypeGroup = QButtonGroup()
        self.pointerTypeGroup.addButton(pointerButton, Scene.MoveItem)
        self.pointerTypeGroup.addButton(linePointerButton, Scene.InsertLine)
        self.pointerTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        # self.pointerToolbar = self.addToolBar("Pointer type")
        self.settingToolBar.addWidget(pointerButton)
        self.settingToolBar.addWidget(linePointerButton)

        self.backToolButton = QToolButton()
        self.backToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.backToolButton.setMenu(
            self.createBackgroundMenu(self.backChanged))
        # self.fillAction = self.fillColorToolButton.menu().defaultAction()
        self.backToolButton.setIcon(QIcon(Func.getImage("background4.png")))
        self.backToolButton.clicked.connect(self.fillButtonTriggered)

        self.settingToolBar.addWidget(self.backToolButton)

        # 左边工具栏添加图形本文

    def createCellWidget(self, text, diagramType):
        item = DiaItem(diagramType, self.itemMenu)
        icon = QIcon(item.image())

        button = Button()
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setCheckable(True)
        self.buttonGroup.addButton(button, diagramType)

        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(text), 1, 0, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def createColorMenu(self, slot, defaultColor):
        colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

        colorMenu = QMenu(self)
        action1 = QAction('More..', self, triggered=slot)
        action1.setData('More..')
        for color, name in zip(colors, names):
            action = QAction(self.createColorIcon(color), name, self,
                             triggered=slot)
            action.setData(QColor(color))
            colorMenu.addAction(action)
            if color == defaultColor:
                colorMenu.setDefaultAction(action)
        colorMenu.addAction(action1)
        return colorMenu

    def createBackgroundMenu(self, slot):
        backMenu = QMenu(self)
        action1 = QAction(QIcon(Func.getImage("background1.png")), 'Blue Grid', self, triggered=slot)
        action2 = QAction(QIcon(Func.getImage("background2.png")), 'White Grid', self, triggered=slot)
        action3 = QAction(QIcon(Func.getImage("background3.png")), 'Gray Grid', self, triggered=slot)
        action4 = QAction(QIcon(Func.getImage("background4.png")), 'No Grid', self, triggered=slot)
        action1.setData('1')
        action2.setData('2')
        action3.setData('3')
        action4.setData('4')
        backMenu.setDefaultAction(action4)
        backMenu.addAction(action1)
        backMenu.addAction(action2)
        backMenu.addAction(action3)
        backMenu.addAction(action4)
        return backMenu

    def createColorToolButtonIcon(self, imageFile, color):
        pixmap = QPixmap(50, 80)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        image = QPixmap(imageFile)
        target = QRect(0, 0, 50, 60)
        source = QRect(0, 0, 42, 42)
        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()

        return QIcon(pixmap)

    def createColorIcon(self, color):
        pixmap = QPixmap(20, 20)
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 20, 20), color)
        painter.end()

        return QIcon(pixmap)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getinfo()
        # 发送信号
        # self.propertiesChange.emit(self.default_properties)

    # 设置输入输出设备
    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro_window.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro_window.duration.in_devices_dialog.addDevices(devices)

    def getinfo(self):
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def getInfo(self):
        self.all_properties = {'default_properties': self.pro_window.default_properties}
        for i in range(len(self.scene.items())):
            try:
                self.scene.items()[i].setProperties()
                self.all_properties[i + 1] = self.scene.items()[i].default_properties
            except Exception as e:
                print(e)

        return self.all_properties

    def restore(self, properties: dict):
        for d in properties:
            if d == 'default_properties':
                self.pro_window.setProperties(properties[d])
            else:
                dic = properties[d]
                if dic['name'] == 'text':
                    item = DiagramTextItem()
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    self.scene.addItem(item)
                    item.setPos(QPoint(dic['x_pos'], dic['y_pos']))
                elif dic['name'] < 4:
                    item = DiaItem(dic['name'], self.itemMenu, self.attributes)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                elif dic['name'] == 4:
                    p1 = QPointF(int(dic['P1 X']), int(dic['P1 Y']))
                    p2 = QPointF(int(dic['P2 X']), int(dic['P2 Y']))
                    p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
                    p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
                    item = DiaItem(dic['name'], self.itemMenu, self.attributes, p3, p4)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                else:
                    item = PixItem(dic['name'], self.itemMenu, self.attributes)
                    item.restore(dic)
                    self.scene.addItem(item)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(dic['x_pos'], dic['y_pos']))

    def clone(self, widget_id: str):
        """
        根据传入的widget_id，复制一个widget
        :param widget_id:
        :return:
        """
        slider = Slider(widget_id=widget_id)
        slider.pro_window.setProperties(self.pro_window.getInfo())
        for item in self.scene.items():
            item1 = item.clone()
            slider.scene.addItem(item1)
            item1.setPos(item.scenePos())
            slider.scene.update()
        return slider

    def changeWidgetId(self, new_widget_id: str):
        """
        修改widget的wid
        :param new_widget_id:
        :return:
        """
        self.widget_id = new_widget_id
