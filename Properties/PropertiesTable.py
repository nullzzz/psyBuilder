from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from NoDashDelegate import NoDashDelegate


class PropertiesTable(QTableWidget):
    def __init__(self, parent=None):
        super(PropertiesTable, self).__init__(parent)

        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(NoDashDelegate())
        self.horizontalHeader().setStretchLastSection(True)

        # 两列
        self.setColumnCount(2)

    def addProperty(self, name, property):
        self.insertRow(self.rowCount())

        nameItem = QTableWidgetItem(name)
        nameItem.setTextAlignment(Qt.AlignCenter)
        nameItem.setFlags(Qt.ItemIsEditable)
        nameItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        propertyItem = QTableWidgetItem(property)
        propertyItem.setTextAlignment(Qt.AlignCenter)
        propertyItem.setFlags(Qt.ItemIsEditable)
        propertyItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setItem(self.rowCount() - 1, 0, nameItem)
        self.setItem(self.rowCount() - 1, 1, propertyItem)
