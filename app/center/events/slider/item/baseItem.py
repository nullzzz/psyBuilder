from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainterPath, QColor
from PyQt5.QtWidgets import QGraphicsItem, QWidget


class BaseItem(QGraphicsItem):
    SLIDER_COUNT: dict = {
        "polygon": 0,
        "arc": 0,
        "rect": 0,
        "circle": 0,
        "image": 0,
        "text": 0,
        "video": 0,
        "sound": 0,
        "snow": 0,
        "gabor": 0,
        "line": 0,
    }

    # "polygon", "arc", "rect", "circle", "image", "text", "video", "sound", "snow", "gabor", "line"

    def __init__(self, item_type, item_name: str = ""):
        super().__init__()
        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        self.default_properties: dict = {}
        self.properties: dict = {}
        self.pro_window = QWidget()

    def generateItemName(self) -> str:
        name = self.item_type
        cnt = BaseItem.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        BaseItem.SLIDER_COUNT[name] += 1
        return item_name

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
                __start_angle = self.properties["Angle Start"]
                start_angle = 0 if __start_angle.startswith("[") else float(__start_angle)
                __angle_length = self.properties["Angle Length"]
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
            super().mouseMoveEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != Qt.LeftButton:
            return
        if mouseEvent.modifiers() == Qt.AltModifier:
            self.arbitrary_resize = True
            self.setCursor(Qt.SizeAllCursor)

        elif mouseEvent.modifiers() == Qt.ShiftModifier:
            self.keep_resize = True
            self.setCursor(Qt.SizeAllCursor)

        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        self.unsetCursor()
        self.resizingFlag = False
        self.arbitrary_resize = False
        self.keep_resize = False
        super().mouseReleaseEvent(mouseEvent)

    def mouseDoubleClickEvent(self, mouseEvent):
        self.openPro()

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.setWh()
        self.pro_window.show()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.changeSomething()

    def updateInfo(self):
        self.pro_window.updateInfo()
        self.properties["X"] = self.scenePos().x()
        self.properties["Y"] = self.scenePos().y()
        self.properties["Z"] = self.zValue()

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.properties["X"] = properties["X"]
        self.properties["Y"] = properties["Y"]
        self.properties["Z"] = properties["Z"]
        self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def setPosition(self):
        if self.item_type == self.Polygon:
            self.setVertex()
        self.pro_window.general.setPosition(self.scenePos().x(), self.scenePos().y())

    def setWh(self):
        self.pro_window.general.setWh(self.boundingRect().width(), self.boundingRect().height())

    def setVertex(self):
        points = []
        for p in range(len(self.polygon()) - 1):
            points.append(
                (self.polygon()[p].x() + self.scenePos().x(),
                 self.polygon()[p].y() + self.scenePos().y()))

        self.pro_window.general.setVertex(points)

    def setWidth(self, width):
        if isinstance(width, str) and width.isdigit():
            width = int(width)
        pen = self.pen()
        pen.setWidth(width)
        self.setPen(pen)
        self.update()

        old_width = self.properties["Border Width"]
        if not old_width.startswith("["):
            self.properties["Border Width"] = str(width)
            self.pro_window.general.setBorderWidth(width)

    def setColor(self, color: QColor):
        pen = self.pen()
        pen.setColor(color)
        self.setPen(pen)
        self.update()

        old_rgb = self.properties["Border Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Border Color"] = rgb
            self.pro_window.general.setBorderColor(rgb)

    def setItemColor(self, color):
        self.fill_color = color

        old_rgb = self.properties["Fill Color"]
        if not old_rgb.startswith("["):
            rgb = f"{color.red()},{color.green()},{color.blue()}"
            self.properties["Fill Color"] = rgb
            self.pro_window.general.setItemColor(rgb)
