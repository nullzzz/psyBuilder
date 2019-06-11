from PyQt5.QtCore import Qt, pyqtSignal, QDataStream, QIODevice
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QMessageBox, QApplication

from app.func import Func
from app.info import Info
from .widget_icon_table.main import WidgetIconTable


class WidgetIconArea(QFrame):
    # 箭头显示 (pos_x -> widget_icon_table)
    signShow = pyqtSignal(int)
    # 箭头隐藏 (none -> widget_icon_table)
    signHide = pyqtSignal()
    # widget icon新增, 新增情况要分直接添加，复制，引用(parent_widget_id, widget_id, name, flag, old_widget_id -> structure)
    widgetIconAdd = pyqtSignal(str, str, str, int, str)
    # widget icon位置变化，因为会影响到attributes所以也要发一个信号到attributes (widget_id, drag_col, target_col -> structure, attributes)
    widgetIconMove = pyqtSignal(str, int, int)

    def __init__(self, parent=None, widget_id=''):
        super(WidgetIconArea, self).__init__(parent)
        self.setAcceptDrops(True)
        # data
        self.widget_id = widget_id
        # icon table
        self.widget_icon_table = WidgetIconTable(self)
        self.vBox = QVBoxLayout(self)
        self.vBox.addWidget(self.widget_icon_table)
        self.setLayout(self.vBox)
        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        self.signShow.connect(self.widget_icon_table.showSign)
        self.signHide.connect(self.widget_icon_table.hideSign)

    def dragEnterEvent(self, e):
        try:
            if e.mimeData().hasFormat("widget_icon_bar/widget_icon_type") or \
                    e.mimeData().hasFormat("widget_icon_table/copy-col") or \
                    e.mimeData().hasFormat("widget_icon_table/move-col") or \
                    e.mimeData().hasFormat("structure_tree/move-wid") or \
                    e.mimeData().hasFormat("structure_tree/copy-wid") or \
                    e.mimeData().hasFormat("structure_tree/refer-wid"):
                # 先对从widget bar中拖拽类型进行过滤
                if e.mimeData().hasFormat("widget_icon_bar/widget_icon_type"):
                    # 从widget icon bar拖拽到widget icon area中
                    data = e.mimeData().data("widget_icon_bar/widget_icon_type")
                    stream = QDataStream(data, QIODevice.ReadOnly)
                    # 读取当前拖拽widget类型
                    widget_type = stream.readQString()
                    # 对widget类型进行过滤 (可在info.py中查看所有widget_type)
                    if widget_type in ['widget_type_1', 'widget_type_2', '...']:
                        e.ignore()
                        return None
                # 根据不同类型读取id
                data = e.mimeData().data("structure_tree/move-wid")
                if e.mimeData().hasFormat("structure_tree/copy-wid"):
                    data = e.mimeData().data("structure_tree/copy-wid")
                elif e.mimeData().hasFormat("structure_tree/refer-wid"):
                    data = e.mimeData().data("structure_tree/refer-wid")
                stream = QDataStream(data, QIODevice.ReadOnly)
                widget_id = stream.readQString()
                # 检测widget_id是否违法
                if Func.checkValidityDragFromStructure(self.widget_id, widget_id):
                    # sign显示
                    self.signShow.emit(e.pos().x())
                    e.setDropAction(Qt.CopyAction)
                    e.accept()
                else:
                    QMessageBox.information(self, 'Warning', 'Invalid drag!')
                    e.ignore()
            else:
                e.ignore()
        except Exception as e:
            print(f"error {e} happens in drag enter widget icon area. [widget_icon_area/main.py]")

    def dragMoveEvent(self, e):
        try:
            if e.mimeData().hasFormat("widget_icon_bar/widget_icon_type") or \
                    e.mimeData().hasFormat("widget_icon_table/copy-col") or \
                    e.mimeData().hasFormat("widget_icon_table/move-col") or \
                    e.mimeData().hasFormat("structure_tree/move-wid") or \
                    e.mimeData().hasFormat("structure_tree/copy-wid") or \
                    e.mimeData().hasFormat("structure_tree/refer-wid"):
                # sign显示
                self.signShow.emit(e.pos().x())
                e.setDropAction(Qt.CopyAction)
                e.accept()
            else:
                e.ignore()
        except Exception as e:
            print(f"error {e} happens in drag move in widget icon area. [widget_icon_area/main.py]")

    def dropEvent(self, e):
        try:
            if e.mimeData().hasFormat("widget_icon_bar/widget_icon_type"):
                # 从widget icon bar拖拽到widget icon area中
                data = e.mimeData().data("widget_icon_bar/widget_icon_type")
                stream = QDataStream(data, QIODevice.ReadOnly)
                # 读取当前拖拽widget类型
                widget_type = stream.readQString()
                # 先直接放入末尾(非最后一列的意思)，因为这样省事
                self.widget_icon_table.insertColumn(self.widget_icon_table.widget_icon_count + 1)
                widget_id = self.widget_icon_table.setWidgetIcon(self.widget_icon_table.widget_icon_count, widget_type)
                name = Func.generateValidName(widget_id)
                self.widget_icon_table.setWidgetName(self.widget_icon_table.widget_icon_count, name)
                # 根据鼠标的位置进行移动
                drag_col = self.widget_icon_table.widget_icon_count
                target_col = self.widget_icon_table.getColumnForInsert(e.pos().x())
                if target_col != -1 and target_col < drag_col:
                    self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                # end
                QApplication.processEvents()
                self.signHide.emit()
                QApplication.processEvents()
                self.widgetIconAdd.emit(self.widget_id, widget_id, name, Info.WidgetAdd, '')
                QApplication.processEvents()
                self.widgetIconMove.emit(widget_id, drag_col, target_col)
                QApplication.processEvents()
                e.setDropAction(Qt.CopyAction)
                QApplication.processEvents()
                e.accept()
                QApplication.processEvents()
            elif e.mimeData().hasFormat("widget_icon_table/move-col"):
                # widget icon table中widget icon的移动
                data = e.mimeData().data("widget_icon_table/move-col")
                stream = QDataStream(data, QIODevice.ReadOnly)
                drag_col = stream.readInt()
                target_col = -1
                mouse_col = self.widget_icon_table.columnAt(e.pos().x())
                # move to front
                if drag_col > mouse_col != -1:
                    target_col = self.widget_icon_table.getColumnToFront(e.pos().x())
                    self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                # move to back
                elif drag_col < mouse_col or mouse_col == -1:
                    target_col = self.widget_icon_table.getColumnToBack(e.pos().x())
                    self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                # end
                QApplication.processEvents()
                self.signHide.emit()
                QApplication.processEvents()
                if target_col != -1:
                    self.widgetIconMove.emit(self.widget_icon_table.cellWidget(1, target_col).widget_id, drag_col,
                                             target_col)
                QApplication.processEvents()
                e.setDropAction(Qt.CopyAction)
                QApplication.processEvents()
                e.accept()
                QApplication.processEvents()
            elif e.mimeData().hasFormat("widget_icon_table/copy-col"):
                # widget icon table中widget icon的复制
                data = e.mimeData().data("widget_icon_table/copy-col")
                stream = QDataStream(data, QIODevice.ReadOnly)
                col = stream.readInt()
                # 复制就和新添加差不多，但是多一个复制信号的发射
                old_widget_id = self.widget_icon_table.cellWidget(1, col).widget_id
                widget_type = old_widget_id.split('.')[0]
                # 插入一列，放到最后
                self.widget_icon_table.insertColumn(self.widget_icon_table.widget_icon_count + 1)
                new_widget_id = self.widget_icon_table.setWidgetIcon(self.widget_icon_table.widget_icon_count,
                                                                     widget_type)
                name = Func.generateValidName(new_widget_id)
                self.widget_icon_table.setWidgetName(self.widget_icon_table.widget_icon_count, name)
                # 根据鼠标的位置进行移动
                drag_col = self.widget_icon_table.widget_icon_count
                target_col = self.widget_icon_table.getColumnForInsert(e.pos().x())
                if target_col != -1 and target_col < drag_col:
                    self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                # end
                QApplication.processEvents()
                self.signHide.emit()
                QApplication.processEvents()
                self.widgetIconAdd.emit(self.widget_id, new_widget_id, name, Info.WidgetCopy, old_widget_id)
                QApplication.processEvents()
                self.widgetIconMove.emit(new_widget_id, drag_col, target_col)
                QApplication.processEvents()
                e.setDropAction(Qt.CopyAction)
                QApplication.processEvents()
                e.accept()
                QApplication.processEvents()
            elif e.mimeData().hasFormat("structure_tree/move-wid"):
                # move要将原有的删除
                data = e.mimeData().data("structure_tree/move-wid")
                stream = QDataStream(data, QIODevice.ReadOnly)
                widget_id = stream.readQString()
                # 检测是否在此timeline中已经存在同名widget，如果有则变成已有的widget进行移动
                name = Info.WID_NODE[widget_id].text(0)
                existed = False
                drag_col = -1
                for col in range(1, self.widget_icon_table.widget_icon_count + 1):
                    if name == self.widget_icon_table.item(3, col).text():
                        existed = True
                        drag_col = col
                if existed:
                    # widget icon table中widget icon的移动
                    target_col = -1
                    mouse_col = self.widget_icon_table.columnAt(e.pos().x())
                    # move to front
                    if drag_col > mouse_col and mouse_col != -1:
                        target_col = self.widget_icon_table.getColumnToFront(e.pos().x())
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                    # move to back
                    elif drag_col < mouse_col or mouse_col == -1:
                        target_col = self.widget_icon_table.getColumnToBack(e.pos().x())
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                    # end
                    QApplication.processEvents()
                    self.signHide.emit()
                    QApplication.processEvents()
                    if target_col != -1:
                        self.widgetIconMove.emit(self.widget_icon_table.cellWidget(1, target_col).widget_id, drag_col,
                                                 target_col)
                    QApplication.processEvents()
                    e.setDropAction(Qt.CopyAction)
                    QApplication.processEvents()
                    e.accept()
                    QApplication.processEvents()
                else:
                    # 相当于add一个已有widget_id的widget_icon
                    # 先直接放入末尾(非最后一列的意思)，因为这样省事
                    self.widget_icon_table.insertColumn(self.widget_icon_table.widget_icon_count + 1)
                    self.widget_icon_table.setWidgetIcon(self.widget_icon_table.widget_icon_count,
                                                         widget_type=widget_id.split('.')[0],
                                                         widget_id=widget_id)
                    self.widget_icon_table.setWidgetName(self.widget_icon_table.widget_icon_count, name)
                    # 根据鼠标的位置进行移动
                    target_col = self.widget_icon_table.getColumnForInsert(e.pos().x())
                    if target_col != -1 and target_col < drag_col:
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                    # 信号
                    self.widgetIconAdd.emit(self.widget_id, widget_id, name, Info.WidgetMove, '')
                    self.widgetIconMove.emit(widget_id, drag_col, target_col)
                    # end
                    QApplication.processEvents()
                    self.signHide.emit()
                    QApplication.processEvents()
                    e.setDropAction(Qt.CopyAction)
                    QApplication.processEvents()
                    e.accept()
                    QApplication.processEvents()
            elif e.mimeData().hasFormat("structure_tree/copy-wid"):
                data = e.mimeData().data("structure_tree/copy-wid")
                stream = QDataStream(data, QIODevice.ReadOnly)
                old_widget_id = stream.readQString()
                widget_type = old_widget_id.split('.')[0]
                # 插入一列，放到最后
                self.widget_icon_table.insertColumn(self.widget_icon_table.widget_icon_count + 1)
                new_widget_id = self.widget_icon_table.setWidgetIcon(self.widget_icon_table.widget_icon_count,
                                                                     widget_type)
                name = Func.generateValidName(new_widget_id)
                self.widget_icon_table.setWidgetName(self.widget_icon_table.widget_icon_count, name)
                # 根据鼠标的位置进行移动
                drag_col = self.widget_icon_table.widget_icon_count
                target_col = self.widget_icon_table.getColumnForInsert(e.pos().x())
                if target_col != -1 and target_col < drag_col:
                    self.widget_icon_table.moveWidgetIcon(drag_col, target_col)

                # end
                QApplication.processEvents()
                self.signHide.emit()
                QApplication.processEvents()
                self.widgetIconAdd.emit(self.widget_id, new_widget_id, name, Info.WidgetCopy, old_widget_id)
                QApplication.processEvents()
                self.widgetIconMove.emit(new_widget_id, drag_col, target_col)
                QApplication.processEvents()
                e.setDropAction(Qt.CopyAction)
                QApplication.processEvents()
                e.accept()
                QApplication.processEvents()
            elif e.mimeData().hasFormat("structure_tree/refer-wid"):
                data = e.mimeData().data("structure_tree/refer-wid")
                stream = QDataStream(data, QIODevice.ReadOnly)
                old_widget_id = stream.readQString()
                # 检测是否在此timeline中已经存在同名widget，如果有则变成已有的widget进行移动
                name = Info.WID_NODE[old_widget_id].text(0)
                existed = False
                drag_col = -1
                for col in range(1, self.widget_icon_table.widget_icon_count + 1):
                    if name == self.widget_icon_table.item(3, col).text():
                        existed = True
                        drag_col = col
                if existed:
                    # widget icon table中widget icon的移动
                    target_col = -1
                    mouse_col = self.widget_icon_table.columnAt(e.pos().x())
                    # move to front
                    if drag_col > mouse_col and mouse_col != -1:
                        target_col = self.widget_icon_table.getColumnToFront(e.pos().x())
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                    # move to back
                    elif drag_col < mouse_col or mouse_col == -1:
                        target_col = self.widget_icon_table.getColumnToBack(e.pos().x())
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)
                    # end
                    QApplication.processEvents()
                    self.signHide.emit()
                    QApplication.processEvents()
                    if target_col != -1:
                        self.widgetIconMove.emit(self.widget_icon_table.cellWidget(1, target_col).widget_id, drag_col,
                                                 target_col)
                    QApplication.processEvents()
                    e.setDropAction(Qt.CopyAction)
                    QApplication.processEvents()
                    e.accept()
                    QApplication.processEvents()
                else:
                    widget_type = old_widget_id.split('.')[0]
                    # 先直接放入末尾(非最后一列)，因为这样省事
                    self.widget_icon_table.insertColumn(self.widget_icon_table.widget_icon_count + 1)
                    new_widget_id = self.widget_icon_table.setWidgetIcon(self.widget_icon_table.widget_icon_count,
                                                                         widget_type)
                    self.widget_icon_table.setWidgetName(self.widget_icon_table.widget_icon_count, name)
                    # 根据鼠标的位置进行移动
                    drag_col = self.widget_icon_table.widget_icon_count
                    target_col = self.widget_icon_table.getColumnForInsert(e.pos().x())
                    if target_col != -1 and target_col < drag_col:
                        self.widget_icon_table.moveWidgetIcon(drag_col, target_col)

                    # end
                    QApplication.processEvents()
                    self.signHide.emit()
                    QApplication.processEvents()
                    QApplication.processEvents()
                    self.widgetIconAdd.emit(self.widget_id, new_widget_id, name, Info.WidgetRefer, old_widget_id)
                    QApplication.processEvents()
                    self.widgetIconMove.emit(new_widget_id, drag_col, target_col)
                    QApplication.processEvents()
                    e.setDropAction(Qt.CopyAction)
                    QApplication.processEvents()
                    e.accept()
                    QApplication.processEvents()
                # end
                QApplication.processEvents()
                self.signHide.emit()
                QApplication.processEvents()
                e.setDropAction(Qt.CopyAction)
                QApplication.processEvents()
                e.accept()
                QApplication.processEvents()
            else:
                QApplication.processEvents()
                e.ignore()
                QApplication.processEvents()
        except Exception as e:
            QApplication.processEvents()
            self.signHide.emit()
            QApplication.processEvents()
            print(f"error {e} happens in drop in widget icon area. [widget_icon_area/main.py]")

    def dragLeaveEvent(self, e):
        self.signHide.emit()

    def getInfo(self):
        info = {}
        info['widget_icon_table'] = self.widget_icon_table.getInfo()
        return info

    def restore(self, info):
        self.widget_icon_table.restore(info['widget_icon_table'])
