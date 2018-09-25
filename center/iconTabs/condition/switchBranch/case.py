from PyQt5.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QGroupBox
from PyQt5.QtCore import pyqtSignal, Qt

from ..iconChoose import IconChoose
from ..addDeleteButton import AddDeleteButton


class Case(QGroupBox):
    add = pyqtSignal()
    delete = pyqtSignal()

    def __init__(self, title: str='test', parent=None, can_add=False, can_delete=False):
        super(Case, self).__init__(title, parent)
        # case
        self.case_comBox = QComboBox(self)
        # icon choose
        self.icon_choose = IconChoose(self)
        self.add_button = AddDeleteButton(self, 'add')
        self.delete_button = AddDeleteButton(self, 'delete')

        self.grid_layout = QGridLayout(self)

        label = QLabel("Case Value:")
        label.setAlignment(Qt.AlignRight)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.case_comBox, 0, 1, 1, 5)
        self.grid_layout.addWidget(self.icon_choose, 1, 0, 3, 5)
        self.grid_layout.addWidget(self.add_button, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.delete_button, 4, 3, 1, 1)
        self.setLayout(self.grid_layout)

        if not can_add:
            self.add_button.setDisabled(True)
        if not can_delete:
            self.delete_button.setDisabled(True)

    def setAddDisabled(self, disabled=False):
        if disabled:
            self.add_button.setDisabled(True)
        else:
            self.add_button.setDisabled(False)

    def setDeleteDisabled(self, disabled=False):
        if disabled:
            self.delete_button.setDisabled(True)
        else:
            self.delete_button.setDisabled(False)
