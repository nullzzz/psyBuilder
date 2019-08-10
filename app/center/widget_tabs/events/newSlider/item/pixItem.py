from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

# 画图
from app.center.widget_tabs.events.newSlider.image.imageProperty import ImageProperty
from app.center.widget_tabs.events.newSlider.text.textProperty import TextProperty
from app.center.widget_tabs.events.slider.Slider import DiagramPixmapItem
from app.func import Func


class PixItem(QGraphicsPixmapItem):
    Image, Text, Video, Sound, Snow, Gabor = 2, 3, 4, 5, 6, 7

    def __init__(self, pix_type, parent=None):
        super(PixItem, self).__init__(parent)

        self.diagram_type = pix_type
        self.attributes: list = []
        if self.diagram_type == self.Image:
            self.pro_window = ImageProperty()
            self.setPixmap(QPixmap(Func.getImage("image.png")).scaled(100, 100))
        elif self.diagram_type == self.Text:
            self.pro_window = TextProperty()
            self.setPixmap(QPixmap(Func.getImage("text.png")).scaled(100, 100))
        # elif self.diagram_type == self.Video:
        #     self.pro_window = VideoProperty()
        #     self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(100, 100))
        # elif self.diagram_type == self.Sound:
        #     self.pro_window = SoundProperty()
        #     self.setPixmap(QPixmap(Func.getImage("sound.png")).scaled(100, 100))
        # elif self.diagram_type == self.Snow:
        #     self.pro_window = SnowProperty()
        #     self.setPixmap(QPixmap(Func.getImage("snow.png")).scaled(100, 100))
        # elif self.diagram_type == self.Gabor:
        #     self.pro_window = GaborProperty()
        #     self.setPixmap(QPixmap(Func.getImage("gabor.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.flag = False
        self.arbitrary_resize = False
        self.keep_resize = False

        self.default_properties = {
            'name': self.diagram_type,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties
        }

    def mousePressEvent(self, event):
        if self.diagram_type < 8:
            if event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier:
                self.arbitrary_resize = True
                self.setCursor(Qt.SizeAllCursor)
            elif event.button() == Qt.LeftButton and event.modifiers() == Qt.ShiftModifier:
                self.keep_resize = True
                self.setCursor(Qt.SizeAllCursor)
            else:
                super(PixItem, self).mousePressEvent(event)
        else:
            super(PixItem, self).mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     x = event.pos().x()
    #     y = event.pos().y()
    #     print("moving")
    #     if self.diagram_type > 7:
    #         self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
    #     if self.arbitrary_resize:
    #         self.flag = True
    #     if self.keep_resize:
    #         self.flag = True
    #         if x > y:
    #             x = y
    #         else:
    #             y = x
    #     if self.flag:
    #         if self.diagram_type == self.Video:
    #             self.setPixmap(QPixmap(Func.getImage("video.png")).scaled(x, y))
    #         elif self.diagram_type == self.Sound:
    #             self.setPixmap(QPixmap(Func.getImage("music.png")).scaled(x, y))
    #         elif self.diagram_type == self.Image:
    #             self.setPixmap(QPixmap("D:\\PsyDemo\\image\\image.png").scaled(x, y))
    #         self.update()
    #     else:
    #         super(PixItem, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.unsetCursor()
        self.arbitrary_resize = False
        self.keep_resize = False
        self.flag = False
        super(PixItem, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttributes(self.attributes)
        if self.diagram_type == self.Snow:
            self.default_properties['Center X'] = str(int(self.scenePos().x()))
            self.default_properties['Center Y'] = str(int(self.scenePos().y()))
        elif self.diagram_type == self.Gabor:
            self.default_properties['Center X'] = str(int(self.scenePos().x()))
            self.default_properties['Center Y'] = str(int(self.scenePos().y()))
        self.pro_window.setProperties(self.default_properties)

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
        # 加载之前的default_properties
        self.pro_window.loadSetting()

    def apply(self):
        self.pro_window.getInfo()
        self.default_properties = {
            'name': self.diagram_type,
            'z': self.zValue(),
            'x_pos': 1,
            'y_pos': 1,
            **self.pro_window.default_properties
        }
        # if self.diagram_type == self.Snow:
        #     try:
        #         s = int(self.default_properties["Scale"])
        #         snow = Snow(int(int(self.default_properties["Height"]) / s),
        #                     int(int(self.default_properties["Width"]) / s))
        #         pix = QPixmap(Func.getImage("snow1.png"))
        #         pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
        #         self.setPos(QPoint(float(self.pro_window.frame.default_properties["Center X"]),
        #                            float(self.pro_window.frame.default_properties["Center Y"])))
        #
        #         self.setPixmap(pix)
        #         x = self.boundingRect().center().x()
        #         y = self.boundingRect().center().y()
        #         self.setTransformOriginPoint(x, y)
        #         self.setRotation(int(self.default_properties["Rotation"]))
        #
        #         # self.setScale(float(self.default_properties["Scale"]))
        #         self.update()
        #     except Exception as e:
        #         print(e)
        # if self.diagram_type == self.Gabor:
        #     try:
        #         spFreq = float(self.default_properties['spatialFreq(cycles/pixel)'])
        #         Contrast = float(self.default_properties['Contrast'])
        #         phase = float(self.default_properties['phase'])
        #         orientation = float(self.default_properties['orientation'])
        #         s = self.default_properties['bkColor']
        #         s = s.split(',')
        #         sdx = float(self.default_properties['SDx(pixels)'])
        #         sdy = float(self.default_properties['SDy(pixels)'])
        #         width = int(self.default_properties["Width"])
        #         height = int(self.default_properties["Height"])
        #         bkColor = (float(s[0]), float(s[1]), float(s[2]))
        #         g = makeGabor_bcl(spFreq, Contrast, phase, orientation,
        #                           bkColor, width, height, sdx, sdy)
        #         pix = QPixmap(Func.getImage("gabor1.png"))
        #         pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
        #         self.setPos(QPoint(float(self.pro_window.frame.default_properties["Center X"]),
        #                            float(self.pro_window.frame.default_properties["Center Y"])))
        #         self.setPixmap(pix)
        #         x = self.boundingRect().center().x()
        #         y = self.boundingRect().center().y()
        #         self.setTransformOriginPoint(x, y)
        #         self.setRotation(int(self.default_properties["rotation"]))
        #         self.update()
        #     except Exception as e:
        #         print(e)
        self.default_properties = {
            'name': self.diagram_type,
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
            # if self.diagram_type == self.Snow:
            #     try:
            #         snow = Snow(int(properties["Width"]), int(properties["Height"]))
            #         pix = QPixmap(Func.getImage("snow.png"))
            #         pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
            #         self.setPixmap(pix)
            #         x = self.boundingRect().center().x()
            #         y = self.boundingRect().center().y()
            #         self.setTransformOriginPoint(x, y)
            #         self.setRotation(int(properties["Rotation"]))
            #         self.update()
            #     except Exception as e:
            #         print(e)
            # if self.diagram_type == self.Gabor:
            #     try:
            #         spFreq = float(self.default_properties['spatialFreq(cycles/pixel)'])
            #         Contrast = float(self.default_properties['Contrast'])
            #         phase = float(self.default_properties['phase'])
            #         orientation = float(self.default_properties['orientation'])
            #         s = self.default_properties['bkColor']
            #         s = s.split(',')
            #         sdx = float(self.default_properties['SDx(pixels)'])
            #         sdy = float(self.default_properties['SDy(pixels)'])
            #         width = int(self.default_properties["Width"])
            #         height = int(self.default_properties["Height"])
            #         bkColor = (float(s[0]), float(s[1]), float(s[2]))
            #         g = makeGabor_bcl(spFreq, Contrast, phase, orientation,
            #                           bkColor, width, height, sdx, sdy)
            #         pix = QPixmap(Func.getImage("gabor1.png"))
            #         pix = pix.scaled(int(self.default_properties["Width"]), int(self.default_properties["Height"]))
            #         self.setPixmap(pix)
            #         x = self.boundingRect().center().x()
            #         y = self.boundingRect().center().y()
            #         self.setTransformOriginPoint(x, y)
            #         self.setRotation(int(properties["rotation"]))
            #         self.update()
            #     except Exception as e:
            #         print(e)

    def clone(self):
        new = DiagramPixmapItem(self.diagram_type, self.contextMenu, self.attributes)
        properties = self.pro_window.getInfo()
        new.pro_window.setProperties(properties)
        new.setPixmap(self.pixmap())
        new.setZValue(self.zValue())

        return new
