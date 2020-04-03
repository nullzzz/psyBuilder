from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout

from .videoGeneral import VideoTab1
from ..duration import DurationPage
from ..framePage import FramePage


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.tab = QTabWidget()

        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.general = VideoTab1()
        self.frame = FramePage()
        self.duration = DurationPage()

        self.default_properties = {**self.general.default_properties, **self.frame.default_properties,
                                   **self.duration.default_properties}

        self.tab.addTab(self.general, "general")
        self.tab.addTab(self.frame, "frame")
        self.tab.addTab(self.duration, "duration")
        self.setButtons()
        self.setUI()

        # 生成主界面

    def setUI(self):
        self.setWindowTitle("Video property")
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

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties = {**self.general.getInfo(), **self.frame.updateInfo(), **self.duration.updateInfo()}
        return self.default_properties

    def setProperties(self, properties: dict):
        self.general.setProperties(properties.get("General"))
        self.frame.setProperties(properties.get("Frame"))
        self.duration.setProperties(properties.get("Duration"))
