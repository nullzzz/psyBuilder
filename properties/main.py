from PyQt5.QtWidgets import QWidget, QDockWidget, QComboBox, QTextEdit, QGridLayout
from .propertiesTable import PropertiesTable


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.setMaximumWidth(300)


class Properties(QDockWidget):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        # widget
        self.my_widget = MyWidget(self)
        self.combo = QComboBox(self.my_widget)
        self.properties_table = PropertiesTable(self.my_widget)
        self.text_edit = QTextEdit()
        self.text_edit.setMaximumHeight(100)

        grid = QGridLayout(self.my_widget)

        grid.addWidget(self.combo, 0, 0, 1, 1)
        grid.addWidget(self.properties_table, 1, 0, 1, 1)
        grid.addWidget(self.text_edit, 2, 0, 1, 1)

        self.my_widget.setLayout(grid)
        self.setWidget(self.my_widget)

        for i in range(0, 10):
            self.properties_table.addProperty(" ", " ")

    def showProperties(self, properties):
        try:
            # 讲table初始化
            for row in range(0, self.properties_table.rowCount()):
                self.properties_table.removeRow(0)
            # 将properties变成从小到大排序的list
            sorted_properties = sorted(properties.items(), key=lambda x: x[0])
            for key, value in sorted_properties:
                self.properties_table.addProperty(key, str(value))
            # 为了美观, 保证至少十行
            if len(properties) < 10:
                for i in range(len(properties), 10):
                    self.properties_table.addProperty("", "")
        except Exception:
            print("error happens in show properties. [properties/main.py]")
