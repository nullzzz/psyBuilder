from PyQt5.QtWidgets import QDockWidget
from .NameTable import NameTable
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon


class Attributes(QDockWidget):
    def __init__(self, parent=None):
        super(Attributes, self).__init__(parent)
        # set UI
        self.setWindowTitle("Attributes")
        self.setMaximumWidth(200)
        self.setMinimumWidth(150)
        self.tableWidget = NameTable()
        self.setFloating(False)
        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setWidget(self.tableWidget)

        self.setItem(0, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "2"))
        self.setItem(1, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "1"))
        self.setItem(2, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "4"))
        self.setItem(3, 0, QTableWidgetItem(QIcon(".\\Image\\arrows_up.png"), "3"))

    def setItem(self, row, col, QTableWidgetItem):
        # set Row Count
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(row, col, QTableWidgetItem)
