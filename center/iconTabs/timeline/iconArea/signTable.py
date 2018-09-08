from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QTableWidget, QAbstractItemView, QLabel


class SignTable(QTableWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None, sign=""):
        super(SignTable, self).__init__(parent)
        self.sign = sign
        # col用来记录最后一次sign出现在的col
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
        self.setStyleSheet("background-color:transparent")
        # 设置为一行
        self.setRowCount(1)
        self.setRowHeight(0, 80)

    def showSign(self, col):
        try:
            sign = QLabel()
            sign.setPixmap(QPixmap(".\\.\\.\\Image\\" + self.sign).scaledToHeight(40))
            sign.setAlignment(Qt.AlignCenter)
            if col == -1:
                col = self.columnCount() - 1
            if self.col != col:
                if self.col != -2:
                    self.removeCellWidget(0, self.col)
                self.setCellWidget(0, col, sign)
                self.col = col
        except Exception:
            print("error happens in show sign. [signTable.py]")

    def hideSign(self):
        try:
            if self.col != -2:
                self.removeCellWidget(0, self.col)
                self.col = -2
        except Exception:
            print("error happens in hide sign. [signTable.py]")

    # 用以消除其双击事件
    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass