from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from lib import TableWidget


class PropertiesTable(TableWidget):
    """

    """

    def __init__(self):
        super(PropertiesTable, self).__init__(None)
        # about its ui
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        # set two columns
        self.setColumnCount(2)

    def addProperty(self, property_name: str, property_value: str):
        """
        add property into table
        @param property_name:
        @param property_value:
        @return:
        """
        # add new row
        self.insertRow(self.rowCount())
        # set item
        name_item = QTableWidgetItem(property_name)
        name_item.setFlags(Qt.ItemIsEnabled)
        name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setItem(self.rowCount() - 1, 0, name_item)
        value_item = QTableWidgetItem(property_value)
        value_item.setFlags(Qt.ItemIsEnabled)
        value_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setItem(self.rowCount() - 1, 1, value_item)

    def resizeEvent(self, QResizeEvent):
        """
        resize width of col
        @param QResizeEvent:
        @return:
        """
        self.setColumnWidth(0, self.width() / 2)
