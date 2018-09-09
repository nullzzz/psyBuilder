from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QMouseEvent, QDragMoveEvent, QCursor
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, \
    QListView, QFrame, QPushButton, QMenu

in_device = {
    "mouse": 0,
    "keyboard": 0,
    "response box": 0,
    "game pad": 0
}
out_device = {
    "serial_port": 0,
    "parallel_port": 0,
    "network_port": 0,
}


class GlobalDevice(QWidget):
    InputDevice = 0
    outputDevice = 1
    # 发送到duration的类变量中最为合适 (device_type, devices: name->type)
    deviceSelect = pyqtSignal(int, dict)

    def __init__(self, device_type=0, parent=None):
        super(GlobalDevice, self).__init__(parent)
        self.device_type = device_type
        if device_type:
            self.devices = out_device
            self.setWindowTitle("Output Devices")
        else:
            self.devices = in_device
            self.setWindowTitle("Input Devices")
        self.devices_list = QListWidget()
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(10)
        self.devices_list.setFrameStyle(QFrame.NoFrame)
        self.devices_list.setIconSize(QSize(40, 40))

        self.selected_devices = DropDemo(self.device_type)
        self.describe = QTextEdit()
        self.describe.setText("此处留白\n\t设备描述\n\t参数设置")

        self.ok_bt = QPushButton("Ok")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.close)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):

        for device in self.devices:
            self.devices_list.addItem(DeviceItem(device, device))

        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.addWidget(self.selected_devices, 1)
        layout1.addWidget(self.describe, 1)
        layout2 = QHBoxLayout()
        layout2.addStretch(5)
        layout2.addWidget(self.ok_bt)
        layout2.addWidget(self.cancel_bt)
        layout2.addWidget(self.apply_bt)

        layout.addWidget(self.devices_list, 1)
        layout.addLayout(layout1, 3)
        layout.addLayout(layout2, 1)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()

    def apply(self):
        self.deviceSelect.emit(self.device_type, self.selected_devices.getInfo())


class DeviceItem(QListWidgetItem):
    def __init__(self, device_type: str, name: str, parent=None):
        super(DeviceItem, self).__init__(name, parent)
        self.types = ("mouse", "keyboard")
        self.item_type = device_type
        self.describe = QTextEdit()
        # self.setIcon(QIcon(r"..\image\{}_device.png".format(self.item_type)))
        self.setIcon(QIcon("image/{}_device.png".format(self.item_type)))

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        return DeviceItem(self.item_type, self.text())


class DropDemo(QListWidget):

    def __init__(self, device_type=0, parent=None):
        super(DropDemo, self).__init__(parent)
        self.device_type = device_type

        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)
        self.createContextMenu()


    def dropEvent(self, e):
        source = e.source()
        item_type = source.currentItem().item_type
        drop_item = source.currentItem().clone()
        if self.device_type:
            out_device[item_type] += 1
            if out_device[item_type] > 1:
                drop_item.setText("{}{}".format(drop_item.text(), out_device[item_type]))
        else:
            in_device[item_type] += 1
            if in_device[item_type] > 1:
                drop_item.setText("{}{}".format(drop_item.text(), in_device[item_type]))

        # 当前位置item
        item = self.itemAt(e.pos())
        insert_pos = self.row(item)
        # 外部添加
        if source != self:
            if item is not None:
                self.insertItem(insert_pos, drop_item)
            else:
                self.addItem(drop_item)
        # 内部调序
        # 暂不支持
        elif source == self:
            if self.dragItem == item:
                pass
            else:
                if item is None:
                    self.addItem(self.dragItem.clone())
                else:
                    self.insertItem(insert_pos-1, self.dragItem.clone())

    def dragEnterEvent(self, e):
        source = e.source()
        if source != self:
            e.setDropAction(Qt.MoveAction)
        e.accept()

    # 记录鼠标按下的信息
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            item = self.itemAt(e.pos())
            self.start_pos = self.row(item)
            self.dragItem = item
        QListWidget.mousePressEvent(self, e)

    def dragMoveEvent(self, e: QDragMoveEvent):
        item = self.itemAt(e.pos())
        if item:
            item.setSelected(True)
        e.accept()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)
        self.delete_action = self.contextMenu.addAction("delete")
        self.delete_action.triggered.connect(self.deleteItem)
        self.clear_action = self.contextMenu.addAction("clear")
        self.clear_action.triggered.connect(self.clear)

    def deleteItem(self):
        self.takeItem(self.currentRow())

    def showContextMenu(self, pos):
        if self.count():
            item = self.itemAt(pos)
            if item:
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    # 返回选择设备
    # type: dict
    # name: type
    def getInfo(self):
        dic = {}
        for i in range(self.count()):
            dic[self.item(i).text()] = self.item(i).item_type
        return dic


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = GlobalDevice(1)

    t.show()

    sys.exit(app.exec())
