from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from app.lib import NoDash


class PropertiesTable(QTableWidget):
    def __init__(self, parent=None):
        super(PropertiesTable, self).__init__(parent)
        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setItemDelegate(NoDash())
        self.horizontalHeader().setStretchLastSection(True)
        # 基础设置
        self.setColumnCount(2)
        self.setColumnWidth(0, 130)

    def addProperty(self, property_name: str, property_value: str):
        try:
            self.insertRow(self.rowCount())

            property_name_item = QTableWidgetItem(property_name)
            property_name_item.setTextAlignment(Qt.AlignCenter)
            property_name_item.setFlags(Qt.ItemIsEnabled)
            property_name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.setItem(self.rowCount() - 1, 0, property_name_item)

            property_value_item = QTableWidgetItem(property_value)
            property_value_item.setTextAlignment(Qt.AlignCenter)
            property_value_item.setFlags(Qt.ItemIsEnabled)
            property_value_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.setItem(self.rowCount() - 1, 1, property_value_item)
        except Exception as e:
            print(f"error {e} happens in add property. [properties/properties_table.py]")
