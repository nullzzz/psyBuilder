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

    def showProperties(self, wid_or_data):
        """
        将控件的properties显示
        :param wid_or_data: 
        :return: 
        """
        if isinstance(wid_or_data, str):
            properties = Func.getProperties(wid_or_data, True)
        elif isinstance(wid_or_data, dict):
            properties = wid_or_data
        else:
            raise ValueError
        # 将properties table清空
        while self.properties_table.rowCount():
            self.properties_table.removeRow(0)
        # 将properties变成从小到大排序的list
        sorted_properties = sorted(properties.items(), key=lambda x: x[0])
        for key, value in sorted_properties:
            self.properties_table.addProperty(key, str(value))
