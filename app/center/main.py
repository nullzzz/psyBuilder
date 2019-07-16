from PyQt5.QtWidgets import QDockWidget

from app.info import Info
from .widget_tabs.main import WidgetTabs


class Center(QDockWidget):
    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # set UI
        self.widget_tabs = WidgetTabs(self)
        self.setWidget(self.widget_tabs)

    def isFocused(self) -> bool:
        """
        返回当前焦点在何窗口
        :return:
        """
        try:
            if self.widget_tabs.currentWidget().widget_icon_area.widget_icon_table.focus:
                return Info.TimelineFocused
            return Info.NotFocused
        except:
            try:
                if self.widget_tabs.currentWidget().timeline_table.focus:
                    return Info.CycleFocused
                return Info.NotFocused
            except:
                return Info.NotFocused
