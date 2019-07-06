from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout

from app.center.widget_tabs.timeline.widget_icon_area.main import WidgetIconArea
from app.center.widget_tabs.timeline.widget_icon_bar import WidgetIconBar


class Timeline(QWidget):
    # 无用信号，只是为了统一串信号用
    propertiesChange = pyqtSignal(str)

    def __init__(self, parent=None, widget_id: str = ""):
        """
        init
        :param parent:
        :param widget_id:
        """
        super(Timeline, self).__init__(parent)
        # id
        self.widget_id = widget_id
        self.current_wid = widget_id

        # widgets
        self.widget_icon_bar = WidgetIconBar(self)
        self.widget_icon_area = WidgetIconArea(self, self.widget_id)
        grid = QGridLayout(self)
        grid.addWidget(self.widget_icon_bar, 0, 0, 1, 1)
        grid.addWidget(self.widget_icon_area, 1, 0, 1, 1)
        self.setLayout(grid)

    def getProperties(self):
        return {}

    def getInfo(self):
        """
        返回控件复原所需信息
        :return:
        """
        info = {'widget_icon_area': self.widget_icon_area.getInfo()}
        return info

    def restore(self, info):
        """
        复原控件
        :param info:
        :return:
        """
        self.widget_icon_area.restore(info['widget_icon_area'])
