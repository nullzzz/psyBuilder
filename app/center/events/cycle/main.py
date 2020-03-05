from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction

from app.func import Func
from app.info import Info
from lib import TabItemMainWindow
from .attribute_dialog import AttributeDialog
from .cycle_table import CycleTable
from .properties import Properties


class Cycle(TabItemMainWindow):
    """

    """

    # when add new timeline, emit signal(parent_widget_id, widget_id, widget_name, index)
    itemAdded = pyqtSignal(str, str, str, int)
    # when delete signals, emit signal(sender_widget, widget_id)
    itemDeleted = pyqtSignal(int, str)

    def __init__(self, widget_id: str, widget_name: str):
        super(Cycle, self).__init__(widget_id, widget_name)
        self.cycle_table = CycleTable()
        self.properties = Properties()
        self.attribute_dialog = AttributeDialog(self.cycle_table.default_value)
        self.setCentralWidget(self.cycle_table)
        # set tool bar
        self.setToolBar()
        # init one row
        self.cycle_table.addRow(0)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        """
        self.cycle_table.timelineAdded.connect(
            lambda widget_id, widget_name, index: self.itemAdded.emit(self.widget_id, widget_id, widget_name, index))
        self.cycle_table.timelineDeleted.connect(lambda widget_id: self.itemDeleted.emit(Info.CycleSend, widget_id))
        self.properties.propertiesChanged.connect(lambda: self.propertiesChanged.emit(self.widget_id))
        self.cycle_table.headerDoubleClicked.connect(
            lambda col, name, value: self.attribute_dialog.showWindow(0, col, name, value))
        self.attribute_dialog.attributesAdded.connect(self.handleAttributesAdd)
        self.attribute_dialog.attributesChanged.connect(self.handleAttributeChanged)

    def setToolBar(self):
        """

        @return:
        """
        tool_bar = self.addToolBar("Tool Bar")
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)
        # add action
        tool_bar.addAction(Func.getImage("tool_bar/setting.png", 1), "Setting", self.properties.exec)
        tool_bar.addAction(Func.getImage("tool_bar/add_row.png", 1), "Add Row", self.addRow)
        add_rows_action = QAction(Func.getImage("tool_bar/add_rows.png", 1), "Add Rows", self)
        tool_bar.addAction(add_rows_action)
        delete_row_action = QAction(Func.getImage("tool_bar/delete_row.png", 1), "Delete Row", self)
        tool_bar.addAction(delete_row_action)
        tool_bar.addAction(Func.getImage("tool_bar/add_column.png", 1), "Add Attribute",
                           lambda: self.attribute_dialog.showWindow(0))
        tool_bar.addAction(Func.getImage("tool_bar/add_columns.png", 1), "Add Attributes",
                           lambda: self.attribute_dialog.showWindow(1))
        delete_column_action = QAction(Func.getImage("tool_bar/delete_column.png", 1), "Delete Attributes", self)
        tool_bar.addAction(delete_column_action)

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

    def handleAttributesAdd(self):
        """
        when user want to add new attributes
        """
        attributes = self.attribute_dialog.getAttributes()
        for name, value in attributes:
            self.cycle_table.addAttribtueColumn(-1, name, value)

    def handleAttributeChanged(self, col: int, attribute_name: str, attribute_value: str):
        """
        when user change some attribute
        """
        self.cycle_table.changeAttributeColumn(col, attribute_name, attribute_value)

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
