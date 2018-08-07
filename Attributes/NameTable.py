from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QIcon, QFont
from NoDashDelegate import NoDashDelegate



class NameTable(QTableWidget):
    def __init__(self, parent=None):
        super(NameTable, self).__init__(parent)
        # 设置每一行Icon大小
        self.setIconSize(QSize(15, 15))
        # set row and col count
        self.setColumnCount(1)
        self.setRowCount(0)
        # 设置网格及列头
        # self.setShowGrid(False)
        self.setItemDelegate(NoDashDelegate())
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(["Name"])
        headerFont = QFont("Tahoma", 13, QFont.Bold)
        self.horizontalHeaderItem(0).setFont(headerFont)
        # 设置排序相关
        self.asc = True
        self.setSortingEnabled(True)
        self.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicatorShown(False)
        self.horizontalHeader().sectionClicked.connect(self.sortChangeIcon)
        # 设置tableWidget为可拖动
        self.setDragEnabled(True)

    # 根据顺序来改变Icon
    def sortChangeIcon(self, col):
        if self.asc:
            for i in range(0, self.rowCount()):
                self.item(i, col).setIcon(QIcon(".\\Image\\arrows_down.png"))
            self.asc = False
        else:
            for i in range(0, self.rowCount()):
                self.item(i, col).setIcon(QIcon(".\\Image\\arrows_up.png"))
            self.asc = True

    # 重写startDrag实现拖拽功能
    # def startDrag(self, dropActions):
    #     item = self.currentItem()
    #     data = QByteArray()
    #     stream = QDataStream(data, QIODevice.WriteOnly)
    #     stream.writeQString(item.text())
    #     mimeData = QMimeData()
    #     mimeData.setData("application/x-text", data)
    #     drag = QDrag(self)
    #     drag.setMimeData(mimeData)
    #     drag.setHotSpot(QPoint(12, 12))
    #     drag.exec(Qt.CopyAction)
