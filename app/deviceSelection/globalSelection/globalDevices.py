from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QApplication, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit, QMessageBox

from app.center.widget_tabs.events.durationPage import DurationPage
from app.deviceSelection.globalSelection.describer import Describer
from app.deviceSelection.globalSelection.device import Device
from app.deviceSelection.globalSelection.selectionList import SelectArea
from app.info import Info


class GlobalDevice(QWidget):
    """
    :param io_type: 输出、输入设备
    """
    # 发送到duration的类变量中最为合适 (device_type, devices: name->type)
    deviceSelect = pyqtSignal(int, dict)
    deviceNameChanged = pyqtSignal(str, str)

    def __init__(self, io_type=0, parent=None):
        super(GlobalDevice, self).__init__(parent)

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
        self.device_type = io_type

        # device_list是写死的
        if io_type == Info.OUTPUT_DEVICE:
            self.devices = ("serial_port", "parallel_port", "network_port", "screen", "sound")
            self.setWindowTitle("Output Devices")
        else:
            self.devices = ("mouse", "keyboard", "response box", "game pad")
            self.setWindowTitle("Input Devices")
        for device in self.devices:
            self.devices_list.addItem(Device(device))

        # 已选择设备
        self.selected_devices = SelectArea(self.device_type)
        self.selected_devices.itemDoubleClicked.connect(self.rename)
        self.selected_devices.itemDoubleClick.connect(self.rename)
        self.selected_devices.itemChanged.connect(self.changeItem)

        # 展示区
        self.describer = Describer()
        self.describer.portChanged.connect(self.changePort)
        self.describer.ipPortChanged.connect(self.changeIpPort)
        self.describer.colorChanged.connect(self.changeColor)
        self.describer.sampleChanged.connect(self.changeSample)
        self.describer.baudChanged.connect(self.changeBaud)
        self.describer.bitsChanged.connect(self.changeBits)
        self.describer.clientChanged.connect(self.changeClient)
        self.describer.samplingRateChanged.connect(self.changeSamplingRate)
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
        default_properties: dict = self.selected_devices.getInfo()
        self.deviceSelect.emit(self.device_type, default_properties)

    def changeItem(self, device_type: str, device_name: str, device_port: str, others: dict):
        self.describer.describe(device_type, device_name, device_port, others)

    def changePort(self, port: str):
        self.selected_devices.changeCurrentPort(port)

    def changeColor(self, color: str):
        self.selected_devices.changeCurrentColor(color)

    def changeSample(self, sample: str):
        self.selected_devices.changeCurrentSample(sample)

    def changeIpPort(self, ip_port: str):
        self.selected_devices.changeCurrentIpPort(ip_port)

    def changeClient(self, client: str):
        self.selected_devices.changeCurrentClient(client)

    def changeSamplingRate(self, sampling_rate: str):
        self.selected_devices.changeCurrentSamplingRate(sampling_rate)

    def changeBaud(self, baud: str):
        self.selected_devices.changeCurrentBaud(baud)

    def changeBits(self, bits: str):
        self.selected_devices.changeCurrentBits(bits)

    def rename(self, item: Device):
        name: str = item.text()
        item_name: str = name.lower()

        text, ok = QInputDialog.getText(self, "Change Device Name", "Device Name:", QLineEdit.Normal, item.text())
        if ok and text != '':
            text: str
            if text.lower() in self.selected_devices.device_name and item_name != text.lower():
                QMessageBox.warning(self, f"{text} is invalid!", "Device name must be unique and without spaces",
                                    QMessageBox.Ok)
            else:
                self.selected_devices.changeCurrentName(text)
                self.describer.changeName(text)
                self.getInfo()
                self.deviceNameChanged.emit(item.getDeviceId(), text)

    # 参数导出, 记录到Info
    def getInfo(self):
        device_info: dict = self.selected_devices.getInfo()
        if self.device_type:
            Info.OUTPUT_DEVICE_INFO = device_info.copy()
        else:
            Info.INPUT_DEVICE_INFO = device_info.copy()

    # 参数导入
    def setProperties(self, properties: dict):
        self.selected_devices.clearAll()
        self.selected_devices.setProperties(properties)
        # 更新全局信息
        if self.device_type:
            Info.OUTPUT_DEVICE_INFO.update(properties)
        else:
            Info.INPUT_DEVICE_INFO.update(properties)
