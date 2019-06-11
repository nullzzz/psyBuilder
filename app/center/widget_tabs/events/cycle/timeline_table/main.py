import copy

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView

from app.center.widget_tabs.timeline.widget_icon import WidgetIcon
from app.func import Func
from app.info import Info
from app.lib import NoDash


class TimelineTable(QTableWidget):
    # timeline新增 (cycle_widget_id, timeline_widget_id, name, flag, existed_timeline_widget_id, refresh(False) -> structure)
    timeline_add = pyqtSignal(str, str, str, int, str, bool)
    # timeline删除，如果timeline_table中的某个name的timeline全部消失，要将structure中该node删除 (wid -> structure)
    timeline_delete = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        """
        init
        :param parent:
        :param widget_id:
        """
        super(TimelineTable, self).__init__(parent)
        # data
        self.widget_id = widget_id
        self.col_attribute = ["Weight", "Timeline"]
        self.attribute_value = {"Weight": '', "Timeline": ''}
        self.old_timeline_name = ''
        self.edit_row = -2
        self.name_wid = {}
        self.name_count = {}
        # 美化
        self.setItemDelegate(NoDash())
        # 初始化
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.col_attribute)
        self.addRow()
        # 双击单元格修改
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

        # Alt仿excel复制
        self.is_copying = False
        self.selected_text = ""

        # signals
        self.linkSignals()
        # menu
        self.setMenuAndShortcut()

        # self.grabKeyboard()

    def linkSignals(self) -> None:
        """
        连接信号
        :return:
        """
        self.itemChanged.connect(self.addTimeline)
        self.itemChanged.connect(self.deleteTimeline)
        self.cellClicked.connect(self.selectCell)

    def setMenuAndShortcut(self) -> None:
        """

        :return:
        """
        pass

    def addRow(self) -> None:
        """
        增加一行，需要考虑到attributes
        :return:
        """
        try:
            # 插入一行
            self.insertRow(self.rowCount())
            # 根据attribute设置内容
            self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(self.attribute_value[self.col_attribute[0]]))
            item = QTableWidgetItem(self.attribute_value[self.col_attribute[1]])
            item.setFlags(Qt.ItemIsEnabled)
            self.setItem(self.rowCount() - 1, 1, item)
            for col in range(0, len(self.col_attribute)):
                self.setItem(self.rowCount() - 1, col, QTableWidgetItem(self.attribute_value[self.col_attribute[col]]))
        except Exception as e:
            print(f"error {e} happen in add row. [timeline_table/main.py]")

    def deleteRow(self, row) -> None:
        """
        删除选中的某行
        :param row:
        :return:
        """
        try:
            timeline_name = self.item(row, 1).text()
            # 如果存在着timeline
            if timeline_name:
                self.name_count[timeline_name] -= 1
                if not self.name_count[timeline_name]:
                    del self.name_count[timeline_name]
                    self.timeline_delete.emit(self.name_wid[timeline_name])
                    del self.name_wid[timeline_name]
            self.removeRow(row)
        except Exception as e:
            print(f"error {e} happen in delete row. [timeline_table/main.py]")

    def addAttribute(self, attribute='', default_value='') -> None:
        """
        添加attribute
        :param attribute: attribute名
        :param default_value: attribute默认值
        :return:
        """
        try:
            # 添加进字典
            self.col_attribute.append(attribute)
            self.attribute_value[attribute] = default_value
            self.insertColumn(self.columnCount())
            self.setHorizontalHeaderLabels(self.col_attribute)
            # 所有列置为初始值
            for row in range(self.rowCount()):
                item = QTableWidgetItem(default_value)
                self.setItem(row, self.columnCount() - 1, item)
        except Exception as e:
            print(f"error {e} happen in add attribute. [timeline_table/main.py]")

    def addAttributes(self, attribute_list: list, value: list) -> None:
        """
        添加attributes
        :param attribute_list: attributes名列表
        :param value: 对应值
        :return:
        """
        try:
            for i in range(len(attribute_list)):
                self.addAttribute(attribute_list[i], value[i])
        except Exception as e:
            print(f"error {e} happen in add attributes. [timeline_table/main.py]")

    def changeAttribute(self, col: int, attribute: str, value: str):
        """
        修改attribute的名或值
        :param col: 列索引
        :param attribute:
        :param value:
        :return:
        """
        try:
            old_attribute = self.col_attribute[col]
            old_value = self.attribute_value[old_attribute]
            # 于旧的名与值比较
            if old_attribute == attribute:
                self.attribute_value[attribute] = value
                for row in range(self.rowCount()):
                    if self.item(row, col).text() == old_value:
                        self.item(row, col).setText(value)
            else:
                if value != old_value:
                    for row in range(self.rowCount()):
                        if self.item(row, col).text() == old_value:
                            self.item(row, col).setText(value)
                else:
                    del self.attribute_value[old_attribute]
                self.col_attribute[col] = attribute
                self.attribute_value[attribute] = value
        except Exception as e:
            print(f"error {e} happen in change attribute. [timeline_table/main.py]")

    def deleteAttribute(self, col):
        """
        删除attribute
        :param col: 索引
        :return:
        """
        try:
            # 不能删除第0和1列
            if col not in [0, 1]:
                del self.attribute_value[self.col_attribute[col]]
                self.col_attribute.pop(col)
                self.removeColumn(col)
                self.setHorizontalHeaderLabels(self.col_attribute)
        except Exception as e:
            print(f"error {e} happen in delete attribute. [timeline_table/main.py]")

    def addTimeline(self, item: QTableWidgetItem):
        """
        当timeline那列item被修改时，需要作出一系列反应，add和delete
        :param item:
        :return:
        """
        try:
            if self.edit_row == item.row() and item.column() == 1 and item.text():
                name = item.text()
                self.edit_row = -2
                validity, existed_widget_id = Func.checkTimelineNameValidity(name, self.widget_id)
                if validity == Info.TimelineNameRight:
                    # 没有出现过是要进行新增的
                    if name not in self.name_count:
                        widget_icon = WidgetIcon(widget_type=Info.TIMELINE)
                        timeline_widget_id = widget_icon.widget_id
                        self.timeline_add.emit(self.widget_id, timeline_widget_id, name, Info.WidgetAdd, '', False)
                        self.name_count[name] = 1
                        self.name_wid[name] = timeline_widget_id
                    else:
                        self.name_count[name] += 1
                    # 如果old_name有效，其被修改后，count-1
                    if (self.old_timeline_name):
                        self.name_count[self.old_timeline_name] -= 1
                        # 如果此cycle中不存在相同名的timeline需要进行删除
                        if not self.name_count[self.old_timeline_name]:
                            del self.name_count[self.old_timeline_name]
                            self.timeline_delete.emit(self.name_wid[self.old_timeline_name])
                            del self.name_wid[self.old_timeline_name]
                elif validity == Info.TimelineNameExist:
                    # 没有出现过是要进行新增的，且是引用
                    if name not in self.name_count:
                        widget_icon = WidgetIcon(widget_type=Info.TIMELINE)
                        timeline_widget_id = widget_icon.widget_id
                        self.timeline_add.emit(self.widget_id, timeline_widget_id, name, Info.WidgetRefer,
                                               existed_widget_id, False)
                        self.name_count[name] = 1
                        self.name_wid[name] = timeline_widget_id
                    else:
                        self.name_count[name] += 1
                    # 如果old_name有效，其被修改后，count-1
                    if (self.old_timeline_name):
                        self.name_count[self.old_timeline_name] -= 1
                        # 如果此cycle中不存在相同名的timeline需要进行删除
                        if not self.name_count[self.old_timeline_name]:
                            del self.name_count[self.old_timeline_name]
                            self.timeline_delete.emit(self.name_wid[self.old_timeline_name])
                            del self.name_wid[self.old_timeline_name]
                elif validity == Info.TimelineNameError:
                    item.setText(self.old_timeline_name)
                    QMessageBox.information(self, 'Warning', "Name must start with letter.")
                elif validity == Info.TimelineTypeError:
                    item.setText(self.old_timeline_name)
                    QMessageBox.information(self, 'Warning', "Can't refer different type widget.")
                elif validity == Info.TimelineParentError:
                    item.setText(self.old_timeline_name)
                    QMessageBox.information(self, 'Warning', "Can't refer this timeline.")
                else:
                    raise Exception("Unknown validity type.")
                self.old_timeline_name = ''
        except Exception as e:
            print(f"error {e} happens in add timeline. [timeline_table/main.py]")

    def deleteTimeline(self, item: QTableWidgetItem):
        """
        这个函数是来应对timeline的name被修改为空，或者删除某一行时被调用
        :param item:
        :return:
        """
        try:
            if self.edit_row == item.row() and item.column() == 1 and not item.text():
                self.edit_row = -2
                self.name_count[self.old_timeline_name] -= 1
                if not self.name_count[self.old_timeline_name]:
                    del self.name_count[self.old_timeline_name]
                    self.timeline_delete.emit(self.name_wid[self.old_timeline_name])
                    del self.name_wid[self.old_timeline_name]
                self.old_timeline_name = ''
        except Exception as e:
            print(f"error {e} happens in delete timeline. [timeline_table/main.py]")

    def getInfo(self):
        try:
            # col_attribute, attribute_value, name_wid, name_count
            info = {
                'col_attribute': self.col_attribute,
                'attribute_value': self.col_attribute,
                'name_wid': self.name_wid,
                'name_count': self.name_count,
                'row': self.rowCount(),
                'col': self.columnCount(),
                'data': []
            }
            for row in range(self.rowCount()):
                data = []
                for col in range(self.columnCount()):
                    data.append(self.item(row, col).text())
                info['data'].append(data)
            return info
        except Exception as e:
            print(f"error {e} happens in get info. [timeline_table/main.py]")

    def restore(self, info):
        try:
            # data
            self.col_attribute = info['col_attribute']
            self.attribute_value = info['attribute_value']
            self.name_wid = info['name_wid']
            self.name_count = info['name_count']
            # table
            self.setRowCount(info['row'])
            self.setColumnCount(info['col'])
            data = info['data']
            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    self.setItem(row, col, QTableWidgetItem(data[row][col]))
            self.setHorizontalHeaderLabels(self.col_attribute)
        except Exception as e:
            print(f"error {e} happens in restore. [cycle/main.py]")

    def clone(self, clone_table):
        try:
            # data
            clone_table.col_attribute = copy.deepcopy(self.col_attribute)
            clone_table.attribute_value = copy.deepcopy(self.attribute_value)
            clone_table.name_count = copy.deepcopy(self.name_count)
            for name in clone_table.name_count:
                wid = Func.getWidgetId(clone_table.widget_id, name)
                clone_table.name_wid[name] = wid
            # table
            clone_table.setRowCount(self.rowCount())
            clone_table.setColumnCount(self.columnCount())
            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    clone_table.setItem(row, col, QTableWidgetItem(self.item(row, col).text()))
            clone_table.setHorizontalHeaderLabels(clone_table.col_attribute)
        except Exception as e:
            print(f"error {e} happens in clone timeline table. [timeline_table/main.py]")

    def selectCell(self, row: int, column: int):
        item: QTableWidgetItem = self.item(row, column)
        self.selected_text = item.text()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.is_copying = True
            self.setCursor(Qt.SplitVCursor)
        else:
            QTableWidget.keyPressEvent(self, e)

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.is_copying = False
            self.unsetCursor()
        else:
            QTableWidget.keyReleaseEvent(self, e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        try:
            if self.is_copying and self.selected_text:
                items = self.selectedItems()
                for item in items:
                    item.setText(self.selected_text)
                # 重置name_count
                name_count = {}
                for row in range(self.rowCount()):
                    name = self.item(row, 1).text()
                    if name:
                        if name in name_count:
                            name_count[name] += 1
                        else:
                            name_count[name] = 1
                # 可能会有timeline被覆盖掉
                for name in self.name_count:
                    if name not in name_count:
                        self.timeline_delete.emit(self.name_wid[name])
                        del self.name_wid[name]
                self.name_count = name_count
        except Exception as e:
            print(f"error {e} happen in copy. [timeline_table/main.py]")
        finally:
            QTableWidget.mouseReleaseEvent(self, e)

    def mouseDoubleClickEvent(self, e):
        row = self.rowAt(e.pos().y())
        col = self.columnAt(e.pos().x())
        if col != 1:
            super(TimelineTable, self).mouseDoubleClickEvent(e)
        else:
            if row != -1:
                self.setFocus()
                self.old_timeline_name = self.item(row, col).text()
                self.editItem(self.item(row, col))
                self.edit_row = row
            else:
                super(TimelineTable, self).mouseDoubleClickEvent(e)

    def focusInEvent(self, *args, **kwargs):
        self.grabKeyboard()
        return QTableWidget.focusInEvent(self, *args, **kwargs)

    def focusOutEvent(self, *args, **kwargs):
        if not self.is_copying:
            self.releaseKeyboard()
        return QTableWidget.focusOutEvent(self, *args, **kwargs)

    def getTimelines(self):
        """
        按顺序返回timelines
        :return:
        """
        try:
            timelines = []
            for i in range(0, self.rowCount()):
                try:
                    timeline_name = self.item(i, 1).text()
                    timelines.append([timeline_name, self.name_wid[timeline_name]])
                except:
                    timelines.append(["", ""])
            return timelines
        except Exception as e:
            print(f"error {e} happen in get timelines. [timeline_table/main.py]")
            return []

    def getAttributes(self, index: int):
        """
        根据行索引返回某行的属性
        :return: 对应行的属性的一个字典
        """
        try:
            attributes = {}
            for i in range(0, self.columnCount()):
                try:
                    attributes[self.col_attribute[i]] = self.item(index, i).text()
                except:
                    attributes[self.col_attribute[i]] = ""
            return attributes
        except Exception as e:
            print(f"error {e} happen in get attributes. [timeline_table/main.py]")
            return {}
