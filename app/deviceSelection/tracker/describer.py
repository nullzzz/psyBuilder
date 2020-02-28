from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QSpinBox, QGridLayout, QLineEdit, QComboBox


class Describer(QWidget):
    selectTrackerTypeChanged = pyqtSignal(str)

    calibrateTrackerChanged = pyqtSignal(str)
    calibrationBeepChanged = pyqtSignal(str)

    trackerDatafileChanged = pyqtSignal(str)

    velocityThresholdChanged = pyqtSignal(str)

    accelerationThresholdChanged = pyqtSignal(str)

    forceDriftCorrection = pyqtSignal(str)

    pupilSizeModeChanged = pyqtSignal(str)

    IPAddressChanged = pyqtSignal(str)

    sendPortChanged = pyqtSignal(str)

    receivePortChanged = pyqtSignal(str)
    ipv46AddressChanged = pyqtSignal(str)

    UDPPortChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Describer, self).__init__(parent)

        self.tracker_name_tip = QLabel("Tracker Name:")
        self.tracker_name = QLabel("Unselected")

        self.tracker_type_tip = QLabel("Tracker Type:")
        self.tracker_type = QComboBox()
        self.tracker_type.addItems(("Simple dummy", "Advanced dummy(mouse simulation)", "EyeLink", "SMI",
                                    "EyeTribe", "OpenGaze", "Tobii", "Tobii-legacy", "Tobii Pro Glasses 2"))
        self.tracker_type.currentIndexChanged.connect(self.typeChanged)
        self.tracker_type.currentTextChanged.connect(lambda x: self.selectTrackerTypeChanged.emit(x))

        self.calibrate_tracker = QCheckBox("Calibrate Tracker")
        self.calibration_beep = QCheckBox("Calibration Beep")

        # self.tracker_datafile_tip = QLabel("Eye Tracker Datafile:")
        self.tracker_datafile_tip = QLabel("Datafile:")
        self.tracker_datafile = QLineEdit("automatic")
        self.tracker_datafile.textChanged.connect(lambda x: self.trackerDatafileChanged.emit(x))

        # self.velocity_threshold_tip = QLabel("Saccade Velocity Threshold:")
        self.velocity_threshold_tip = QLabel("Velocity:")
        self.velocity_threshold = QSpinBox()
        self.velocity_threshold.setSuffix("°/s")
        self.velocity_threshold.valueChanged.connect(lambda x: self.velocityThresholdChanged.emit(str(x)))

        # self.acceleration_threshold_tip = QLabel("Saccade Acceleration Threshold:")
        self.acceleration_threshold_tip = QLabel("Acceleration:")
        self.acceleration_threshold = QSpinBox()
        self.acceleration_threshold.setSuffix("°/s/s")
        self.acceleration_threshold.setMaximum(99999)
        self.acceleration_threshold.valueChanged.connect(lambda x: self.accelerationThresholdChanged.emit(str(x)))

        self.force_drift_correction = QCheckBox("Force Drift Correction")
        # self.force_drift_correction = QCheckBox("Force Drift Correction (For EyeLink 1000)")

        self.pupil_size_mode_tip = QLabel("Pupil Size Mode:")
        self.pupil_size_mode = QComboBox()
        self.pupil_size_mode.addItems(("area", "diameter"))
        self.pupil_size_mode.currentTextChanged.connect(lambda x: self.pupilSizeModeChanged.emit(x))

        self.IP_address_tip = QLabel("IP Address:")
        self.IP_address = QLineEdit("127.0.0.1")
        self.IP_address.textChanged.connect(lambda x: self.IPAddressChanged.emit(x))

        self.send_port_tip = QLabel("Send Port:")
        self.send_port = QSpinBox()
        self.send_port.valueChanged.connect(lambda x: self.sendPortChanged.emit(str(x)))

        self.receive_port_tip = QLabel("Receive Port:")
        self.receive_port = QSpinBox()
        self.receive_port.valueChanged.connect(lambda x: self.receivePortChanged.emit(str(x)))

        # self.ipv46_address_tip = QLabel("Tobii Glasses IPv4/6 Address:")
        self.ipv46_address_tip = QLabel("IPv4/6 Address:")
        self.ipv46_address = QLineEdit("192.168.71.50")
        self.ipv46_address.textChanged.connect(lambda x: self.ipv46AddressChanged.emit(x))

        # self.UDP_port_tip = QLabel("Tobii Glasses UDP Port:")
        self.UDP_port_tip = QLabel("UDP Port:")
        self.UDP_port = QSpinBox()
        self.UDP_port.valueChanged.connect(lambda x: self.UDPPortChanged.emit(str(x)))
        self.setUI()

    def setUI(self):
        self.tracker_name_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracker_type_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracker_datafile_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.velocity_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.acceleration_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pupil_size_mode_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.IP_address_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.send_port_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.receive_port_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ipv46_address_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.UDP_port_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(self.tracker_name_tip, 0, 0, 1, 1)
        layout.addWidget(self.tracker_name, 0, 1, 1, 1)
        layout.addWidget(self.tracker_type_tip, 1, 0, 1, 1)
        layout.addWidget(self.tracker_type, 1, 1, 1, 1)
        layout.addWidget(self.calibrate_tracker, 2, 1, 1, 1)
        layout.addWidget(self.calibration_beep, 3, 1, 1, 1)
        layout.addWidget(self.tracker_datafile_tip, 4, 0, 1, 1)
        layout.addWidget(self.tracker_datafile, 4, 1, 1, 1)
        layout.addWidget(self.velocity_threshold_tip, 5, 0, 1, 1)
        layout.addWidget(self.velocity_threshold, 5, 1, 1, 1)
        layout.addWidget(self.acceleration_threshold_tip, 6, 0, 1, 1)
        layout.addWidget(self.acceleration_threshold, 6, 1, 1, 1)
        layout.addWidget(self.force_drift_correction, 7, 1, 1, 1)
        layout.addWidget(self.pupil_size_mode_tip, 8, 0, 1, 1)
        layout.addWidget(self.pupil_size_mode, 8, 1, 1, 1)
        layout.addWidget(self.IP_address_tip, 9, 0, 1, 1)
        layout.addWidget(self.IP_address, 9, 1, 1, 1)
        layout.addWidget(self.send_port_tip, 10, 0, 1, 1)
        layout.addWidget(self.send_port, 10, 1, 1, 1)
        layout.addWidget(self.receive_port_tip, 11, 0, 1, 1)
        layout.addWidget(self.receive_port, 11, 1, 1, 1)
        layout.addWidget(self.ipv46_address_tip, 12, 0, 1, 1)
        layout.addWidget(self.ipv46_address, 12, 1, 1, 1)
        layout.addWidget(self.UDP_port_tip, 13, 0, 1, 1)
        layout.addWidget(self.UDP_port, 13, 1, 1, 1)

        self.setLayout(layout)

    def typeChanged(self, index):
        self.force_drift_correction.setEnabled(index == 2)
        self.pupil_size_mode.setEnabled(index == 2)
        self.IP_address.setEnabled(index == 2 or index == 3)
        self.send_port.setEnabled(index == 2 or index == 3)
        self.receive_port.setEnabled(index == 2 or index == 3)
        self.ipv46_address.setEnabled(index == 8)
        self.UDP_port.setEnabled(index == 8)

    def describe(self, tracker_name, info: dict):
        self.tracker_name.setText(tracker_name)
        self.tracker_type.setCurrentText(info.get("Select tracker type", "Simple dummy"))
        self.tracker_datafile.setText(info.get("Eye tracker datafile", "automatic"))
        self.calibrate_tracker.setCheckState(info.get("Calibrate tracker", "") == "Yes")
        self.calibration_beep.setCheckState(info.get("Calibration beep", "") == "Yes")
        self.velocity_threshold.setValue(int(info.get("Saccade velocity threshold", "0")))
        self.acceleration_threshold.setValue(int(info.get("Saccade acceleration threshold", "0")))
        self.force_drift_correction.setCheckState((info.get("Force drift correction", "") == "Yes") * 2)
        self.pupil_size_mode.setCurrentText(info.get("Pupil size mode", "area"))
        self.IP_address.setText(info.get("IP address", "127.0.0.0"))
        self.send_port.setValue(int(info.get("Send port", "0")))
        self.receive_port.setValue(int(info.get("Receive port", "0")))
        self.ipv46_address.setText(info.get("Ipv4/Ipv6 address", "192.168.71.50"))
        self.UDP_port.setValue(int(info.get("UDP port", "0")))

    def changeName(self, name: str):
        self.tracker_name.setText(name)
