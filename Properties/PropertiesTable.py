from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from noDash import NoDash


class PropertiesTable(QTableWidget):
    def __init__(self, parent=None):
        super(PropertiesTable, self).__init__(parent)

        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(NoDash())
        self.horizontalHeader().setStretchLastSection(True)

        # 两列
        self.setColumnCount(2)

    def addProperty(self, name, property):
        self.insertRow(self.rowCount())

        name_item = QTableWidgetItem(name)
        name_item.setTextAlignment(Qt.AlignCenter)
        name_item.setFlags(Qt.ItemIsEditable)
        name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        property_item = QTableWidgetItem(property)
        property_item.setTextAlignment(Qt.AlignCenter)
        property_item.setFlags(Qt.ItemIsEditable)
        property_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setItem(self.rowCount() - 1, 0, name_item)
        self.setItem(self.rowCount() - 1, 1, property_item)
