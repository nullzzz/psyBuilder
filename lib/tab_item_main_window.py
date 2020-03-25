from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from app.func import Func


class TabItemMainWindow(QMainWindow):
    """
    base class for widgets which will be tab in tab widget

    you should complete all necessary function.
    """

    """
    signals
    """

    # you can show properties in Properties Window through this signal. (widget_id)
    propertiesChanged = pyqtSignal(str)
    tabClosed = pyqtSignal(str)
    # you can show loading dialog window through this signal
    waitStart = pyqtSignal()
    # you can end loading dialog window through this signal
    waitEnd = pyqtSignal()

    def __init__(self, widget_id: str, widget_name: str):
        super(TabItemMainWindow, self).__init__(None)
        # widget_id is used to distinguish different widgets
        self.widget_id = widget_id
        self.widget_name = widget_name
        self.default_properties: dict = {}

    def refresh(self):
        """
        update some things such as device information
        :return:
        """

    def setAttributes(self, attributes: list):
        """
        set completer.
        :param attributes:
        :return:
        """

    def getProperties(self, display: bool = True) -> dict:
        """
        You should finish the job
        get this widget's properties to show it in Properties Window.
        :param display: whether or not to display these properties in main window.
        :return: a dict of properties
        :rtype: dict
        """
        return {}

    def getUsingDeviceCount(self) -> int:
        """
        You should finish the job.

        return count of using device
        :return:
        :rtype: int
        """
        input_device: dict = self.default_properties.get("Input Devices", {})

        return len(input_device)

    def getHiddenAttributes(self) -> list:
        """
        You should finish the job.

        every widget has global attributes and own attributes,
        we get global attributes through common function Func.getAttributes(widget_id) and
        we get widget's own attributes through this function.
        Its values are also depended on device whether used.
        used:
        not used:
        :return: list of attributes
        """
        if self.getUsingDeviceCount():
            return ["respOnSettingTime", "acc", "resp", "rt"]
        return ["OnSettingTime"]

    """
    about widget
    """

    def changeWidgetId(self, widget_id: str):
        """
        change this widget's widget id, because referable widget may be deleted and we
        need to change widget id.
        :param widget_id:
        :return:
        """
        self.widget_id = widget_id

    def store(self):
        """
        You should finish the job.

        return necessary data for restoring this widget.
        :return:
        """

    def restore(self, data) -> None:
        """
        You should finish the job.

        restore this widget according to data.
        :param data: necessary data for restoring this widget
        :return:
        """

    def clone(self, new_widget_id: str, new_widget_name: str):
        """
        You should finish the job.

        return a copy of this widget, and set the widget id and name of the copy.
        :param new_widget_id:
        :param new_widget_name:
        :return: a new widget with new name and id.
        """

    """
    other function may be needed to all, but I forget those.
    """

    def __repr__(self):
        return f"{Func.getWidgetType(self.widget_id)} [{self.widget_id}: {self.widget_name}]"
