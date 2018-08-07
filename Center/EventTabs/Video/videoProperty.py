from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout, QApplication

from .VideoTab3 import VideoTab3
from .videoTab1 import VideoTab1
from .videoTab2 import VideoTab2


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()
        self.ok_bt = QPushButton("Ok")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.tab1 = VideoTab1()
        self.tab2 = VideoTab2()
        self.tab3 = VideoTab3()

        self.tab.addTab(self.tab1, "general")
        self.tab.addTab(self.tab2, "frame")
        self.tab.addTab(self.tab3, "action")
        self.setButtons()
        self.setUI()

        # 生成主界面
    def setUI(self):
        self.setWindowTitle("Video property")
        self.resize(600, 800)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tab, 6)
        mainLayout.addWidget(self.below, 1)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

    def setButtons(self):
        belowLayout = QHBoxLayout()
        belowLayout.addStretch(10)
        belowLayout.addWidget(self.ok_bt, 1)
        belowLayout.addWidget(self.cancel_bt, 1)
        belowLayout.addWidget(self.apply_bt, 1)
        belowLayout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(belowLayout)
