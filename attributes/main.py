from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget

from .attributesTable import AttributesTable
from .attributeItem import AttributeItem


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

    def setAttributeItem(self, row, col, attribute_name, attribute_value):
        try:
            # set Row Count
            attribute = AttributeItem(attribute_name, attribute_value)
            if row == self.attributes_table.rowCount():
                self.attributes_table.setRowCount(self.attributes_table.rowCount() + 1)
            self.attributes_table.setItem(row, col, attribute)
        except Exception as e:
            print(f"error {e} happens in set attribute")

    def showAttributes(self, attributes):
        try:
            # 讲attribute table初始化
            for row in range(0, self.attributes_table.rowCount()):
                self.attributes_table.removeRow(0)
            for name in attributes:
                self.setAttributeItem(self.attributes_table.rowCount(), 0, name, attributes[name])
        except Exception:
            print("error happens show timeline attributes. [attributes/main.py]")