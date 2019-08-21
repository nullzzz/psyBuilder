import numpy as np
import qimage2ndarray
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from app.center.widget_tabs.events.newSlider.item.gabor import GaborProperty
from app.center.widget_tabs.events.newSlider.item.snow import SnowProperty
from app.func import Func
from app.info import Info


class OtherItem(QGraphicsPixmapItem):
    Snow, Gabor = 9, 10
    name = {
        Snow: "snow",
        Gabor: "gabor",
    }

    def __init__(self, item_type, item_name: str = "", parent=None):
        super(OtherItem, self).__init__(parent=parent)

        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        self.attributes: list = []

        if self.item_type == self.Snow:
            self.pro_window = SnowProperty()
            self.setPixmap(QPixmap(Func.getImage("snow.png")).scaled(100, 100))
        elif self.item_type == self.Gabor:
            self.pro_window = GaborProperty()
            self.setPixmap(QPixmap(Func.getImage("gabor.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.default_properties = {
            'name': self.item_name,
            'z': self.zValue(),
            'x': 1,
            'y': 1,
            **self.pro_window.getInfo(),
        }

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.SLIDER_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.SLIDER_COUNT[name] += 1
        return item_name

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.pro_window.show()

    def getName(self):
        return self.item_name

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        self.changeSomething()

    def changeSomething(self):
        __w = self.default_properties["Width"]
        w = int(__w) if __w.isdigit() else 100
        __h = self.default_properties["Height"]
        h = int(__h) if __h.isdigit() else 100

        __cx = self.default_properties["Center X"]
        cx = int(__cx) if __cx.isdigit() else self.scenePos().x()
        __cy = self.default_properties["Center Y"]
        cy = int(__cy) if __cy.isdigit() else self.scenePos().y()

        __rotate = self.default_properties["Rotation"]
        rotate = int(__rotate) if __rotate.isdigit() else 0

        if self.item_type == self.Snow:
            __scale = self.default_properties["Scale"]
            scale = int(__scale) if __scale.isdigit() else 8

            snow_stimulate = self.getSnow(w // scale, h // scale)

            pix = QPixmap(qimage2ndarray.array2qimage(snow_stimulate))
            self.setPixmap(pix.scaled(w, h))

        elif self.item_type == self.Gabor:
            __spatial = self.default_properties['Spatial']
            spatial = 0.033 if __spatial.startswith("[") else float(__spatial)

            __contrast = self.default_properties['Contrast']
            contrast = 1 if __contrast.startswith("[") else float(__contrast)

            __phase = self.default_properties['Phase']
            phase = 0 if __phase.startswith("[") else float(__phase)

            __orientation = self.default_properties['Orientation']
            orientation = 0 if __orientation.startswith("[") else float(__orientation)

            __back_color = self.default_properties['Back color']
            back_color = (128.0, 128.0, 128.0) if __back_color.startswith("[") else tuple(float(x) for x in __back_color.split(","))

            __sdx = self.default_properties['SDx']
            sdx = 30 if __sdx.startswith("[") else int(__sdx)

            __sdy = self.default_properties['SDy']
            sdy = 30 if __sdy.startswith("[") else int(__sdy)

            gabor_stimulate = self.getGabor(spatial, contrast, phase, orientation,
                                            back_color, w, h, sdx, sdy)
            pix = QPixmap(qimage2ndarray.array2qimage(gabor_stimulate))
            self.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))

        self.setPos(QPoint(cx, cy))
        x = self.boundingRect().center().x()
        y = self.boundingRect().center().y()

        self.setTransformOriginPoint(x, y)
        self.setRotation(rotate)
        self.update()

    @staticmethod
    def getSnow(w, h, is_binary=False):
        snow = np.random.rand(w, h)
        snow = snow * 255
        if is_binary:
            snow[snow <= 0.5] = 0
            snow[snow > 0.5] = 255
        snow.astype(np.uint8)
        return snow

    @staticmethod
    def getGabor(cycles_per_pix, contrast, phase, orientation, back_color:tuple, width, height, sdx, sdy):
        phase = (phase % 360) * (np.pi / 180)
        orientation = (orientation % 360) * (np.pi / 180)
        # to force the width and height to be even
        width = int(width / 2.0) * 2
        height = int(height / 2.0) * 2

        radius = (int(width / 2.0), int(height / 2.0))
        [x, y] = np.meshgrid(range(-radius[0], radius[0] + 1), range(-radius[1], radius[1] + 1))

        circle_mask = (x / radius[0]) ** 2 + (y / radius[1]) ** 2

        circle_mask = circle_mask >= 1

        xm = x * np.cos(orientation) - y * np.sin(orientation)
        ym = x * np.sin(orientation) + y * np.cos(orientation)

        circular_gaussian_mask_matrix = np.exp(-((xm / sdx) ** 2 + (ym / sdy) ** 2) / 2)
        circular_gaussian_mask_matrix[circle_mask] = 0

        f = 2 * np.pi * cycles_per_pix
        a = np.cos(orientation) * f
        b = np.sin(orientation) * f

        layer = 255 * circular_gaussian_mask_matrix * (np.cos(a * x + b * y + phase) * contrast + 1.0) / 2.0

        gabor = np.zeros((height + 1, width + 1, 3))

        for i in range(height + 1):
            for j in range(width + 1):
                for k in range(3):
                    gabor[i, j, k] = layer[i, j]

        for iDim in range(0, np.size(back_color)):
            gabor[:, :, iDim] = gabor[:, :, iDim] + (1 - circular_gaussian_mask_matrix) * back_color[iDim]
        gabor.astype(np.uint8)
        return gabor

    def setPosition(self):
        self.pro_window.setPosition(self.scenePos().x(), self.scenePos().y())

    def getInfo(self):
        self.default_properties.clear()
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
            self.getInfo()

    def loadSetting(self):
        x = self.default_properties.get("x", 0)
        y = self.default_properties.get("y", 0)
        z = self.default_properties.get("z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        clone_page = OtherItem(self.item_type)
        properties = self.getInfo()
        clone_page.pro_window.setProperties(properties)
        return clone_page
