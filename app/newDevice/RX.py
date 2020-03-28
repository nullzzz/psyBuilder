from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit, QMessageBox

from app.func import Func
from app.info import Info
from app.newDevice.describer.control import Describer
from app.newDevice.device.control import DeviceHome, Device


class RX(QWidget):
    """
    :param device_type: 0-输入、1-输出设备、2-quest、3-tracker
    """
    deviceNameChanged = pyqtSignal(str, str)
    deviceOK = pyqtSignal()

    def __init__(self, device_type: int = 0, parent=None):
        super(RX, self).__init__(parent)

        if True:
            # 上方待选择设备
            self.devices_list = QListWidget()
            self.devices_list.setViewMode(QListView.IconMode)
            self.devices_list.setSortingEnabled(True)
            self.devices_list.setAcceptDrops(False)
            self.devices_list.setAutoFillBackground(True)
            self.devices_list.setWrapping(False)
            self.devices_list.setSpacing(10)
            self.devices_list.setFrameStyle(QFrame.NoFrame)
            self.devices_list.setIconSize(QSize(40, 40))

            # 设备类型
            self.device_type = device_type
            # 设备信息
            self.default_properties: dict = {}

        # 已选择设备
        self.selected_devices = DeviceHome()
        self.selected_devices.itemDoubleClicked.connect(self.rename)
        self.selected_devices.itemDoubleClick.connect(self.rename)
        self.selected_devices.deviceChanged.connect(self.changeItem)
        self.selected_devices.deviceDeleted.connect(self.changeItem)

        # 展示区
        self.describer = Describer()

        # very import!!!
        # very import!!!
        # very import!!!
        self.selected_devices.default_properties = self.default_properties
        self.describer.default_properties = self.default_properties

        # device_list是写死的
        if device_type == Info.OUTPUT_DEVICE:
            self.selected_devices.createDevice("screen")
            Info.OUTPUT_DEVICE_INFO = self.default_properties
            self.devices = ("serial_port", "parallel_port", "network_port", "screen", "sound")
            self.setWindowTitle("Output Devices")
        elif device_type == Info.INPUT_DEVICE:
            self.selected_devices.createDevice("mouse")
            self.selected_devices.createDevice("keyboard")
            Info.INPUT_DEVICE_INFO = self.default_properties
            self.devices = ("mouse", "keyboard", "response box", "game pad", "action")
            self.setWindowTitle("Input Devices")
        elif device_type == Info.QUEST_DEVICE:
            Info.QUEST_DEVICE_INFO = self.default_properties
            self.devices = ("quest",)
            self.setWindowTitle("Quest Devices")
        elif device_type == Info.TRACKER_DEVICE:
            Info.TRACKER_DEVICE_INFO = self.default_properties
            self.devices = ("tracker",)
            self.setWindowTitle("Tracker Devices")
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))
        for device in self.devices:
            self.devices_list.addItem(Device(device))

        self.ok()

        # 按键区
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
        layout1.addWidget(self.describer, 1)

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
        self.selected_devices.loadSetting()

    def apply(self):
        self.getInfo()
        self.deviceOK.emit()

    def changeItem(self, device_id: str, info: dict):
        self.describer.describe(device_id, info)

    def rename(self, item: Device):
        name: str = item.text()
        item_name: str = name.lower()

        text, ok = QInputDialog.getText(self, "Change Device Name", "Device Name:", QLineEdit.Normal, item.text())
        if ok and text != '' and "." not in text:
            text: str
            if text.lower() in self.selected_devices.device_list and item_name != text.lower():
                QMessageBox.warning(self, f"{text} is invalid!", "Device name must be unique and without spaces",
                                    QMessageBox.Ok)
            else:
                self.selected_devices.changeCurrentName(item_name, text)
                self.describer.changeName(item_name, text)
                # self.getInfo()
                self.deviceNameChanged.emit(item.getDeviceId(), text)

    # 参数导出, 记录到Info
    def getInfo(self):
        # get device information from GUI
        self.describer.updateInfo()
        # update device information
        self.selected_devices.updateDeviceInfo()
        return self.default_properties.copy()

    # 参数导入
    def setProperties(self, properties: dict):
        self.default_properties.clear()
        self.default_properties.update(properties)
        self.loadSetting()
        self.deviceOK.emit()

    def loadSetting(self):
        self.selected_devices.loadSetting()

    def refresh(self):
        self.describer.updateSimpleInfo()

    def show(self) -> None:
        self.refresh()
        super().show()
