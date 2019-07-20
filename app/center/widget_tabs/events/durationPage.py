from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QGroupBox, \
    QHBoxLayout, QGridLayout, QVBoxLayout, QCompleter, QMessageBox, QListWidgetItem

from app.center.widget_tabs.events.inDevicePro import InDeviceInfoAtDuration, InDeviceRespAtDuration
from app.center.widget_tabs.events.outDevicePro import OutDeviceInfoAtDuration
from app.deviceSelection.widgetSelection.InputDeviceItem import DeviceInItem
from app.deviceSelection.widgetSelection.OutputDeviceItem import DeviceOutItem
from app.deviceSelection.widgetSelection.deviceChooseDialog import DeviceOutDialog, DeviceInDialog
from app.deviceSelection.widgetSelection.deviceShowArea import ShowArea
from app.func import Func
from app.info import Info
from app.lib import PigComboBox


class DurationPage(QWidget):
    def __init__(self, parent=None):
        super(DurationPage, self).__init__(parent)

        self.attributes = []
        self.default_properties = {
            "Duration": "(Infinite)",
            "Input devices": {},
            "Output devices": {}
        }
        # top
        self.duration = PigComboBox()
        self.duration.setInsertPolicy(QComboBox.NoInsert)
        self.duration.installEventFilter(self)
        # output device
        # 输出设备
        self.out_devices = ShowArea()
        # 参数
        self.out_info = OutDeviceInfoAtDuration()
        self.out_devices.infoChanged.connect(self.out_info.showInfo)
        self.out_devices.areaStatus.connect(self.controlOutDevice)
        self.out_info.valueOrMessageChanged.connect(self.out_devices.changeValueOrMessage)
        self.out_info.pulseDurationChanged.connect(self.out_devices.changePulseDuration)
        self.out_info.hide()

        self.out_add_bt = QPushButton("+")
        self.out_add_bt.clicked.connect(self.showOutDevices)
        self.out_del_bt = QPushButton("-")
        self.out_del_bt.clicked.connect(self.out_devices.delDevice)
        self.out_del_bt.setEnabled(False)
        self.out_tip = QLabel("Add output device(s) first")
        self.out_tip.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # input device
        self.in_info = InDeviceInfoAtDuration()
        self.in_resp = InDeviceRespAtDuration()
        self.out_devices.usingOutputDeviceUpdate.connect(self.in_resp.changeOutputDevice)
        self.in_tip1 = QLabel("Add input device(s) first")
        self.in_tip2 = QLabel("Resp Trigger:")
        self.in_tip1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.in_tip2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # self.selected_in_devices = []
        self.in_devices = ShowArea(device_type=Info.INPUT_DEVICE)
        self.in_info.allowableChanged.connect(self.in_devices.changeAllowable)
        self.in_info.correctChanged.connect(self.in_devices.changeCorrect)
        self.in_info.rtWindowChanged.connect(self.in_devices.changeRtWindow)
        self.in_info.endActionChanged.connect(self.in_devices.changeEndAction)

        self.in_resp.rightChanged.connect(self.in_devices.changeRight)
        self.in_resp.wrongChanged.connect(self.in_devices.changeWrong)
        self.in_resp.ignoreChanged.connect(self.in_devices.changeIgnore)
        self.in_resp.outputChanged.connect(self.in_devices.changeOutput)
        self.in_info.hide()
        self.in_resp.hide()
        self.in_devices.infoChanged.connect(self.in_info.showInfo)
        self.in_devices.respChanged.connect(self.in_resp.showResp)
        self.in_devices.areaStatus.connect(self.controlInDevice)
        self.in_add_bt = QPushButton("&Add...")
        self.in_del_bt = QPushButton("&Remove...")
        self.in_add_bt.clicked.connect(self.showInDevices)
        self.in_del_bt = QPushButton("-")
        self.in_del_bt.clicked.connect(self.in_devices.delDevice)
        self.setUI()

    # 生成duration页面
    def setUI(self):
        group0 = QGroupBox()
        self.duration.addItems(("(Infinite)", "100", "250", "500", "1000", "2000", "3000", "4000", "5000", "0~200"))
        self.duration.setEditable(True)

        layout0 = QHBoxLayout()
        layout0.addWidget(QLabel("Duration(ms):"), 1)
        layout0.addWidget(self.duration, 4)
        group0.setLayout(layout0)

        group1 = QGroupBox("Stim Trigger")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("Output Devices"), 0, 0, 1, 2)
        layout1.addWidget(QLabel("Trigger Info"), 0, 2, 1, 1)
        layout1.addWidget(self.out_devices, 1, 0, 2, 2)
        layout1.addWidget(self.out_add_bt, 3, 0, 1, 1)
        layout1.addWidget(self.out_del_bt, 3, 1, 1, 1)
        layout1.addWidget(self.out_tip, 1, 2, 2, 2)
        layout1.addWidget(self.out_info, 1, 2, 2, 2)
        layout1.setVerticalSpacing(0)
        group1.setLayout(layout1)

        group2 = QGroupBox("Input Devices")
        layout2 = QGridLayout()
        self.in_del_bt.setEnabled(False)

        self.in_devices.setStyleSheet("background-color: white;")
        layout2.addWidget(QLabel("Device(s)"), 0, 0, 1, 1)
        layout2.addWidget(self.in_devices, 1, 0, 3, 2)
        layout2.addWidget(self.in_add_bt, 4, 0, 1, 1)
        layout2.addWidget(self.in_del_bt, 4, 1, 1, 1)
        layout2.addWidget(self.in_tip1, 1, 2, 5, 2)
        layout2.addWidget(self.in_info, 0, 2, 5, 2)
        layout2.addWidget(self.in_tip2, 5, 0, 2, 4)
        layout2.addWidget(self.in_resp, 5, 0, 2, 4)
        layout2.setVerticalSpacing(0)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group0, 1)
        layout.addWidget(group1, 6)
        layout.addWidget(group2, 6)
        self.setLayout(layout)

    # 弹出输入设备选择框
    def showInDevices(self):
        self.in_devices_dialog = DeviceInDialog()
        self.in_devices_dialog.addDevices(Info.INPUT_DEVICE_INFO)

        self.in_devices_dialog.ok_bt.clicked.connect(self.selectIn)
        self.in_devices_dialog.cancel_bt.clicked.connect(self.in_devices_dialog.close)

        self.in_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.in_devices_dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.in_devices_dialog.show()

    # 弹出输出设备选择框
    def showOutDevices(self):
        self.out_devices_dialog = DeviceOutDialog()

        self.out_devices_dialog.addDevices(Info.OUTPUT_DEVICE_INFO)
        self.out_devices_dialog.ok_bt.clicked.connect(self.selectOut)
        self.out_devices_dialog.cancel_bt.clicked.connect(self.out_devices_dialog.close)
        self.out_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.out_devices_dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.out_devices_dialog.show()

    # 添加输入设备
    def selectIn(self, e):
        # 选中设备，默认为0号位置
        temp: QListWidgetItem = self.in_devices_dialog.devices_list.currentItem()
        if temp:
            device_name = temp.text()
            device_id = temp.data(3)
            item = DeviceInItem(device_name, device_id)
            self.in_devices.addDevice(item)
            self.in_devices_dialog.close()
        else:
            self.in_devices_dialog.close()

    # 添加输出设备
    def selectOut(self, e):
        temp: QListWidgetItem = self.out_devices_dialog.devices_list.currentItem()
        if temp:
            device_name: str = temp.text()
            device_id: str = temp.data(3)
            item = DeviceOutItem(device_name, device_id)
            self.out_devices.addDevice(item)
            self.out_devices_dialog.close()
        else:
            self.out_devices_dialog.close()

    # 移除输入设备
    def removeInDevices(self):
        index = self.in_devices.currentRow()
        # 选中有效
        if index != -1:
            self.delInDevice(index)

    def controlOutDevice(self, status: int):
        if status == 0:
            self.out_del_bt.setEnabled(False)
            self.out_tip.show()
            self.out_info.hide()
        elif status == -1:
            self.out_add_bt.setEnabled(False)
        else:
            self.out_add_bt.setEnabled(True)
            self.out_del_bt.setEnabled(True)
            self.out_info.show()
            self.out_tip.hide()

    def controlInDevice(self, status: int):
        if status == 0:
            self.in_del_bt.setEnabled(False)
            self.in_tip1.show()
            self.in_tip2.show()
            self.in_info.hide()
            self.in_resp.hide()
        elif status == -1:
            self.in_add_bt.setEnabled(False)
        else:
            self.in_add_bt.setEnabled(True)
            self.in_del_bt.setEnabled(True)
            self.in_info.show()
            self.in_resp.show()
            self.in_tip1.hide()
            self.in_tip2.hide()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.duration.setCompleter(QCompleter(self.attributes))
        self.out_info.setAttributes(attributes)
        self.in_info.setAttributes(attributes)
        self.in_resp.setAttributes(attributes)

    # 返回参数
    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Duration"] = self.duration.currentText()
        self.default_properties["Input devices"] = self.in_devices.getInfo().copy()
        self.default_properties["Output devices"] = self.out_devices.getInfo().copy()
        return self.default_properties

    # 设置参数
    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.duration.setCurrentText(self.default_properties["Duration"])
        self.out_devices.setProperties(self.default_properties.get("Output devices"))
        self.in_devices.setProperties(self.default_properties.get("Input devices"))

    def clone(self):
        clone_page = DurationPage()
        clone_page.setProperties(self.default_properties)
        return clone_page

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.duration:
            if e.type() == QEvent.FocusOut:
                text = self.duration.currentText()
                # 是否是变量
                if text not in self.attributes:
                    # 是否是提供选项
                    if self.duration.findText(text, Qt.MatchCaseSensitive) == -1:
                        # 输入的数字
                        if text.isdigit():
                            pass
                        else:
                            # 输入的范围
                            split = text.split("~")
                            if len(split) == 2:
                                if split[0].isdigit() and split[1].isdigit():
                                    pass
                                else:
                                    QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                                    self.duration.setCurrentIndex(0)
                            else:
                                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                                self.duration.setCurrentIndex(0)

        return QWidget.eventFilter(self, obj, e)

    def changeCertainDeviceName(self, d_id, name):
        io_type = Func.getIOType(d_id)
        if io_type == Info.INPUT_DEVICE:
            self.in_devices.changeDeviceName(d_id, name)
        else:
            self.out_devices.changeDeviceName(d_id, name)
