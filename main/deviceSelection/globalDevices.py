from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QApplication, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit, QMessageBox, QStackedWidget

from Info import Info
from main.deviceSelection.inputDevice import InputDevice
from main.deviceSelection.outputDevice import OutputDevice
from main.deviceSelection.selectionList import SelectArea


class GlobalDevice(QWidget):
    InputDevice = 0
    OutputDevice = 1
    # 发送到duration的类变量中最为合适 (device_type, devices: name->type)
    deviceSelect = pyqtSignal(int, dict)
    """
    :param io_type: 输出、输入设备
    """
    def __init__(self, io_type=0, parent=None):
        super(GlobalDevice, self).__init__(parent)

        # 待选择设备
        self.devices_list = QListWidget()
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(10)
        self.devices_list.setFrameStyle(QFrame.NoFrame)
        self.devices_list.setIconSize(QSize(40, 40))

        self.device_type = io_type
        # device_list是写死的
        if io_type:
            self.devices = ("serial_port", "parallel_port", "network_port")
            self.setWindowTitle("Output Devices")
            # 添加设备
            for device in self.devices:
                self.devices_list.addItem(OutputDevice(device, device))
        else:
            self.devices = ("mouse", "keyboard", "response box", "game pad")
            self.setWindowTitle("Input Devices")
            for device in self.devices:
                self.devices_list.addItem(InputDevice(device, device))

        # 已选择设备
        self.selected_devices = SelectArea(self.device_type)
        self.selected_devices.itemDoubleClicked.connect(self.reName)
        self.selected_devices.itemDoubleClick.connect(self.reName)

        # self.selected_devices.currentItemChanged.connect(self.itemChanged)

        # 还母鸡要做啥子
        self.describe = QStackedWidget()
        # self.describe.setText("此处留白\n\t设备描述\n\t参数设置")

        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):

        layout = QVBoxLayout()

        layout1 = QHBoxLayout()
        layout1.addWidget(self.selected_devices, 1)
        layout1.addWidget(self.selected_devices.parameters, 1)
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

    def cancel(self):
        # self.selected_devices.clear()
        self.selected_devices.loadSetting()
        # print("cancel")
        # self.close()

    def apply(self):
        self.getInfo()
        default_properties = self.selected_devices.getInfo()
        self.deviceSelect.emit(self.device_type, default_properties)
        # print(default_properties)

    def itemChanged(self, e):
        if e:
            index = self.selected_devices.row(e)
            self.describe.setCurrentIndex(index)

    def reName(self, item):
        name: str = item.text()
        item_name: str = name.lower()
        text, ok = QInputDialog.getText(self, "Change Device Name", "Device Name:", QLineEdit.Normal, item.text())
        if ok and text != '':
            text: str
            if " " in text or (text.lower() in self.selected_devices.device_name and item_name != text.lower()):
                QMessageBox.warning(self, f"{text} is invalid!",
                                    "Device name must be unique and without spaces", QMessageBox.Ok)
            else:
                try:
                    self.selected_devices.device_name.remove(item.text().lower())
                except ValueError:
                    pass
                self.selected_devices.device_name.append(text.lower())
                if name in self.selected_devices.default_properties.keys():
                    self.selected_devices.default_properties[text] = self.selected_devices.default_properties[name].copy()
                    self.selected_devices.default_properties.pop(name)
                item.setName(text)

    # todo: 参数导出
    def getInfo(self):
        if self.device_type:
            Info.OUTPUT_DEVICE_INFO.update(self.selected_devices.getInfo().copy())
        else:
            Info.INPUT_DEVICE_INFO.update(self.selected_devices.getInfo().copy())

    # todo:参数导入
    def setProperties(self, properties: dict):
        self.selected_devices.clearAll()
        self.selected_devices.setProperties(properties)
        # 更新全局信息
        if self.device_type:
            Info.OUTPUT_DEVICE_INFO.update(properties)
        else:
            Info.INPUT_DEVICE_INFO.update(properties)



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = GlobalDevice(1)

    t.show()

    sys.exit(app.exec())
