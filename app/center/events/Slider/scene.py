from PyQt5.QtCore import pyqtSignal, Qt, QLineF
from PyQt5.QtGui import QPen, QTransform, QKeyEvent
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsLineItem

from app.info import Info
from ...events.Slider.item.diaItem import DiaItem
from ...events.Slider.item.lasso import Lasso
from ...events.Slider.item.linItem import LineItem
from ...events.Slider.item.otherItem import OtherItem
from ...events.Slider.item.pixItem import PixItem
from ...events.Slider.item.textItem import TextItem


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
                return
            self.addItem(item)
            item.setPos(event.scenePos())  # move the item in the scene

            item.setPosition()  # update the general tab
            item.getInfo()  # get default_property from general tab

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
                item.setColor(color)

    def setItemColor(self, color):
        for item in self.selectedItems():
            if isinstance(item, DiaItem):
                item.setBrush(color)
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
            new_line = QLineF(self.line.line().p1(), event.scenePos())
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
            item = LineItem(self.line.line())
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
            item_info[item.getName()] = item.updateInfo()
        return item_info

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
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
                    x1: str = v.get("X1")
                    y1: str = v.get("Y1")
                    x2: str = v.get("X2")
                    y2: str = v.get("Y2")
                    if x1.startswith("[") or x2.startswith("[") or y1.startswith("[") or y2.startswith("["):
                        line = QLineF(100, 100, 200, 200)
                    else:
                        line = QLineF(float(x1), float(y1), float(x2), float(y2))
                    item = LineItem(line, k)
                    item.setLine(line)

                self.addItem(item)
                item.setProperties(v)
                item.apply()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for item in self.items():
            item.setAttributes(attributes)
