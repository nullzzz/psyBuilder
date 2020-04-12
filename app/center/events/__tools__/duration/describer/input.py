from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QCompleter, QGridLayout, QLabel

from lib import VarLineEdit, VarComboBox


class RespTrigger(QWidget):
    OUTPUT_DEVICE = {}

    def __init__(self, parent=None):
        super(RespTrigger, self).__init__(parent=parent)

        self.using_output_device = {}
        self.current_output_device_id = ""
        self.right = VarLineEdit()
        self.wrong = VarLineEdit()
        self.ignore = VarLineEdit()
        self.resp_trigger_out = QComboBox()
        self.resp_trigger_out.currentTextChanged.connect(self.changeOutput)
        self.resp_trigger_out.addItem("none")
        self.resp_trigger_out.addItems(RespTrigger.OUTPUT_DEVICE.values())

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Resp Trigger"), 0, 0, 1, 2)
        layout.addWidget(QLabel("Right:"), 1, 0)
        layout.addWidget(self.right, 1, 1)
        layout.addWidget(QLabel("Wrong:"), 1, 2)
        layout.addWidget(self.wrong, 1, 3)
        layout.addWidget(QLabel("No resp:"), 1, 4)
        layout.addWidget(self.ignore, 1, 5)
        layout.addWidget(QLabel("Device:"), 1, 6)
        layout.addWidget(self.resp_trigger_out, 1, 7)
        self.setLayout(layout)

    def describe(self, info: dict):
        right = info.get("Right")
        wrong = info.get("Wrong")
        ignore = info.get("Ignore")
        output_device_name = info.get("Output Device")
        self.right.setText(right)
        self.wrong.setText(wrong)
        self.ignore.setText(ignore)
        self.resp_trigger_out.setCurrentText(output_device_name)

    def setAttributes(self, attributes):
        self.right.setCompleter(QCompleter(attributes))
        self.wrong.setCompleter(QCompleter(attributes))
        self.ignore.setCompleter(QCompleter(attributes))

    def updateExternalDeviceInformation(self, simple_info: dict):
        self.using_output_device.clear()
        self.resp_trigger_out.clear()
        self.resp_trigger_out.addItem("none")
        self.resp_trigger_out.addItems(simple_info.values())

        if (output_name := self.using_output_device.get(self.current_output_device_id, "")) != "":
            self.resp_trigger_out.setCurrentText(output_name)
        else:
            self.resp_trigger_out.setCurrentIndex(0)

    def changeOutput(self, current_name: str):
        for k, v in self.using_output_device.items():
            if current_name == v:
                self.current_output_device_id = k
                break
        self.right.setEnabled(current_name != "none")
        self.wrong.setEnabled(current_name != "none")
        self.ignore.setEnabled(current_name != "none")

    def getInfo(self):
        info = {
            "Right": self.right.text(),
            "Wrong": self.wrong.text(),
            "No Resp": self.ignore.text(),
            "Output Device": self.resp_trigger_out.currentText(),
        }
        return info


class EyeAction(QWidget):
    def __init__(self, parent=None):
        super(EyeAction, self).__init__(parent)

        self.start = VarLineEdit()
        self.end = VarLineEdit()
        self.mean = VarLineEdit()
        self.is_oval = QComboBox()
        self.is_oval.addItems(("No", "Yes"))

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Eye action correct(gaze area rect)"), 0, 0, 1, 8)
        layout.addWidget(QLabel("Start:"), 1, 0)
        layout.addWidget(self.start, 1, 1)
        layout.addWidget(QLabel("End:"), 1, 2)
        layout.addWidget(self.end, 1, 3)
        layout.addWidget(QLabel("Mean:"), 1, 4)
        layout.addWidget(self.mean, 1, 5)
        layout.addWidget(QLabel("IsOval:"), 1, 6)
        layout.addWidget(self.is_oval, 1, 7)
        self.setLayout(layout)

    def describe(self, info: dict):
        device_id: str = info.get("Device Id")

        start = info.get("Start")
        end = info.get("End")
        mean = info.get("Mean")
        is_oval = info.get("Is Oval")
        self.start.setText(start)
        self.end.setText(end)
        self.mean.setText(mean)
        self.is_oval.setCurrentText(is_oval)
        self.setEnabled(device_id.startswith("action"))

    def setAttributes(self, attributes):
        self.start.setCompleter(QCompleter(attributes))
        self.end.setCompleter(QCompleter(attributes))
        self.mean.setCompleter(QCompleter(attributes))

    def getInfo(self):
        info = {
            "Start": self.start.text(),
            "End": self.end.text(),
            "Mean": self.mean.text(),
            "Is Oval": self.is_oval.currentText(),
        }
        return info


class RespInfo(QWidget):

    def __init__(self, parent=None):
        super(RespInfo, self).__init__(parent=parent)

        self.device_label = QLabel()

        self.allowable = VarLineEdit()

        self.correct = VarLineEdit()

        self.RT_window = VarComboBox()
        self.RT_window.setEditable(True)
        self.RT_window.addItems(["(Same as duration)", "(End of timeline)", "1000", "2000", "3000", "4000", "5000"])

        self.end_action = VarComboBox()
        self.end_action.addItems(["Terminate", "(None)"])
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Response:", self.device_label)
        layout.addRow("Allowable:", self.allowable)
        layout.addRow("Correct:", self.correct)
        layout.addRow("RT Window:", self.RT_window)
        layout.addRow("End Action:", self.end_action)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(layout)

    def describe(self, info: dict):
        device_name = info.get("Device Name")
        allowable = info.get("Allowable")
        correct = info.get("Correct")
        rt_window = info.get("RT Window")
        end_action = info.get("End Action")

        self.device_label.setText(device_name)
        self.allowable.setText(allowable)
        self.correct.setText(correct)
        self.RT_window.setCurrentText(rt_window)
        self.end_action.setCurrentText(end_action)

    def changeName(self, new_name: str):
        self.device_label.setText(new_name)

    def setAttributes(self, attributes):
        self.allowable.setCompleter(QCompleter(attributes))
        self.correct.setCompleter(QCompleter(attributes))

    def getInfo(self):
        info = {
            "Device Name": self.device_label.text(),
            "Allowable": self.allowable.text(),
            "Correct": self.correct.text(),
            "RT Window": self.RT_window.currentText(),
            "End Action": self.end_action.currentText(),
        }
        return info