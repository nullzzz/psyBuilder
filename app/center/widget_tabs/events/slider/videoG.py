from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import QPushButton, QSpinBox, QGridLayout, QLabel, QFileDialog, QMessageBox, QCompleter, QWidget

from app.func import Func
from app.lib import PigComboBox, PigLineEdit, ColorListEditor


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
            "Clear after": "Yes",
            "Screen name": "screen.0"
        }
        # general
        self.file_name = PigLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.start_pos = PigLineEdit()
        self.end_pos = PigLineEdit()

        # 倍速
        self.playback_rate = PigComboBox()
        self.playback_rate_tip = QLabel()
        self.transparent = QSpinBox()
        self.aspect_ratio = PigComboBox()

        self.screen_name = PigComboBox()
        self.clear_after = PigComboBox()

        self.screen_name.currentTextChanged.connect(self.changeDevice)
        self.using_device_id = "screen.0"
        self.setUI()

    def setUI(self):
        valid_pos = QRegExp(r"(\d{1,2}:\d{1,2}:\d{2}\.\d{3})|(\[\w+\])")
        self.start_pos.setText("00:00:00.000")
        self.start_pos.setMinimumWidth(120)
        self.end_pos.setText("99:99:99.999")
        self.start_pos.setValidator(QRegExpValidator(valid_pos, self))
        self.end_pos.setValidator(QRegExpValidator(valid_pos, self))
        self.start_pos.textChanged.connect(self.findVar)
        self.start_pos.returnPressed.connect(self.finalCheck)
        self.end_pos.textChanged.connect(self.findVar)
        self.end_pos.returnPressed.connect(self.finalCheck)

        self.playback_rate.addItems(["1.0", "1.25", "1.5", "1.75", "2.0", "-1.0"])
        self.playback_rate.currentTextChanged.connect(self.pbTip)
        self.aspect_ratio.addItems(["Default", "Ignore", "Keep", "KeepByExpanding"])

        self.screen_name.addItems(["screen.0"])
        self.clear_after.addItems(["Yes", "No"])

        l0 = QLabel("File Name:")
        l1 = QLabel("Start Position:")
        l2 = QLabel("End Position:")
        l3 = QLabel("Playback Rate:")
        l4 = QLabel("Aspect Ratio:")
        l5 = QLabel("Screen Name:")
        l6 = QLabel("Clear After:")
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
        # layout.addWidget(l5, 5, 0, 1, 1)
        # layout.addWidget(self.screen_name, 5, 1, 1, 1)
        # layout.addWidget(l6, 6, 0, 1, 1)
        # layout.addWidget(self.clear_after, 6, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

    def pbTip(self, text):
        if text == "-1.0":
            self.playback_rate_tip.setText("may not support")
        else:
            self.playback_rate_tip.setText("")

    def changeDevice(self, device_name):
        self.using_device_id = Func.getDeviceIdByName(device_name)

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
        self.start_pos.setCompleter(QCompleter(self.attributes))
        self.end_pos.setCompleter(QCompleter(self.attributes))

    def setScreen(self, screen: list):
        selected = self.screen_name.currentText()
        self.screen_name.clear()
        self.screen_name.addItems(screen)
        if selected in screen:
            self.screen_name.setCurrentText(selected)
        else:
            new_name = Func.getDeviceNameById(self.using_device_id)
            if new_name:
                self.screen_name.setCurrentText(new_name)

    def getInfo(self):
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Start position"] = self.start_pos.text()
        self.default_properties["End position"] = self.end_pos.text()
        self.default_properties["Aspect ratio"] = self.aspect_ratio.currentText()
        self.default_properties["Playback rate"] = self.playback_rate.currentText()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        if Func.getDeviceNameById(self.using_device_id):
            self.default_properties["Screen name"] = Func.getDeviceNameById(self.using_device_id)
        else:
            self.default_properties["Screen name"] = self.screen_name.currentText()
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
        self.screen_name.setCurrentText(self.default_properties["Screen name"])
