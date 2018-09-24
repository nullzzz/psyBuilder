from PyQt5.QtWidgets import QTableWidget, QFrame, QTableWidgetItem, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import Qt

from .case import Case
from noDash import NoDash


class CaseTable(QTableWidget):
    MAX_CASE_COUNT = 9
    def __init__(self, parent=None):
        super(CaseTable, self).__init__(parent)
        # data
        self.var = QComboBox(self)
        self.cases = []
        self.add_buttons = []

        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        self.setItemDelegate(NoDash())
        self.setStyleSheet("""
            QTableView{
                selection-background-color: transparent;
            }
            QTableWidget::item{
                border-bottom:1px solid;
            }
        """)

        self.setRowCount(2)
        self.setColumnCount(3)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 300)
        self.setColumnWidth(2, 300)
        # first row
        label = QLabel("Switch:")
        label.setAlignment(Qt.AlignRight)
        self.setCellWidget(0, 0, label)
        self.setCellWidget(0, 1, self.var)
        # second row
        self.setRowHeight(1, 300)
        case_1 = Case("Case 1")
        self.setCellWidget(1, 0, case_1)
        case_2 = Case("Case 2")
        self.setCellWidget(1, 1, case_2)
        case_default = Case("Case default")
        self.setCellWidget(1, 2, case_default)

    def insertCase(self, index):
        pass
