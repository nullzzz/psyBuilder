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

from app.center.widget_tabs.events.slider.gabor import GaborProperty
from app.center.widget_tabs.events.slider.graph import Snow, makeGabor_bcl
from app.center.widget_tabs.events.slider.image.imageProperty import ImageProperty

from app.center.widget_tabs.events.slider.polygon.polygonProperty import PolygonProperty
from app.center.widget_tabs.events.slider.property import SliderProperty
from app.center.widget_tabs.events.slider.snow import snowProperty
from app.center.widget_tabs.events.slider.sound.soundProperty import SoundProperty
from app.center.widget_tabs.events.slider.video.videoProperty import VideoProperty
from app.func import Func
from lib.psy_message_box import PsyMessageBox as QMessageBox
from app.center.widget_tabs.events.slider.graph import makeGabor_bcl

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
