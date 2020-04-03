from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout)

from ...events.Slider.general import SliderGeneral
from ...events.duration import DurationPage
from ...events.framePage import FramePage


class SliderProperty(QWidget):
    def __init__(self, parent=None):
        super(SliderProperty, self).__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.tab = QTabWidget()

        self.general = SliderGeneral()
        self.frame = FramePage()
        self.duration = DurationPage()

        self.tab.addTab(self.general, "general")
        self.tab.addTab(self.frame, "frame")
        self.tab.addTab(self.duration, "duration")

        self.default_properties = {
            "General": self.general.default_properties,
            "Frame": self.frame.default_properties,
            "Duration": self.duration.default_properties
        }
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Slider property")
        self.resize(600, 800)
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        main_layout.addLayout(below_layout, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def refresh(self):
        self.general.refresh()
        self.duration.refresh()

    def getInfo(self):
        self.default_properties = {
            **self.duration.updateInfo(), **self.frame.updateInfo(), **self.general.getInfo()}
        return self.default_properties

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    def loadSetting(self):
        self.general.setProperties(self.default_properties)
        self.frame.setProperties(self.default_properties)
        self.duration.setProperties(self.default_properties)

    def getScreenId(self) -> str:
        return self.general.using_screen_id
