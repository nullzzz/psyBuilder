from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout

from ..iconChoose import IconChoose


class Case(QWidget):
    def __init__(self, parent=None):
        super(Case, self).__init__(parent)
        # case
        self.case_comBox = QComboBox(self)
        # icon choose
        self.icon_choose = IconChoose(self)

        self.v_box = QVBoxLayout(self)

        self.v_box.addWidget(self.case_comBox)
        self.v_box.addWidget(self.icon_choose)

        self.setLayout(self.v_box)