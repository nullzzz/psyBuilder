from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QSpinBox, QGridLayout, QFormLayout, QLineEdit, QComboBox

from lib import VarComboBox


class Tracker(QWidget):
    def __init__(self, parent=None):
        super(Tracker, self).__init__(parent)

        self.device_name_tip = QLabel("Tracker Name:")
        self.device_name = QLabel("Unselected")

        self.device_type_tip = QLabel("Tracker Type:")
        self.device_type = QComboBox()
        self.device_type.addItems(("Simple dummy", "Advanced dummy(mouse simulation)", "EyeLink", "SMI",
                                   "EyeTribe", "OpenGaze", "Tobii", "Tobii-legacy", "Tobii Pro Glasses 2"))
        self.device_type.currentIndexChanged.connect(self.typeChanged)

        self.calibrate_tracker = QCheckBox("Calibrate Tracker")
        self.calibration_beep = QCheckBox("Calibration Beep")

        # self.tracker_datafile_tip = QLabel("Eye Tracker Datafile:")
        self.tracker_datafile_tip = QLabel("Datafile:")
        self.tracker_datafile = QLineEdit("automatic")

        # self.velocity_threshold_tip = QLabel("Saccade Velocity Threshold:")
        self.velocity_threshold_tip = QLabel("Velocity:")
        self.velocity_threshold = QSpinBox()
        self.velocity_threshold.setSuffix("°/s")

        # self.acceleration_threshold_tip = QLabel("Saccade Acceleration Threshold:")
        self.acceleration_threshold_tip = QLabel("Acceleration:")
        self.acceleration_threshold = QSpinBox()
        self.acceleration_threshold.setSuffix("°/s/s")
        self.acceleration_threshold.setMaximum(99999)

        self.force_drift_correction = QCheckBox("Force Drift Correction")
        # self.force_drift_correction = QCheckBox("Force Drift Correction (For EyeLink 1000)")

        self.pupil_size_mode_tip = QLabel("Pupil Size Mode:")
        self.pupil_size_mode = QComboBox()
        self.pupil_size_mode.addItems(("area", "diameter"))

        self.IP_address_tip = QLabel("IP Address:")
        self.IP_address = QLineEdit("127.0.0.1")

        self.send_port_tip = QLabel("Send Port:")
        self.send_port = QSpinBox()

        self.receive_port_tip = QLabel("Receive Port:")
        self.receive_port = QSpinBox()

        # self.ipv46_address_tip = QLabel("Tobii Glasses IPv4/6 Address:")
        self.ipv46_address_tip = QLabel("IPv4/6 Address:")
        self.ipv46_address = QLineEdit("192.168.71.50")

        # self.UDP_port_tip = QLabel("Tobii Glasses UDP Port:")
        self.UDP_port_tip = QLabel("UDP Port:")
        self.UDP_port = QSpinBox()
        self.setUI()

    def setUI(self):
        self.device_name_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.device_type_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
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
        layout.addWidget(self.device_name_tip, 0, 0, 1, 1)
        layout.addWidget(self.device_name, 0, 1, 1, 1)
        layout.addWidget(self.device_type_tip, 1, 0, 1, 1)
        layout.addWidget(self.device_type, 1, 1, 1, 1)
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

    def describe(self, info: dict):
        device_name = info.get("Device Name")
        self.device_name.setText(device_name)
        self.device_type.setCurrentText(info.get("Select Tracker Type", "Simple dummy"))
        self.tracker_datafile.setText(info.get("Eye Tracker Datafile", "automatic"))
        self.calibrate_tracker.setCheckState(info.get("Calibrate Tracker", "") == "Yes")
        self.calibration_beep.setCheckState(info.get("Calibration Beep", "") == "Yes")
        self.velocity_threshold.setValue(int(info.get("Saccade Belocity Threshold", "0")))
        self.acceleration_threshold.setValue(int(info.get("Saccade Acceleration Threshold", "0")))
        self.force_drift_correction.setCheckState((info.get("Force Drift Correction", "") == "Yes") * 2)
        self.pupil_size_mode.setCurrentText(info.get("Pupil Size Mode", "area"))
        self.IP_address.setText(info.get("IP Address", "127.0.0.0"))
        self.send_port.setValue(int(info.get("Send Port", "0")))
        self.receive_port.setValue(int(info.get("Receive Port", "0")))
        self.ipv46_address.setText(info.get("Ipv4/Ipv6 Address", "192.168.71.50"))
        self.UDP_port.setValue(int(info.get("UDP Port", "0")))

    def changeName(self, name: str):
        self.device_name.setText(name)


class Action(QWidget):
    def __init__(self, parent=None):
        super(Action, self).__init__(parent)

        self.device_type = QLabel("Action")
        self.device_name = QLabel()
        self.status_message = VarComboBox()
        self.tracker_name = VarComboBox()

        self.default_properties = {
            "Status Message": "Saccade start",
            "EyeTracker Name": "",
        }
        self.msg = ""
        self.setUI()
        self.status_message.setFocus()

    def setUI(self):
        self.status_message.addItems(
            ("Saccade start", "Saccade end", "Fixation start", "Fixation end", "Blink start", "Blink end"))

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Status Message:", self.status_message)
        layout.addRow("EyeTracker Name:", self.tracker_name)

        self.setLayout(layout)

    def describe(self, info: dict):
        device_name = info.get("Device Name", "")
        self.device_name.setText(device_name)

        status_message = info.get("Status Message", "Saccade start")
        self.status_message.setCurrentText(status_message)

        tracker_name = info.get("Tracker Name", "")
        self.tracker_name.setCurrentText(tracker_name)

    def changeName(self, name: str):
        self.device_name.setText(name)
