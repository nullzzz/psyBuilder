from PyQt5.QtWidgets import (QWidget, QTabWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from center.iconTabs.events.durationPage import DurationPage
from center.iconTabs.events.framePage import Tab2
from center.iconTabs.events.text.textGeneral import TextTab1


class TextProperty(QWidget):
    def __init__(self, parent=None):
        super(TextProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()

        self.general = TextTab1()
        self.frame = Tab2()
        self.duration = DurationPage()
        self.tab.addTab(self.general, "general")
        self.tab.addTab(self.frame, "frame")
        self.tab.addTab(self.duration, "duration")
        # bottom
        self.ok_bt = QPushButton("Ok")
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

    # 设置界面居中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def getInfo(self):
        pass

    def setAttributes(self, attributes):
        self.general.setAttributes(attributes)
        self.frame.setAttributes(attributes)
        self.duration.setAttributes(attributes)