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
            "Buffer mode": "Buffered",
            "Start offset": "0",
            "Stop offset": "0",
            "Loop": "Yes",
            "Volume control": 0,
            "Volume": "100",
            "Pan control": 0,
            "Pan": "0"
        }
        self.file_name = PigLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.volume_control = QCheckBox("Volume control")
        self.volume_control.stateChanged.connect(self.volumeChecked)
        self.volume = PigLineEdit()
        self.volume.setText("0")
        self.volume.textChanged.connect(self.findVar)
        self.volume.returnPressed.connect(self.finalCheck)
        # self.volume = QSpinBox()
        self.pan_control = QCheckBox("Pan control")
        self.pan_control.stateChanged.connect(self.panChecked)
        self.pan = PigLineEdit()
        self.pan.setText("0")
        self.pan.textChanged.connect(self.findVar)
        self.pan.returnPressed.connect(self.finalCheck)

        self.buffer_size = PigLineEdit()
        self.buffer_mode = PigComboBox()

        self.start_offset = PigLineEdit()
        self.stop_offset = PigLineEdit()
        self.loop = PigComboBox()

        self.sound_device = PigComboBox()
        self.sound_device.currentTextChanged.connect(self.changeDevice)
        self.using_device_id = ""

        self.setGeneral()

    def setGeneral(self):
        valid_input = QRegExp(r"(\d+)|(\[[_\d\w]+\]")
        self.start_offset.setValidator(QRegExpValidator(valid_input, self))
        self.stop_offset.setValidator(QRegExpValidator(valid_input, self))
        self.buffer_mode.addItems(["Buffered", "Streaming"])
        self.loop.addItems(["Yes", "No"])
        self.buffer_size.setText("5000")
        self.start_offset.setText("0")
        self.stop_offset.setText("0")
        self.volume.setEnabled(False)
        self.pan.setEnabled(False)
        self.buffer_size.textChanged.connect(self.findVar)
        self.start_offset.textChanged.connect(self.findVar)
        self.stop_offset.textChanged.connect(self.findVar)
        self.buffer_size.returnPressed.connect(self.finalCheck)
        self.start_offset.returnPressed.connect(self.finalCheck)
        self.stop_offset.returnPressed.connect(self.finalCheck)
        l0 = QLabel("File Name:")
        l1 = QLabel("Buffer Size (ms):")
        l2 = QLabel("Buffer Mode:")
        l3 = QLabel("Start Offset (ms):")
        l4 = QLabel("Stop Offset (ms):")
        l5 = QLabel("Loop:")
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
        layout1.addWidget(self.buffer_mode, 2, 1)

        layout1.addWidget(l3, 3, 0)
        layout1.addWidget(self.start_offset, 3, 1)
        layout1.addWidget(l4, 4, 0)
        layout1.addWidget(self.stop_offset, 4, 1)

        layout1.addWidget(l5, 5, 0)
        layout1.addWidget(self.loop, 5, 1)
        group1.setLayout(layout1)

        group2 = QGroupBox()
        layout2 = QFormLayout()
        layout2.addRow(self.volume_control)
        layout2.addRow("\tvolume:", self.volume)
        layout2.addRow(self.pan_control)
        layout2.addRow("\tpan:", self.pan)
        layout2.addRow("Sound Device:", self.sound_device)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 2)
        layout.addWidget(group2, 1)
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

    def panChecked(self, e):
        if e == 2:
            self.pan.setEnabled(True)
        else:
            self.pan.setEnabled(False)

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

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.buffer_size.setCompleter(QCompleter(self.attributes))
        self.start_offset.setCompleter(QCompleter(self.attributes))
        self.stop_offset.setCompleter(QCompleter(self.attributes))
        self.volume.setCompleter(QCompleter(self.attributes))
        self.pan.setCompleter(QCompleter(self.attributes))
        self.sound_device.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Buffer size"] = self.buffer_size.text()
        self.default_properties["Buffer mode"] = self.buffer_mode.currentText()
        self.default_properties["Start offset"] = self.start_offset.text()
        self.default_properties["Stop offset"] = self.stop_offset.text()
        self.default_properties["Loop"] = self.loop.currentText()
        self.default_properties["Volume control"] = self.volume_control.checkState()
        # self.default_properties["Volume"] = self.volume.value()
        self.default_properties["Volume"] = self.volume.text()

        self.default_properties["Pan control"] = self.pan_control.checkState()
        # self.default_properties["Pan"] = self.pan.value()
        self.default_properties["Pan"] = self.pan.text()
        if Func.getDeviceNameById(self.using_device_id):
            self.default_properties["Sound device"] = Func.getDeviceNameById(self.using_device_id)
        else:
            self.default_properties["Sound device"] = self.sound_device.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.buffer_size.setText(self.default_properties["Buffer size"])
        self.buffer_mode.setCurrentText(self.default_properties["Buffer mode"])
        self.start_offset.setText(self.default_properties["Start offset"])
        self.stop_offset.setText(self.default_properties["Stop offset"])
        self.loop.setCurrentText(self.default_properties["Loop"])
        self.volume_control.setCheckState(self.default_properties["Volume control"])
        # self.volume.setValue(self.default_properties["Volume"])
        self.volume.setText(self.default_properties["Volume"])

        self.pan_control.setCheckState(self.default_properties["Pan control"])
        # self.pan.setValue(self.default_properties["Pan"])
        self.pan.setText(self.default_properties["Pan"])

        self.sound_device.setCurrentText((self.default_properties["Sound device"]))

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
