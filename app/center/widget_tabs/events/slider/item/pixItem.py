import numpy as np
import qimage2ndarray
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from app.center.widget_tabs.events.slider.gabor import GaborProperty
from app.center.widget_tabs.events.slider.graph import Snow, makeGabor_bcl
from app.center.widget_tabs.events.slider.image.imageProperty import ImageProperty
from app.center.widget_tabs.events.slider.snow import snowProperty
from app.center.widget_tabs.events.slider.sound.soundProperty import SoundProperty
from app.center.widget_tabs.events.slider.video.videoProperty import VideoProperty
from app.func import Func
from app.info import Info


class PixItem(QGraphicsPixmapItem):
    Image,Text, Video, Sound, Snow, Gabor = range(5,11)
    # Image = Info.ITEM_IMAGE
    # Text = Info.ITEM_TEXT
    # Video = Info.ITEM_VIDEO
    # Sound = Info.ITEM_SOUND
    # Snow = Info.ITEM_SNOW
    # Gabor = Info.ITEM_GABOR

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
        if self.diagramType in [5,6]:
            pass
        # self.pro_window.frame.setPos(self.scenePos().x(), self.scenePos().y())
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
                snowStim = Snow(int(int(self.default_properties["Width"]) / snowPixSize),
                                int(int(self.default_properties["Height"]) / snowPixSize))
                snowStim = snowStim.astype(np.uint8)

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
                spFreq = float(self.default_properties['spatialFreq(cycles/pixel)'])
                Contrast = float(self.default_properties['Contrast'])
                phase = float(self.default_properties['phase'])
                orientation = float(self.default_properties['orientation'])

                rgbValue = self.default_properties['bkColor'].split(',')
                sdx = float(self.default_properties['SDx(pixels)'])
                sdy = float(self.default_properties['SDy(pixels)'])
                width = int(self.default_properties["Width"])
                height = int(self.default_properties["Height"])
                bkColor = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))

                stim = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                     bkColor, width, height, sdx, sdy)
                stim = stim.astype(np.uint8)
                pix = QPixmap(qimage2ndarray.array2qimage(stim))
                pix = pix.scaled(int(self.default_properties['Width']),
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
                    spFreq = float(self.default_properties['spatialFreq(cycles/pixel)'])
                    Contrast = float(self.default_properties['Contrast'])
                    phase = float(self.default_properties['phase'])
                    orientation = float(self.default_properties['orientation'])
                    rgbValue = self.default_properties['bkColor'].split(',')
                    sdx = float(self.default_properties['SDx(pixels)'])
                    sdy = float(self.default_properties['SDy(pixels)'])
                    width = int(self.default_properties["Width"])
                    height = int(self.default_properties["Height"])
                    bkColor = (float(rgbValue[0]), float(rgbValue[1]), float(rgbValue[2]))

                    stim = makeGabor_bcl(spFreq, Contrast, phase, orientation,
                                         bkColor, width, height, sdx, sdy)

                    stim = stim.astype(np.uint8)
                    pix = QPixmap(qimage2ndarray.array2qimage(stim))

                    pix = pix.scaled(int(self.default_properties['Width']),
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
