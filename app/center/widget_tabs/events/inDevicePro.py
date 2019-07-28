from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QCompleter, QGridLayout, QLabel

from app.lib import PigLineEdit, PigComboBox


class InDeviceRespAtDuration(QWidget):
    rightChanged = pyqtSignal(str)
    wrongChanged = pyqtSignal(str)
    ignoreChanged = pyqtSignal(str)
    outputChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.attributes = []
        self.using_output_device = {}
        self.current_output_device_id = ""
        self.right = PigLineEdit()
        self.right.textChanged.connect(lambda x: self.rightChanged.emit(x))
        self.wrong = PigLineEdit()
        self.wrong.textChanged.connect(lambda x: self.wrongChanged.emit(x))
        self.ignore = PigLineEdit()
        self.ignore.textChanged.connect(lambda x: self.ignoreChanged.emit(x))
        self.resp_trigger_out = QComboBox()
        self.resp_trigger_out.currentTextChanged.connect(self.changeOutput)

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

    def showResp(self, value: tuple):
        r, w, i, d = value
        self.right.setText(r)
        self.wrong.setText(w)
        self.ignore.setText(i)
        self.resp_trigger_out.setCurrentText(d)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.right.setCompleter(QCompleter(self.attributes))
        self.wrong.setCompleter(QCompleter(self.attributes))
        self.ignore.setCompleter(QCompleter(self.attributes))
        # self.resp_trigger_out.setCompleter(QCompleter(self.attributes))

    def changeOutputDevice(self, output: dict):
        self.using_output_device.clear()
        self.using_output_device = output.copy()
        self.resp_trigger_out.clear()
        self.resp_trigger_out.addItems(output.values())

        if self.using_output_device.get(self.current_output_device_id):
            self.resp_trigger_out.setCurrentText(self.using_output_device.get(self.current_output_device_id))
        else:
            self.resp_trigger_out.setCurrentIndex(0)

    def changeOutput(self, current_name: str):
        for k, v in self.using_output_device.items():
            if current_name == v:
                self.current_output_device_id = k
                break
        self.outputChanged.emit(current_name)


class InDeviceInfoAtDuration(QWidget):
    allowableChanged = pyqtSignal(str)
    correctChanged = pyqtSignal(str)
    rtWindowChanged = pyqtSignal(str)
    endActionChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.attributes = []

        self.device_label = QLabel()

        self.allowable = PigLineEdit()
        self.allowable.textChanged.connect(lambda x: self.allowableChanged.emit(x))

        self.correct = PigLineEdit()
        self.correct.textChanged.connect(lambda x: self.correctChanged.emit(x))

        self.RT_window = PigComboBox()
        self.RT_window.addItems(["(Same as duration)", "(End of timeline)", "1000", "2000", "3000", "4000", "5000"])
        self.RT_window.currentTextChanged.connect(lambda x: self.rtWindowChanged.emit(x))

        self.end_action = PigComboBox()
        self.end_action.addItems(["Terminate", "(None)"])
        self.end_action.currentTextChanged.connect(lambda x: self.endActionChanged.emit(x))
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Response:", self.device_label)
        layout.addRow("Allowable:", self.allowable)
        layout.addRow("Correct:", self.correct)
        layout.addRow("RT window:", self.RT_window)
        layout.addRow("End action:", self.end_action)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(layout)

    def showInfo(self, value: tuple):
        n, a, c, r, e = value
        self.device_label.setText(n)
        self.allowable.setText(a)
        self.correct.setText(c)
        self.RT_window.setCurrentText(r)
        self.end_action.setCurrentText(e)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.allowable.setCompleter(QCompleter(self.attributes))
        self.correct.setCompleter(QCompleter(self.attributes))
        # self.RT_window.setCompleter(QCompleter(self.attributes))
        # self.end_action.setCompleter(QCompleter(self.attributes))
