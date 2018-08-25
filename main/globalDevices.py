from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QMouseEvent, QDragMoveEvent
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QTextEdit, QVBoxLayout, QHBoxLayout, QApplication, \
    QListView, QFrame, QPushButton

in_device = {
    "mouse": 0,
    "keyboard": 0,
    "response box": 0
}
out_device = {

}

# 暂时只考虑输出设备的选择
# 写完了输出在写输出
# 重点是我特么一个输出设备都不知道


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

        self.selected_devices = DropDemo()
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
        self.setIcon(QIcon(".\\.\\image\\{}_device.png".format(self.item_type)))

    # 重写clone，返回的是DeviceItem类型，而不是QListWidgetItem类型
    def clone(self):
        return DeviceItem(self.item_type, self.text())


class DropDemo(QListWidget):

    def __init__(self, parent=None):
        super(DropDemo, self).__init__(parent)
        # 拖动的图标
        self.dragItem = None
        # self.setViewMode(QListView.IconMode)
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
        self.setWrapping(False)

    def dropEvent(self, e):
        source = e.source()
        item_type = source.currentItem().item_type
        in_device[item_type] += 1
        drop_item = source.currentItem().clone()
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

    # 返回选择设备
    # type: dict
    # name: type
    def getInfo(self):
        dic = {}
        for i in range(self.count()):
            dic[self.item(i).text()] = self.item(i).item_type
        print(dic)
        return dic


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = GlobalDevice(1)

    t.show()

    sys.exit(app.exec())
