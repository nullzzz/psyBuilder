from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QDialog, QFrame

from .selection import Selection


class Property(QDialog):
    def __init__(self, parent=None):
        super(Property, self).__init__(parent)
        # self.tab = QTabWidget(self)
        self.tab = QFrame(self)
        self.below = QWidget(self)

        self.ok_bt = QPushButton("OK")
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
        self.setWindowTitle("properties")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab, 6)
        # mainLayout.addStretch(2)
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
