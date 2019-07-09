from PyQt5.QtCore import Qt, QSize, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from PyQt5.QtGui import QIcon, QFont, QDrag
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from app.func import Func
from app.info import Info
from app.lib import NoDash


class AttributesTable(QTableWidget):
    def __init__(self, parent=None):
        super(AttributesTable, self).__init__(parent)
        # 美化
        self.setItemDelegate(NoDash())
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        # 基础设置
        self.setColumnCount(1)
        self.setRowCount(0)
        self.setIconSize(QSize(15, 15))
        self.setHorizontalHeaderLabels(["sort"])
        self.horizontalHeaderItem(0).setFont(QFont("Tahoma", 12))
        self.setDragEnabled(True)
        # 排序相关
        self.asc = True
        self.setSortingEnabled(True)
        self.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicatorShown(False)
        self.horizontalHeader().sectionClicked.connect(self.changeSortIcon)

    def sizeHint(self):
        return QSize(10, 100)

    def changeSortIcon(self, col):
        if self.asc:
            for i in range(0, self.rowCount()):
                self.item(i, col).setIcon(QIcon(Func.getImage("arrows_down.png")))
            self.asc = False
        else:
            for i in range(0, self.rowCount()):
                self.item(i, col).setIcon(QIcon(Func.getImage("arrows_up.png")))
            self.asc = True

    def addAttribute(self, attribute_name):
        self.insertRow(self.rowCount())
        item = QTableWidgetItem(attribute_name)
        item.setFlags(Qt.ItemIsEnabled)
        self.setItem(self.rowCount() - 1, 0, item)

    def mouseMoveEvent(self, e):
        attribute: QTableWidgetItem = self.itemAt(e.pos())
        if attribute:
            text: str = attribute.text()
            pix = Func.getTrackingPix(text)

            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeQString(text)

            mime_data = QMimeData()
            mime_data.setData(Info.FromAttributeToLineEdit, data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(pix)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec()
