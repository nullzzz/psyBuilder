from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QComboBox, QSpinBox, QGridLayout, QLabel, QFileDialog, QMessageBox,
                             QCompleter)
from PyQt5.QtWidgets import QWidget

from ...colorBobox import ColorListEditor


class VideoTab1(QWidget):
    def __init__(self, parent=None):
        super(VideoTab1, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "File name": "",
            "Start position": "00:00:00.000",
            "End position": "00:00:00.000",
            "Aspect ratio": "Default",
            "Playback rate": "1",
            # "Back color": "white",
            # "Transparent": 100,
            "Clear after": "Yes",
            "Screen name": "Display"
        }
        # general
        self.file_name = QLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.start_pos = QLineEdit()
        self.end_pos = QLineEdit()

        self.back_color = ColorListEditor()
        # 倍速
        self.playback_rate = QComboBox()
        self.playback_rate_tip = QLabel()
        self.transparent = QSpinBox()

        # self.stop_after = QComboBox()
        # self.stop_after_mode = QComboBox()
        # self.stretch = QComboBox()
        # self.stretch_mode = QComboBox()

        self.aspect_ratio = QComboBox()

        # self.end_video_action = QComboBox()
        self.screen_name = QComboBox()
        self.clear_after = QComboBox()
        self.setUI()

    def setUI(self):
        valid_pos = QRegExp("(\d{1,2}:\d{1,2}:\d{2}\.\d{3})|(\[\w+\])")
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

        # self.stop_after.addItems(["No", "Yes"])
        # self.stop_after.currentTextChanged.connect(self.changed1)
        # self.stop_after_mode.addItems(["NextOnsetTime", "OffsetTime"])
        # self.stop_after_mode.setEnabled(False)

        # self.stretch.addItems(["No", "Yes"])
        # self.stretch.currentTextChanged.connect(self.stretchChange)
        # self.stretch_mode.addItems(["Both", "LeftRight", "UpDown"])
        # self.stretch_mode.setEnabled(False)

        self.aspect_ratio.addItems(["Default", "Ignore", "Keep", "KeepByExpanding"])
        self.transparent.setMaximum(100)
        self.transparent.setSuffix("%")
        self.transparent.setValue(100)
        self.screen_name.addItems(["Display"])
        self.clear_after.addItems(["Yes", "No"])

        l1 = QLabel("Start Position:")
        l2 = QLabel("End Position:")
        l3 = QLabel("Playback Rate:")
        # l4 = QLabel("Transparent:")
        l4 = QLabel("Aspect Ratio:")
        l5 = QLabel("Screen Name:")
        l6 = QLabel("Clear After:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(QLabel("File Name:"), 0, 0, 1, 1)
        layout.addWidget(self.file_name, 0, 1, 1, 2)
        layout.addWidget(self.open_bt, 0, 3, 1, 1)

        layout.addWidget(l1, 1, 0, 1, 1)
        layout.addWidget(self.start_pos, 1, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 1, 2, 1, 1)
        layout.addWidget(l2, 2, 0, 1, 1)
        layout.addWidget(self.end_pos, 2, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 2, 2, 1, 1)

        # layout.addWidget(l3, 3, 0, 1, 1)
        # layout.addWidget(self.back_color, 3, 1, 1, 1)

        layout.addWidget(l3, 3, 0, 1, 1)
        layout.addWidget(self.playback_rate, 3, 1, 1, 1)
        layout.addWidget(self.playback_rate_tip, 3, 2, 1, 1)

        # layout.addWidget(l4, 4, 0, 1, 1)
        # layout.addWidget(self.transparent, 4, 1, 1, 1)
        # layout.addWidget(QLabel("Stop After:"), 5, 0, 1, 1)
        # layout.addWidget(self.stop_after, 5, 1, 1, 1)
        # layout.addWidget(QLabel("Stop After Mode:"), 5, 2, 1, 1)
        # layout.addWidget(self.stop_after_mode, 5, 3, 1, 1)
        # layout.addWidget(QLabel("Stretch:"), 6, 0, 1, 1)
        # layout.addWidget(self.stretch, 6, 1, 1, 1)
        # layout.addWidget(QLabel("Stretch Mode:"), 6, 2, 1, 1)
        # layout.addWidget(self.stretch_mode, 6, 3, 1, 1)
        layout.addWidget(l4, 4, 0, 1, 1)
        layout.addWidget(self.aspect_ratio, 4, 1, 1, 1)
        # layout.addWidget(QLabel("End Video Action:"), 7, 0, 1, 1)
        # layout.addWidget(self.end_video_action, 7, 1, 1, 1)
        layout.addWidget(l5, 5, 0, 1, 1)
        layout.addWidget(self.screen_name, 5, 1, 1, 1)
        layout.addWidget(l6, 6, 0, 1, 1)
        layout.addWidget(self.clear_after, 6, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

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

    def getInfo(self):
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Start position"] = self.start_pos.text()
        self.default_properties["End position"] = self.end_pos.text()
        self.default_properties["Aspect ratio"] = self.aspect_ratio.currentText()
        self.default_properties["Playback rate"] = self.playback_rate.currentText()
        # self.default_properties["Back color"] = self.back_color.currentText()
        # self.default_properties["Transparent"] = self.transparent.value()
        self.default_properties["Clear after"] = self.clear_after.currentText()
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
        # self.back_color.setCurrentText(self.default_properties["Back color"])
        self.playback_rate.setCurrentText(self.default_properties["Playback rate"])
        # self.transparent.setValue(self.default_properties["Transparent"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.screen_name.setCurrentText(self.default_properties["Screen name"])
