import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QCheckBox, QSpinBox

from app.lib import PigComboBox, PigLineEdit


class Open(QWidget):

    def __init__(self, parent=None):
        super(Open, self).__init__(parent)

        self.select_tracker_type_tip = QLabel("Select Tracker Type:")
        self.select_tracker_type = PigComboBox()

        self.calibrate_tracker = QCheckBox("Calibrate Tracker")
        self.calibration_beep = QCheckBox("Calibration Beep")

        self.eye_tracker_datafile_tip = QLabel("Eye Tracker Datafile:")
        self.eye_tracker_datafile = PigLineEdit()
        self.saccade_velocity_threshold_tip = QLabel("Saccade Velocity Threshold:")
        self.saccade_velocity_threshold = QSpinBox()
        self.saccade_acceleration_threshold_tip = QLabel("Saccade Acceleration Threshold:")
        self.saccade_acceleration_threshold = QSpinBox()
        self.force_drift_correction = QCheckBox("Force Drift Correction (For EyeLink 1000)")
        self.pupil_size_mode_tip = QLabel("Pupil Size Mode:")
        self.pupil_size_mode = PigComboBox()
        self.SMI_IP_address_tip = QLabel("IP Address:")
        self.SMI_IP_address = PigLineEdit()
        self.SMI_send_port_number_tip = QLabel("Send Port Number:")
        self.SMI_send_port_number = QSpinBox()
        self.SMI_receive_port_number_tip = QLabel("Receive Port Number:")
        self.SMI_receive_port_number = QSpinBox()
        self.tobii_glasses_ipv46_address_tip = QLabel("Tobii Glasses Ipv4/Ipv6_Address:")
        self.tobii_glasses_ipv46_address = PigLineEdit()
        self.tobii_glasses_UDP_port_number_tip = QLabel("Tobii Glasses UDP Port Number:")
        self.tobii_glasses_UDP_port_number = QSpinBox()

        self.setUI()
        self.isFirst = True

    def setUI(self):
        self.select_tracker_type_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.eye_tracker_datafile_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.saccade_velocity_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.saccade_acceleration_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pupil_size_mode_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_IP_address_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_send_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_receive_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tobii_glasses_ipv46_address_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tobii_glasses_UDP_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.select_tracker_type.addItems(["Simple dummy", "Advanced dummy(mouse simulation)", "EyeLink", "SMI",
                                           "EyeTribe", "OpenGaze", "Tobii", "Tobii-legacy", "Tobii Pro Glasses 2"])
        self.select_tracker_type.currentIndexChanged.connect(self.typeChanged)
        self.eye_tracker_datafile.setText("automatic")
        self.saccade_velocity_threshold.setSuffix("°/s")
        self.saccade_acceleration_threshold.setSuffix("°/s/s")
        self.pupil_size_mode.addItems(("area", "diameter"))
        self.SMI_IP_address.setText("127.0.0.1")
        self.SMI_send_port_number.setMaximum(99999)
        self.SMI_receive_port_number.setMaximum(99999)
        self.tobii_glasses_ipv46_address.setText("192.168.71.50")
        self.tobii_glasses_UDP_port_number.setMaximum(99999)

        self.select_tracker_type.setMaximumWidth(300)
        self.eye_tracker_datafile.setMaximumWidth(300)
        self.saccade_velocity_threshold.setMaximumWidth(300)
        self.saccade_acceleration_threshold.setMaximumWidth(300)
        self.pupil_size_mode.setMaximumWidth(300)
        self.SMI_IP_address.setMaximumWidth(300)
        self.SMI_send_port_number.setMaximumWidth(300)
        self.SMI_receive_port_number.setMaximumWidth(300)
        self.tobii_glasses_ipv46_address.setMaximumWidth(300)
        self.tobii_glasses_UDP_port_number.setMaximumWidth(300)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(self.select_tracker_type_tip, 2, 0, 1, 1)
        layout1.addWidget(self.select_tracker_type, 2, 1, 1, 1)
        layout1.addWidget(self.calibrate_tracker, 3, 1, 1, 1)
        layout1.addWidget(self.calibration_beep, 4, 1, 1, 1)
        layout1.addWidget(self.eye_tracker_datafile_tip, 5, 0, 1, 1)
        layout1.addWidget(self.eye_tracker_datafile, 5, 1, 1, 1)
        layout1.addWidget(self.saccade_velocity_threshold_tip, 6, 0, 1, 1)
        layout1.addWidget(self.saccade_velocity_threshold, 6, 1, 1, 1)
        layout1.addWidget(self.saccade_acceleration_threshold_tip, 7, 0, 1, 1)
        layout1.addWidget(self.saccade_acceleration_threshold, 7, 1, 1, 1)
        layout1.addWidget(self.force_drift_correction, 8, 1, 1, 1)
        layout1.addWidget(self.pupil_size_mode_tip, 9, 0, 1, 1)
        layout1.addWidget(self.pupil_size_mode, 9, 1, 1, 1)
        layout1.addWidget(self.SMI_IP_address_tip, 10, 0, 1, 1)
        layout1.addWidget(self.SMI_IP_address, 10, 1, 1, 1)
        layout1.addWidget(self.SMI_send_port_number_tip, 11, 0, 1, 1)
        layout1.addWidget(self.SMI_send_port_number, 11, 1, 1, 1)
        layout1.addWidget(self.SMI_receive_port_number_tip, 12, 0, 1, 1)
        layout1.addWidget(self.SMI_receive_port_number, 12, 1, 1, 1)
        layout1.addWidget(self.tobii_glasses_ipv46_address_tip, 13, 0, 1, 1)
        layout1.addWidget(self.tobii_glasses_ipv46_address, 13, 1, 1, 1)
        layout1.addWidget(self.tobii_glasses_UDP_port_number_tip, 14, 0, 1, 1)
        layout1.addWidget(self.tobii_glasses_UDP_port_number, 14, 1, 1, 1)
        layout1.setSpacing(20)

        layout2 = QHBoxLayout()
        layout2.addStretch(10)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)
        self.setLayout(layout)
        self.select_tracker_type.setCurrentIndex(1)

    def typeChanged(self, index):
        self.hideAll()
        if index == 2:
            self.force_drift_correction.show()
            self.pupil_size_mode_tip.show()
            self.pupil_size_mode.show()
            self.saccade_velocity_threshold_tip.show()
            self.saccade_velocity_threshold.show()
            self.saccade_acceleration_threshold_tip.show()
            self.saccade_acceleration_threshold.show()
            self.SMI_IP_address_tip.show()
            self.SMI_IP_address.show()
            self.SMI_send_port_number_tip.show()
            self.SMI_send_port_number.show()
            self.SMI_receive_port_number_tip.show()
            self.SMI_receive_port_number.show()
        elif index == 3:
            self.saccade_velocity_threshold_tip.show()
            self.saccade_velocity_threshold.show()
            self.saccade_acceleration_threshold_tip.show()
            self.saccade_acceleration_threshold.show()
            self.SMI_IP_address_tip.show()
            self.SMI_IP_address.show()
            self.SMI_send_port_number_tip.show()
            self.SMI_send_port_number.show()
            self.SMI_receive_port_number_tip.show()
            self.SMI_receive_port_number.show()
        elif index == 8:
            self.saccade_velocity_threshold_tip.show()
            self.saccade_velocity_threshold.show()
            self.saccade_acceleration_threshold_tip.show()
            self.saccade_acceleration_threshold.show()
            self.tobii_glasses_ipv46_address_tip.show()
            self.tobii_glasses_ipv46_address.show()
            self.tobii_glasses_UDP_port_number_tip.show()
            self.tobii_glasses_UDP_port_number.show()
        else:
            self.saccade_velocity_threshold_tip.show()
            self.saccade_velocity_threshold.show()
            self.saccade_acceleration_threshold_tip.show()
            self.saccade_acceleration_threshold.show()

    def hideAll(self):
        self.saccade_velocity_threshold_tip.hide()
        self.saccade_velocity_threshold.hide()
        self.saccade_acceleration_threshold_tip.hide()
        self.saccade_acceleration_threshold.hide()
        self.force_drift_correction.hide()
        self.pupil_size_mode_tip.hide()
        self.pupil_size_mode.hide()
        self.SMI_IP_address_tip.hide()
        self.SMI_IP_address.hide()
        self.SMI_send_port_number_tip.hide()
        self.SMI_send_port_number.hide()
        self.SMI_receive_port_number_tip.hide()
        self.SMI_receive_port_number.hide()
        self.tobii_glasses_ipv46_address_tip.hide()
        self.tobii_glasses_ipv46_address.hide()
        self.tobii_glasses_UDP_port_number_tip.hide()
        self.tobii_glasses_UDP_port_number.hide()

    def getSelectTrackerType(self) -> str:
        return self.select_tracker_type.currentText()

    def getEyeTrackerDatafile(self) -> str:
        return self.eye_tracker_datafile.text()

    def getIsCalibrateTracker(self) -> bool:
        return bool(self.calibrate_tracker.checkState())

    def getIsCalibrationBeep(self) -> bool:
        return bool(self.calibration_beep.checkState())

    def getSaccadeVelocityThreshold(self) -> str:
        return str(self.saccade_velocity_threshold.value())

    def getSaccadeAccelerationThreshold(self) -> str:
        return str(self.saccade_acceleration_threshold.value())

    def getIsForceDriftCorrection(self) -> bool:
        return bool(self.force_drift_correction.checkState())

    def getPupilSizeMode(self) -> str:
        return self.pupil_size_mode.text()

    def getSMIIPAddress(self) -> str:
        return self.SMI_IP_address.text()

    def getSMISendPortNumber(self) -> str:
        return str(self.SMI_send_port_number.value())

    def getSMIReceivePortNumber(self) -> str:
        return str(self.SMI_receive_port_number.value())

    def getTobiiGlassesIpv46Address(self) -> str:
        return self.tobii_glasses_ipv46_address.text()

    def getTobiiGlassesUDPPortNumber(self) -> str:
        return str(self.tobii_glasses_UDP_port_number.value())

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)
