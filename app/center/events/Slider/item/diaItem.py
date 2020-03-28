import numpy as np
from PyQt5.QtCore import QPointF, QRectF, QPoint, Qt
from PyQt5.QtGui import QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPolygonItem

from app.info import Info
from ..item.arc import ArcProperty
from ..item.circle import CircleProperty
from ..item.polygon import PolygonProperty
from ..item.rect import RectProperty


class DiaItem(QGraphicsPolygonItem):
    Polygon, Circle, Arc, Rect = range(1, 5)

    name: dict = {
        Polygon: Info.ITEM_POLYGON,
        Arc: Info.ITEM_ARC,
        Circle: Info.ITEM_CIRCLE,
        Rect: Info.ITEM_RECT,
    }

    def __init__(self, item_type, item_name: str = "", parent=None):
        super(DiaItem, self).__init__(parent=parent)
        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()
        self.attributes = []

        path = QPainterPath()
        # circle
        if self.item_type == self.Circle:
            path.addEllipse(QRectF(-100, -100, 200, 200))
            self.pro_window = CircleProperty()

        #  rectangle
        elif self.item_type == self.Rect:
            path.addRect(QRectF(-100, -100, 200, 200))
            self.pro_window = RectProperty()

        # arc
        elif self.item_type == self.Arc:
            path.arcTo(QRectF(-100, -100, 200, 200), 0, 270)
            self.pro_window = ArcProperty()

        # polygon
        elif self.item_type == self.Polygon:
            # added by yang to plot the triangle
            self.pro_window = PolygonProperty()
            n = 3
            points = []
            for p in range(n):
                x = int(100 * np.cos(np.pi / 2 - p * 2 * np.pi / n))
                y = int(100 * np.sin(p * 2 * np.pi / n - np.pi / 2))
                points.append((x, y))
                if p == 0:
                    path.moveTo(points[p][0], points[p][1])
                else:
                    path.lineTo(points[p][0], points[p][1])
            path.lineTo(points[0][0], points[0][1])

        self.mPolygon = path.toFillPolygon()

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setPolygon(self.mPolygon)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.arbitrary_resize = False
        self.keep_resize = False
        self.resizingFlag = False

        self.center = QPointF(0, 0)
        self.fill_color = '0,0,0'
        self.border_color = '255,255,255'
        self.border_width = 1

        self.default_properties = {
            'name': self.item_name,
            'z': self.zValue(),
            'x': 1,
            'y': 1,
            **self.pro_window.getInfo(),
        }

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def getName(self):
        return self.item_name

    def setLineColor(self, color):
        self.border_color = color
        self.pro_window.setLineColor(color)

    def setLineWidth(self, width):
        self.border_width = width
        self.pro_window.setLineWidth(width)

    def noOutLineBoundingRect(self):
        cBoundRect = self.polygon().boundingRect()
        # print(f"line 109: {cBoundRect}")
        # cBoundRect = cBoundRect.adjusted(self.pen().width()/2,
        #                                               self.pen().width()/2,
        #                                               -self.pen().width(),
        #                                             -self.pen().width())
        # print(f"line 114: {cBoundRect}")
        return cBoundRect

    def mouseMoveEvent(self, mouseEvent):
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()

        bounding_rect = self.polygon().boundingRect()

        height = bounding_rect.height()
        width = bounding_rect.width()

        # 非等比例
        if self.arbitrary_resize:
            self.resizingFlag = True
        # 等比例
        if self.keep_resize:
            self.resizingFlag = True

            if height < 5:
                height = 5

            if width < 5:
                width = 5

            # make sure the zoom in/out ratio equal for h and w
            ratio = height / width

            if (y - height) / (x - width) > ratio:
                y = ratio * (x - width) + height
            else:
                x = (y - height) / ratio + width

        if self.resizingFlag:
            x0 = bounding_rect.left()
            y0 = bounding_rect.top()

            path = QPainterPath()

            new_width = x - x0
            new_height = y - y0

            new_rect = QRectF(x0 - (new_width - width) / 2, y0 - (new_height - height) / 2, new_width, new_height)

            if self.item_type == self.Circle:
                path.addEllipse(new_rect)

            elif self.item_type == self.Arc:
                path.moveTo(new_rect.center())
                __start_angle = self.default_properties["Angle start"]
                start_angle = 0 if __start_angle.startswith("[") else float(__start_angle)
                __angle_length = self.default_properties["Angle length"]
                angle_length = 0 if __angle_length.startswith("[") else float(__angle_length)

                path.arcTo(new_rect, start_angle, angle_length)

            elif self.item_type == self.Rect:
                path.addRect(new_rect)

            elif self.item_type == self.Polygon:

                h_ratio = (x - x0) / width
                v_ratio = (y - y0) / height

                if self.keep_resize:
                    if h_ratio > v_ratio:
                        v_ratio = h_ratio
                    else:
                        h_ratio = v_ratio

                for iVertex in range(len(self.polygon())):
                    cX = self.polygon().value(iVertex).x() * h_ratio
                    cY = self.polygon().value(iVertex).y() * v_ratio

                    if iVertex == 0:
                        path.moveTo(cX, cY)
                    else:
                        path.lineTo(cX, cY)


            else:
                raise Exception("item_type should be of 'Arc','rectangle', or 'circle' !!")

            self.mPolygon = path.toFillPolygon()
            self.setPolygon(self.mPolygon)
            self.update()

            bound_rect = self.polygon().boundingRect()
            self.center = bound_rect.center()

        else:
            super(DiaItem, self).mouseMoveEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != Qt.LeftButton:
            return
        if mouseEvent.modifiers() == Qt.AltModifier:
            self.arbitrary_resize = True
            self.setCursor(Qt.SizeAllCursor)

        elif mouseEvent.modifiers() == Qt.ShiftModifier:
            self.keep_resize = True
            self.setCursor(Qt.SizeAllCursor)

        super(DiaItem, self).mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.resizingFlag = False
        self.arbitrary_resize = False
        self.keep_resize = False
        super(DiaItem, self).mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        self.openPro()

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.setWh()
        self.pro_window.show()

    def setPosition(self):
        if self.item_type == self.Polygon:
            self.setVertex()
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def setWh(self):
        self.pro_window.setWh(self.boundingRect().width(), self.boundingRect().height())

    def setVertex(self):
        points = []
        for p in range(len(self.polygon()) - 1):
            points.append(
                (self.polygon()[p].x() + self.scenePos().x(),
                 self.polygon()[p].y() + self.scenePos().y()))

        self.pro_window.setVertex(points)

    def setPoint(self):
        # todo: 设置polygon顶点
        pass

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        self.changeSomething()

    def getInfo(self):
        self.default_properties = {
            'name': self.item_name,
            'z': self.zValue(),
            'x': self.scenePos().x(),
            'y': self.scenePos().y(),
            **self.pro_window.getInfo(),
        }
        return self.default_properties

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.pro_window.setProperties(properties)
            self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("x", 0)
        y = self.default_properties.get("y", 0)
        z = self.default_properties.get("z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        new = DiaItem(self.item_type)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        new.setZValue(self.zValue())

        return new

    def changeSomething(self):
        __cx = self.default_properties["Center X"]
        cx = int(__cx) if __cx.isdigit() else self.scenePos().x()
        __cy = self.default_properties["Center Y"]
        cy = int(__cy) if __cy.isdigit() else self.scenePos().y()

        self.setPos(QPoint(cx, cy))

        # fill color
        fill_color = self.default_properties["Fill color"]
        if not fill_color.startswith("["):
            self.fill_color = fill_color
        # todo
        color = [int(x) for x in self.fill_color.split(",")]
        if len(color) == 3:
            r, g, b = color
            a = 255
        else:
            r, g, b, a = color

        self.setBrush(QColor(r, g, b, a))
        # border color
        border_color = self.default_properties["Border color"]
        if not border_color.startswith("["):
            self.border_color = border_color

        border_width = self.default_properties["Border width"]
        if not border_width.startswith("["):
            self.border_width = int(border_width)
        pen = self.pen()
        pen.setWidth(self.border_width)

        color = [int(x) for x in self.border_color.split(",")]
        if len(color) == 3:
            r, g, b = color
            a = 255
        else:
            r, g, b, a = color
        pen.setColor(QColor(r, g, b, a))
        self.setPen(pen)

        path = QPainterPath()
        if self.item_type == self.Polygon:
            points = self.default_properties["Points"]
            flag = True
            for p in points:
                x, y = p
                if x.startswith("[") or y.startswith("["):
                    flag = False
                    break
            if flag:
                for i, p in enumerate(points):
                    x = int(p[0])
                    y = int(p[1])
                    if i == 0:
                        path.moveTo(x - cx, y - cy)
                    else:
                        path.lineTo(x - cx, y - cy)
                path.lineTo(int(points[0][0]) - cx, int(points[0][1]) - cy)

        else:
            __w = self.default_properties["Width"]
            w = int(__w) if __w.isdigit() else 100
            __h = self.default_properties["Height"]
            h = int(__h) if __h.isdigit() else 100
            if self.item_type == self.Circle:
                rect = QRectF(-w / 2, -h / 2, w, h)
                path.addEllipse(rect)

            elif self.item_type == self.Arc:
                rect = QRectF(-w / 2, -h / 2, w, h)
                __start = self.default_properties["Angle start"]
                start = 0 if __start.startswith("[") else float(__start)

                __length = self.default_properties["Angle length"]
                length = 360 if __length.startswith("[") else float(__length)

                path.arcTo(rect, start, length)

            elif self.item_type == self.Rect:
                rect = QRectF(-w / 2, -h / 2, w, h)
                path.addRect(rect)

        self.mPolygon = path.toFillPolygon()
        self.setPolygon(self.mPolygon)
        self.update()

    def setWidth(self, width):
        if isinstance(width, str) and width.isdigit():
            width = int(width)
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)
        self.update()

        old_width = self.default_properties["Border width"]
        if not old_width.startswith("["):
            self.pro_window.default_properties["Border width"] = str(width)
            self.pro_window.general.default_properties["Border width"] = str(width)
            self.default_properties["Border width"] = str(width)
            self.pro_window.general.border_width.setText(str(width))

    def setColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        self.update()

        old_rgb = self.default_properties["Border color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.pro_window.default_properties["Border color"] = rgb
            self.pro_window.general.default_properties["Border color"] = rgb
            self.default_properties["Border color"] = rgb
            self.pro_window.general.border_color.setCurrentText(rgb)

    def setItemColor(self, color):
        self.fill_color = color

        old_rgb = self.default_properties["Fill color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.pro_window.default_properties["Fill color"] = rgb
            self.pro_window.general.default_properties["Fill color"] = rgb
            self.default_properties["Fill color"] = rgb
            self.pro_window.general.fill_color.setCurrentText(rgb)
