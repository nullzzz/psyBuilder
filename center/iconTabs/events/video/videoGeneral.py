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
        # general
        self.file_name = QLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.startPos = QLineEdit()
        self.endPos = QLineEdit()

        self.back_color = ColorListEditor()
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
        self.startPos.setText("00:00:00.000")
        self.startPos.setMinimumWidth(120)
        self.endPos.setText("00:00:00.000")
        self.startPos.setValidator(QRegExpValidator(valid_pos, self))
        self.endPos.setValidator(QRegExpValidator(valid_pos, self))
        self.startPos.textChanged.connect(self.findVar)
        self.startPos.returnPressed.connect(self.finalCheck)
        self.endPos.textChanged.connect(self.findVar)
        self.endPos.returnPressed.connect(self.finalCheck)

        # self.stop_after.addItems(["No", "Yes"])
        # self.stop_after.currentTextChanged.connect(self.changed1)
        # self.stop_after_mode.addItems(["NextOnsetTime", "OffsetTime"])
        # self.stop_after_mode.setEnabled(False)

        # self.stretch.addItems(["No", "Yes"])
        # self.stretch.currentTextChanged.connect(self.stretchChange)
        # self.stretch_mode.addItems(["Both", "LeftRight", "UpDown"])
        # self.stretch_mode.setEnabled(False)

        self.aspect_ratio.addItems(["default", "ignore", "keep", "keepByExpanding"])
        self.transparent.setMaximum(100)
        self.transparent.setSuffix("%")
        self.transparent.setValue(100)
        self.screen_name.addItems(["Display"])
        self.clear_after.addItems(["Yes", "No"])

        l1 = QLabel("Start Position:")
        l2 = QLabel("End Position:")
        l3 = QLabel("Back Color:")
        l4 = QLabel("Transparent:")
        l5 = QLabel("Aspect Ratio:")
        l6 = QLabel("Screen Name:")
        l7 = QLabel("Clear After:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(QLabel("File Name:"), 0, 0, 1, 1)
        layout.addWidget(self.file_name, 0, 1, 1, 2)
        layout.addWidget(self.open_bt, 0, 3, 1, 1)

        layout.addWidget(l1, 1, 0, 1, 1)
        layout.addWidget(self.startPos, 1, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 1, 2, 1, 1)
        layout.addWidget(l2, 2, 0, 1, 1)
        layout.addWidget(self.endPos, 2, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xxx"), 2, 2, 1, 1)
        layout.addWidget(l3, 3, 0, 1, 1)
        layout.addWidget(self.back_color, 3, 1, 1, 1)
        layout.addWidget(l4, 4, 0, 1, 1)
        layout.addWidget(self.transparent, 4, 1, 1, 1)
        # layout.addWidget(QLabel("Stop After:"), 5, 0, 1, 1)
        # layout.addWidget(self.stop_after, 5, 1, 1, 1)
        # layout.addWidget(QLabel("Stop After Mode:"), 5, 2, 1, 1)
        # layout.addWidget(self.stop_after_mode, 5, 3, 1, 1)
        # layout.addWidget(QLabel("Stretch:"), 6, 0, 1, 1)
        # layout.addWidget(self.stretch, 6, 1, 1, 1)
        # layout.addWidget(QLabel("Stretch Mode:"), 6, 2, 1, 1)
        # layout.addWidget(self.stretch_mode, 6, 3, 1, 1)
        layout.addWidget(l5, 6, 0, 1, 1)
        layout.addWidget(self.aspect_ratio, 6, 1, 1, 1)
        # layout.addWidget(QLabel("End Video Action:"), 7, 0, 1, 1)
        # layout.addWidget(self.end_video_action, 7, 1, 1, 1)
        layout.addWidget(l6, 8, 0, 1, 1)
        layout.addWidget(self.screen_name, 8, 1, 1, 1)
        layout.addWidget(l7, 9, 0, 1, 1)
        layout.addWidget(self.clear_after, 9, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

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
        self.startPos.setCompleter(QCompleter(self.attributes))
        self.endPos.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        return {
            "File name": self.file_name.text(),
            "Start position": self.startPos.text(),
            "End position": self.endPos.text(),
            # "Stretch": self.stretch.currentText(),
            # "Stretch mode": self.stretch_mode.currentText(),
            "Aspect ratio": self.aspect_ratio.currentText(),
            "Back color": self.back_color.currentText(),
            "Transparent": "{}%".format(self.transparent.value()),
            "Clear after": self.clear_after.currentText(),
            "Screen name": self.screen_name.currentText()
        }
