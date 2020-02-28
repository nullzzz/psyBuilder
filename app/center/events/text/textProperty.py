from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout)

from app.center.events.durationPage import DurationPage
from app.center.events.framePage import FramePage
from app.center.events.text.textGeneral import TextTab1


class TextProperty(QWidget):
    def __init__(self, parent=None):
        super(TextProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()

        self.general = TextTab1()
        self.frame = FramePage()
        self.frame.x_pos.setCurrentText("50%")
        self.frame.y_pos.setCurrentText("50%")
        self.duration = DurationPage()

        self.html = self.general.html

        self.default_properties = {**self.general.getInfo(), **self.frame.getInfo(), **self.duration.getInfo()}

        self.tab.addTab(self.general, "general")
        self.tab.addTab(self.frame, "frame")
        self.tab.addTab(self.duration, "duration")
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setButtons()

        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Text property")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        # main_layout.addStretch(2)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    # 生成下方三个按钮
    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    def refresh(self):
        self.general.refresh()

    def getInfo(self):
        self.general.apply()
        self.html = self.general.html
        self.default_properties = {**self.general.getInfo(), **self.frame.getInfo(), **self.duration.getInfo()}
        return self.default_properties

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def setOther(self, html: str = ""):
        self.html = html

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.general.setProperties(self.default_properties, self.html)
        self.frame.setProperties(self.default_properties)
        self.duration.setProperties(self.default_properties)

    def clone(self):
        clone_page = TextProperty()
        clone_page.setOther(self.html)
        clone_page.setProperties(self.default_properties)
        return clone_page
