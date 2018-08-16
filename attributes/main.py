from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QDockWidget

from .attributesTable import AttributesTable


class Attributes(QDockWidget):
    def __init__(self, parent=None):
        super(Attributes, self).__init__(parent)
        # set UI
        self.setMaximumWidth(200)
        self.setMinimumWidth(150)
        self.attributes_table = AttributesTable()
        self.setFloating(False)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setWidget(self.attributes_table)

        self.setItem(0, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "2"))
        self.setItem(1, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "1"))
        self.setItem(2, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "4"))
        self.setItem(3, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "3"))

    def setItem(self, row, col, QTableWidgetItem):
        # set Row Count
        self.attributes_table.setRowCount(self.attributes_table.rowCount() + 1)
        self.attributes_table.setItem(row, col, QTableWidgetItem)
