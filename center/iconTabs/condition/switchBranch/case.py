from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal, Qt

from ..iconChoose import IconChoose


class Case(QGroupBox):
    add = pyqtSignal()
    delete = pyqtSignal()

    def __init__(self, title: str='test', parent=None):
        super(Case, self).__init__(title, parent)
        # case
        self.case_comBox = QComboBox(self)
        # icon choose
        self.icon_choose = IconChoose(self)

        self.grid_layout = QGridLayout(self)

        label = QLabel("Case Value:")
        label.setAlignment(Qt.AlignRight)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.case_comBox, 0, 1, 1, 3)
        self.grid_layout.addWidget(self.icon_choose, 1, 0, 3, 4)
        self.setLayout(self.grid_layout)


