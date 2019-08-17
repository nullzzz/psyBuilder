import numpy as np
from PyQt5.QtCore import QPointF, QRectF, QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPolygonItem
from app.center.widget_tabs.events.slider.polygon.polygonProperty import PolygonProperty
from app.func import Func
from app.info import Info


class DiaItem(QGraphicsPolygonItem):
    Line, Polygon, Arc, Circle, Rect  = range(5)

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

        #  rectangle
        elif self.diagramType == self.Rect:
            path.addRect(QRectF(-100, -100, 200, 200))
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('rect')

        # arc
        elif self.diagramType == self.Arc:
            path.arcTo(QRectF(-100, -100, 200, 200), 0, 270)
            self.mPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('arc')

        # polygon
        elif self.diagramType == self.Polygon:
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
            self.pro_window = PolygonProperty('polygon')

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
        if self.arbitrary_resize and self.diagramType in [self.Polygon , self.Circle , self.Arc , self.Rect ]:
            self.resizingFlag = True
        # 等比例
        if self.keep_resize and self.diagramType in [self.Polygon , self.Circle , self.Arc , self.Rect ]:
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

            elif self.diagramType == self.Rect:
                path.addRect(cRect)

            elif self.diagramType == self.Polygon:

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

        elif self.diagramType == self.Rect:
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

        elif self.diagramType == self.Polygon:
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

        elif self.diagramType == self.Rect:
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

        elif self.diagramType == self.Polygon:
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
