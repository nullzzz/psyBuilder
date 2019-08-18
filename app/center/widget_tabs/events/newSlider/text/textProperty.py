from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from app.center.widget_tabs.events.newSlider.text.textGeneral import TextGeneral


class TextProperty(QWidget):
    def __init__(self, parent=None):
        super(TextProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()
        self.general = TextGeneral()

        # self.html = self.general.html

        self.default_properties = self.general.getInfo()

        self.tab.addTab(self.general, "general")
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

    def getInfo(self):
        # self.apply()
        # self.html = self.general.html
        self.default_properties = self.general.getInfo()
        return self.default_properties

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)

    def setOther(self, html: str = ""):
        self.html = html

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.general.setProperties(self.default_properties)

    def clone(self):
        clone_page = TextProperty()
        # clone_page.setOther(self.html)
        clone_page.setProperties(self.default_properties)
        return clone_page
