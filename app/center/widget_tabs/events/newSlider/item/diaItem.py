# 绘制形状
import numpy as np
from PyQt5.QtCore import QRectF, QPointF, QPoint, Qt
from PyQt5.QtGui import QPainterPath, QPolygonF, QColor, QPixmap, QPen, QPainter
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem

from app.center.widget_tabs.events.newSlider.polygon.PolygonProperty import PolygonProperty


class DiaItem(QGraphicsPolygonItem):
    Step, Conditional, Circle, Io = range(4)
    Line = 4

    def __init__(self, diagram_type, p1=None, p2=None, parent=None):
        super(DiaItem, self).__init__(parent=parent)

        self.diagram_type = diagram_type
        self.attributes = []

        self.default_properties = {
            "name": self.diagram_type,
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
            "Point": [['0', '0'], ['0', '0'], ['0', '0']],  # added by yang
            "start": "0",
            "end angle": "0",
            "Long axis": "0",
            "Short axis": "0",
            "Border color": "black",
            "Border width": 1,
            "Fill color": "white",
            'z': self.zValue()
        }
        self.p1 = p1
        self.p2 = p2

        path = QPainterPath()
        if self.diagram_type == self.Circle:
            path.addEllipse(QRectF(-100, -100, 200, 200))
            self.myPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('one')
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)

        elif self.diagram_type == self.Conditional:
            # 菱形
            # myPolygon = QPolygonF([
            #     QPointF(-100, 0), QPointF(0, 100),
            #     QPointF(100, 0), QPointF(0, -100),
            #     QPointF(-100, 0)])
            # path.addPolygon(myPolygon)
            path.moveTo(-100, 0)
            path.lineTo(0, 100)
            path.lineTo(100, 0)
            path.lineTo(0, -100)
            path.lineTo(-100, 0)
            self.myPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('four')
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)
        elif self.diagram_type == self.Step:
            # path.addRect(QRectF(-100, -100, 200, 200))
            # ------ added by yang to plot the triangle -----------------------------------------------/
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
            # -----------------------------------------------------------------------------------------\
            self.myPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('four')
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)
        elif self.diagram_type == self.Line:
            # center = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
            # print(center.x())
            # print(self.scenePos())
            path.moveTo(p1.x(), p1.y())
            path.lineTo(p2.x(), p2.y())
            self.myPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('two')
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)
        else:
            myPolygon = QPolygonF([
                QPointF(-120, -80), QPointF(-70, 80),
                QPointF(120, 80), QPointF(70, -80),
                QPointF(-120, -80)])
            path.addPolygon(myPolygon)
            self.myPolygon = path.toFillPolygon()
            self.pro_window = PolygonProperty('four')
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setPolygon(self.myPolygon)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.resizing = False
        self.sresizing = False
        self.flag = False
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

    def boundingRect(self):
        return self.polygon().boundingRect().adjusted(-self.pen().width(), -self.pen().width(), self.pen().width(),
                                                      self.pen().width())

    def mouseMoveEvent(self, mouseEvent):
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()
        rect0 = self.polygon().boundingRect()
        self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
        # 非等比例
        if self.resizing and self.diagram_type < 4:
            self.flag = True
        # 等比例
        if self.sresizing and self.diagram_type < 4:
            self.flag = True
            a = rect0.height()
            if a < 5:
                a = 5
            b = rect0.width()
            if b < 5:
                b = 5
            c = a / b
            if (y - a) / (x - b) > c:
                y = c * (x - b) + a
            else:
                x = (y - a) / c + b
        if self.flag:
            if self.diagram_type == self.Circle:
                path = QPainterPath()
                rect = QRectF(rect0.left(), rect0.top(), x - rect0.left(), y - rect0.top())
                path.addEllipse(rect)
                self.mpolygon = path.toFillPolygon()
            elif self.diagram_type == self.Conditional:
                path = QPainterPath()
                mpolygon = QPolygonF([QPointF(-100, (y + rect0.top()) / 2), QPointF((x + rect0.left()) / 2, y),
                                      QPointF(x, (y + rect0.top()) / 2), QPointF((x + rect0.left()) / 2, -100),
                                      QPointF(-100, (y + rect0.top()) / 2)])
                path.addPolygon(mpolygon)
                self.mpolygon = path.toFillPolygon()
            elif self.diagram_type == self.Step:
                path = QPainterPath()
                rect = QRectF(rect0.left(), rect0.top(), x - rect0.left(), y - rect0.top())
                path.addRect(rect)
                self.mpolygon = path.toFillPolygon()
            else:
                path = QPainterPath()
                mpolygon = QPolygonF([QPointF(-120, -80), QPointF(-120 + (5 * y + 400) / 16, y),
                                      QPointF(x, y), QPointF(x - (5 * y + 400) / 16, -80),
                                      QPointF(-120, -80)])
                path.addPolygon(mpolygon)
                self.mpolygon = path.toFillPolygon()
            self.setPolygon(self.mpolygon)
            self.update()
            self.center = self.polygon().boundingRect().center()
        else:
            super(DiaItem, self).mouseMoveEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.AltModifier:
            self.resizing = True
            self.setCursor(Qt.SizeAllCursor)
        elif mouseEvent.button() == Qt.LeftButton and mouseEvent.modifiers() == Qt.ShiftModifier:
            self.sresizing = True
            self.setCursor(Qt.SizeAllCursor)
        else:
            super(DiaItem, self).mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.flag1 = False
        self.resizing = False
        self.sresizing = False
        self.flag = False
        super(DiaItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, event):
        if self.diagram_type != self.Line:
            self.setProperties()
            self.pro_window.frame.getProperties(self.default_properties)
            self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setAttributes(self.attributes)
            self.pro_window.show()
        else:
            self.setProperties()
            self.pro_window.frame.getProperties(self.default_properties)
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
        painter.drawPolyline(self.myPolygon)
        return pixmap

    # def contextMenuEvent(self, event):
    #     self.scene().clearSelection()
    #     self.setSelected(True)
    #     # Here is a bug, Fuck you!
    #     # self.myContextMenu.exec_(event.screenPos())
    #     self.contextMenu.exec_(event.screenPos())

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

        if self.diagram_type == self.Circle:
            path = QPainterPath()
            rect = QRectF(-int(self.pro_window.frame.default_properties["Long axis"]) / 2,
                          -int(self.pro_window.frame.default_properties["Short axis"]) / 2,
                          int(self.pro_window.frame.default_properties["Long axis"]),
                          int(self.pro_window.frame.default_properties["Short axis"]))
            path.addEllipse(rect)
            self.mpolygon = path.toFillPolygon()
            self.setPos(QPoint(int(self.pro_window.frame.default_properties["Center X"]),
                               int(self.pro_window.frame.default_properties["Center Y"])))

        elif self.diagram_type == self.Line:
            path = QPainterPath()
            path.moveTo(int(self.pro_window.frame.default_properties["P1 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P1 Y"]) - cy)
            path.lineTo(int(self.pro_window.frame.default_properties["P2 X"]) - cx,
                        int(self.pro_window.frame.default_properties["P2 Y"]) - cy)
            self.setPos(QPoint(int(self.pro_window.frame.default_properties["Center X"]),
                               int(self.pro_window.frame.default_properties["Center Y"])))
            self.mpolygon = path.toFillPolygon()
        else:
            path = QPainterPath()
            # print(f"{self.pro_window.frame.default_properties}")

            verticesXY = self.pro_window.frame.default_properties["Point"]

            # added by yang to plot the m-polygon
            for iVertex in range(len(verticesXY)):
                if iVertex == 0:
                    path.moveTo(int(verticesXY[iVertex][0]) - cx + dx, int(verticesXY[iVertex][1]) - cy + dy)
                else:
                    path.lineTo(int(verticesXY[iVertex][0]) - cx + dx, int(verticesXY[iVertex][1]) - cy + dy)
            path.lineTo(int(verticesXY[0][0]) - cx + dx, int(verticesXY[0][1]) - cy + dy)

            # x1 = int(self.pro_window.frame.default_properties["P1 X"]) - cx
            # y1 = int(self.pro_window.frame.default_properties["P1 Y"]) - cy
            # x2 = int(self.pro_window.frame.default_properties["P2 X"]) - cx
            # y2 = int(self.pro_window.frame.default_properties["P2 Y"]) - cy
            # x3 = int(self.pro_window.frame.default_properties["P3 X"]) - cx
            # y3 = int(self.pro_window.frame.default_properties["P3 Y"]) - cy
            # x4 = int(self.pro_window.frame.default_properties["P4 X"]) - cx
            # y4 = int(self.pro_window.frame.default_properties["P4 Y"]) - cy
            # # mpolygon = QPolygonF([
            # #     QPointF(x1, y1), QPointF(x2, y2),
            # #     QPointF(x3, y3), QPointF(x4, y4),
            # #     QPointF(x1, y1)])
            # # path.addPolygon(mpolygon)
            # path.moveTo(x1 + dx, y1 + dy)
            # path.lineTo(x2 + dx, y2 + dy)
            # path.lineTo(x3 + dx, y3 + dy)
            # path.lineTo(x4 + dx, y4 + dy)
            # path.lineTo(x1 + dx, y1 + dy)

            self.setPos(QPoint(int(self.pro_window.frame.default_properties["Center X"]),
                               int(self.pro_window.frame.default_properties["Center Y"])))

            self.mpolygon = path.toFillPolygon()
        self.setPolygon(self.mpolygon)
        self.update()

    def setProperties(self):
        if self.diagram_type == self.Line:
            x = int(self.scenePos().x())
            y = int(self.scenePos().y())
            self.default_properties["Center X"] = str(int(self.scenePos().x()))
            self.default_properties["Center Y"] = str(int(self.scenePos().y()))
            self.default_properties["P1 X"] = str(int(self.polygon()[0].x()) + x)
            self.default_properties["P1 Y"] = str(int(self.polygon()[0].y()) + y)
            self.default_properties["P2 X"] = str(int(self.polygon()[1].x()) + x)
            self.default_properties["P2 Y"] = str(int(self.polygon()[1].y()) + y)
        else:
            if self.diagram_type == self.Circle:
                self.default_properties["Center X"] = str(int(self.scenePos().x()))
                self.default_properties["Center Y"] = str(int(self.scenePos().y()))
                self.default_properties["Long axis"] = str(int(self.polygon().boundingRect().height()))
                self.default_properties["Short axis"] = str(int(self.polygon().boundingRect().width()))
            else:
                x = int(self.scenePos().x())
                y = int(self.scenePos().y())
                # "Point": [["0", "0"], ["0", "0"], ["0", "0"]]
                print(f"slider Line 704: {len(self.polygon())}")
                print(f"slider Line 704: {self.polygon()[0].x()}")
                self.default_properties["Center X"] = str(int(self.scenePos().x()))
                self.default_properties["Center Y"] = str(int(self.scenePos().y()))

                verticesXY = []
                for iVertex in range(len(self.polygon()) - 1):
                    verticesXY.append(
                        [str(int(self.polygon()[iVertex].x()) + x), str(int(self.polygon()[iVertex].y()) + y)])
                    # self.default_properties["Point"] = [[str(int(self.polygon()[0].x()) + x),str(int(self.polygon()[0].y()) + y)],
                    #                                     [str(int(self.polygon()[1].x()) + x),str(int(self.polygon()[1].y()) + y)],
                    #                                     [str(int(self.polygon()[2].x()) + x),str(int(self.polygon()[2].y()) + y)]]
                print(f"line 746 : {verticesXY}")
                self.default_properties["Point"] = verticesXY
                self.default_properties["start"] = '0'
                self.default_properties["end angle"] = '360'
                # self.default_properties["P1 X"] = str(int(self.polygon()[0].x()) + x)
                # self.default_properties["P1 Y"] =
                # self.default_properties["P2 X"] = str(int(self.polygon()[1].x()) + x)
                # self.default_properties["P2 Y"] = str(int(self.polygon()[1].y()) + y)
                # self.default_properties["P3 X"] = str(int(self.polygon()[2].x()) + x)
                # self.default_properties["P3 Y"] = str(int(self.polygon()[2].y()) + y)
                # self.default_properties["P4 X"] = str(int(self.polygon()[3].x()) + x)
                # self.default_properties["P4 Y"] = str(int(self.polygon()[3].y()) + y)
        self.default_properties["Border color"] = self.LineColor
        self.default_properties["Border width"] = str(self.LineWidth)
        self.default_properties["Fill color"] = self.ItemColor
        self.default_properties["z"] = self.zValue()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.frame.getProperties(self.default_properties)
            self.apply()

    def clone(self):
        if self.diagram_type == self.Line:
            item = DiaItem(self.diagram_type, self.p1, self.p2)
        else:
            item = DiaItem(self.diagram_type)
        item.setPolygon(self.polygon())
        item.setLineWidth(self.LineWidth)
        item.setLineColor(self.LineColor)
        item.setItemColor(self.ItemColor)
        item.setBrush(QColor(self.ItemColor))
        item.setPen(self.pen())

        return item
