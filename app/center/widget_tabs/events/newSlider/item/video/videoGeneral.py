from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QPushButton, QSpinBox, QGridLayout, QLabel, QFileDialog, QCompleter, QWidget, QGroupBox, \
    QVBoxLayout

from app.lib import PigComboBox, PigLineEdit


class VideoGeneral(QWidget):
    def __init__(self, parent=None):
        super(VideoGeneral, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "File name": "",
            "Start position": "00:00:00.000",
            "End position": "99:99:99.999",
            "Aspect ratio": "Default",
            "Playback rate": "1",
            "Transparent": "100",
            "X position": "50%",
            "Y position": "50%",
            "Width": "100%",
            "Height": "100%",
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
        # self.transparent = QSpinBox()
        self.aspect_ratio = PigComboBox()

        # transparent
        self.transparent = PigComboBox()

        # x y and maximum width and height
        self.x_pos = PigComboBox()
        self.y_pos = PigComboBox()
        self._width = PigComboBox()
        self._height = PigComboBox()

        self.setUI()

    def setUI(self):
        valid_pos = QRegExp(r"(\d{1,2}:\d{1,2}:\d{2}\.\d{3})|(\[\w+\])")
        self.start_pos.setText("00:00:00.000")
        self.start_pos.setMinimumWidth(120)
        self.end_pos.setText("99:99:99.999")
        self.start_pos.setValidator(QRegExpValidator(valid_pos, self))
        self.end_pos.setValidator(QRegExpValidator(valid_pos, self))

        self.playback_rate.addItems(["1.0", "2.0", "-1.0", "-2.0"])
        self.playback_rate.currentTextChanged.connect(self.pbTip)
        self.playback_rate_tip.setText("+faster, -slower")

        self.aspect_ratio.addItems(["Default", "Ignore", "Keep", "KeepByExpanding"])

        self.transparent.addItems(("0%","25%", "50%", "75%", "100%"))
        self.transparent.setCurrentText("100%")
        self.transparent.setEditable(True)
        self.transparent.setReg(r"\d+%?|\d+\.\d+%?")

        self.x_pos.addItems(("100", "200", "300", "400"))
        self.x_pos.setCurrentText("50%")
        self.x_pos.setEditable(True)
        self.x_pos.setReg(r"\d+%?")

        self.y_pos.addItems(("100", "200", "300", "400"))
        self.y_pos.setCurrentText("100")
        self.y_pos.setEditable(True)
        self.y_pos.setReg(r"\d+%?")

        self._width.addItems(("25%", "50%", "75%", "100%"))
        self._width.setCurrentText("100%")
        self._width.setEditable(True)
        self._width.setReg(r"\d+%?")

        self._height.addItems(("25%", "50%", "75%", "100%"))
        self._height.setCurrentText("100%")
        self._height.setEditable(True)
        self._height.setReg(r"\d+%?")

        l0 = QLabel("File Name:")
        l1 = QLabel("Start Position:")
        l2 = QLabel("End Position:")
        l3 = QLabel("Playback Rate:")
        l4 = QLabel("Aspect Ratio:")

        l5 = QLabel("Transparent (%):")

        l_x_pos = QLabel("Center X:")
        l_y_pos = QLabel("Center Y:")
        l_width = QLabel("Maximum Width:")
        l_height = QLabel("Maximum Height:")

        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l_x_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_y_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_width.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_height.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Effects")

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

        layout.addWidget(l5, 4, 2, 1, 1)
        layout.addWidget(self.transparent, 4, 3, 1, 1)


        group1.setLayout(layout)

        group2 = QGroupBox("Geometry")

        layout2 = QGridLayout()

        layout2.addWidget(l_x_pos, 0, 0, 1, 1)
        layout2.addWidget(self.x_pos, 0, 1)

        layout2.addWidget(l_width, 0, 2, 1, 2)
        layout2.addWidget(self._width, 0, 4)

        layout2.addWidget(l_y_pos, 1, 0, 1, 1)
        layout2.addWidget(self.y_pos, 1, 1)

        layout2.addWidget(l_height, 1, 2, 1, 2)
        layout2.addWidget(self._height, 1, 4)

        group2.setLayout(layout2)



        layout = QVBoxLayout()

        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    def pbTip(self, text):
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

    # def changed1(self, e):
    #     if e == "Yes":
    #         self.stop_after_mode.setEnabled(True)
    #     else:
    #         self.stop_after_mode.setEnabled(False)

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
        self.transparent.setCompleter(QCompleter(self.attributes))
        self.x_pos.setCompleter(QCompleter(self.attributes))
        self.y_pos.setCompleter(QCompleter(self.attributes))
        self._width.setCompleter(QCompleter(self.attributes))
        self._height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Start position"] = self.start_pos.text()
        self.default_properties["End position"] = self.end_pos.text()
        self.default_properties["Aspect ratio"] = self.aspect_ratio.currentText()
        self.default_properties["Playback rate"] = self.playback_rate.currentText()
        self.default_properties["Transparent"] = self.transparent.currentText()
        self.default_properties["Center X"] = self.x_pos.currentText()
        self.default_properties["Center Y"] = self.y_pos.currentText()
        self.default_properties["Width"] = self._width.currentText()
        self.default_properties["Height"] = self._height.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.x_pos.currentText().startswith("["):
            self.x_pos.setCurrentText(str(int(x)))
        if not self.y_pos.currentText().startswith("["):
            self.y_pos.setCurrentText(str(int(y)))

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.start_pos.setText(self.default_properties["Start position"])
        self.end_pos.setText(self.default_properties["End position"])
        self.aspect_ratio.setCurrentText(self.default_properties["Aspect ratio"])
        self.playback_rate.setCurrentText(self.default_properties["Playback rate"])
        self.transparent.setCurrentText(self.default_properties["Transparent"])
        self.x_pos.setCurrentText(self.default_properties["Center X"])
        self.y_pos.setCurrentText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])
