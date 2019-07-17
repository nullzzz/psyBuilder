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

# class DeviceInItem(QListWidgetItem):
#     varColor = "blue"
#
#     def __init__(self, name: str, device_id: str, parent=None):
#         super(DeviceInItem, self).__init__(name, parent)
#         self.attributes = []
#         self.name = name
#         self.device_id = device_id
#         self.device_type = device_id.split(".")[0]
#         self.setIcon(QIcon(Func.getImage("{}_device.png".format(self.device_type))))
#         """
#         :device_type: 0一般类型，1那个啥eye的类型
#         """
#         if self.device_type != "eye":
#             self.default_properties = {
#                 "Device name": "",
#                 "Device type": self.device_id,
#                 "Allowable": "",
#                 "Correct": "",
#                 "RT window": "",
#                 "End action": "",
#                 "Right": "",
#                 "Wrong": "",
#                 "No resp": "",
#                 "Output device": ""
#             }
#         else:
#             self.default_properties = {
#                 "Device name": "",
#                 "Device type": self.device_id,
#                 "Action": "",
#                 "ROA": "",
#                 "ROA action": "",
#                 "duration": "",
#                 "Right": "",
#                 "Wrong": "",
#                 "No resp": "",
#                 "Output device": ""
#             }
#
#         self.pro1 = QWidget()
#         self.device_label = QLabel(name)
#         self.allowable = PigLineEdit()
#         self.allowable.textChanged.connect(self.findVar)
#         self.allowable.returnPressed.connect(self.finalCheck)
#         self.correct = PigLineEdit()
#         self.correct.textChanged.connect(self.findVar)
#         self.correct.returnPressed.connect(self.finalCheck)
#         self.RT_window = PigComboBox()
#         self.RT_window.addItems(["(Same as duration)", "(End of timeline)", "1000", "2000", "3000", "4000", "5000"])
#         self.RT_window.setEditable(True)
#         self.RT_window.setInsertPolicy(QComboBox.NoInsert)
#         self.RT_window.lineEdit().textChanged.connect(self.findVar)
#         self.RT_window.lineEdit().returnPressed.connect(self.finalCheck)
#         self.end_action = PigComboBox()
#         self.end_action.setInsertPolicy(QComboBox.NoInsert)
#         self.action = PigComboBox()
#         self.action.setInsertPolicy(QComboBox.NoInsert)
#         self.ROA = PigLineEdit()
#         self.ROA.textChanged.connect(self.findVar)
#         self.ROA.returnPressed.connect(self.finalCheck)
#         self.ROA2 = PigComboBox()
#         self.ROA2.addItems(["Outside", "Inside"])
#
#         self.pro2 = QWidget()
#         self.right = PigLineEdit()
#         self.right.textChanged.connect(self.findVar)
#         self.right.returnPressed.connect(self.finalCheck)
#         self.wrong = PigLineEdit()
#         self.wrong.textChanged.connect(self.findVar)
#         self.wrong.returnPressed.connect(self.finalCheck)
#         self.ignore = PigLineEdit()
#         self.ignore.textChanged.connect(self.findVar)
#         self.ignore.returnPressed.connect(self.finalCheck)
#         self.resp_trigger_out = QComboBox()
#         self.setPro()
#
#     def setPro(self):
#         self.end_action.addItems(["Terminate", "(None)"])
#         self.action.addItems(["Fixation", "Saccade"])
#         if self.device_id != "eye":
#             layout1 = QFormLayout()
#             layout1.addRow("Response:", self.device_label)
#             layout1.addRow("Allowable:", self.allowable)
#             layout1.addRow("Correct:", self.correct)
#             layout1.addRow("RT window:", self.RT_window)
#             layout1.addRow("End action:", self.end_action)
#             layout1.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
#         else:
#             layout1 = QGridLayout()
#             l1 = QLabel("Response:")
#             l1.setAlignment(Qt.AlignRight)
#             layout1.addWidget(l1, 0, 0, 1, 1)
#             layout1.addWidget(self.device_label, 0, 1, 1, 2)
#             l2 = QLabel("Action:")
#             l2.setAlignment(Qt.AlignRight)
#             layout1.addWidget(l2, 1, 0, 1, 1)
#             layout1.addWidget(self.action, 1, 1, 1, 2)
#             l3 = QLabel("ROA:")
#             l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             layout1.addWidget(l3, 2, 0, 1, 1)
#             layout1.addWidget(self.ROA, 2, 1, 1, 1)
#             layout1.addWidget(self.ROA2, 2, 2, 1, 1)
#             l4 = QLabel("Duration:")
#             l4.setAlignment(Qt.AlignRight)
#             layout1.addWidget(l4, 3, 0, 1, 1)
#             layout1.addWidget(self.RT_window, 3, 1, 1, 2)
#             l5 = QLabel("End Action:")
#             l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             layout1.addWidget(l5, 4, 0, 1, 1)
#             layout1.addWidget(self.end_action, 4, 1, 1, 2)
#         layout1.setVerticalSpacing(20)
#         layout1.setContentsMargins(10, 0, 0, 0)
#         self.pro1.setLayout(layout1)
#
#         layout2 = QGridLayout()
#         layout2.addWidget(QLabel("Resp Trigger"), 0, 0, 1, 2)
#         layout2.addWidget(QLabel("Right:"), 1, 0)
#         layout2.addWidget(self.right, 1, 1)
#         layout2.addWidget(QLabel("Wrong:"), 1, 2)
#         layout2.addWidget(self.wrong, 1, 3)
#         layout2.addWidget(QLabel("No resp:"), 1, 4)
#         layout2.addWidget(self.ignore, 1, 5)
#         layout2.addWidget(QLabel("Device:"), 1, 6)
#         layout2.addWidget(self.resp_trigger_out, 1, 7)
#         self.pro2.setLayout(layout2)
#
#     # 设置可选变量
#     def setAttributes(self, attributes):
#         self.attributes = attributes
#         self.allowable.setCompleter(QCompleter(self.attributes))
#         self.correct.setCompleter(QCompleter(self.attributes))
#         self.RT_window.setCompleter(QCompleter(self.attributes))
#         self.ROA.setCompleter(QCompleter(self.attributes))
#         self.right.setCompleter(QCompleter(self.attributes))
#         self.wrong.setCompleter(QCompleter(self.attributes))
#         self.ignore.setCompleter(QCompleter(self.attributes))
#
#     def getInfo(self) -> dict:
#         # todo：当初说的啥眼动设备，属性不一样，现在还不知道是啥子
#         if self.device_id != "eye":
#             self.default_properties["Allowable"] = self.allowable.text()
#             self.default_properties["Correct"] = self.correct.text()
#             self.default_properties["RT window"] = self.RT_window.currentText()
#             self.default_properties["End action"] = self.end_action.currentText()
#         else:
#             self.default_properties["Action"] = self.action.currentText()
#             self.default_properties["ROA"] = self.ROA.text()
#             self.default_properties["ROA action"] = self.ROA2.currentText()
#             self.default_properties["duration"] = self.RT_window.currentText()
#         self.default_properties["Device name"] = self.name
#         self.default_properties["Right"] = self.right.text()
#         self.default_properties["Wrong"] = self.wrong.text()
#         self.default_properties["No resp"] = self.ignore.text()
#         self.default_properties["Output device"] = self.resp_trigger_out.currentText()
#         return self.default_properties
#
#     def setProperties(self, device_info: dict):
#         self.default_properties = device_info
#         self.loadSetting()
#
#     def loadSetting(self):
#         if self.device_id != "eye":
#             self.allowable.setText(self.default_properties["Allowable"])
#             self.correct.setText(self.default_properties["Correct"])
#             self.RT_window.setCurrentText(self.default_properties["RT window"])
#             self.end_action.setCurrentText(self.default_properties["End action"])
#         else:
#             self.action.setCurrentText(self.default_properties["Action"])
#             self.ROA.setText(self.default_properties["ROA"])
#             self.ROA2.setCurrentText(self.default_properties["ROA action"])
#             self.RT_window.setCurrentText(self.default_properties["duration"])
#         self.right.setText(self.default_properties["Right"])
#         self.wrong.setText(self.default_properties["Wrong"])
#         self.ignore.setText(self.default_properties["No resp"])
#         self.resp_trigger_out.setCurrentText(self.default_properties["Output device"])
