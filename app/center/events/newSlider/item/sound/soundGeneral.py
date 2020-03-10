from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QFileDialog, QCompleter, QSpacerItem, QSizePolicy

from app.func import Func
from lib import VarLineEdit, VarComboBox


# sound event专属页面
class SoundGeneral(QWidget):
    def __init__(self, parent=None):
        super(SoundGeneral, self).__init__(parent)
        self.attributes = []

        self.default_properties = {
            "File name": "",
            "Buffer size": "5000",
            "Stream refill": "0",
            "Start offset": "0",
            "Stop offset": "0",
            "Repetitions": "1",
            "Volume control": 0,
            "Volume": "1",
            "Latency Bias": 0,
            "Bias time": "0",
            "Sound Device": "",
            "Wait for start": "No"
        }
        self.file_name = VarLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.volume_control = QCheckBox("Volume Control (0~1):")  # Volume control
        self.volume_control.setLayoutDirection(Qt.RightToLeft)

        self.volume_control.stateChanged.connect(self.volumeChecked)
        self.volume = VarLineEdit()
        self.volume.setText("1")

        self.latency_bias = QCheckBox("Latency Bias (ms):")  # Latency Bias
        self.latency_bias.setLayoutDirection(Qt.RightToLeft)

        self.latency_bias.stateChanged.connect(self.latencyBiasChecked)
        self.bias_time = VarLineEdit()
        self.bias_time.setText("0")

        self.buffer_size = VarLineEdit()
        self.stream_refill = VarComboBox()

        self.start_offset = VarLineEdit("0")
        self.stop_offset = VarLineEdit("0")
        self.repetitions = VarLineEdit("1")

        self.sound = VarComboBox()

        self.using_sound_id: str = ""
        self.sound = VarComboBox()
        self.sound_info = Func.getSoundInfo()
        self.sound.addItems(self.sound_info.values())
        self.sound.currentTextChanged.connect(self.changeSound)

        self.wait_for_start = VarComboBox()
        self.wait_for_start.addItems(("No", "Yes"))

        self.setUI()

    def setUI(self):
        self.stream_refill.addItems(("0", "1", "2"))
        self.repetitions.setText("1")
        self.buffer_size.setText("5000")
        self.volume.setEnabled(False)
        self.bias_time.setEnabled(False)

        l0 = QLabel("File Name:")
        l1 = QLabel("Buffer Size (ms):")
        l2 = QLabel("Stream Refill:")
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
        layout1.addWidget(self.stream_refill, 2, 1)

        layout1.addWidget(l3, 3, 0)
        layout1.addWidget(self.start_offset, 3, 1)
        layout1.addWidget(l4, 4, 0)
        layout1.addWidget(self.stop_offset, 4, 1)

        layout1.addWidget(l5, 5, 0)
        layout1.addWidget(self.repetitions, 5, 1)
        group1.setLayout(layout1)

        l6 = QLabel("Sound Device:")
        l7 = QLabel("Wait For Start:")

        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group2 = QGroupBox()
        layout2 = QGridLayout()

        layout2.addWidget(self.volume_control, 0, 0, )
        layout2.addWidget(self.volume, 0, 1, )
        layout2.addWidget(l6, 0, 2)
        layout2.addWidget(self.sound, 0, 3)

        layout2.addWidget(self.latency_bias, 1, 0)
        layout2.addWidget(self.bias_time, 1, 1)
        self.bias_time.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        self.volume.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        layout2.addWidget(l7, 1, 2)
        layout2.addWidget(self.wait_for_start, 1, 3)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 2)
        layout.addWidget(group2, 1)

        self.setLayout(layout)

    def refresh(self):
        self.sound_info = Func.getSoundInfo()
        sound_id = self.using_sound_id
        self.sound.clear()
        self.sound.addItems(self.sound_info.values())
        sound_name = self.sound_info.get(sound_id)
        if sound_name:
            self.sound.setCurrentText(sound_name)
            self.using_sound_id = sound_id

    def changeSound(self, sound):
        for k, v in self.sound_info.items():
            if v == sound:
                self.using_sound_id = k
                break

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the sound file", self.file_name.text(),
                                                   "Sound File (*)", options=options)
        if file_name:
            self.file_name.setText(file_name)

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

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.buffer_size.setCompleter(QCompleter(self.attributes))
        self.start_offset.setCompleter(QCompleter(self.attributes))
        self.stop_offset.setCompleter(QCompleter(self.attributes))
        self.volume.setCompleter(QCompleter(self.attributes))
        self.bias_time.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Buffer size"] = self.buffer_size.text()
        self.default_properties["Stream refill"] = self.stream_refill.currentText()
        self.default_properties["Start offset"] = self.start_offset.text()
        self.default_properties["Stop offset"] = self.stop_offset.text()
        self.default_properties["Repetitions"] = self.repetitions.text()
        self.default_properties["Volume control"] = self.volume_control.checkState()
        self.default_properties["Volume"] = self.volume.text()
        self.default_properties["Latency bias"] = self.latency_bias.checkState()
        self.default_properties["Bias time"] = self.bias_time.text()
        self.default_properties["Sound device"] = self.sound.currentText()
        self.default_properties["Wait for start"] = self.wait_for_start.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def setPosition(self, x, y):
        pass # do nothing here

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.buffer_size.setText(self.default_properties["Buffer size"])
        self.stream_refill.setCurrentText(self.default_properties["Stream refill"])
        self.start_offset.setText(self.default_properties["Start offset"])
        self.stop_offset.setText(self.default_properties["Stop offset"])
        self.repetitions.setText(self.default_properties["Repetitions"])
        self.volume_control.setCheckState(self.default_properties["Volume control"])
        self.volume.setText(self.default_properties["Volume"])
        self.latency_bias.setCheckState(self.default_properties["Latency bias"])
        self.bias_time.setText(self.default_properties["Bias time"])
        self.sound.setCurrentText((self.default_properties["Sound device"]))
        self.wait_for_start.setCurrentText(self.default_properties["Wait for start"])

    def clone(self):
        clone_page = SoundGeneral()
        clone_page.setProperties(self.default_properties)
        return clone_page
