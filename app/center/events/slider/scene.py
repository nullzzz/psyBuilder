from PyQt5.QtCore import pyqtSignal, Qt, QLineF, QPointF
from PyQt5.QtGui import QPen, QTransform
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem, QGraphicsItem

from app.info import Info
from .item.openglItem import GLItem
from ...events.slider.item import *


class Scene(QGraphicsScene):
    InsertItem, InsertLine, MoveItem, SelectItem = range(4)

    itemAdd = pyqtSignal(str)
    itemSelected = pyqtSignal()

    def __init__(self, parent=None):
        super(Scene, self).__init__(parent)

        # self.addLine(0, 0, 100, 100)
        self.my_mode = Scene.InsertItem

        self.attributes: list = []
        self.line = None
        self.lasso = None

        self.line_color = Qt.black
        self.fill_color = Qt.transparent
        self.border_color = Qt.black
        self.border_width = 2

        self.t = QTransform()

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
            # if self.my_mode == self.InsertItem:
            item_type, ok = event.mimeData().data("item-type").toUInt()
            if TextItem.Text == item_type:
                item = TextItem(item_type)
            elif PixItem.Image <= item_type <= PixItem.Sound:
                item = PixItem(item_type)
            elif OtherItem.Snow <= item_type <= OtherItem.Gabor:
                item = OtherItem(item_type)
                # item.getInfo()
            elif DiaItem.Polygon <= item_type <= DiaItem.Rect:
                item = DiaItem(item_type)
            else:
                item = GLItem(item_type)
            self.addItem(item)
            item.setPos(event.scenePos())  # move the item in the scene

            item.setPosition()  # update the general tab
            item.updateInfo()  # get default_property from general tab

            # todo 苟且一下
            if item_type == DiaItem.Polygon:
                # item.setPosition()
                item.pro_window.general.add_bt.click()
                item.pro_window.general.del_bt.click()

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
            if isinstance(item, LineItem) or isinstance(item, DiaItem):
                item.setLineColor(color)

    def setItemColor(self, color):
        for item in self.selectedItems():
            if isinstance(item, DiaItem):
                item.setItemColor(color)  # update the default properties in GeneralTab

    def setLineWidth(self, width):
        for item in self.selectedItems():
            if isinstance(item, LineItem) or isinstance(item, DiaItem):
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
            line = self.line.line()
            p2 = event.scenePos()
            # straight line
            if event.modifiers() == Qt.ControlModifier:
                dx = p2.x() - line.x1()
                dy = p2.y() - line.y1()
                if dx < 10:
                    p2.setX(line.x1())
                if dy < 10:
                    p2.setY(line.y1())
            new_line = QLineF(line.p1(), p2)
            self.line.setLine(new_line)
        elif self.my_mode == self.MoveItem or self.my_mode == self.InsertItem:
            self.update()
            super(Scene, self).mouseMoveEvent(event)
        # 套索模式
        elif self.my_mode == self.SelectItem and self.lasso:
            self.lasso: Lasso
            x = event.scenePos().x()
            y = event.scenePos().y()
            self.lasso.draw(x, y)
            self.update()

            self.lasso.center = self.lasso.polygon().boundingRect().center()
            self.setSelectionArea(self.lasso.path, self.t)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.my_mode == self.InsertLine:
            item = LineItem(LineItem.Line)
            l: QLineF = self.line.line()
            cx, cy = self.line.line().center().x(), self.line.line().center().y()
            item.setPos(self.line.line().center())
            line = QLineF(l.x1() - cx, l.y1() - cy, l.x2() - cx, l.y2() - cy)
            item.setLine(line)
            item.setPosition()
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
            item.setPosition()
            item_info[item.getName()] = item.getInfo()
        return item_info

    def setProperties(self, properties: dict):
        self.clear()
        for k, v in properties.items():
            k: str
            if k.startswith(Info.ITEM_IMAGE):
                item = PixItem(PixItem.Image, k)
            elif k.startswith(Info.ITEM_TEXT):
                item = TextItem(TextItem.Text, k)
            elif k.startswith(Info.ITEM_VIDEO):
                item = PixItem(PixItem.Video, k)
            elif k.startswith(Info.ITEM_SOUND):
                item = PixItem(PixItem.Sound, k)
            elif k.startswith(Info.ITEM_SNOW):
                item = OtherItem(OtherItem.Snow, k)
            elif k.startswith(Info.ITEM_GABOR):
                item = OtherItem(OtherItem.Gabor, k)
            elif k.startswith(Info.ITEM_POLYGON):
                item = DiaItem(DiaItem.Polygon, k)
            elif k.startswith(Info.ITEM_ARC):
                item = DiaItem(DiaItem.Arc, k)
            elif k.startswith(Info.ITEM_RECT):
                item = DiaItem(DiaItem.Rect, k)
            elif k.startswith(Info.ITEM_CIRCLE):
                item = DiaItem(DiaItem.Circle, k)
            elif k.startswith(Info.ITEM_LINE):
                item = LineItem(LineItem.Line, k)

            self.addItem(item)
            item.setProperties(v)
            item.apply()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for item in self.items():
            item.setAttributes(attributes)

    def copyItem(self, item: QGraphicsItem):
        new_item = item.clone()
        new_pos = QPointF(item.scenePos().x() + 20, item.scenePos().y() + 20)
        self.addItem(new_item)
        new_item.setPos(new_pos)
        new_item.setPosition()
        new_item.updateInfo()
        new_item.setAttributes(self.attributes)
        self.update()
        self.itemAdd.emit(new_item.getName())

        item.setSelected(False)
        new_item.setSelected(True)
