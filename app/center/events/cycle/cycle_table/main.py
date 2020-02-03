import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidget

from lib import MessageBox
from .attribute_item import AttributeItem
from .timeline_item import TimelineItem
from .weight_item import WeightItem


class CycleTable(QTableWidget):
    """

    """

    # when timeline is added, emit this signal (widget id, widget_name)
    timelineAdded = pyqtSignal(int, str)
    timelineDeleted = pyqtSignal(int)

    def __init__(self):
        super(CycleTable, self).__init__(None)
        # col attributes and its default value
        self.attributes = ["Weight", "Timeline"]
        self.default_value = {"Weight": "1", "Timeline": ""}
        # timeline_name:[count in this table, widget_id]
        self.timelines = {}
        #
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.attributes)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """

        @return:
        """
        self.itemChanged.connect(self.dealItemChanged)

    def addRow(self, index: int):
        """
        add row in table
        @return:
        """
        # insert new row
        self.insertRow(index)
        # add items, weight, timeline and attributes
        weight_item = WeightItem(self.default_value[self.attributes[0]])
        self.setItem(index, 0, weight_item)
        timeline_item = TimelineItem()
        self.setItem(index, 1, timeline_item)
        for col in range(2, len(self.attributes)):
            default_value = self.default_value[self.attributes[col]]
            attribute_item = AttributeItem(default_value)
            self.setItem(index, col, attribute_item)

    def deleteRow(self, index: int):
        """
        delete row
        @param index:
        @return:
        """

    def addAttribtueColumn(self, index: int, attribute: str):
        """
        add attribute column
        @param index:
        @param attribute:
        @return:
        """

    def deleteAttributeColumn(self, index: int):
        """
        delete attribute column
        @param index:
        @return:
        """

    def dealItemChanged(self, item):
        """
        when cell changed, we need to make some judgement
        @param item:
        @return:
        """
        # if this item was just added in the table, we ignore it
        if not item.new:
            text = item.text()
            if type(item) == WeightItem:
                # only positive number
                if not re.match(r"^[0-9]+$", text):
                    MessageBox.information(self, "warning", "Value must be positive integer.")
                    item.redo()
                else:
                    item.save()
            elif type(item) == TimelineItem:
                print("Timeline item changed", "Name must start with a letter and contain only letters, numbers and _.")

            elif type(item) == AttributeItem:
                print("Attribute item changed")
        else:
            item.new = False
