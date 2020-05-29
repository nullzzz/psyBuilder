from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QSpinBox, QGridLayout, QLabel, QFileDialog, QCompleter, QWidget, QComboBox

from app.func import Func
from lib import VarComboBox, VarLineEdit


class VideoTab1(QWidget):
    def __init__(self, parent=None):
        super(VideoTab1, self).__init__(parent)

        self.default_properties = {
            "File Name": "",
            "Start Position": "0",
            "End Position": "9999999",
            "Aspect Ratio": "Default",
            "Playback Rate": "1",
            "Clear After": "clear_0",
            "Screen Name": "screen_0"
        }
        # general
        self.file_name = VarLineEdit()
        self.open_bt = QPushButton("Open file")
        self.open_bt.clicked.connect(self.openFile)

        self.start_pos = VarLineEdit()

        self.end_pos = VarLineEdit()

        # 倍速
        self.playback_rate = VarComboBox()
        self.playback_rate_tip = QLabel()
        self.transparent = QSpinBox()
        self.aspect_ratio = VarComboBox()

        self.clear_after = VarComboBox()

        self.using_screen_id: str = "screen.0"
        self.screen_name = QComboBox()
        self.screen_info = Func.getDeviceInfo("screen")
        self.screen_name.addItems(self.screen_info.values())
        self.screen_name.currentTextChanged.connect(self.changeScreen)

        self.setUI()

    def setUI(self):
        self.start_pos.setText("00")
        self.start_pos.setMinimumWidth(120)
        self.start_pos.setToolTip("In milliseconds")
        self.end_pos.setText("9999999")
        self.end_pos.setToolTip("In milliseconds")

        self.playback_rate.addItems(("1.0", "1.25", "1.5", "1.75", "2.0", "-1.0"))
        self.playback_rate.currentTextChanged.connect(self.changeRateTip)
        self.aspect_ratio.addItems(("Default", "Ignore", "Keep", "KeepByExpanding"))

        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        l0 = QLabel("File Name:")
        l1 = QLabel("Start Timepoint:")
        l2 = QLabel("End Timepoint:")
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
        layout.addWidget(QLabel("ms"), 1, 2, 1, 1)
        layout.addWidget(l2, 2, 0, 1, 1)
        layout.addWidget(self.end_pos, 2, 1, 1, 1)
        layout.addWidget(QLabel("ms"), 2, 2, 1, 1)

        layout.addWidget(l3, 3, 0, 1, 1)
        layout.addWidget(self.playback_rate, 3, 1, 1, 1)
        layout.addWidget(self.playback_rate_tip, 3, 2, 1, 1)

        layout.addWidget(l4, 4, 0, 1, 1)
        layout.addWidget(self.aspect_ratio, 4, 1, 1, 1)
        layout.addWidget(l5, 5, 0, 1, 1)
        layout.addWidget(self.screen_name, 5, 1, 1, 1)
        layout.addWidget(l6, 6, 0, 1, 1)
        layout.addWidget(self.clear_after, 6, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getDeviceInfo("screen")
        screen_id = self.using_screen_id
        self.screen_name.clear()
        self.screen_name.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen_name.setCurrentText(screen_name)
            self.using_screen_id = screen_id

        self.updateInfo()

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def changeRateTip(self, text):
        if text == "-1.0":
            self.playback_rate_tip.setText("may not support")
        else:
            self.playback_rate_tip.setText("+faster, -slower")

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the video file", self.file_name.text(),
                                                   "Video File (*)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def setAttributes(self, attributes):
        self.file_name.setCompleter(QCompleter(attributes))
        self.start_pos.setCompleter(QCompleter(attributes))
        self.end_pos.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties["File Name"] = self.file_name.text()
        self.default_properties["Start Position"] = self.start_pos.text()
        self.default_properties["End Position"] = self.end_pos.text()
        self.default_properties["Aspect Ratio"] = self.aspect_ratio.currentText()
        self.default_properties["Playback Rate"] = self.playback_rate.currentText()
        self.default_properties["Clear After"] = self.clear_after.currentText()
        self.default_properties["Screen Name"] = self.screen_name.currentText()

    def getProperties(self):
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File Name"])
        self.start_pos.setText(self.default_properties["Start Position"])
        self.end_pos.setText(self.default_properties["End Position"])
        self.aspect_ratio.setCurrentText(self.default_properties["Aspect Ratio"])
        self.playback_rate.setCurrentText(self.default_properties["Playback Rate"])
        self.clear_after.setCurrentText(self.default_properties["Clear After"])
        self.screen_name.setCurrentText(self.default_properties["Screen Name"])
