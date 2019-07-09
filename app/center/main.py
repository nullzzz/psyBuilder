from PyQt5.QtWidgets import QDockWidget

from .widget_tabs.main import WidgetTabs


class Center(QDockWidget):
    def __init__(self, parent=None):
        super(Center, self).__init__(parent)
        # set UI
        self.widget_tabs = WidgetTabs(self)
        self.setWidget(self.widget_tabs)

    def isFocused(self) -> bool:
        """

        :return:
        """
        try:
            return self.widget_tabs.currentWidget().widget_icon_area.widget_icon_table.focus
        except:
            return False
