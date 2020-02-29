from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Tracker(QListWidgetItem):
    def __init__(self, tracker_type, tracker_id: str = "", parent=None):
        super(Tracker, self).__init__(tracker_type, parent)

        self.tracker_type = tracker_type

        self.tracker_id: str = tracker_id

        self.select_tracker_type = "Simple dummy"
        self.eye_tracker_datafile = "automatic"
        self.calibrate_tracker = "No"
        self.calibration_beep = "No"
        self.saccade_velocity_threshold = "30"
        self.saccade_acceleration_threshold = "9500"
        self.force_drift_correction = "Yes"
        self.pupil_size_mode = "area"
        self.IP_address = "127.0.0.1"
        self.send_port_number = "0"
        self.receive_port_number = "0"
        self.tobii_glasses_ipv46_address = "192.168.71.50"
        self.tobii_glasses_UDP_port_number = "0"

        # 设置图标
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.tracker_type))))

        self.default_properties = {
            "Tracker Type": self.tracker_type,
            "Tracker Name": tracker_id,
        }

    def setName(self, name: str):
        self.setText(name)

    def getId(self) -> str:
        return self.tracker_id

    def getName(self) -> str:
        return self.text()

    def getType(self) -> str:
        return self.tracker_type

    def getSelectTrackerType(self) -> str:
        return self.select_tracker_type

    def setSelectTrackerType(self, select_tracker_type):
        self.select_tracker_type = select_tracker_type

    def getEyeTrackerDatafile(self) -> str:
        return self.eye_tracker_datafile

    def setEyeTrackerDatafile(self, tracker_datafile):
        self.eye_tracker_datafile = tracker_datafile

    def getIsCalibrateTracker(self) -> str:
        return self.calibrate_tracker

    def setIsCalibrateTracker(self, calibrate_tracker):
        self.calibrate_tracker = calibrate_tracker

    def getIsCalibrationBeep(self) -> str:
        return self.calibration_beep

    def setIsCalibrationBeep(self, calibration_beep):
        self.calibration_beep = calibration_beep

    def getSaccadeVelocityThreshold(self) -> str:
        return self.saccade_velocity_threshold

    def setSaccadeVelocityThreshold(self, velocity_threshold):
        self.saccade_velocity_threshold = velocity_threshold

    def getSaccadeAccelerationThreshold(self) -> str:
        return self.saccade_acceleration_threshold

    def setSaccadeAccelerationThreshold(self, acceleration_threshold):
        self.saccade_acceleration_threshold = acceleration_threshold

    def getIsForceDriftCorrection(self) -> str:
        return self.force_drift_correction

    def setIsForceDriftCorrection(self, force_drift_correction):
        self.force_drift_correction = force_drift_correction

    def getPupilSizeMode(self) -> str:
        return self.pupil_size_mode

    def setPupilSizeMode(self, pupil_size_mode):
        self.pupil_size_mode = pupil_size_mode

    def getIPAddress(self) -> str:
        return self.IP_address

    def setIPAddress(self, ip_address):
        self.IP_address = ip_address

    def getSendPortNumber(self) -> str:
        return self.send_port_number

    def setSendPortNumber(self, send_port):
        self.send_port_number = send_port

    def getReceivePortNumber(self) -> str:
        return self.receive_port_number

    def setReceivePortNumber(self, receive_port):
        self.receive_port_number = receive_port

    def getTobiiGlassesIpv46Address(self) -> str:
        return self.tobii_glasses_ipv46_address

    def setTobiiGlassesIpv46Address(self, ipv46_address):
        self.tobii_glasses_ipv46_address = ipv46_address

    def getTobiiGlassesUDPPortNumber(self) -> str:
        return self.tobii_glasses_UDP_port_number

    def setTobiiGlassesUDPPortNumber(self, udp_port):
        self.tobii_glasses_UDP_port_number = udp_port

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Tracker Name"])
        self.select_tracker_type = self.default_properties["Select tracker type"]
        self.eye_tracker_datafile = self.default_properties["Eye tracker datafile"]
        self.calibrate_tracker = self.default_properties["Calibrate tracker"]
        self.calibration_beep = self.default_properties["Calibration beep"]
        self.saccade_velocity_threshold = self.default_properties["Saccade velocity threshold"]
        self.saccade_acceleration_threshold = self.default_properties["Saccade acceleration threshold"]
        self.force_drift_correction = self.default_properties["Force drift correction"]
        self.pupil_size_mode = self.default_properties["Pupil size mode"]
        self.IP_address = self.default_properties["IP address"]
        self.send_port_number = self.default_properties["Send port"]
        self.receive_port_number = self.default_properties["Receive port"]
        self.tobii_glasses_ipv46_address = self.default_properties["Ipv4/Ipv6 address"]
        self.tobii_glasses_UDP_port_number = self.default_properties["UDP port"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Tracker Name"] = self.text()
        self.default_properties["Tracker Type"] = self.tracker_type
        self.default_properties["Select tracker type"] = self.select_tracker_type
        self.default_properties["Eye tracker datafile"] = self.eye_tracker_datafile
        self.default_properties["Calibrate tracker"] = self.calibrate_tracker
        self.default_properties["Calibration beep"] = self.calibration_beep
        self.default_properties["Saccade velocity threshold"] = self.saccade_velocity_threshold
        self.default_properties["Saccade acceleration threshold"] = self.saccade_acceleration_threshold
        self.default_properties["Force drift correction"] = self.force_drift_correction
        self.default_properties["Pupil size mode"] = self.pupil_size_mode
        self.default_properties["IP address"] = self.IP_address
        self.default_properties["Send port"] = self.send_port_number
        self.default_properties["Receive port"] = self.receive_port_number
        self.default_properties["Ipv4/Ipv6 address"] = self.tobii_glasses_ipv46_address
        self.default_properties["UDP port"] = self.tobii_glasses_UDP_port_number
        return self.default_properties
