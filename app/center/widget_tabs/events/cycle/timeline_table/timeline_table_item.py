import re

from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem


class TimelineTableItem(QTableWidgetItem):
    def __init__(self, text: str = ""):
        """
        init
        :param text: 
        """
        if text:
            super(TimelineTableItem, self).__init__(text)
            # 如果是变量形式，则变为蓝色
            if re.search(r"^\[.*?\]", text):
                self.setForeground(QBrush(QColor(0, 0, 255)))
            else:
                self.setForeground(QBrush(QColor(0, 0, 0)))
        else:
            super(TimelineTableItem, self).__init__()

    def setText(self, text: str):
        """
        设置text
        :param text:
        :return:
        """
        super(TimelineTableItem, self).setText(text)
        if re.search(r"^\[.*?\]", text):
            self.setForeground(QBrush(QColor(0, 0, 255)))
        else:
            self.setForeground(QBrush(QColor(0, 0, 0)))
