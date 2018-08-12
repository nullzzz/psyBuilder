from PyQt5.QtWidgets import QWidget, QDockWidget, QComboBox, QTextEdit, QGridLayout
from PyQt5.QtCore import QSize
from .PropertiesTable import PropertiesTable


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.setMaximumWidth(300)


class Properties(QDockWidget):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        # widget
        self.myWidget = MyWidget(self)
        self.combo = QComboBox(self.myWidget)
        self.propertiesTable = PropertiesTable(self.myWidget)
        self.textEdit = QTextEdit()
        self.textEdit.setMaximumHeight(100)

        grid = QGridLayout(self.myWidget)

        grid.addWidget(self.combo, 0, 0, 1, 1)
        grid.addWidget(self.propertiesTable, 1, 0, 1, 1)
        grid.addWidget(self.textEdit, 2, 0, 1, 1)

        self.myWidget.setLayout(grid)
        self.setWidget(self.myWidget)

        for i in range(0, 10):
            self.propertiesTable.addProperty(" ", " ")

    def setProperties(self, properties):
        # 讲table初始化
        for row in range(0, self.propertiesTable.rowCount()):
            self.propertiesTable.removeRow(0)
        # 将properties变成从小到大排序的list
        sortedProperties = sorted(properties.items(), key=lambda x: x[0])
        for key, value in sortedProperties:
            self.propertiesTable.addProperty(key, str(value))
        # 为了美观, 保证至少十行
        if len(properties) < 10:
            for i in range(len(properties), 10):
                self.propertiesTable.addProperty("", "")
