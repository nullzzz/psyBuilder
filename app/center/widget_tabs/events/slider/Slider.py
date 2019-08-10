from PyQt5.QtCore import (pyqtSignal, QLineF, QPointF, QRect, QRectF, QSize, QPoint, Qt, QByteArray, QDataStream,
                          QIODevice, QMimeData)
from PyQt5.QtGui import (QBrush, QColor, QFont, QIcon, QIntValidator, QPainter,
                         QPainterPath, QPen, QPixmap, QPolygonF, QDrag)
from PyQt5.QtWidgets import (QAction, QButtonGroup, QComboBox, QFontComboBox, QGraphicsItem,
                             QGraphicsLineItem, QGraphicsPolygonItem,
                             QGraphicsScene, QGraphicsTextItem, QGraphicsView, QGridLayout, QGraphicsPixmapItem,
                             QHBoxLayout, QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QToolBox, QToolButton,
                             QWidget, QPushButton, QColorDialog)

from app.center.widget_tabs.events.slider.SliderProperty import SliderProperty
from app.center.widget_tabs.events.slider.gabor import gaborProperty
from app.center.widget_tabs.events.slider.graph import Snow, makeGabor_bcl
from app.center.widget_tabs.events.slider.image import ImageProperty
from app.center.widget_tabs.events.slider.polygonitem import polygonProperty
from app.center.widget_tabs.events.slider.snow import snowProperty
from app.center.widget_tabs.events.slider.sound import SoundProperty
from app.center.widget_tabs.events.slider.viedeo import VideoProperty
from .text import TextTab2
from app.func import Func
from lib.psy_message_box import PsyMessageBox as QMessageBox
import numpy as np

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


class DiagramTextItem(QGraphicsTextItem):
    lostFocus      = pyqtSignal(QGraphicsTextItem)
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
        self.default_properties['size']   = self.font().pointSize()
        self.default_properties['B']      = self.font().bold()
        self.default_properties['I']      = self.font().italic()
        self.default_properties['U']      = self.font().underline()
        self.default_properties['color']  = self.defaultTextColor().name()
        self.default_properties['text']   = self.toPlainText()
        self.default_properties['z']      = self.zValue()
        self.default_properties['x_pos']  = self.scenePos().x()
        self.default_properties['y_pos']  = self.scenePos().y()

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


