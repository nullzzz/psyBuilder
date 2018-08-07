from PyQt5.QtWidgets import QFrame, QTableWidget, QAbstractItemView, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


class Sign(QTableWidget):
    clicked = pyqtSignal()
    def __init__(self, parent=None, icon=""):
        super(Sign, self).__init__(parent)
        self.icon = icon
        # col设置为无法得到的数值, 用来记录最后一次出的列
        self.col = -2
        # 隐藏表头
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        # 隐藏scroll
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 其他美化
        self.setShowGrid(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        # 设置为一行
        self.setRowCount(1)
        self.setRowHeight(0, 35)

    def showIcon(self, col):
        label = QLabel()
        label.setPixmap(QPixmap(".\\.\\Image\\" + self.icon).scaledToHeight(35))
        label.setAlignment(Qt.AlignCenter)
        if col == -1:
            col = self.columnCount() - 1
        if self.col != col:
            if self.col != -2:
                self.removeCellWidget(0, self.col)
            self.setCellWidget(0, col, label)
            self.col = col

    def hideIcon(self):
        if self.col != -2:
            self.removeCellWidget(0, self.col)
            self.col = -2

    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass
