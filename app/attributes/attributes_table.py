from PyQt5.QtCore import Qt, QSize, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QTableWidgetItem

from app.func import Func
from app.info import Info
from lib import TableWidget


class AttributesTable(TableWidget):
    """

    """

    def __init__(self):
        super(AttributesTable, self).__init__(None)
        # about its ui
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        self.setIconSize(QSize(15, 15))
        # set one column and header sort
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(["Sort"])
        self.horizontalHeader().setSortIndicatorShown(False)
        # it can sort
        self.sort_order = 1
        self.setSortingEnabled(True)
        self.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        # set it draggable
        self.setDragEnabled(True)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        :return:
        """
        self.horizontalHeader().sectionClicked.connect(self.changeSortOrder)

    def changeSortOrder(self, col: int):
        """
        change sort order
        :return:
        """
        self.sort_order = not self.sort_order
        image_path = "attributes/asc.png"
        if not self.sort_order:
            image_path = "attributes/desc.png"
        for i in range(0, self.rowCount()):
            self.item(i, col).setIcon(Func.getImagePath(image_path, 1))

    def addAttribute(self, attribute: str):
        """
        add an attribute into table
        :param attribute:
        :return:
        """
        # add new row
        self.insertRow(self.rowCount())
        # set item
        item = QTableWidgetItem(attribute)
        item.setFlags(Qt.ItemIsEnabled)
        self.setItem(self.rowCount() - 1, 0, item)

    def mouseMoveEvent(self, e):
        """

        :param e:
        :return:
        """
        item: QTableWidgetItem = self.itemAt(e.pos())
        if item:
            text: str = item.text()
            pix = Func.getTrackingPix(text)
            data = QByteArray()
            stream = QDataStream(data, QIODevice.WriteOnly)
            stream.writeQString(text)
            mime_data = QMimeData()
            mime_data.setData(Info.AttributesToLineEdit, data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(pix)
            drag.setHotSpot(QPoint(12, 12))
            drag.exec()