class DiagramPixmapItem(QGraphicsPixmapItem):
    Video, Picture, Sound, Snow, Gabor = 5, 6, 7, 8, 9

    def __init__(self, diagramType, contextMenu, attributes=None, parent=None):
        super(DiagramPixmapItem, self).__init__(parent)

        self.diagramType = diagramType
        self.contextMenu = contextMenu
        self.attributes  = attributes

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
            self.pro_window = gaborProperty()
            self.setPixmap(QPixmap(Func.getImage("Gabor.png")))

        else:
            self.pro_window = ImageProperty()
            self.setPixmap(QPixmap(Func.getImage("Picture.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.resizingFlag      = False
        self.resizing          = False
        self.keepRatioResizing = False

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
                self.resizing = True
                self.setCursor(Qt.SizeAllCursor)
            elif mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.ShiftModifier:
                self.keepRatioResizing = True
                self.setCursor(Qt.SizeAllCursor)
            else:
                super(DiagramPixmapItem, self).mousePressEvent(mouseEvent)
        else:
            super(DiagramPixmapItem, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()
        if self.diagramType > 7:
            self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
        if self.resizing:
            self.resizingFlag = True
        if self.keepRatioResizing:
            self.resizingFlag = True
            if x > y:
                x = y
            else:
                y = x
        if self.resizingFlag:
            if self.diagramType == self.Video:
                self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(x, y))
            elif self.diagramType == self.Sound:
                self.setPixmap(QPixmap(Func.getImage("music.png")).scaled(x, y))
            else:
                self.setPixmap(QPixmap(Func.getImage("Picture.png")).scaled(x, y))
            self.update()
        else:
            super(DiagramPixmapItem, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.resizing = False
        self.keepRatioResizing = False
        self.resizingFlag = False
        super(DiagramPixmapItem, self).mouseReleaseEvent(mouseEvent)

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
            **self.pro_window.default_properties
        }
        if self.diagramType == self.Snow:
            try:
                rgbValue = int(self.default_properties["Scale"])
                snow = Snow(int(int(self.default_properties["Height"]) / rgbValue),
                            int(int(self.default_properties["Width"]) / rgbValue))
                pix = QPixmap(Func.getImage("snow1.png"))
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

                rgbValue       = self.default_properties['bkColor'].split(',')
                sdx     = float(self.default_properties['SDx(pixels)'])
                sdy     = float(self.default_properties['SDy(pixels)'])
                width   = int(self.default_properties["Width"])
                height  = int(self.default_properties["Height"])
                bkColor = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))
                g       = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                  bkColor, width, height, sdx, sdy)
                pix = QPixmap(Func.getImage("gabor1.png"))
                pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
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
            **self.pro_window.default_properties
        }

    def setProperties(self):
        self.default_properties['x_pos'] = self.scenePos().x()
        self.default_properties['y_pos'] = self.scenePos().y()

    def restore(self, properties: dict):
        if properties:
            self.pro_window.setProperties(properties)
            if self.diagramType == self.Snow:
                try:
                    snow = Snow(int(properties["Width"]), int(properties["Height"]))
                    pix  = QPixmap(Func.getImage("snow.png"))
                    pix  = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
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
                    sdx         = float(self.default_properties['SDx(pixels)'])
                    sdy         = float(self.default_properties['SDy(pixels)'])
                    width       = int(self.default_properties["Width"])
                    height      = int(self.default_properties["Height"])
                    bkColor     = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))
                    g = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                      bkColor, width, height, sdx, sdy)
                    pix = QPixmap(Func.getImage("gabor1.png"))
                    pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
                    self.setPixmap(pix)
                    x = self.boundingRect().center().x()
                    y = self.boundingRect().center().y()
                    self.setTransformOriginPoint(x, y)
                    self.setRotation(int(properties["rotation"]))
                    self.update()
                except Exception as e:
                    print(e)

    def clone(self):
        new = DiagramPixmapItem(self.diagramType, self.contextMenu, self.attributes)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        new.setPixmap(self.pixmap())
        new.setZValue(self.zValue())

        return new


