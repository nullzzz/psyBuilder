import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QComboBox, QCheckBox, QSpinBox, QMessageBox, QCompleter


class Open(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(Open, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.attributes = []

        self.select_tracker_type_tip = QLabel("Select Tracker Type:")
        self.select_tracker_type = QComboBox()

        self.calibrate_tracker = QCheckBox("Calibrate Tracker")
        self.calibration_beep = QCheckBox("Calibration Beep")
        self.eye_tracker_datafile_tip = QLabel("Eye Tracker Datafile:")
        self.eye_tracker_datafile = QLineEdit()
        self.saccade_velocity_threshold_tip = QLabel("Saccade Velocity Threshold:")
        self.saccade_velocity_threshold = QSpinBox()
        self.saccade_acceleration_threshold_tip = QLabel("Saccade Acceleration Threshold:")
        self.saccade_acceleration_threshold = QSpinBox()
        self.force_drift_correction = QCheckBox("Force Drift Correction (For EyeLink 1000)")
        self.pupil_size_mode_tip = QLabel("Pupil Size Mode:")
        self.pupil_size_mode = QComboBox()
        self.SMI_IP_address_tip = QLabel("SMI IP Address:")
        self.SMI_IP_address = QLineEdit()
        self.SMI_send_port_number_tip = QLabel("SMI Send Port Number:")
        self.SMI_send_port_number = QSpinBox()
        self.SMI_receive_port_number_tip = QLabel("SMI Receive Port Number:")
        self.SMI_receive_port_number = QSpinBox()
        self.tobii_glasses_ipv46_address_tip = QLabel("Tobii Glasses Ipv4/Ipv6_Address:")
        self.tobii_glasses_ipv46_address = QLineEdit()
        self.tobii_glasses_UDP_port_number_tip = QLabel("Tobii Glasses UDP Port Number:")
        self.tobii_glasses_UDP_port_number = QSpinBox()

        self.eye_tracker_datafile.textChanged.connect(self.findVar)
        self.eye_tracker_datafile.returnPressed.connect(self.finalCheck)
        self.SMI_IP_address.textChanged.connect(self.findVar)
        self.SMI_IP_address.returnPressed.connect(self.finalCheck)
        self.tobii_glasses_ipv46_address.textChanged.connect(self.findVar)
        self.tobii_glasses_ipv46_address.returnPressed.connect(self.finalCheck)

        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(["test"])

        self.isFirst = True

    def setUI(self):
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Open")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Init")
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Initialize and calibrate eye tracker")

        self.select_tracker_type_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.eye_tracker_datafile_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.saccade_velocity_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.saccade_acceleration_threshold_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.pupil_size_mode_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_IP_address_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_send_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.SMI_receive_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tobii_glasses_UDP_port_number_tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.select_tracker_type.addItems(["Simple dummy", "Advanced dummy(mouse simulation)", "EyeLink", "SMI",
                                           "EyeTribe", "OpenGaze", "Tobii", "Tobii-legacy", "Tobii Pro Glasses 2"])
        self.select_tracker_type.currentIndexChanged.connect(self.typeChanged)
        self.eye_tracker_datafile.setText("automatic")
        self.saccade_velocity_threshold.setSuffix("°/s")
        self.saccade_acceleration_threshold.setSuffix("°/s/s")
        self.pupil_size_mode.addItems(["area", "diameter"])
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
        # layout.setContentsMargins(30, 50, 30, 0)
        self.setLayout(layout)
        self.select_tracker_type.setCurrentIndex(1)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self)

    def cancel(self):
        self.close()
        self.tabClose.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getProperties())

    def typeChanged(self, index):
        # print(index)
        self.hideAll()
        if index == 2:
            self.force_drift_correction.show()
            self.pupil_size_mode_tip.show()
            self.pupil_size_mode.show()
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

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        self.eye_tracker_datafile.setCompleter(QCompleter(self.attributes))
        self.SMI_IP_address.setCompleter(QCompleter(self.attributes))
        self.tobii_glasses_ipv46_address.setCompleter(QCompleter(self.attributes))

    def getProperties(self):
        tracker_type = self.select_tracker_type.currentText()
        is_tracker = self.calibrate_tracker.checkState()
        is_beep = self.calibration_beep.checkState()
        datafile = self.eye_tracker_datafile.text()
        velocity = self.saccade_velocity_threshold.value()
        acceleration = self.saccade_acceleration_threshold.value()
        is_force = self.force_drift_correction.checkState()
        pupil = self.pupil_size_mode.currentText()
        ip = self.SMI_IP_address.text()
        send_port = self.SMI_send_port_number.value()
        receive_port = self.SMI_receive_port_number.value()
        tobii_address = self.tobii_glasses_ipv46_address.text()
        tobii_port = self.tobii_glasses_UDP_port_number.value()
        return {
            "Select tracker type": tracker_type,
            "Eye tracker datafile": datafile,
            "Calibrate tracker": bool(is_tracker),
            "Calibrate beep": bool(is_beep),
            "Saccade velocity threshold": "{}°/s".format(velocity),
            "Saccade acceleration threshold": "{}°/s/s".format(acceleration),
            "Force drift correction": bool(is_force),
            "Pupil size mode": pupil,
            "SMI IP address": ip,
            "SMI send port number": send_port,
            "SMI receive port number": receive_port,
            "Tobii glasses Ipv4/Ipv6 address": tobii_address,
            "Tobii glasses UDP port number": tobii_port
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pro = Open()
    pro.show()
    sys.exit(app.exec())


