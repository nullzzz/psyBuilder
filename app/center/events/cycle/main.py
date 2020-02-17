from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QAction

from app.func import Func
from app.info import Info
from lib import TabItemWidget
from .cycle_table import CycleTable


class Cycle(TabItemWidget):
    """

    """

    # when add new timeline, emit signal(parent_widget_id, widget_id, widget_name, index)
    itemAdded = pyqtSignal(int, int, str, int)
    # when delete signals, emit signal(origin_widget, widget_id)
    itemDeleted = pyqtSignal(int, int)

    def __init__(self, widget_id: int, widget_name: str):
        super(Cycle, self).__init__(widget_id, widget_name)
        self.cycle_table = CycleTable()
        layout = QVBoxLayout()
        self.tool_bar = QToolBar("ToolBar")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.tool_bar)
        layout.addWidget(self.cycle_table)
        self.setLayout(layout)
        # set tool bar
        self.setToolBar()
        # init one row
        self.cycle_table.addRow(0)
        # link signals
        self.linkSignals()
        # set shortcut

    def linkSignals(self):
        """

        @return:
        """
        self.cycle_table.timelineAdded.connect(
            lambda widget_id, widget_name, index: self.itemAdded.emit(self.widget_id, widget_id, widget_name, index))
        self.cycle_table.timelineDeleted.connect(lambda widget_id: self.itemDeleted.emit(Info.CycleSignal, widget_id))

    def setToolBar(self):
        """

        @return:
        """
        self.tool_bar.setMovable(False)
        self.tool_bar.setFloatable(False)
        # add action
        # todo add insert action and connect function
        setting_action = QAction(Func.getImage("tool_bar/setting.png", 1), "Setting", self)
        add_row_action = QAction(Func.getImage("tool_bar/add_row.png", 1), "Add Row", self)
        add_row_action.triggered.connect(self.addRow)
        add_rows_action = QAction(Func.getImage("tool_bar/add_rows.png", 1), "Add Rows", self)
        delete_row_action = QAction(Func.getImage("tool_bar/delete_row.png", 1), "Delete Row", self)
        add_column_action = QAction(Func.getImage("tool_bar/add_column.png", 1), "Add Row", self)
        add_columns_action = QAction(Func.getImage("tool_bar/add_columns.png", 1), "Add Rows", self)
        delete_column_action = QAction(Func.getImage("tool_bar/delete_column.png", 1), "Delete Row", self)
        self.tool_bar.addAction(setting_action)
        self.tool_bar.addAction(add_row_action)
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

    def copy(self, widget_id: int, widget_name: str):
        """
        return copy of this widget
        @param widget_id:
        @param widget_name:
        @return:
        """
        return Cycle(widget_id, widget_name)
