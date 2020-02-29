import re

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QShortcut

from app.func import Func
from app.info import Info
from lib import MessageBox
from .attribute_item import AttributeItem
from .timeline_item import TimelineItem
from .weight_item import WeightItem


class CycleTable(QTableWidget):
    """

    """

    # when timeline is added, emit this signal (widget id, widget_name, index)
    timelineAdded = pyqtSignal(int, str, int)
    timelineDeleted = pyqtSignal(int)

    def __init__(self):
        super(CycleTable, self).__init__(None)
        # col attributes and its default value
        self.attributes = ["Weight", "Timeline"]
        self.default_value = {"Weight": "1", "Timeline": ""}
        self.alt_key = False
        self.drag_copy_row_col = [-2, -2]
        # timeline_name : [widget_id, count in this table]
        self.timelines = {}
        #
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.attributes)
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

    def linkSignals(self):
        """

        @return:
        """
        self.itemChanged.connect(self.dealItemChanged)

    def setMenuAndShortcut(self):
        """
        set menu and shortcut
        @return:
        """
        self.copy_shortcut = QShortcut(QKeySequence(QKeySequence.Copy), self)
        self.copy_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.copy_shortcut.activated.connect(self.copyActionFunc)
        self.paste_shortcut = QShortcut(QKeySequence(QKeySequence.Paste), self)
        self.paste_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.paste_shortcut.activated.connect(self.pasteActionFunc)

    def addRow(self, index: int = -1):
        """
        add row in timeline
        @param index: row's index, if -1, add in the bottom
        @return:
        """
        if index != -1:
            # insert new row
            self.insertRow(index)
        else:
            index = self.rowCount()
            self.addRow(index)
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

    def deleteTimeline(self, timeline: str):
        """
        delete
        @param timeline:
        @return:
        """
        for row in range(self.rowCount() - 1, -1, -1):
            if self.item(row, 1).text() == timeline:
                self.removeRow(row)
        del self.timelines[timeline]

    def dealItemChanged(self, item):
        """
        when cell changed, we need to make some judgement
        @param item:
        @return:
        """
        # if text isn't changed, we ignore it
        if item.changed():
            text = item.text()
            if type(item) == WeightItem:
                # only positive number
                if not re.match(Info.WeightPattern[0], text):
                    MessageBox.information(self, "warning", Info.WeightPattern[1])
                    item.redo()
                else:
                    item.save()
            elif type(item) == TimelineItem:
                item: TimelineItem
                # empty => something: maybe add a timeline
                # something => another something: maybe add a timeline, maybe delete a timeline
                # something => empty: maybe delete a timeline
                if not item.old_text:
                    # empty => something, if something is valid and new timeline, emit add signal
                    if not re.match(Info.WidgetPattern[0], text):
                        MessageBox.information(self, "warning", Info.WidgetPattern[1])
                        item.redo()
                    else:
                        if text not in self.timelines:
                            # if it is new timeline in this cycle, but may have existed in other cycles
                            if Func.checkWidgetNameExisted(widget_name=text):
                                MessageBox.information(self, "warning", "Name already exists in other cycles.")
                                item.redo()
                            else:
                                # generate new timeline's widget_id
                                widget_id = Func.generateWidgetId(Info.TIMELINE)
                                self.timelineAdded.emit(widget_id, text, len(self.timelines))
                                self.timelines[text] = [widget_id, 1]
                                item.save()

                        else:
                            self.timelines[text][1] += 1
                            item.save()
                else:
                    if text:
                        # something => another something
                        if not re.match(Info.WidgetPattern[0], text):
                            MessageBox.information(self, "warning", Info.WidgetPattern[1])
                            item.redo()
                        else:
                            if text not in self.timelines:
                                # new timeline in this cycle
                                if Func.checkWidgetNameExisted(widget_name=text):
                                    # valid
                                    MessageBox.information(self, "warning", "Name already exists in other cycles.")
                                    item.redo()
                                else:
                                    # generate new timeline's widget_id
                                    widget_id = Func.generateWidgetId(Info.TIMELINE)
                                    self.timelineAdded.emit(widget_id, text, len(self.timelines))
                                    self.timelines[text] = [widget_id, 1]
                                    # secondly check old text
                                    self.timelines[item.old_text][1] -= 1
                                    if not self.timelines[item.old_text][1]:
                                        # if user delete all this timeline, we delete data
                                        self.timelineDeleted.emit(self.timelines[item.old_text][0])
                                        del self.timelines[item.old_text]
                                    item.save()
                            else:
                                # simply change data and check old text
                                self.timelines[text][1] += 1
                                self.timelines[item.old_text][1] -= 1
                                if not self.timelines[item.old_text][1]:
                                    # if user delete all this timeline, we delete data
                                    self.timelineDeleted.emit(self.timelines[item.old_text][0])
                                    del self.timelines[item.old_text]
                                item.save()
                    else:
                        # something => empty
                        self.timelines[item.old_text][1] -= 1
                        if not self.timelines[item.old_text][1]:
                            # if user delete all this timeline, we delete data
                            self.timelineDeleted.emit(self.timelines[item.old_text][0])
                            del self.timelines[item.old_text]
                        item.save()
            elif type(item) == AttributeItem:
                print("Attribute item changed")

    def mouseMoveEvent(self, e):
        """
        when dragging the mouse while holding down alt/option
        @param e:
        @return:
        """
        super(CycleTable, self).mouseMoveEvent(e)
        # 如果是已经按住alt，并刚刚开始滑动
        if e.modifiers() == Qt.AltModifier:
            if not self.alt_key:
                row = self.rowAt(e.pos().y())
                col = self.columnAt(e.pos().x())
                if row != -1 and col != -1:
                    self.drag_copy_row_col = [row, col]
                    self.alt_key = True
                    self.setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, e):
        """

        @param e:
        @return:
        """
        if self.alt_key:
            print(self.drag_copy_row_col)
            self.alt_key = False
            self.unsetCursor()

    def copyActionFunc(self):
        """
        copy data to table
        @return:
        """
        print("copy")

    def pasteActionFunc(self):
        """
        paste data to table
        @return:
        """
        print("paste")
