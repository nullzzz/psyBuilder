import re

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QShortcut, QTableWidgetItem

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
    timelineAdded = pyqtSignal(str, str, int)
    timelineDeleted = pyqtSignal(str)
    # when header is double clicked, emit signal (col, name, value)
    headerDoubleClicked = pyqtSignal(int, str, str)

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
        self.horizontalHeader().sectionDoubleClicked.connect(
            lambda col: self.headerDoubleClicked.emit(col, self.attributes[col],
                                                      self.default_value[self.attributes[col]]))
        self.itemChanged.connect(self.handleItemChanged)

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

    def addAttribtueColumn(self, col: int, attribute_name: str, attribute_value):
        """
        add attribute column
        if col == -1, add last col
        """
        # add new column
        if col == -1:
            col = self.columnCount()
            self.insertColumn(self.columnCount())
        else:
            self.insertColumn(col)
        # set header
        self.setHorizontalHeaderItem(col, QTableWidgetItem(attribute_name))
        # set value
        for row in range(self.rowCount()):
            attribute_item = AttributeItem(attribute_value)
            self.setItem(row, col, attribute_item)
        # related value
        self.attributes.insert(col, attribute_name)
        self.default_value[attribute_name] = attribute_value

    def changeAttributeColumn(self, col: int, attribute_name: str, attribute_value):
        """
        change attribute column: name and default value
        """
        # header
        if attribute_name != self.attributes[col]:
            self.horizontalHeaderItem(col).setText(attribute_name)
            del self.default_value[attribute_name]
        # data
        self.attributes[col] = attribute_name
        self.default_value[attribute_value] = attribute_name
        # value: we just change empty to new default value
        for row in range(self.rowCount()):
            item = self.item(row, col)
            if not item.text():
                item.setText(attribute_value)

    def deleteAttributeColumn(self, col: int):
        """
        delete attribute column
        """

    def deleteTimeline(self, timeline: str):
        """
        delete timeline in this cycle
        """
        for row in range(self.rowCount() - 1, -1, -1):
            if self.item(row, 1).text() == timeline:
                self.removeRow(row)
        del self.timelines[timeline]

    def handleItemChanged(self, item):
        """
        when cell changed, we need to make some judgement
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
                    item.saveFile()
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

        """
        if self.alt_key:
            print(self.drag_copy_row_col)
            self.alt_key = False
            self.unsetCursor()

    def copyActionFunc(self):
        """
        copy data to table
        """
        print("copy")

    def pasteActionFunc(self):
        """
        paste data to table
        """
        print("paste")
