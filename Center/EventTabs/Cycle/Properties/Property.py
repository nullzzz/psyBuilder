from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QPushButton, QVBoxLayout, QDialog, QFrame

from .General import General
from .Selection import Selection


class Property(QDialog):
    def __init__(self, parent=None):
        super(Property, self).__init__(parent)
        # self.tab = QTabWidget(self)
        self.tab = QFrame(self)
        self.below = QWidget(self)

        self.ok_bt = QPushButton("Ok")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")

        # self.general = General()
        self.selection = Selection(self.tab)

        # self.tab.addTab(self.general, "General")
        # self.tab.addTab(self.selection, "Selection")

        self.setButtons()
        self.setUI()

        self.cancel_bt.clicked.connect(self.close)

        # 生成主界面

    def setUI(self):
        self.setWindowTitle("Properties")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tab, 6)
        # mainLayout.addStretch(2)
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
