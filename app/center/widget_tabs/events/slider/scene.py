from PyQt5.QtCore import (pyqtSignal, QLineF, QPointF, Qt)
from PyQt5.QtGui import (QFont, QPen)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsLineItem, QGraphicsScene, QGraphicsTextItem,QGraphicsPixmapItem)
from app.center.widget_tabs.events.slider.item.diaItem import DiaItem
from app.center.widget_tabs.events.slider.item.diagramTextItem import DiagramTextItem
from app.center.widget_tabs.events.slider.item.pixItem import PixItem


class Scene(QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem = range(4)

    itemInserted = pyqtSignal(DiaItem)
    textInserted = pyqtSignal(QGraphicsTextItem)
    itemSelected = pyqtSignal(QGraphicsItem)
    pixItemInserted = pyqtSignal(QGraphicsPixmapItem)
    DitemSelected = pyqtSignal(dict)

    def __init__(self, itemMenu, attributes, parent=None):
        super(Scene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.myItemType = DiaItem.PolygonStim
        self.attributes = attributes
        self.line = None
        self.textItem = None
        self.myItemColor = Qt.white
        self.myTextColor = Qt.black
        self.myLineColor = Qt.black
        self.myFont = QFont()
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
            if self.myMode == self.InsertItem:
                if self.myItemType < 4:
                    # 参数：图形的形状，右键菜单
                    item = DiaItem(self.myItemType, self.myItemMenu, self.attributes)
                    pen = item.pen()
                    pen.setColor(self.myLineColor)
                    pen.setWidth(self.myLineWidth)
                    item.setBrush(self.myItemColor)
                    item.setPen(pen)
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self.itemInserted.emit(item)
                    self.update()
                # 添加图片
                else:
                    item = PixItem(self.myItemType, self.myItemMenu, self.attributes)
                    self.addItem(item)
                    item.setPos(event.scenePos())
                    self.pixItemInserted.emit(item)
                    self.update()
            elif self.myMode == self.InsertText:
                textItem = DiagramTextItem()
                textItem.setFont(self.myFont)
                textItem.setPlainText('Text')
                textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
                textItem.setZValue(1000.0)  # a possible reason why text is always on the front
                textItem.lostFocus.connect(self.editorLostFocus)
                textItem.selectedChange.connect(self.itemSelected)
                self.addItem(textItem)
                textItem.setDefaultTextColor(self.myTextColor)
                textItem.setPos(event.scenePos())
                self.textInserted.emit(textItem)

            action = Qt.MoveAction
            event.setDropAction(action)
            event.accept()
        else:
            event.ignore()

    def setLineColor(self, color):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            pen = item.pen()
            pen.setColor(color)
            item.setPen(pen)
            item.setLineColor(color.name())

    def setLineWidth(self, size):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            pen = item.pen()
            pen.setWidth(size)
            item.setPen(pen)
            item.setLineWidth(size)
            self.update()

    def setTextColor(self, color):
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(color)

    def setItemColor(self, color):
        if self.isItemChange(DiaItem):
            item = self.selectedItems()[0]
            item.setBrush(color)
            item.setItemColor(color.name())

    def setFont(self, font):
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setFont(font)

    def setMode(self, mode):
        self.myMode = mode

    def setItemType(self, type):
        self.myItemType = type

    def editorLostFocus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        # BUG
        # if item.toPlainText():
        if not item.toPlainText():
            self.removeItem(item)
            item.deleteLater()

    def mousePressEvent(self, mouseEvent):
        d = {'itemcolor': 'white',
             'linecolor': 'black',
             'linewidth': 1}
        if self.selectedItems() and self.isItemChange(DiaItem):
            it = self.selectedItems()[0]
            d = {'itemcolor': it.ItemColor,
                 'linecolor': it.LineColor,
                 'linewidth': it.LineWidth}
            self.DitemSelected.emit(d)

        if (mouseEvent.button() != Qt.LeftButton):
            return

        if self.myMode == self.InsertLine:
            self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(),
                                                 mouseEvent.scenePos()))
            self.line.setPen(QPen(self.myLineColor, 2))
            self.addItem(self.line)

        self.DitemSelected.emit(d)
        super(Scene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.InsertLine and self.line:
            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            self.update()
            super(Scene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.myMode == self.InsertLine:
            p1 = self.line.line().p1()
            p2 = self.line.line().p2()
            p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
            p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
            center = QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)
            item = DiaItem(DiaItem.Line, self.myItemMenu, self.attributes, p3, p4)
            self.addItem(item)
            item.setPos(center)
            self.update()
            self.removeItem(self.line)
            self.line = None

        self.line = None
        super(Scene, self).mouseReleaseEvent(mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False
