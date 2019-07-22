from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QApplication, QFileDialog, QCompleter, QMessageBox, QFormLayout

from app.func import Func
from app.lib import PigLineEdit, PigComboBox


# soundOut event专属页面
class SoundTab1(QWidget):
    def __init__(self, parent=None):
        super(SoundTab1, self).__init__(parent)
        self.attributes = []

        self.default_properties = {
            "File name": "",
            "Buffer size": "5000",
            "Refill mode": "Buffered",
            "Start offset": "0",
            "Stop offset": "0",
            "Repetitions": "Yes",
            "Volume control": 0,
            "Volume": "100",
            "Latency Bias": 0,
            "Bias time": "0",
            "Sound Device": "",
            "Wait for start": "No"
        }
        self.file_name = PigLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.volume_control = QCheckBox("")#Volume control
        self.volume_control.stateChanged.connect(self.volumeChecked)
        self.volume = PigLineEdit()
        self.volume.setText("0")
        self.volume.textChanged.connect(self.findVar)
        self.volume.returnPressed.connect(self.finalCheck)
        self.latency_bias = QCheckBox("")#Latency Bias
        self.latency_bias.stateChanged.connect(self.latencyBiasChecked)
        self.bias_time = PigLineEdit()
        self.bias_time.setText("0")
        self.bias_time.textChanged.connect(self.findVar)
        self.bias_time.returnPressed.connect(self.finalCheck)

        self.buffer_size = PigLineEdit()
        self.refill_mode = PigComboBox()

        self.start_offset = PigLineEdit()
        self.stop_offset = PigLineEdit()
        self.repetitions = PigComboBox()

        self.sound_device = PigComboBox()
        self.sound_device.currentTextChanged.connect(self.changeDevice)
        self.using_device_id = ""

        self.wait_for_start = PigComboBox()
        self.wait_for_start.addItems(("No", "Yes"))

        self.setGeneral()

    def setGeneral(self):
        valid_input = QRegExp(r"(\d+)|(\[[_\d\w]+\]")
        self.start_offset.setValidator(QRegExpValidator(valid_input, self))
        self.stop_offset.setValidator(QRegExpValidator(valid_input, self))
        self.refill_mode.addItems(["Buffered", "Streaming"])
        self.repetitions.addItems(["Yes", "No"])
        self.buffer_size.setText("5000")
        self.start_offset.setText("0")
        self.stop_offset.setText("0")
        self.volume.setEnabled(False)
        self.bias_time.setEnabled(False)
        self.buffer_size.textChanged.connect(self.findVar)
        self.start_offset.textChanged.connect(self.findVar)
        self.stop_offset.textChanged.connect(self.findVar)
        self.buffer_size.returnPressed.connect(self.finalCheck)
        self.start_offset.returnPressed.connect(self.finalCheck)
        self.stop_offset.returnPressed.connect(self.finalCheck)
        l0 = QLabel("File Name:")
        l1 = QLabel("Buffer Size (ms):")
        l2 = QLabel("Refill Mode:")
        l3 = QLabel("Start Offset (ms):")
        l4 = QLabel("Stop Offset (ms):")
        l5 = QLabel("Repetitions:")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox()
        layout1 = QGridLayout()
        layout1.addWidget(l0, 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 2)
        layout1.addWidget(self.open_bt, 0, 3, 1, 1)

        layout1.addWidget(l1, 1, 0)
        layout1.addWidget(self.buffer_size, 1, 1)

        layout1.addWidget(l2, 2, 0)
        layout1.addWidget(self.refill_mode, 2, 1)

        layout1.addWidget(l3, 3, 0)
        layout1.addWidget(self.start_offset, 3, 1)
        layout1.addWidget(l4, 4, 0)
        layout1.addWidget(self.stop_offset, 4, 1)

        layout1.addWidget(l5, 5, 0)
        layout1.addWidget(self.repetitions, 5, 1)
        group1.setLayout(layout1)

        l6 = QLabel("Volume control (0~1):")
        l7 = QLabel("Latency bias (ms):")

        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group2 = QGroupBox()
        layout2 = QGridLayout()

        layout2.addWidget(l6, 0, 0, 1, 1)
        layout2.addWidget(self.volume_control, 0, 1, 1, 1)
        layout2.addWidget(self.volume, 0, 3, 1, 1)

        layout2.addWidget(l7, 1, 0, 1, 1)
        layout2.addWidget(self.latency_bias, 1, 1, 1, 1)
        layout2.addWidget(self.bias_time, 1, 3, 1, 1)

        group2.setLayout(layout2)


        group3  = QGroupBox()
        layout3 = QFormLayout()

        layout3.addRow("Sound Device:", self.sound_device)
        layout3.addRow("Wait For Start:", self.wait_for_start)
        group3.setLayout(layout3)

        layout = QVBoxLayout()

        layout.addWidget(group1, 4)
        layout.addWidget(group2, 1)
        layout.addWidget(group3, 1)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the sound file", self.file_name.text(),
                                                   "Sound File (*)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def changeDevice(self, device_name):
        self.using_device_id = Func.getDeviceIdByName(device_name)

    def volumeChecked(self, e):
        if e == 2:
            self.volume.setEnabled(True)
        else:
            self.volume.setEnabled(False)

    def latencyBiasChecked(self, e):
        if e == 2:
            self.bias_time.setEnabled(True)
        else:
            self.bias_time.setEnabled(False)

    def setSound(self, sound: list):
        selected = self.sound_device.currentText()
        self.sound_device.clear()
        self.sound_device.addItems(sound)
        if selected in sound:
            self.sound_device.setCurrentText(selected)
        else:
            new_name = Func.getDeviceNameById(self.using_device_id)
            if new_name:
                self.sound_device.setCurrentText(new_name)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color: black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.buffer_size.setCompleter(QCompleter(self.attributes))
        self.start_offset.setCompleter(QCompleter(self.attributes))
        self.stop_offset.setCompleter(QCompleter(self.attributes))
        self.volume.setCompleter(QCompleter(self.attributes))
        self.bias_time.setCompleter(QCompleter(self.attributes))
        self.sound_device.setCompleter(QCompleter(self.attributes))
        self.wait_for_start.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Buffer size"] = self.buffer_size.text()
        self.default_properties["Refill mode"] = self.refill_mode.currentText()
        self.default_properties["Start offset"] = self.start_offset.text()
        self.default_properties["Stop offset"] = self.stop_offset.text()
        self.default_properties["Repetitions"] = self.repetitions.currentText()

        self.default_properties["Volume control"] = self.volume_control.checkState()
        self.default_properties["Volume"] = self.volume.text()
        self.default_properties["Latency bias"] = self.latency_bias.checkState()
        self.default_properties["Bias time"] = self.bias_time.text()
        if Func.getDeviceNameById(self.using_device_id):
            self.default_properties["Sound device"] = Func.getDeviceNameById(self.using_device_id)
        else:
            self.default_properties["Sound device"] = self.sound_device.currentText()
        self.default_properties["Wait for start"] = self.wait_for_start.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.buffer_size.setText(self.default_properties["Buffer size"])
        self.refill_mode.setCurrentText(self.default_properties["Refill mode"])
        self.start_offset.setText(self.default_properties["Start offset"])
        self.stop_offset.setText(self.default_properties["Stop offset"])
        self.repetitions.setCurrentText(self.default_properties["Repetitions"])
        self.volume_control.setCheckState(self.default_properties["Volume control"])
        self.volume.setText(self.default_properties["Volume"])
        self.latency_bias.setCheckState(self.default_properties["Latency bias"])
        self.bias_time.setText(self.default_properties["Bias time"])
        self.sound_device.setCurrentText((self.default_properties["Sound device"]))
        self.wait_for_start.setCurrentText(self.default_properties["Wait for start"])

    def clone(self):
        clone_page = SoundTab1()
        clone_page.setProperties(self.default_properties)
        return clone_page


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = SoundTab1()

    t.show()

    sys.exit(app.exec())
