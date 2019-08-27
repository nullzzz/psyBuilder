from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout

from .videoGeneral import VideoGeneral


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.general = VideoGeneral()

        self.default_properties = self.general.default_properties

        self.tab.addTab(self.general, "general")
        self.setButtons()
        self.setUI()

        # 生成主界面

    def setUI(self):
        self.setWindowTitle("Video property")
        self.resize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties = self.general.getInfo()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def setPosition(self, x, y):
        self.general.setPosition(x, y)

    def loadSetting(self):
        self.general.setProperties(self.default_properties)

    def clone(self):
        properties = self.getInfo()
        clone_page = VideoProperty()
        clone_page.setProperties(properties)
        return clone_page
