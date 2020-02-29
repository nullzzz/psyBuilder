from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Device(QListWidgetItem):
    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Device, self).__init__(device_type, parent)
        # 设备类型
        self.device_type = device_type
        self.device_id = device_id
        # 设置图标
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Type": self.device_type,
            "Device Name": self.text(),
        }

    def getType(self) -> str:
        return self.device_type

    def setName(self, name: str):
        self.setText(name)

    def getDeviceId(self) -> str:
        return self.device_id

    def getName(self) -> str:
        return self.text()

    def getInfo(self):
        pass

    def restore(self):
        pass


class Output(Device):
    """
    :param device_type: 串、并、网口、
    :param device_id: 设备标识符
    """

    def __init__(self, device_type: str, device_id: str = None, parent=None):
        super(Output, self).__init__(device_type, device_id, parent)
        # 地址
        if device_type == "network_port":
            self.port = "127.0.0.1"
        elif device_type == "parallel_port":
            self.port = "D010"
        elif device_type == "serial_port":
            self.port = "com1"
        elif device_type == "screen":
            self.port = "0"
        elif device_type == "sound":
            self.port = "1"
        elif device_type in ("keyboard", "mouse", "game pad"):
            self.port = "0"
        else:
            self.port = "null"

        # screen 专属
        self.back_color = "0,0,0"
        self.sample = "0"
        self.resolution = "auto"
        self.refresh_rate = "auto"
        # parallel
        self.is_client: str = "Yes"
        # net
        self.ip_port: str = "25576"
        # serial
        self.baud_rate: str = "9600"
        self.data_bits: str = "8"
        # sound
        self.sampling_rate: str = "auto"
        # 设备标识符
        self.device_id: str = device_id

        # 设置图标
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

    def getPort(self) -> str:
        return self.port

    def getColor(self) -> str:
        if self.device_type == "screen":
            return self.back_color
        return ""

    def getSample(self) -> str:
        if self.device_type == "screen":
            return self.sample
        return ""

    def getSamplingRate(self) -> str:
        if self.device_type == "sound":
            return self.sampling_rate
        return ""

    def getResolution(self) -> str:
        return self.resolution

    def getRefreshRate(self) -> str:
        return self.refresh_rate

    def setPort(self, port: str):
        if port.startswith("screen") or port.startswith("sound"):
            self.port = port.split(".")[-1]
        elif port.startswith("serial_port"):
            self.port = f"com{port.split('.')[-1]}"
        elif port.startswith("keyboard") or port.startswith("mouse") or port.startswith("game pad"):
            self.port = port.split(".")[-1]
        elif port.startswith(self.device_type):
            pass
        else:
            self.port = port

    def setColor(self, color: str):
        self.back_color = color

    def setSample(self, sample: str):
        self.sample = sample

    def setBaud(self, baud: str):
        self.baud_rate = baud

    def setBits(self, bits: str):
        self.data_bits = bits

    def setClient(self, client: str):
        self.is_client = client

    def setIpPort(self, ip_port: str):
        self.ip_port = ip_port

    def setSamplingRate(self, sampling_rate: str):
        self.sampling_rate = sampling_rate

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def setResolution(self, resolution):
        self.resolution = resolution

    def setRefreshRate(self, refresh_rate):
        self.refresh_rate = refresh_rate

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.setPort(self.default_properties["Device Port"])
        self.setColor(self.default_properties.get("Back Color", "0,0,0"))
        self.setPort(self.default_properties.get("Multi Sample", "0"))
        self.setBaud(self.default_properties.get("Baud Rate", "9600"))
        self.setBits(self.default_properties.get("Data Bits", "8"))
        self.setIpPort(self.default_properties.get("IP Port", "25576"))
        self.setClient(self.default_properties.get("Is Client", "1"))
        self.setSamplingRate(self.default_properties.get("Sampling Rate", "auto"))
        self.setResolution(self.default_properties.get("Resolution", "auto"))
        self.setRefreshRate(self.default_properties.get("Refresh Rate", "auto"))

    def getInfo(self) -> dict:
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Port"] = self.port
        self.default_properties["Back Color"] = self.back_color
        self.default_properties["Multi Sample"] = self.sample
        self.default_properties["Baud Rate"] = self.baud_rate
        self.default_properties["Data Bits"] = self.data_bits
        self.default_properties["IP Port"] = self.ip_port
        self.default_properties["Is Client"] = self.is_client
        self.default_properties["Sampling Rate"] = self.sampling_rate
        self.default_properties["Resolution"] = self.resolution
        self.default_properties["Refresh Rate"] = self.refresh_rate

        return self.default_properties