class DiagramItem(QGraphicsPolygonItem):
    PolygonStim, Arc, Circle, Rectangle, Line = range(5)

    def __init__(self, diagramType, contextMenu, attributes=None, p1=None, p2=None, parent=None, scene=None):
        super(DiagramItem, self).__init__()

        self.diagramType = diagramType
        self.contextMenu = contextMenu
        self.attributes  = attributes

        self.default_properties = {
            "name": self.diagramType,
            "Center X": "0",
            "Center Y": "0",
            "P1 X": "0",
            "P1 Y": "0",
            "P2 X": "0",
            "P2 Y": "0",
            "P3 X": "0",
            "P3 Y": "0",
            "P4 X": "0",
            "P4 Y": "0",
            "Point": [['0', '0'], ['0', '0'], ['0', '0']],# added by yang
            "Start angle": "0",
            "End angle": "0",
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
            self.myPolygon  = path.toFillPolygon()
            self.pro_window = polygonProperty('circle')

        #  rectange
        elif self.diagramType == self.Rectangle:
            path.addRect(QRectF(-100, -100, 200, 200))
            self.myPolygon  = path.toFillPolygon()
            self.pro_window = polygonProperty('arc')

        # arc
        elif self.diagramType == self.Arc:
            path.arcTo(QRectF(-100, -100, 200, 200),0, 270)
            self.myPolygon  = path.toFillPolygon()
            self.pro_window = polygonProperty('arc')

        # polygon
        elif self.diagramType == self.PolygonStim:
            #added by yang to plot the triangle
            nVertices  = 3
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
            self.myPolygon = path.toFillPolygon()
            self.pro_window = polygonProperty('polygonStim')

        elif self.diagramType == self.Line:
            path.moveTo(p1.x(), p1.y())
            path.lineTo(p2.x(), p2.y())
            self.myPolygon = path.toFillPolygon()
            self.pro_window = polygonProperty('line')

        else:
            pass
            # myPolygon = QPolygonF([
            #     QPointF(-120, -80), QPointF(-70, 80),
            #     QPointF(120, 80), QPointF(70, -80),
            #     QPointF(-120, -80)])
            #
            # path.addPolygon(myPolygon)
            # self.myPolygon = path.toFillPolygon()
            # self.pro_window = polygonProperty('arc')

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setPolygon(self.myPolygon)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.resizing          = False
        self.keepRatioResizing = False
        self.resizingFlag      = False
        # self.flag1 = False
        self.center    = QPointF(0, 0)
        self.ItemColor = 'white'
        self.LineColor = 'black'
        self.LineWidth = 1

    def setItemColor(self, color):
        self.ItemColor = color

    def setLineColor(self, color):
        self.LineColor = color

    def setLineWidth(self, width):
        self.LineWidth = width

    def boundingRect(self):
        return self.polygon().boundingRect().adjusted(-self.pen().width(), -self.pen().width(), self.pen().width(),
                                                      self.pen().width())

    def mouseMoveEvent(self, mouseEvent):
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()
        rect0 = self.polygon().boundingRect()
        self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
        # 非等比例
        if self.resizing and self.diagramType < 4:
            self.resizingFlag = True
        # 等比例
        if self.keepRatioResizing and self.diagramType < 4:
            self.resizingFlag = True
            cHeight = rect0.height()
            if cHeight < 5:
                cHeight = 5
            cWidth = rect0.width()
            if cWidth < 5:
                cWidth = 5
                
            ratio = cHeight / cWidth
            if (y - cHeight) / (x - cWidth) > ratio:
                y = ratio * (x - cWidth) + cHeight
            else:
                x = (y - cHeight) / ratio + cWidth
                
        if self.resizingFlag:
            if self.diagramType == self.Circle:
                path = QPainterPath()
                rect = QRectF(rect0.left(), rect0.top(), x - rect0.left(), y - rect0.top())
                path.addEllipse(rect)
                self.mPolygon = path.toFillPolygon()

            elif self.diagramType == self.Arc:
                path = QPainterPath()
                mPolygon = QPolygonF([QPointF(-100, (y + rect0.top()) / 2), QPointF((x + rect0.left()) / 2, y),
                                      QPointF(x, (y + rect0.top()) / 2), QPointF((x + rect0.left()) / 2, -100),
                                      QPointF(-100, (y + rect0.top()) / 2)])
                path.addPolygon(mPolygon)
                self.mPolygon = path.toFillPolygon()

            elif self.diagramType == self.PolygonStim:
                path = QPainterPath()
                rect = QRectF(rect0.left(), rect0.top(), x - rect0.left(), y - rect0.top())
                path.addRect(rect)
                self.mPolygon = path.toFillPolygon()

            else:
                path = QPainterPath()
                mPolygon = QPolygonF([QPointF(-120, -80), QPointF(-120 + (5 * y + 400) / 16, y),
                                      QPointF(x, y), QPointF(x - (5 * y + 400) / 16, -80),
                                      QPointF(-120, -80)])
                path.addPolygon(mPolygon)
                self.mPolygon = path.toFillPolygon()

            self.setPolygon(self.mPolygon)
            self.update()
            self.center = self.polygon().boundingRect().center()
        else:
            super(DiagramItem, self).mouseMoveEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.AltModifier:
            self.resizing = True
            self.setCursor(Qt.SizeAllCursor)

        elif mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.ShiftModifier:
            self.keepRatioResizing = True
            self.setCursor(Qt.SizeAllCursor)

        else:
            super(DiagramItem, self).mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.flag1        = False # what does this for ????
        self.resizingFlag = False

        self.resizing          = False
        self.keepRatioResizing = False
        super(DiagramItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        if self.diagramType != self.Line:
            self.setProperties()

            self.pro_window.frame.setProperties(self.default_properties)
            self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setAttributes(self.attributes)
            self.pro_window.show()

        elif self.diagramType == self.Line:
            self.setProperties()
            self.pro_window.frame.setProperties(self.default_properties)
            self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setAttributes(self.attributes)
            self.pro_window.show()

        else:
            return

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def image(self):
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.myPolygon)
        return pixmap

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
        # 加载之前的deafult_properties
        self.pro_window.frame.loadSetting()

    def apply(self):
        cx0 = int(self.pro_window.frame.default_properties["Center X"])
        cy0 = int(self.pro_window.frame.default_properties["Center Y"])
        self.pro_window.frame.getInfo()
        cx = int(self.pro_window.frame.default_properties["Center X"])
        cy = int(self.pro_window.frame.default_properties["Center Y"])
        dx = cx - cx0
        dy = cy - cy0
        self.ItemColor = self.pro_window.frame.default_properties["Fill color"]
        self.LineColor = self.pro_window.frame.default_properties["Border color"]
        self.LineWidth = int(self.pro_window.frame.default_properties["Border width"])
        self.setBrush(QColor(self.ItemColor))
        pen = self.pen()
        pen.setWidth(self.LineWidth)
        pen.setColor(QColor(self.LineColor))
        self.setPen(pen)

        if self.diagramType == self.Circle:
            path = QPainterPath()
            rect = QRectF(-int(self.pro_window.frame.default_properties["Width"]) / 2,
                          -int(self.pro_window.frame.default_properties["Height"]) / 2,
                          int(self.pro_window.frame.default_properties["Width"]),
                          int(self.pro_window.frame.default_properties["Height"]))
            path.addEllipse(rect)

        elif self.diagramType == self.Line:
            path = QPainterPath()
            path.moveTo(int(self.pro_window.frame.default_properties["P1 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P1 Y"]) - cy)
            path.lineTo(int(self.pro_window.frame.default_properties["P2 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P2 Y"]) - cy)

        else:
            path = QPainterPath()

            verticesXY = self.pro_window.frame.default_properties["Point"]

            # added by yang to plot the m-polygon
            for iVertex in range(len(verticesXY)):
                if iVertex == 0:
                    path.moveTo(int(verticesXY[iVertex][0]) - cx + dx, int(verticesXY[iVertex][1]) - cy + dy)
                else:
                    path.lineTo(int(verticesXY[iVertex][0]) - cx + dx, int(verticesXY[iVertex][1])  - cy + dy)
            path.lineTo(int(verticesXY[0][0]) - cx + dx, int(verticesXY[0][1])  - cy + dy)


        self.setPos(QPoint(int(self.pro_window.frame.default_properties["Center X"]),
                           int(self.pro_window.frame.default_properties["Center Y"])))

        self.mPolygon = path.toFillPolygon()
        self.setPolygon(self.mPolygon)
        self.update()

    def setProperties(self):
        x = int(self.scenePos().x())
        y = int(self.scenePos().y())

        self.default_properties["Center X"] = str(int(self.scenePos().x()))
        self.default_properties["Center Y"] = str(int(self.scenePos().y()))

        if self.diagramType == self.Line:

            self.default_properties["P1 X"] = str(int(self.polygon()[0].x()) + x)
            self.default_properties["P1 Y"] = str(int(self.polygon()[0].y()) + y)
            self.default_properties["P2 X"] = str(int(self.polygon()[1].x()) + x)
            self.default_properties["P2 Y"] = str(int(self.polygon()[1].y()) + y)

        elif self.diagramType == self.Circle:
            self.default_properties["Height"]   = str(int(self.polygon().boundingRect().height()))
            self.default_properties["Width"]    = str(int(self.polygon().boundingRect().width()))

            self.default_properties["Start angle"] = '0'
            self.default_properties["End angle"]   = '360'

        elif self.diagramType == self.PolygonStim:
            verticesXY = []
            for iVertex in range(len(self.polygon())-1):
                verticesXY.append([str(int(self.polygon()[iVertex].x()) + x),str(int(self.polygon()[iVertex].y()) + y)])

            self.default_properties["Point"] = verticesXY
            # self.default_properties["Start angle"] = '0'
            # self.default_properties["End angle"] = '360'


        self.default_properties["Border color"] = self.LineColor
        self.default_properties["Border width"] = str(self.LineWidth)
        self.default_properties["Fill color"]   = self.ItemColor
        self.default_properties["z"]            = self.zValue()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.frame.setProperties(self.default_properties)
            self.apply()

    def clone(self):
        if self.diagramType == self.Line:
            item = DiagramItem(self.diagramType, self.contextMenu, self.attributes, self.p1, self.p2)
        else:
            item = DiagramItem(self.diagramType, self.contextMenu, self.attributes)
        item.setPolygon(self.polygon())
        item.setLineWidth(self.LineWidth)
        item.setLineColor(self.LineColor)
        item.setItemColor(self.ItemColor)
        item.setBrush(QColor(self.ItemColor))
        item.setPen(self.pen())

        return item


class DiagramScene(QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem = range(4)

    itemInserted    = pyqtSignal(DiagramItem)
    textInserted    = pyqtSignal(QGraphicsTextItem)
    itemSelected    = pyqtSignal(QGraphicsItem)
    pixitemInserted = pyqtSignal(QGraphicsPixmapItem)
    DitemSelected   = pyqtSignal(dict)

    def __init__(self, itemMenu, attributes, parent=None):
        super(DiagramScene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.myItemType = DiagramItem.PolygonStim
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
                    item = DiagramItem(self.myItemType, self.myItemMenu, self.attributes)
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
                    item = DiagramPixmapItem(self.myItemType, self.myItemMenu, self.attributes)
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self.pixitemInserted.emit(item)
                    self.update()
            elif self.myMode == self.InsertText:
                textItem = DiagramTextItem()
                textItem.setFont(self.myFont)
                textItem.setPlainText('Text')
                textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
                textItem.setZValue(1000.0)# a possible reason why text is always on the front
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
        if self.isItemChange(DiagramItem):
            item = self.selectedItems()[0]
            pen = item.pen()
            pen.setColor(color)
            item.setPen(pen)
            item.setLineColor(color.name())

    def setLineWidth(self, size):
        if self.isItemChange(DiagramItem):
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
        if self.isItemChange(DiagramItem):
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
        if self.selectedItems() and self.isItemChange(DiagramItem):
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
        super(DiagramScene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.InsertLine and self.line:
            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            self.update()
            super(DiagramScene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.myMode == self.InsertLine:
            p1 = self.line.line().p1()
            p2 = self.line.line().p2()
            p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
            p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
            center = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
            item   = DiagramItem(DiagramItem.Line, self.myItemMenu, self.attributes, p3, p4)
            self.addItem(item)
            item.setPos(center)
            self.update()
            self.removeItem(self.line)
            self.line = None

        self.line = None
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False


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

        self.scene = DiagramScene(self.itemMenu, self.attributes)

        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.pixitemInserted.connect(self.pixitemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.itemSelected.connect(self.itemSelected)
        self.scene.DitemSelected.connect(self.DitemSelected)

        self.createToolbars()

        layout = QHBoxLayout()
        layout.addWidget(self.toolBox)
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, 3000, 3000)

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
            self.scene.setMode(DiagramScene.InsertText)
        else:
            self.scene.setItemType(id)
            self.scene.setMode(DiagramScene.InsertItem)

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
            if item.zValue() >= zValue and (isinstance(item, DiagramItem) or isinstance(item, DiagramPixmapItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and (isinstance(item, DiagramItem) or isinstance(item, DiagramPixmapItem))):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.pointerTypeGroup.button(DiagramScene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def pixitemInserted(self, item):
        self.pointerTypeGroup.button(DiagramScene.MoveItem).setChecked(True)
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
        layout.addWidget(self.createCellWidget("Polygon", DiagramItem.PolygonStim), 0, 0)
        layout.addWidget(self.createCellWidget("Circle", DiagramItem.Circle), 1, 0)
        layout.addWidget(self.createCellWidget("Arc", DiagramItem.Arc), 2, 0)
        layout.addWidget(self.createCellWidget("Rectangle", DiagramItem.Rectangle), 3, 0)

        # layout.addWidget(self.createCellWidget("Conditional", DiagramItem.Conditional), 0, 0)
        # layout.addWidget(self.createCellWidget("Polygon", DiagramItem.Step), 2, 0)
        # layout.addWidget(self.createCellWidget("Circle", DiagramItem.Circle), 2, 0)
        # layout.addWidget(self.createCellWidget("Input/Output", DiagramItem.Io), 3, 0)

        textButton = Button()
        self.buttonGroup.addButton(textButton, self.InsertTextButton)
        textButton.setIcon(QIcon(QPixmap(Func.getImage("textpointer.png")).scaled(50, 50)))
        textButton.setIconSize(QSize(50, 50))
        videoButton = Button()
        self.buttonGroup.addButton(videoButton, DiagramPixmapItem.Video)
        videoButton.setIcon(QIcon(QPixmap(Func.getImage("video.png")).scaled(50, 50)))
        videoButton.setIconSize(QSize(50, 50))
        pictureButton = Button()
        self.buttonGroup.addButton(pictureButton, DiagramPixmapItem.Picture)
        pictureButton.setIcon(QIcon(QPixmap(Func.getImage("Picture.png")).scaled(50, 50)))
        pictureButton.setIconSize(QSize(50, 50))
        soundButton = Button()
        self.buttonGroup.addButton(soundButton, DiagramPixmapItem.Sound)
        soundButton.setIcon(QIcon(QPixmap(Func.getImage("music.png")).scaled(50, 50)))
        soundButton.setIconSize(QSize(50, 50))
        snowButton = Button()
        self.buttonGroup.addButton(snowButton, DiagramPixmapItem.Snow)
        snowButton.setIcon(QIcon(QPixmap(Func.getImage("snow1.png")).scaled(50, 50)))
        snowButton.setIconSize(QSize(50, 50))
        gaborButton = Button()
        self.buttonGroup.addButton(gaborButton, DiagramPixmapItem.Gabor)
        gaborButton.setIcon(QIcon(QPixmap(Func.getImage("Gabor.png")).scaled(50, 50)))
        gaborButton.setIconSize(QSize(50, 50))

        textLayout    = QGridLayout()
        videoLayout   = QGridLayout()
        pictureLayout = QGridLayout()
        soundLayout   = QGridLayout()
        snowLayout    = QGridLayout()
        gaborLayout   = QGridLayout()

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
        self.pointerTypeGroup.addButton(pointerButton, DiagramScene.MoveItem)
        self.pointerTypeGroup.addButton(linePointerButton, DiagramScene.InsertLine)
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
        item = DiagramItem(diagramType, self.itemMenu)
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
                    item = DiagramItem(dic['name'], self.itemMenu, self.attributes)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                elif dic['name'] == 4:
                    p1 = QPointF(int(dic['P1 X']), int(dic['P1 Y']))
                    p2 = QPointF(int(dic['P2 X']), int(dic['P2 Y']))
                    p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
                    p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
                    item = DiagramItem(dic['name'], self.itemMenu, self.attributes, p3, p4)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                else:
                    item = DiagramPixmapItem(dic['name'], self.itemMenu, self.attributes)
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
