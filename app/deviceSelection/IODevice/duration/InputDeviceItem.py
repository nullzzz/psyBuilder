from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class DeviceInItem(QListWidgetItem):
    def __init__(self, device_name: str, device_id: str, parent=None):
        super(DeviceInItem, self).__init__(device_name, parent)
        self.attributes = []
        self.device_name = device_name
        self.device_id = device_id
        self.device_type = device_id.split(".")[0]
        self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))

        self.default_properties = {
            "Device Id": self.device_id,
            "Device Name": self.device_name,
            "Device Type": self.device_type,
            "Allowable": "",
            "Correct": "",
            "RT Window": "",
            "End Action": "",
            "Right": "",
            "Wrong": "",
            "No Resp": "",
            "Output Device": ""
        }

        self.allowable = ""
        self.correct = ""
        self.rt_window = "(Same as duration)"
        self.end_action = "Terminate"
        self.right = ""
        self.wrong = ""
        self.no_resp = ""
        self.output_device = ""

    def getInfo(self) -> dict:
        self.default_properties["Allowable"] = self.allowable
        self.default_properties["Correct"] = self.correct
        self.default_properties["RT Window"] = self.rt_window
        self.default_properties["End Action"] = self.end_action

        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Right"] = self.right
        self.default_properties["Wrong"] = self.wrong
        self.default_properties["No Resp"] = self.no_resp
        self.default_properties["Output Device"] = self.output_device
        return self.default_properties

    def getInProperties(self) -> dict:
        self.default_properties["Allowable"] = self.allowable
        self.default_properties["Correct"] = self.correct
        self.default_properties["RT Window"] = self.rt_window
        self.default_properties["End Action"] = self.end_action

        self.default_properties["Device Name"] = self.device_name
        self.default_properties["Right"] = self.right
        self.default_properties["Wrong"] = self.wrong
        self.default_properties["No Resp"] = self.no_resp
        self.default_properties["Output Device"] = self.output_device
        return self.default_properties

    def setProperties(self, device_info: dict):
        self.default_properties = device_info.copy()
        self.loadSetting()

    def loadSetting(self):
        self.allowable = self.default_properties["Allowable"]
        self.correct = self.default_properties["Correct"]

        self.rt_window = self.default_properties["RT Window"]
        self.end_action = self.default_properties["End Action"]

        self.device_name = self.default_properties["Device Name"]
        self.right = self.default_properties["Right"]
        self.wrong = self.default_properties["Wrong"]
        self.no_resp = self.default_properties["No Resp"]
        self.output_device = self.default_properties["Output Device"]

    def changeAllowable(self, allowable: str):
        self.allowable = allowable

    def changeCorrect(self, correct: str):
        self.correct = correct

    def changeRtWindow(self, rt_window: str):
        self.rt_window = rt_window

    def changeEndAction(self, end_action: str):
        self.end_action = end_action

    def changeRight(self, right: str):
        self.right = right

    def changeWrong(self, wrong: str):
        self.wrong = wrong

    def changeIgnore(self, ignore: str):
        self.no_resp = ignore

    def changeOutput(self, output_device_name: str):
        self.output_device = output_device_name

    def getType(self):
        return self.device_type

    def getValue(self):
        return self.device_name, self.allowable, self.correct, self.rt_window, self.end_action

    def getResp(self):
        return self.right, self.wrong, self.no_resp, self.output_device

    def getDeviceId(self) -> str:
        return self.device_id

    def getDeviceName(self) -> str:
        return self.device_name

    def changeDeviceName(self, new_name: str):
        self.device_name = new_name
        self.setText(new_name)
