from PyQt5.QtWidgets import QTableWidget, QFrame, QTableWidgetItem, QComboBox, QPushButton
from PyQt5.QtCore import Qt

from .case import Case
from noDash import NoDash


class CaseTable(QTableWidget):
    MAX_CASE_COUNT = 10
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
        self.setColumnWidth(1, 300)
        # first row
        item = QTableWidgetItem('Switch')
        item.setFlags(Qt.ItemIsSelectable)
        self.setItem(0, 0, item)
        self.setCellWidget(0, 1, self.var)
        # second row
        item = QTableWidgetItem(f"Case {0}")
        item.setTextAlignment(Qt.AlignTop)
        item.setFlags(Qt.ItemIsSelectable)
        self.setItem(1, 0, item)
        case = Case()
        self.cases.append(case)
        self.setCellWidget(1, 1, case)
        add_button = QPushButton("Add")
        add_button.setFixedHeight(30)
        add_button.clicked.connect(self.insertCase)
        self.add_buttons.append(add_button)
        self.setCellWidget(1, 2, add_button)
        self.setRowHeight(1, 300)

    def insertCase(self):
        if len(self.add_buttons) < CaseTable.MAX_CASE_COUNT:
            index = self.getIndex(self.sender())
            if index != -1:
                self.insertRow(index + 2)
                row = index + 2

                item = QTableWidgetItem(f"Case {index + 1}")
                item.setTextAlignment(Qt.AlignTop)
                item.setFlags(Qt.ItemIsSelectable)
                self.setItem(row, 0, item)

                case = Case()
                self.cases.append(case)
                self.setCellWidget(row, 1, case)

                add_button = QPushButton("Add")
                add_button.clicked.connect(self.insertCase)
                add_button.setFixedHeight(30)
                self.add_buttons.insert(index + 1, add_button)
                self.setCellWidget(row, 2, add_button)

                self.setRowHeight(row, 300)

                # change case name
                for i in range(row + 1, self.rowCount()):
                    self.item(i, 0).setText(f'Case {i - 1}')

    def getIndex(self, add_button):
        for i in range(0, len(self.add_buttons)):
            if add_button == self.add_buttons[i]:
                return i
        return -1
