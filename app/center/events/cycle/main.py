from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction

from app.func import Func
from app.info import Info
from lib import TabItemMainWindow
from .cycle_table import CycleTable
from .properties import Properties


class Cycle(TabItemMainWindow):
    """

    """

    # when add new timeline, emit signal(parent_widget_id, widget_id, widget_name, index)
    itemAdded = pyqtSignal(int, int, str, int)
    # when delete signals, emit signal(origin_widget, widget_id)
    itemDeleted = pyqtSignal(int, int)

    def __init__(self, widget_id: int, widget_name: str):
        super(Cycle, self).__init__(widget_id, widget_name)
        self.cycle_table = CycleTable()
        self.properties = Properties()
        self.setCentralWidget(self.cycle_table)
        # set tool bar
        self.setToolBar()
        # init one row
        self.cycle_table.addRow(0)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """

        @return:
        """
        self.cycle_table.timelineAdded.connect(
            lambda widget_id, widget_name, index: self.itemAdded.emit(self.widget_id, widget_id, widget_name, index))
        self.cycle_table.timelineDeleted.connect(lambda widget_id: self.itemDeleted.emit(Info.CycleSignal, widget_id))
        self.properties.propertiesChanged.connect(lambda: self.propertiesChanged.emit(self.widget_id))

    def setToolBar(self):
        """

        @return:
        """
        self.tool_bar = self.addToolBar("Tool Bar")
        self.tool_bar.setMovable(False)
        self.tool_bar.setFloatable(False)
        # add action
        self.tool_bar.addAction(Func.getImagePath("tool_bar/setting.png", 1), "Setting", self.properties.exec)
        self.tool_bar.addAction(Func.getImagePath("tool_bar/add_row.png", 1), "Add Row", self.addRow)
        add_rows_action = QAction(Func.getImagePath("tool_bar/add_rows.png", 1), "Add Rows", self)
        delete_row_action = QAction(Func.getImagePath("tool_bar/delete_row.png", 1), "Delete Row", self)
        add_column_action = QAction(Func.getImagePath("tool_bar/add_column.png", 1), "Add Row", self)
        add_columns_action = QAction(Func.getImagePath("tool_bar/add_columns.png", 1), "Add Rows", self)
        delete_column_action = QAction(Func.getImagePath("tool_bar/delete_column.png", 1), "Delete Row", self)
        self.tool_bar.addAction(add_rows_action)
        self.tool_bar.addAction(delete_row_action)
        self.tool_bar.addAction(add_column_action)
        self.tool_bar.addAction(add_columns_action)
        self.tool_bar.addAction(delete_column_action)

    def getColumnAttributes(self) -> list:
        """
        return [attr1, attr2]
        @return:
        """
        # todo get column attributes
        return []

    def deleteTimeline(self, timeline: str):
        """

        @param timeline:
        @return:
        """
        self.cycle_table.deleteTimeline(timeline)

    def addRow(self):
        """

        @return:
        """
        self.cycle_table.addRow()

    """
    functions that must be override
    """

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        return self.properties.getProperties()

    def getHiddenAttributes(self) -> list:
        """
        every widget has global attributes and own attributes,
        we get global attributes through common function Func.getAttributes(widget_id) and
        we get widget's own attributes through this function.
        @return: dict of attributes
        """
        return ["cLoop", "rowNums"]

    def store(self):
        """
        todo You should finish the job.

        return necessary data for restoring this widget.
        @return:
        """
        return {}

    def restore(self, data) -> None:
        """
        todo You should finish the job.

        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """

    def copy(self, widget_id: int, widget_name: str):
        """
        todo You should finish the job.

        return a copy of this widget, and set the widget id and name of the copy.
        @param widget_id:
        @return:
        """
        return None
