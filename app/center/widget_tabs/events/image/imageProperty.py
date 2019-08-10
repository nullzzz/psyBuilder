from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from app.center.widget_tabs.events.durationPage import DurationPage
from app.center.widget_tabs.events.framePage import FramePage
from .imageGeneral import ImageTab1


class ImageProperty(QWidget):
    def __init__(self, parent=None):
        super(ImageProperty, self).__init__(parent)

        self.general = ImageTab1()
        self.frame = FramePage()
        self.duration = DurationPage()

        self.default_properties = {**self.general.getProperties(),
                                   **self.frame.getProperties(),
                                   **self.duration.default_properties}
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")

        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Image property")
        self.resize(600, 800)

        below = QWidget()
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        below.setLayout(below_layout)
        tab = QTabWidget()
        tab.addTab(self.general, "general")
        tab.addTab(self.frame, "frame")
        tab.addTab(self.duration, "duration")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab, 6)
        main_layout.addWidget(below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties = {**self.general.getInfo(), **self.frame.getInfo(), **self.duration.getInfo()}
        return self.default_properties

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties = {
            **self.general.getProperties(),
            **self.frame.getProperties(),
            **self.duration.default_properties
        }

    def setAttributes(self, attributes: list):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        # WARNING
        # 这里将主页面的所有属性设置到分页面
        # 主页面重新获取分页面属性时
        # 分页面应先将default_properties清空
        self.general.setProperties(self.default_properties)
        self.frame.setProperties(self.default_properties)
        self.duration.setProperties(self.default_properties)

    def clone(self):
        properties = self.getInfo()
        clone_page = ImageProperty()
        clone_page.setProperties(properties)
        return clone_page
