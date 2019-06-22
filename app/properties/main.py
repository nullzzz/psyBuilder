from PyQt5.QtWidgets import QDockWidget

from app.func import Func
from app.lib import SizeContainerWidget
from .properties_table import PropertiesTable


class Properties(QDockWidget):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        # 美化
        # widget
        self.frame_widget = QDockWidget
        self.properties_table = PropertiesTable(self)
        size_container_widget = SizeContainerWidget()
        size_container_widget.setWidget(self.properties_table)
        self.setWidget(size_container_widget)

    def showProperties(self, widget_pro):
        if isinstance(widget_pro, str):
            properties = Func.getProperties(widget_pro)
        elif isinstance(widget_pro, dict):
            properties = widget_pro
        else:
            raise ValueError
        # 将properties table清空
        while self.properties_table.rowCount():
            self.properties_table.removeRow(0)
        # 将properties变成从小到大排序的list
        sorted_properties = sorted(properties.items(), key=lambda x: x[0])
        for key, value in sorted_properties:
            self.properties_table.addProperty(key, str(value))
