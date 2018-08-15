from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout

from .videoGeneral import VideoTab1
from ..durationPage import Tab3
from ..framePage import Tab2


class VideoProperty(QWidget):
    def __init__(self, parent=None):
        super(VideoProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()
        self.ok_bt = QPushButton("Ok")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.tab1 = VideoTab1()
        try:
            self.tab2 = Tab2()
            self.tab3 = Tab3()
        except Exception as e:
            print(e)

        self.tab.addTab(self.tab1, "general")
        self.tab.addTab(self.tab2, "frame")
        self.tab.addTab(self.tab3, "duration")
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
