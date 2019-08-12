from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsItem


class Lasso(QGraphicsPolygonItem):

    def __init__(self, x, y, parent=None):
        super(Lasso, self).__init__(parent=parent)
        path = QPainterPath()

        path.addRect(QRectF(x, y, 1, 1))
        self.rect = path.toFillPolygon()

        self.setPolygon(self.rect)
        # self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.resizingFlag = True
        self.center = QPointF(0, 0)

    # def boundingRect(self):
    #     return self.polygon().boundingRect().adjusted(-self.pen().width(),
    #                                                   -self.pen().width(),
    #                                                   self.pen().width(),
    #                                                   self.pen().width())

    # def mouseMoveEvent(self, mouseEvent):
    #     x = mouseEvent.pos().x()
    #     y = mouseEvent.pos().y()
    #
    #     rect0 = self.polygon().boundingRect()
    #
    #     if self.resizingFlag:
    #         x0 = rect0.left()
    #         y0 = rect0.top()
    #
    #         path = QPainterPath()
    #         cRect = QRectF(x0, y0, x - x0, y - y0)
    #
    #         path.addRect(cRect)
    #
    #         self.rect = path.toFillPolygon()
    #         self.setPolygon(self.rect)
    #         self.update()
    #
    #         self.center = self.polygon().boundingRect().center()
    #     else:
    #         super(Lasso, self).mouseMoveEvent(mouseEvent)

    # def mouseReleaseEvent(self, mouseEvent):
    #     self.unsetCursor()
    #     self.hide()
    #     self.resizingFlag = False
    #     super(Lasso, self).mouseReleaseEvent(mouseEvent)

    # def contextMenuEvent(self, event):
    #     self.scene().clearSelection()
    #     self.setSelected(True)
