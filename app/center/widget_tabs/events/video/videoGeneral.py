from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QSpinBox, QGridLayout, QLabel, QFileDialog, QCompleter, QWidget

from app.func import Func
from app.lib import PigComboBox, PigLineEdit


class VideoTab1(QWidget):
    def __init__(self, parent=None):
        super(VideoTab1, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "File name": "",
            "Start position": "00:00:00.000",
            "End position": "99:99:99.999",
            "Aspect ratio": "Default",
            "Playback rate": "1",
            "Clear after": "clear_0",
            "Screen name": "screen.0"
        }
        # general
        self.file_name = PigLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.start_pos = PigLineEdit()
        self.end_pos = PigLineEdit()

        # 倍速
        self.playback_rate = PigComboBox()
        self.playback_rate_tip = QLabel()
        self.transparent = QSpinBox()
        self.aspect_ratio = PigComboBox()

        self.clear_after = PigComboBox()

        self.using_screen_id: str = "screen.0"
        self.screen = PigComboBox()
        self.screen_info = Func.getScreenInfo()
        self.screen.addItems(self.screen_info.values())
        self.screen.currentTextChanged.connect(self.changeScreen)

        self.setUI()

    def setUI(self):
        valid_pos = QRegExp(r"(\d{1,2}:\d{1,2}:\d{2}\.\d{3})|(\[\w+\])")
        self.start_pos.setText("00:00:00.000")
        self.start_pos.setMinimumWidth(120)
        self.end_pos.setText("99:99:99.999")
        self.start_pos.setValidator(QRegExpValidator(valid_pos, self))
        self.end_pos.setValidator(QRegExpValidator(valid_pos, self))

        self.playback_rate.addItems(["1.0", "1.25", "1.5", "1.75", "2.0", "-1.0"])
        self.playback_rate.currentTextChanged.connect(self.pbTip)
        self.aspect_ratio.addItems(["Default", "Ignore", "Keep", "KeepByExpanding"])

        self.screen.addItems(["screen.0"])
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        l0 = QLabel("File Name:")
        l1 = QLabel("Start Position:")
        l2 = QLabel("End Position:")
        l3 = QLabel("Playback Rate:")
        l4 = QLabel("Aspect Ratio:")
        l5 = QLabel("Screen Name:")
        l6 = QLabel("Dont Clear After:")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(l0, 0, 0, 1, 1)
        layout.addWidget(self.file_name, 0, 1, 1, 2)
        layout.addWidget(self.open_bt, 0, 3, 1, 1)

        layout.addWidget(l1, 1, 0, 1, 1)
        layout.addWidget(self.start_pos, 1, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 1, 2, 1, 1)
        layout.addWidget(l2, 2, 0, 1, 1)
        layout.addWidget(self.end_pos, 2, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 2, 2, 1, 1)

        layout.addWidget(l3, 3, 0, 1, 1)
        layout.addWidget(self.playback_rate, 3, 1, 1, 1)
        layout.addWidget(self.playback_rate_tip, 3, 2, 1, 1)

        layout.addWidget(l4, 4, 0, 1, 1)
        layout.addWidget(self.aspect_ratio, 4, 1, 1, 1)
        layout.addWidget(l5, 5, 0, 1, 1)
        layout.addWidget(self.screen, 5, 1, 1, 1)
        layout.addWidget(l6, 6, 0, 1, 1)
        layout.addWidget(self.clear_after, 6, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getScreenInfo()
        screen_id = self.using_screen_id
        self.screen.clear()
        self.screen.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen.setCurrentText(screen_name)
            self.using_screen_id = screen_id

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def pbTip(self, text):
        if text == "-1.0":
            self.playback_rate_tip.setText("may not support")
        else:
            self.playback_rate_tip.setText("")

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the video file", self.file_name.text(),
                                                   "Video File (*)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def changed1(self, e):
        if e == "Yes":
            self.stop_after_mode.setEnabled(True)
        else:
            self.stop_after_mode.setEnabled(False)

    def stretchChange(self, e):
        if e == "Yes":
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.start_pos.setCompleter(QCompleter(self.attributes))
        self.end_pos.setCompleter(QCompleter(self.attributes))

    def setScreen(self, screen: list):
        selected = self.screen.currentText()
        self.screen.clear()
        self.screen.addItems(screen)
        if selected in screen:
            self.screen.setCurrentText(selected)
        else:
            new_name = Func.getDeviceNameById(self.using_device_id)
            if new_name:
                self.screen.setCurrentText(new_name)

    def getInfo(self):
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Start position"] = self.start_pos.text()
        self.default_properties["End position"] = self.end_pos.text()
        self.default_properties["Aspect ratio"] = self.aspect_ratio.currentText()
        self.default_properties["Playback rate"] = self.playback_rate.currentText()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        self.default_properties["Screen name"] = self.screen.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.start_pos.setText(self.default_properties["Start position"])
        self.end_pos.setText(self.default_properties["End position"])
        self.aspect_ratio.setCurrentText(self.default_properties["Aspect ratio"])
        self.playback_rate.setCurrentText(self.default_properties["Playback rate"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.screen.setCurrentText(self.default_properties["Screen name"])
