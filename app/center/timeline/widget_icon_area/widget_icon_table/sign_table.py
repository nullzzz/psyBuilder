from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QTableWidget, QAbstractItemView, QLabel

from app.func import Func


class SignTable(QTableWidget):
    def __init__(self, parent=None, sign=""):
        super(SignTable, self).__init__(parent)
        self.sign = sign

        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setShowGrid(False)
        self.setFrameShape(QFrame.NoFrame)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setStyleSheet("background-color:transparent")

        # 初始化
        # col用来记录最后一次sign出现在的col
        self.last_show_col = -2
        # 设置为一行
        self.setRowCount(1)
        self.setRowHeight(0, 80)

    def showSign(self, col):
        try:
            sign = QLabel()
            sign.setPixmap(QPixmap(Func.getImage(self.sign)).scaledToHeight(40))
            sign.setAlignment(Qt.AlignCenter)
            if col == -1:
                col = self.columnCount() - 1
            if self.last_show_col != col:
                if self.last_show_col != -2:
                    self.removeCellWidget(0, self.last_show_col)
                self.setCellWidget(0, col, sign)
                self.last_show_col = col
        except Exception as e:
            print(f"error {e} happens in show sign. [signTable.py]")

    def hideSign(self):
        try:
            if self.last_show_col != -2:
                self.removeCellWidget(0, self.last_show_col)
                self.last_show_col = -2
        except Exception as e:
            print(f"error {e} happens in hide sign. [signTable.py]")

    # 用以消除其双击事件
    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass
