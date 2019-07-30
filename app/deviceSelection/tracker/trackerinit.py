from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QListView, QFrame, \
    QPushButton, QInputDialog, QLineEdit

from app.deviceSelection.tracker.describer import Describer
from app.deviceSelection.tracker.device import Tracker
from app.deviceSelection.tracker.selectionList import SelectArea
from app.func import Func
from app.info import Info
from lib.psy_message_box import PsyMessageBox as QMessageBox


class TrackerInit(QWidget):
    deviceSelect = pyqtSignal(int, dict)
    deviceNameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(TrackerInit, self).__init__(parent)

        self.setWindowTitle("Tracker")
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))

        # 上方待选择设备
        self.tracker_list = QListWidget()
        self.tracker_list.setViewMode(QListView.IconMode)
        self.tracker_list.setSortingEnabled(True)
        self.tracker_list.setAcceptDrops(False)
        self.tracker_list.setAutoFillBackground(True)
        self.tracker_list.setWrapping(False)
        self.tracker_list.setSpacing(10)
        self.tracker_list.setFrameStyle(QFrame.NoFrame)
        self.tracker_list.setIconSize(QSize(40, 40))

        self.trackers: tuple = ("tracker",)
        for tracker in self.trackers:
            self.tracker_list.addItem(Tracker(tracker))

        # 已选择设备
        self.selected_devices = SelectArea()
        self.selected_devices.itemDoubleClicked.connect(self.rename)
        self.selected_devices.itemDoubleClick.connect(self.rename)
        self.selected_devices.itemChanged.connect(self.changeItem)

        # 展示区
        self.describer = Describer()
        self.describer.selectTrackerTypeChanged.connect(self.changeSelectTrackerType)
        self.describer.calibrateTrackerChanged.connect(self.changeIsCalibrateTracker)
        self.describer.calibrationBeepChanged.connect(self.changeIsCalibrationBeep)
        self.describer.trackerDatafileChanged.connect(self.changeEyeTrackerDatafile)
        self.describer.velocityThresholdChanged.connect(self.changeSaccadeVelocityThreshold)
        self.describer.accelerationThresholdChanged.connect(self.changeSaccadeAccelerationThreshold)
        self.describer.forceDriftCorrection.connect(self.changeIsForceDriftCorrection)
        self.describer.pupilSizeModeChanged.connect(self.changePupilSizeMode)
        self.describer.IPAddressChanged.connect(self.changeIPAddress)
        self.describer.sendPortChanged.connect(self.changeSendPortNumber)
        self.describer.receivePortChanged.connect(self.changeReceivePortNumber)
        self.describer.ipv46AddressChanged.connect(self.changeTobiiGlassesIpv46Address)
        self.describer.UDPPortChanged.connect(self.changeTobiiGlassesUDPPortNumber)

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

        layout.addWidget(self.tracker_list, 1)
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

    def changeItem(self, name, info: dict):
        self.describer.describe(name, info)

    def changeSelectTrackerType(self, select_tracker_type: str):
        self.selected_devices.changeCurrentSelectTrackerType(select_tracker_type)

    def changeEyeTrackerDatafile(self, eye_tracker_datafile: str):
        self.selected_devices.changeCurrentEyeTrackerDatafile(eye_tracker_datafile)

    def changeIsCalibrateTracker(self, calibrate_tracker: str):
        self.selected_devices.changeCurrentIsCalibrateTracker(calibrate_tracker)

    def changeIsCalibrationBeep(self, calibration_beep: str):
        self.selected_devices.changeCurrentIsCalibrationBeep(calibration_beep)

    def changeSaccadeVelocityThreshold(self, velocity_threshold: str):
        self.selected_devices.changeCurrentSaccadeVelocityThreshold(velocity_threshold)

    def changeSaccadeAccelerationThreshold(self, acceleration_threshold: str):
        self.selected_devices.changeCurrentSaccadeAccelerationThreshold(acceleration_threshold)

    def changeIsForceDriftCorrection(self, force_drift_correction: str):
        self.selected_devices.changeCurrentIsForceDriftCorrection(force_drift_correction)

    def changePupilSizeMode(self, pupil_size_mode: str):
        self.selected_devices.changeCurrentPupilSizeMode(pupil_size_mode)

    def changeIPAddress(self, ip_address: str):
        self.selected_devices.changeCurrentIPAddress(ip_address)

    def changeSendPortNumber(self, send_port: str):
        self.selected_devices.changeCurrentSendPortNumber(send_port)

    def changeReceivePortNumber(self, receive_port: str):
        self.selected_devices.changeCurrentReceivePortNumber(receive_port)

    def changeTobiiGlassesIpv46Address(self, ipv46_address: str):
        self.selected_devices.changeCurrentTobiiGlassesIpv46Address(ipv46_address)

    def changeTobiiGlassesUDPPortNumber(self, udp_port: str):
        self.selected_devices.changeCurrentTobiiGlassesUDPPortNumber(udp_port)

    def rename(self, item: Tracker):
        name: str = item.text()
        item_name: str = name.lower()

        text, ok = QInputDialog.getText(self, "Change Tracker Name", "Tracker Name:", QLineEdit.Normal, item.text())
        if ok and text != '':
            text: str
            if text.lower() in self.selected_devices.tracker_name and item_name != text.lower():
                QMessageBox.warning(self, f"{text} is invalid!", "Tracker name must be unique",
                                    QMessageBox.Ok)
            else:
                self.selected_devices.changeCurrentName(text)
                self.describer.changeName(text)
                self.getInfo()
                self.deviceNameChanged.emit(item.getId(), text)

    # 参数导出, 记录到Info
    def getInfo(self):
        tracker_info: dict = self.selected_devices.getInfo()
        Info.TRACKER_INFO = tracker_info.copy()

    # 参数导入
    def setProperties(self, properties: dict):
        self.selected_devices.clearAll()
        self.selected_devices.setProperties(properties)
        # 更新全局信息
        Info.QUEST_INFO = properties.copy()
