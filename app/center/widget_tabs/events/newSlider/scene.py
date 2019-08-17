from PyQt5.QtCore import pyqtSignal, Qt, QLineF
from PyQt5.QtGui import QPen, QTransform, QKeyEvent, QPainterPath
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem

from app.center.widget_tabs.events.newSlider.item.diaItem import DiaItem
from app.center.widget_tabs.events.newSlider.item.lasso import Lasso
from app.center.widget_tabs.events.newSlider.item.linItem import LineItem
from app.center.widget_tabs.events.newSlider.item.otherItem import OtherItem
from app.center.widget_tabs.events.newSlider.item.pixItem import PixItem


class Scene(QGraphicsScene):
    InsertItem, InsertLine, MoveItem, SelectItem = range(4)

    itemAdd = pyqtSignal(str)
    itemSelected = pyqtSignal()
    propertyChanged = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        self.my_mode = self.InsertItem

        self.attributes = []
        self.line = None
        self.lasso = None

        self.line_color = Qt.black
        self.fill_color = Qt.transparent
        self.border_color = Qt.black
        self.border_width = 2

        self.t = QTransform()

        self.myLineWidth = 1

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # print(event.key())
        # todo 按键冲突
        if event.key() == Qt.Key_Delete and event.modifiers() == Qt.CTRL:
            print("del")
        super(Scene, self).keyPressEvent(event)

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
            # if self.my_mode == self.InsertItem:
            item_type, ok = event.mimeData().data("item-type").toUInt()
            if PixItem.Image <= item_type <= PixItem.Sound:
                item = PixItem(item_type)
            elif OtherItem.Snow <= item_type <= OtherItem.Gabor:
                item = OtherItem(item_type)
                item.getInfo()
            else:
                return
            self.addItem(item)
            item.setPos(event.scenePos())
            item.setAttributes(self.attributes)
            self.update()
            self.itemAdd.emit(item.getName())
            action = Qt.MoveAction
            event.setDropAction(action)
            event.accept()
        else:
            event.ignore()

    def contextMenuEvent(self, event) -> None:
        it = self.itemAt(event.scenePos().x(), event.scenePos().y(), self.t)
        if it:
            self.clearSelection()
            it.setSelected(True)
            self.menu.exec_(event.screenPos())

    def setLineColor(self, color):
        for item in self.selectedItems():
            if isinstance(item, LineItem):
                item.setColor(color)

    def setItemColor(self, color):
        for item in self.selectedItems():
            if isinstance(item, DiaItem):
                item.setBrush(color)
                item.setItemColor(color.name())

    def setLineWidth(self, width):
        for item in self.selectedItems():
            if isinstance(item, LineItem):
                item.setWidth(width)

    def setMode(self, mode: int):
        self.my_mode = mode

    def mousePressEvent(self, event):
        if self.lasso:
            self.removeItem(self.lasso)
            self.lasso = None
        if event.button() == Qt.LeftButton:
            if self.my_mode == self.InsertLine:
                self.line = QGraphicsLineItem(QLineF(event.scenePos(),
                                                     event.scenePos()))
                self.line.setPen(QPen(self.line_color, 2))
                self.addItem(self.line)
            elif self.my_mode == self.SelectItem:
                x = event.scenePos().x()
                y = event.scenePos().y()
                self.lasso = Lasso(x, y)
                self.addItem(self.lasso)
        super(Scene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.my_mode == self.InsertLine and self.line:
            new_line = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(new_line)
        elif self.my_mode == self.MoveItem or self.my_mode == self.InsertItem:
            self.update()
            super(Scene, self).mouseMoveEvent(event)
        # 套索模式
        elif self.my_mode == self.SelectItem:
            self.lasso: Lasso
            x = event.scenePos().x()
            y = event.scenePos().y()
            if self.lasso is None:
                self.lasso = Lasso(x, y)
                self.addItem(self.lasso)
            self.lasso.draw(x, y)
            self.update()

            self.lasso.center = self.lasso.polygon().boundingRect().center()
            self.setSelectionArea(self.lasso.path, self.t)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.my_mode == self.InsertLine:
            item = LineItem(self.line.line())
            self.addItem(item)
            self.itemAdd.emit(item.getName())
            self.update()
            self.removeItem(self.line)
            self.line = None
        if self.lasso and self.my_mode == self.SelectItem:
            self.removeItem(self.lasso)
            self.lasso = None

        super(Scene, self).mouseReleaseEvent(mouseEvent)

    def getInfo(self):
        item_info: dict = {}
        for item in self.items():
            item_info[item.getName()] = item.getInfo()

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.clear()
            for k, v in properties.items():
                k: str
                if k.startswith("image"):
                    item = PixItem(PixItem.Image, k)
                elif k.startswith("text"):
                    item = PixItem(PixItem.Text, k)
                elif k.startswith("video"):
                    item = PixItem(PixItem.Video, k)
                elif k.startswith("sound"):
                    item = PixItem(PixItem.Sound, k)
                elif k.startswith("snow"):
                    item = OtherItem(OtherItem.Snow, k)
                elif k.startswith("gabor"):
                    item = OtherItem(OtherItem.Gabor, k)
                self.addItem(item)
                item.setProperties(v)

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for item in self.items():
            item.setAttributes(attributes)
