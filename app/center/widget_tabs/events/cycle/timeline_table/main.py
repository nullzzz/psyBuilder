import copy
import re

from PyQt5.QtCore import QDataStream, QIODevice, Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QKeySequence
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QShortcut, QAction, QMenu, QApplication, QMessageBox

from app.center.widget_tabs.timeline.widget_icon import WidgetIcon
from app.func import Func
from app.info import Info
from app.lib import NoDash, PigLineEdit
from .timeline_table_item import TimelineTableItem as QTableWidgetItem


class TimelineTable(QTableWidget):
    # timeline新增 (cycle_widget_id, timeline_widget_id, name, flag, existed_timeline_widget_id, refresh(False) ->
    # structure)
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
        self.attribute_value = {"Weight": '1', "Timeline": ''}
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
        # 允许拖拽
        self.setAcceptDrops(True)
        # 双击单元格修改
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

        # 按住Alt仿excel复制
        self.alt_pressed = False
        self.selected_text = ""
        self.selected_col = -2

        # signals
        self.linkSignals()
        # menu
        self.setMenuAndShortcut()
        # 当前窗口是否为焦点
        self.focus = False

        # 在任意修改时要检测合法性
        self.old_weight_value = ""

        #
        self.line_edit = None
        self.edit_attribute_pos = (-1, -1)

    def linkSignals(self) -> None:
        """
        连接信号
        :return:
        """
        self.itemChanged.connect(self.addTimeline)
        self.itemChanged.connect(self.deleteTimeline)
        self.itemChanged.connect(self.weightChange)

    def setMenuAndShortcut(self):
        """
        设置快捷键和菜单，菜单
        :return:
        """
        # 菜单
        self.right_button_menu = QMenu()
        self.copy_action = QAction("Copy", self.right_button_menu)
        self.paste_action = QAction("Paste", self.right_button_menu)
        self.copy_action.triggered.connect(self.copy_data)
        self.paste_action.triggered.connect(self.paste_data)
        self.right_button_menu.addAction(self.copy_action)
        self.right_button_menu.addAction(self.paste_action)
        # 快捷键
        self.copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.copy_shortcut.activated.connect(self.copy_data)
        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.paste_data)

    def contextMenuEvent(self, e):
        """
        显示菜单
        :param QContextMenuEvent:
        :return:
        """
        # 存在选中区域，则可以复制
        self.copy_action.setEnabled(False)
        if self.selectedItems():
            self.copy_action.setEnabled(True)
        self.right_button_menu.exec(self.mapToGlobal(e.pos()))

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
            self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(self.attribute_value[self.col_attribute[1]]))
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
            # 与旧的名与值比较
            if old_attribute == attribute:
                # 如果与旧名相同，进行修改，且对值进行比较
                self.attribute_value[attribute] = value
                for row in range(self.rowCount()):
                    # 如果为空填入新值
                    if not self.item(row, col).text():
                        self.item(row, col).setText(value)
            else:
                # 名也变了的话，删除旧的
                del self.attribute_value[old_attribute]
                # 判断值是否变化
                if value != old_value:
                    for row in range(self.rowCount()):
                        # 如果为空填入新值
                        if not self.item(row, col).text():
                            self.item(row, col).setText(value)
                # 名字改了，需要修改col_attribute
                self.col_attribute[col] = attribute
                # 修改header
                self.horizontalHeaderItem(col).setText(attribute)
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
                    QMessageBox.information(self, 'Warning',
                                            "The value must start with a letter and only contain numbers，letter and _")
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
            if self.edit_row == item.row() and item.column() == 1 and self.old_timeline_name and not item.text():
                self.edit_row = -2
                self.name_count[self.old_timeline_name] -= 1
                if not self.name_count[self.old_timeline_name]:
                    del self.name_count[self.old_timeline_name]
                    self.timeline_delete.emit(self.name_wid[self.old_timeline_name])
                    del self.name_wid[self.old_timeline_name]
                self.old_timeline_name = ''
        except Exception as e:
            print(f"error {e} happens in delete timeline. [timeline_table/main.py]")

    def getInfo(self) -> dict:
        """
        返回保存所需要的信息
        :return:
        """
        try:
            # col_attribute, attribute_value, name_wid, name_count
            info = {
                'col_attribute': self.col_attribute,
                'attribute_value': self.attribute_value,
                'name_wid': self.name_wid,
                'name_count': self.name_count,
                'row': self.rowCount(),
                'col': self.columnCount(),
                'table_data': []
            }
            for row in range(self.rowCount()):
                data = []
                for col in range(self.columnCount()):
                    data.append(self.item(row, col).text())
                info['table_data'].append(data)
            return info
        except Exception as e:
            print(f"error {e} happens in get info. [timeline_table/main.py]")

    def restore(self, info):
        """
        复原
        :param info:
        :return:
        """
        try:
            # data
            self.col_attribute = info['col_attribute']
            self.attribute_value = info['attribute_value']
            self.name_wid = info['name_wid']
            self.name_count = info['name_count']
            # table
            self.setRowCount(info['row'])
            self.setColumnCount(info['col'])
            data = info['table_data']
            for row in range(self.rowCount()):
                for col in range(self.columnCount()):
                    self.setItem(row, col, QTableWidgetItem(data[row][col]))
            self.setHorizontalHeaderLabels(self.col_attribute)
        except Exception as e:
            print(f"error {e} happens in restore. [cycle/main.py]")

    def clone(self, clone_table):
        """
        复制
        :param clone_table:
        :return:
        """
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

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.alt_pressed = True
            self.setCursor(Qt.CrossCursor)
        else:
            QTableWidget.keyPressEvent(self, e)

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Alt:
            self.alt_pressed = False
            self.unsetCursor()
        else:
            QTableWidget.keyReleaseEvent(self, e)

    def mouseMoveEvent(self, e):
        """
        在滑动时，如果存在按住alt行为，且存在有效的col和row，将刚开始的那个有效item的值与列记录下来
        :param e:
        :return:
        """
        super(TimelineTable, self).mouseMoveEvent(e)
        # 如果是已经按住alt，并刚刚开始滑动
        if self.alt_pressed and self.selected_col == -2:
            # 得到行和列
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())
            # 保证行列有效
            if row in range(0, self.rowCount()) and col in range(0, self.columnCount()):
                item: QTableWidgetItem = self.item(row, col)
                self.selected_text = item.text()
                self.selected_col = col

    def mouseReleaseEvent(self, e: QMouseEvent):
        """

        :param e:
        :return:
        """
        QTableWidget.mouseReleaseEvent(self, e)
        try:
            if self.alt_pressed and self.selected_col != -2:
                items = self.selectedItems()
                for item in items:
                    if item.column() == self.selected_col:
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
                self.selected_col = -2
        except Exception as e:
            print(f"error {e} happen in copy. [timeline_table/main.py]")

    def mouseDoubleClickEvent(self, e):
        """
                通过监听双击事件来记录修改前的旧值。
                :param e:
                :return:
                """
        # 双击位置所在行列
        row = self.rowAt(e.pos().y())
        col = self.columnAt(e.pos().x())
        # 有效行
        if row != -1:
            if col == 0:
                # weight
                self.old_weight_value = self.item(row, col).text()
                # 弹出编辑框
                super(TimelineTable, self).mouseDoubleClickEvent(e)
            elif col == 1:
                # timeline
                self.old_timeline_name = self.item(row, col).text()
                self.edit_row = row
                # 弹出编辑框
                super(TimelineTable, self).mouseDoubleClickEvent(e)
            elif col != -1:
                # 其余attribute，在编辑时使用自定义的lineEdit，使其可以接受变量
                current_value = self.item(row, col).text()
                line_edit = PigLineEdit()
                line_edit.setText(current_value)
                self.line_edit = line_edit
                line_edit.editingFinished.connect(self.revertToItem)
                self.edit_attribute_pos = (row, col)
                self.setCellWidget(row, col, self.line_edit)

    def focusInEvent(self, e):
        """

        :param e:
        :return:
        """
        self.focus = True
        super(TimelineTable, self).focusInEvent(e)

    def focusOutEvent(self, e):
        """

        :param e:
        :return:
        """
        self.focus = False
        super(TimelineTable, self).focusOutEvent(e)

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

    def copy_data(self):
        """
        将选中表格数据以excel的格式粘贴到系统粘贴板中
        :return:
        """
        if self.focus:
            # 获取系统粘贴板
            clipboard = QApplication.clipboard()
            # 获取已选取的区域
            items = self.selectedItems()
            # 所选非空
            if items:
                # 按行对item进行存储
                row_items = {}
                first_row = items[0].row()
                row_items[first_row] = [items[0]]
                # 对以获取区域进行合法性判断，所选列存在不同即为不合法
                cols = [items[0].column()]
                cols_counted = False
                error = False
                for item in items[1:]:
                    # 得到item的位置
                    row = item.row()
                    col = item.column()
                    # 根据item行对item分类存放
                    if row in row_items:
                        row_items[row].append(item)
                    else:
                        row_items[row] = [item]
                    # 如果还未统计完成
                    if not cols_counted:
                        # 如果行仍为第一行，进行统计
                        if row == first_row:
                            cols.append(col)
                        else:
                            cols_counted = True
                            # 已经是下一行了，判断这个item对列是否合理
                            if col not in cols:
                                error = True
                                break
                    else:
                        if col not in cols:
                            error = True
                            break
                # 如果检测不合法，报错，否则按照行顺序，复制到粘贴板中
                if error:
                    QMessageBox.information(self, 'Warning',
                                            "This operation can't be performed on multiple selection areas.")
                else:
                    # 根据字典对行的记录，由小到大，输入到粘贴板中
                    copy_text = ""
                    rows = sorted(row_items)
                    length = len(cols)
                    for row in rows:
                        for i in range(length):
                            item = row_items[row][i]
                            if i == length - 1:
                                if row == rows[-1]:
                                    copy_text = copy_text + item.text()
                                else:
                                    copy_text = copy_text + item.text() + "\n"
                            else:
                                copy_text = copy_text + item.text() + "\t"
                    # 输入到粘贴板中
                    clipboard.setText(copy_text)

    def paste_data(self):
        """
        将系统粘贴板中的数据复制到表格中，具体的判定方法待定
        :return:
        """
        # 需要focus
        if not self.focus:
            return

        # 检测所选择粘贴区域是否合法
        selete_ranges = self.selectedRanges()
        # 没选择区域，无所谓
        if not len(selete_ranges):
            return

        # 只能有一个选择区域
        if len(selete_ranges) != 1:
            QMessageBox.information(self, 'Warning', "This operation can't be performed on multiple selection areas.")
            return

        # 得到所选区域左上角坐标
        start_row = selete_ranges[0].topRow()
        start_col = selete_ranges[0].leftColumn()

        # 获取系统粘贴板
        clipboard = QApplication.clipboard()
        paste_text = clipboard.text()

        # 如果没字，无所谓
        if not paste_text:
            return

        # 解析数据
        paste_rows_data = []
        # 先检测每行列数是否相同
        col_length = 0
        rows_data = re.split(r"\n", paste_text)
        # windows下，数据以\n结尾，所以会多出一个无效的\n，需要进行删除
        if not rows_data[-1]:
            rows_data = rows_data[:-1]
        # 对每行数据进行分割
        for row_data in rows_data:
            temp_data = re.split(r"\t", row_data)
            if not col_length:
                col_length = len(temp_data)
            else:
                if len(temp_data) != col_length:
                    QMessageBox.information(self, 'Warning', "Cols split by '\\t' of each row must be same!")
                    return
            # 保存数据
            paste_rows_data.append(temp_data)
        # 解析出0列
        if not col_length:
            QMessageBox.information(self, 'Warning', "Cols split by '\\t' is zero!")
            return

        # 如果影响列中包含timeline所在列，对数据的值进行判断，查看是否存在违法，去重复等等操作
        end_row = start_row + len(paste_rows_data) - 1
        if start_col == 1 or (not start_col and col_length > 1):
            # 粘贴板中的数据
            paste_timeline_names = []
            timeline_data_col = 0
            if not start_col:
                timeline_data_col = 1
            for paste_row_data in paste_rows_data:
                paste_row_data[timeline_data_col] = re.sub(r"\r", "", paste_row_data[timeline_data_col])
                timeline_name = paste_row_data[timeline_data_col]
                validity, _ = Func.checkTimelineNameValidity(timeline_name, self.widget_id)
                if validity == Info.TimelineNameRight or validity == Info.TimelineNameExist or not timeline_name:
                    paste_timeline_names.append(timeline_name)
                else:
                    QMessageBox.information(self, 'Warning',
                                            f"Data '{timeline_name}' is invalid to set in col 'timeline' !")
                    return
                    # 需要被paste区域的数据
            already_timeline_names = []
            timeline_end_row = end_row
            # 如果超出了
            if timeline_end_row > self.rowCount() - 1:
                timeline_end_row = self.rowCount() - 1
            for row in range(start_row, timeline_end_row + 1):
                # 将非空的timeline加进来
                already_timeline_names.append(self.item(row, 1).text())
            # 对两者直接数据进行处理
            name_res = {}
            # len(paste_timeline_names) >= len(already_timeline_names)
            for i in range(len(paste_timeline_names)):
                # 得到对应数据
                paste = paste_timeline_names[i]
                try:
                    already = already_timeline_names[i]
                except:
                    already = ""
                # 如果paste为""
                if not paste:
                    # 如果already不为空，则需要删除，如果为空，无所谓吧
                    if already:
                        if already in name_res:
                            name_res[already] -= 1
                        else:
                            name_res[already] = -1
                else:
                    # paste不为空，如果相同，无变化，如果不同，删除旧的，增加新的
                    if paste != already:
                        if paste in name_res:
                            name_res[paste] += 1
                        else:
                            name_res[paste] = 1
                        if already:
                            if already in name_res:
                                name_res[already] -= 1
                            else:
                                name_res[already] = -1
            # 根据name
            for name in name_res:
                if name in self.name_count:
                    self.name_count[name] += name_res[name]
                else:
                    # 必是新增
                    # 修改数据
                    self.name_count[name] = name_res[name]
                    # 进行新增
                    validity, existed_widget_id = Func.checkTimelineNameValidity(name, self.widget_id)
                    if validity == Info.TimelineNameRight:
                        widget_icon = WidgetIcon(widget_type=Info.TIMELINE)
                        timeline_widget_id = widget_icon.widget_id
                        self.timeline_add.emit(self.widget_id, timeline_widget_id, name, Info.WidgetAdd, '', False)
                        self.name_wid[name] = timeline_widget_id
                    elif validity == Info.TimelineNameExist:
                        widget_icon = WidgetIcon(widget_type=Info.TIMELINE)
                        timeline_widget_id = widget_icon.widget_id
                        self.timeline_add.emit(self.widget_id, timeline_widget_id, name, Info.WidgetRefer,
                                               existed_widget_id, False)
                        self.name_wid[name] = timeline_widget_id
            # 如果此时self.name_count存在数据小于等于0，则进行删除操作
            names_delete = []
            for name in self.name_count:
                if self.name_count[name] <= 0:
                    names_delete.append(name)
            for name in names_delete:
                del self.name_count[name]
                self.timeline_delete.emit(self.name_wid[name])
                del self.name_wid[name]
        # 现在直接放进去数据就可以了！
        # 先放进去一行，以扩充列
        count = 0
        first_paste_row_data = paste_rows_data[0]
        for i in range(col_length):
            # 数据
            item_text = first_paste_row_data[i]
            # 如果超出列区域
            if start_col + i >= self.columnCount():
                self.addAttribute(f"untitled_var_{count}", item_text)
                count += 1
            else:
                self.item(start_row, start_col + i).setText(item_text)
        # 扩充行
        rows_add_count = end_row + 1 - self.rowCount()
        for i in range(rows_add_count):
            self.addRow()
        # 放入剩余行
        for j in range(1, len(paste_rows_data)):
            paste_row_data = paste_rows_data[j]
            for i in range(col_length):
                item_text = paste_row_data[i]
                self.item(start_row + j, start_col + i).setText(item_text)

    def weightChange(self, item: QTableWidgetItem) -> None:
        """
        当widget列值发生改变时，检查其合法性
        :param item:
        :return:
        """
        # 非timeline列
        if item.column() == 0:
            new_value = item.text()
            # 如果为空无所谓
            if not new_value:
                QMessageBox.information(self, "warning", "value must be positive integer.")
                item.setText(self.old_weight_value)
                self.old_weight_value = ""
                return
            if re.match(r"^[0-9]+$", new_value):
                self.old_weight_value = ""
                return
            QMessageBox.information(self, "warning", "value must be positive integer.")
            item.setText(self.old_weight_value)
            self.old_weight_value = ""

    def revertToItem(self):
        """
        在编辑时被专成了line edit，在编辑完成后需要转回item
        :return:
        """
        # 保证有效
        if self.edit_attribute_pos[0] != -1:
            row, col = self.edit_attribute_pos
            # 移除lineWidget
            self.removeCellWidget(row, col)
            value = self.line_edit.text()
            item = QTableWidgetItem(value)
            self.edit_attribute_pos = (-1, -1)
            self.setItem(row, col, item)

    def dragEnterEvent(self, e):
        """
        拖拽进入
        :param e:
        :return:
        """
        # 符合要求
        if e.mimeData().hasFormat(Info.FromAttributeToLineEdit):
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        """
        拖拽移动
        :param e:
        :return:
        """
        # 符合要求
        if e.mimeData().hasFormat(Info.FromAttributeToLineEdit):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        拖拽结束
        :param e:
        :return:
        """
        # 符合要求
        if e.mimeData().hasFormat(Info.FromAttributeToLineEdit):
            # 根据位置找到准确的item，并将其放入
            row = self.rowAt(e.pos().y())
            col = self.columnAt(e.pos().x())
            # 有效行、有效列（不能是weight和timeline）
            if row != -1 and col >= 2:
                data = e.mimeData().data(Info.FromAttributeToLineEdit)
                stream = QDataStream(data, QIODevice.ReadOnly)
                text = f"[{stream.readQString()}]"
                self.item(row, col).setText(text)
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()
