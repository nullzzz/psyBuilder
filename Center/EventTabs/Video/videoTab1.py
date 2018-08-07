from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QComboBox, QSpinBox, QGridLayout, QLabel, QFileDialog)
from PyQt5.QtWidgets import QWidget

from ..ColorBobox import ColorListEditor


class VideoTab1(QWidget):
    def __init__(self, parent=None):
        super(VideoTab1, self).__init__(parent)
        # general
        self.file_name = QLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.setExistingDirectory)

        self.startPos = QLineEdit()
        self.endPos = QLineEdit()

        self.back_color = ColorListEditor()
        self.transparent = QSpinBox()

        self.stop_after = QComboBox()

        self.stop_after_mode = QComboBox()

        self.stretch = QComboBox()
        self.stretch_mode = QComboBox()

        self.end_video_action = QComboBox()
        self.display_name = QComboBox()
        self.clear_after = QComboBox()
        self.setUI()

    def setUI(self):
        valid_pos = QRegExp("\d{1,2}:\d{1,2}:\d{2}\.\d{3}")
        self.startPos.setPlaceholderText("00:00:00.000")
        self.endPos.setPlaceholderText("00:00:00.000")
        self.startPos.setValidator(QRegExpValidator(valid_pos, self))
        self.endPos.setValidator(QRegExpValidator(valid_pos, self))
        self.stop_after.addItems(["No", "Yes"])
        self.stop_after.currentTextChanged.connect(self.changed1)
        self.stop_after_mode.addItems(["NextOnsetTime", "OffsetTime"])
        self.stop_after_mode.setEnabled(False)
        self.stretch.addItems(["No", "Yes"])
        self.stretch.currentTextChanged.connect(self.changed2)
        self.stretch_mode.addItems(["Both", "LeftRight", "UpDown"])
        self.stretch_mode.setEnabled(False)
        self.transparent.setMaximum(100)
        self.transparent.setSuffix("%")
        self.transparent.setValue(100)

        self.end_video_action.addItems(["none", "Terminate"])
        self.display_name.addItems(["Display"])
        self.display_name.setEditable(True)
        self.clear_after.addItems(["No", "Yes"])

        layout = QGridLayout()
        layout.addWidget(QLabel("File Name:"), 0, 0, 1, 1)
        layout.addWidget(self.file_name, 0, 1, 1, 2)
        layout.addWidget(self.open_bt, 0, 3, 1, 1)

        layout.addWidget(QLabel("Start Position:"), 1, 0, 1, 1)
        layout.addWidget(self.startPos, 1, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xx"), 1, 2, 1, 1)
        layout.addWidget(QLabel("End Position:"), 2, 0, 1, 1)
        layout.addWidget(self.endPos, 2, 1, 1, 1)
        layout.addWidget(QLabel("hh:mm:ss.xx"), 2, 2, 1, 1)
        layout.addWidget(QLabel("Back Color:"), 3, 0, 1, 1)
        layout.addWidget(self.back_color, 3, 1, 1, 1)
        layout.addWidget(QLabel("Transparent:"), 4, 0, 1, 1)
        layout.addWidget(self.transparent, 4, 1, 1, 1)
        layout.addWidget(QLabel("Stop After:"), 5, 0, 1, 1)
        layout.addWidget(self.stop_after, 5, 1, 1, 1)
        layout.addWidget(QLabel("Stop After Mode:"), 5, 2, 1, 1)
        layout.addWidget(self.stop_after_mode, 5, 3, 1, 1)
        layout.addWidget(QLabel("Stretch:"), 6, 0, 1, 1)
        layout.addWidget(self.stretch, 6, 1, 1, 1)
        layout.addWidget(QLabel("Stretch mode:"), 6, 2, 1, 1)
        layout.addWidget(self.stretch_mode, 6, 3, 1, 1)
        layout.addWidget(QLabel("End Video Action:"), 7, 0, 1, 1)
        layout.addWidget(self.end_video_action, 7, 1, 1, 1)
        layout.addWidget(QLabel("Display Name:"), 8, 0, 1, 1)
        layout.addWidget(self.display_name, 8, 1, 1, 1)
        layout.addWidget(QLabel("Clear After:"), 9, 0, 1, 1)
        layout.addWidget(self.clear_after, 9, 1, 1, 1)
        layout.setContentsMargins(40, 0, 40, 0)
        self.setLayout(layout)

    # 打开文件夹
    def setExistingDirectory(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Find the video file)", self.file_name.text(
        ), "Video File (*)", options=options)
        if fileName:
            self.file_name.setText(fileName)

    def changed1(self, e):
        if e == "Yes":
            self.stop_after_mode.setEnabled(True)
        else:
            self.stop_after_mode.setEnabled(False)

    def changed2(self, e):
        if e == "Yes":
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)
