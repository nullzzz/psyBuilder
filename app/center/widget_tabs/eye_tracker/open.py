import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QCheckBox, QSpinBox, QMessageBox, QCompleter

from app.func import Func
from app.lib import PigComboBox, PigLineEdit


class Open(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(Open, self).__init__(parent)
        self.widget_id = widget_id
        self.current_wid = widget_id

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.attributes = []

        self.default_properties = {
            "Select tracker type": "",
            "Eye tracker datafile": "automatic",
            "Calibrate tracker": 0,
            "Calibrate beep": 0,
            "Saccade velocity threshold": 0,
            "Saccade acceleration threshold": 0,
            "Force drift correction": 0,
            "Pupil size mode": "area",
            "SMI IP address": "127.0.0.1",
            "SMI send port number": 0,
            "SMI receive port number": 0,
            "Tobii glasses Ipv4/Ipv6 address": "",
            "Tobii glasses UDP port number": 0
        }
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
        self.SMI_IP_address_tip = QLabel("SMI IP Address:")
        self.SMI_IP_address = PigLineEdit()
        self.SMI_send_port_number_tip = QLabel("SMI Send Port Number:")
        self.SMI_send_port_number = QSpinBox()
        self.SMI_receive_port_number_tip = QLabel("SMI Receive Port Number:")
        self.SMI_receive_port_number = QSpinBox()
        self.tobii_glasses_ipv46_address_tip = QLabel("Tobii Glasses Ipv4/Ipv6_Address:")
        self.tobii_glasses_ipv46_address = PigLineEdit()
        self.tobii_glasses_UDP_port_number_tip = QLabel("Tobii Glasses UDP Port Number:")
        self.tobii_glasses_UDP_port_number = QSpinBox()

        self.eye_tracker_datafile.textChanged.connect(self.findVar)
        self.eye_tracker_datafile.returnPressed.connect(self.finalCheck)
        self.SMI_IP_address.textChanged.connect(self.findVar)
        self.SMI_IP_address.returnPressed.connect(self.finalCheck)
        self.tobii_glasses_ipv46_address.textChanged.connect(self.findVar)
        self.tobii_glasses_ipv46_address.returnPressed.connect(self.finalCheck)

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(Func.getAttributes(self.widget_id))

        self.isFirst = True

    def setUI(self):
        self.setWindowTitle("Open")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Init")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
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
        # layout.setContentsMargins(30, 50, 30, 0)
        self.setLayout(layout)
        self.select_tracker_type.setCurrentIndex(1)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.propertiesChange.emit(self.getInfo())
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

    def typeChanged(self, index):
        # print(index)
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

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Select tracker type"] = self.select_tracker_type.currentText()
        self.default_properties["Eye tracker datafile"] = self.eye_tracker_datafile.text()
        self.default_properties["Calibrate tracker"] = self.calibrate_tracker.checkState()
        self.default_properties["Calibrate beep"] = self.calibration_beep.checkState()
        self.default_properties["Saccade velocity threshold"] = self.saccade_velocity_threshold.value()
        self.default_properties["Saccade acceleration threshold"] = self.saccade_acceleration_threshold.value()
        self.default_properties["Force drift correction"] = self.force_drift_correction.checkState()
        self.default_properties["Pupil size mode"] = self.pupil_size_mode.currentText()
        self.default_properties["SMI IP address"] = self.SMI_IP_address.text()
        self.default_properties["SMI send port number"] = self.SMI_send_port_number.value()
        self.default_properties["SMI receive port number"] = self.SMI_receive_port_number.value()
        self.default_properties["Tobii glasses Ipv4/Ipv6 address"] = self.tobii_glasses_ipv46_address.text()
        self.default_properties["Tobii glasses UDP port number"] = self.tobii_glasses_UDP_port_number.value()

        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print(f"此乱诏也，{self.__class__}不奉命")

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.select_tracker_type.setCurrentText(self.default_properties["Select tracker type"])
        self.eye_tracker_datafile.setText(self.default_properties["Eye tracker datafile"])
        self.calibrate_tracker.setCheckState(self.default_properties["Calibrate tracker"])
        self.calibration_beep.setCheckState(self.default_properties["Calibrate beep"])
        self.saccade_velocity_threshold.setValue(self.default_properties["Saccade velocity threshold"])
        self.saccade_acceleration_threshold.setValue(self.default_properties["Saccade acceleration threshold"])
        self.force_drift_correction.setCheckState(self.default_properties["Force drift correction"])
        self.pupil_size_mode.setCurrentText(self.default_properties["Pupil size mode"])
        self.SMI_IP_address.setText(self.default_properties["SMI IP address"])
        self.SMI_send_port_number.setValue(self.default_properties["SMI send port number"])
        self.SMI_receive_port_number.setValue(self.default_properties["SMI receive port number"])
        self.tobii_glasses_ipv46_address.setText(self.default_properties["Tobii glasses Ipv4/Ipv6 address"])
        self.tobii_glasses_UDP_port_number.setValue(self.default_properties["Tobii glasses UDP port number"])

    def clone(self, new_id: str):
        clone_widget = Open(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
        }
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pro = Open()
    pro.show()
    sys.exit(app.exec())
