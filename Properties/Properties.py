from PyQt5.QtWidgets import QWidget, QDockWidget, QComboBox, QTextEdit, QGridLayout
from .PropertiesTable import PropertiesTable


class Properties(QDockWidget):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        # widget
        self.widget = QWidget(self)
        self.combo = QComboBox(self.widget)
        self.propertiesTable = PropertiesTable(self.widget)
        self.textEdit = QTextEdit()
        self.textEdit.setMaximumHeight(100)

        grid = QGridLayout(self.widget)

        grid.addWidget(self.combo, 0, 0, 1, 1)
        grid.addWidget(self.propertiesTable, 1, 0, 1, 1)
        grid.addWidget(self.textEdit, 2, 0, 1, 1)

        self.widget.setLayout(grid)
        self.setWidget(self.widget)

        for i in range(0, 10):
            self.propertiesTable.addProperty(" ", " ")

    def setProperties(self, properties):
        # 讲table初始化
        for row in range(0, self.propertiesTable.rowCount()):
            self.propertiesTable.removeRow(0)
        # 将properties变成从小到大排序的list
        sortedProperties = sorted(properties.items(), key=lambda x:x[0])
        for key, value in sortedProperties:
            self.propertiesTable.addProperty(key, str(value))
        # 为了美观, 保证至少十行
        if len(properties) < 10:
            for i in range(len(properties), 10):
                self.propertiesTable.addProperty("", "")

