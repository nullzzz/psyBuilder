from PyQt5.QtWidgets import QComboBox, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import Qt

from .case import Case


class CaseArea(QWidget):
    MAX_CASE_COUNT = 9
    def __init__(self, parent=None):
        super(CaseArea, self).__init__(parent)

        # data
        self.cases = []
        self.cases.append(Case(title='Case 1', can_add=True, can_delete=True))
        self.cases.append(Case(title='Case 2', can_add=True, can_delete=False))
        self.cases.append(Case(title='Case Default', can_add=True, can_delete=False))
        self.switch = QComboBox(self)

        self.grid_layout = QGridLayout(self)

        label = QLabel("Switch:")
        label.setAlignment(Qt.AlignRight)
        self.grid_layout.addWidget(label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.switch, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.cases[0], 1, 0, 1, 1)
        self.grid_layout.addWidget(self.cases[1], 1, 1, 1, 1)
        self.grid_layout.addWidget(self.cases[2], 1, 2, 1, 1)
        self.grid_layout.addWidget(QWidget(), 2, 0, 1, 1)
        self.grid_layout.addWidget(QWidget(), 2, 1, 1, 1)
        self.grid_layout.addWidget(QWidget(), 2, 2, 1, 1)
        self.grid_layout.addWidget(QWidget(), 3, 0, 1, 1)
        self.grid_layout.addWidget(QWidget(), 3, 1, 1, 1)
        self.grid_layout.addWidget(QWidget(), 3, 2, 1, 1)
        self.setLayout(self.grid_layout)

    def insertCase(self, index):
        try:
            if index < CaseArea.MAX_CASE_COUNT:
                row = index // 3
                col = index % 3
                # 添加在末尾
                if index == len(self.cases):
                    pass
                else:
                    pass
                if len(self.cases) == CaseArea.MAX_CASE_COUNT:
                    pass
        except Exception as e:
            print(f"error {e} happens in insert case. [switch/caseArea.py]")

    def deleteCase(self, index):
        pass