class Quest(Device):
    def __init__(self, device_type: str = "quest", device_id: str = None, parent=None):
        super(Quest, self).__init__(device_type, device_id, parent)
        self.device_type = device_type

        self.quest_id: str = device_id
        self.estimated_threshold = "0.5"
        self.std_dev = "0.25"
        self.desired_proportion = "0.75"
        self.steepness = "3.5"
        self.proportion = "0.01"
        self.chance_level = "0.05"
        self.method = "quantile"
        self.minimum = "0"
        self.maximum = "1"
        self.is_log10_transform = "Yes"
        # 设置图标
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

    def getThreshold(self) -> str:
        return self.estimated_threshold

    def setThreshold(self, threshold: str):
        self.estimated_threshold = threshold

    def setSD(self, sd: str):
        self.std_dev = sd

    def setDesired(self, desired: str):
        self.desired_proportion = desired

    def setSteep(self, steepness: str):
        self.steepness = steepness

    def setProportion(self, proportion: str):
        self.proportion = proportion

    def setChanceLevel(self, chance_level: str):
        self.chance_level = chance_level

    def setMethod(self, method: str):
        self.method = method

    def setMaximum(self, maximum: str):
        self.maximum = maximum

    def setMinimum(self, minimum: str):
        self.minimum = minimum

    def setIsTransform(self, is_transform: str):
        self.is_log10_transform = is_transform

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Device Name"])
        self.estimated_threshold = self.default_properties["Estimated threshold"]
        self.std_dev = self.default_properties["Std dev"]
        self.desired_proportion = self.default_properties["Desired proportion"]
        self.steepness = self.default_properties["Steepness"]
        self.proportion = self.default_properties["Proportion"]
        self.chance_level = self.default_properties["Chance level"]
        self.method = self.default_properties["Method"]
        self.minimum = self.default_properties["Minimum"]
        self.maximum = self.default_properties["Maximum"]
        self.is_log10_transform = self.default_properties["Is log10 transform"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Estimated threshold"] = self.estimated_threshold
        self.default_properties["Std dev"] = self.std_dev
        self.default_properties["Desired proportion"] = self.desired_proportion
        self.default_properties["Steepness"] = self.steepness
        self.default_properties["Proportion"] = self.proportion
        self.default_properties["Chance level"] = self.chance_level
        self.default_properties["Method"] = self.method
        self.default_properties["Minimum"] = self.minimum
        self.default_properties["Maximum"] = self.maximum
        self.default_properties["Is log10 transform"] = self.is_log10_transform
        return self.default_properties


class Tracker(Device):
    def __init__(self, device_type: str = "tracker", device_id: str = "", parent=None):
        super(Tracker, self).__init__(device_type, device_id, parent)

        self.device_type = device_type

        self.device_id: str = device_id

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
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

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
        self.setName(self.default_properties["Device Name"])
        self.select_tracker_type = self.default_properties["Select Tracker Type"]
        self.eye_tracker_datafile = self.default_properties["Eye Tracker Datafile"]
        self.calibrate_tracker = self.default_properties["Calibrate Tracker"]
        self.calibration_beep = self.default_properties["Calibration Beep"]
        self.saccade_velocity_threshold = self.default_properties["Saccade Velocity Threshold"]
        self.saccade_acceleration_threshold = self.default_properties["Saccade Acceleration Threshold"]
        self.force_drift_correction = self.default_properties["Force Drift Correction"]
        self.pupil_size_mode = self.default_properties["Pupil Size Mode"]
        self.IP_address = self.default_properties["IP Address"]
        self.send_port_number = self.default_properties["Send Port"]
        self.receive_port_number = self.default_properties["Receive Port"]
        self.tobii_glasses_ipv46_address = self.default_properties["Ipv4/Ipv6 Address"]
        self.tobii_glasses_UDP_port_number = self.default_properties["UDP Port"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Select Tracker Type"] = self.select_tracker_type
        self.default_properties["Eye Tracker Datafile"] = self.eye_tracker_datafile
        self.default_properties["Calibrate Tracker"] = self.calibrate_tracker
        self.default_properties["Calibration Beep"] = self.calibration_beep
        self.default_properties["Saccade Velocity Threshold"] = self.saccade_velocity_threshold
        self.default_properties["Saccade Acceleration Threshold"] = self.saccade_acceleration_threshold
        self.default_properties["Force Drift Correction"] = self.force_drift_correction
        self.default_properties["Pupil Size Mode"] = self.pupil_size_mode
        self.default_properties["IP Address"] = self.IP_address
        self.default_properties["Send Port"] = self.send_port_number
        self.default_properties["Receive Port"] = self.receive_port_number
        self.default_properties["Ipv4/Ipv6 Address"] = self.tobii_glasses_ipv46_address
        self.default_properties["UDP Port"] = self.tobii_glasses_UDP_port_number
        return self.default_properties


class Action(Device):
    def __init__(self, device_type: str = "action", device_id: str = "", parent=None):
        super(Action, self).__init__(device_type, device_id, parent)

        self.device_type = device_type
        self.device_id = device_id

        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.device_type))))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Device Type"] = self.device_type

        return self.default_properties