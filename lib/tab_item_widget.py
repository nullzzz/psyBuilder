from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class TabItemWidget(QWidget):
    """
    base class for widgets which will be tab in tab widget

    you should complete all necessary function.
    """

    """
    signals
    """

    # you can show properties in Properties Window through this signal.
    propertiesChanged = pyqtSignal()
    # you can show loading dialog window through this signal
    waitStart = pyqtSignal()
    # you can end loading dialog window through this signal
    waitEnd = pyqtSignal()

    def __init__(self, widget_id: int, widget_name: str):
        super(TabItemWidget, self).__init__(None)
        # widget_id is used to distinguish different widgets
        self.widget_id = widget_id
        self.widget_name = widget_name

    """
    about properties and attributes
    """

    def getProperties(self) -> dict:
        """
        You should finish the job.

        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        return {}

    def getHiddenAttributes(self) -> list:
        """
        You should finish the job.

        every widget has global attributes and own attributes,
        we get global attributes through common function Func.getAttributes(widget_id) and
        we get widget's own attributes through this function.
        @return: dict of attributes
        """
        return []

    """
    about widget
    """

    def store(self):
        """
        You should finish the job.

        return necessary data for restoring this widget.
        @return:
        """
        return {}

    def restore(self, data) -> None:
        """
        You should finish the job.

        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """

    def copy(self, widget_id: int, widget_name: str):
        """
        You should finish the job.

        return a copy of this widget, and set the widget id and name of the copy.
        @param widget_id:
        @return:
        """
        return None

    def changeWidgetId(self, widget_id: int):
        """
        change this widget's widget id, because referable widget may be deleted and we
        need to change widget id.
        @param widget_id:
        @return:
        """
        self.widget_id = widget_id

    """
    other function may be needed to all, but I forget those.
    """
