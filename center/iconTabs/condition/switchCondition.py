from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QTableWidget, QLineEdit, QPushButton, QFrame, QLabel)

from noDash import NoDash


class SwitchCondition(QTableWidget):
    MAX_CONDITION_COUNT = 6
    add_case = pyqtSignal(int)

    def __init__(self, parent=None):
        super(SwitchCondition, self).__init__(parent)
        self.index = 1

        # 美化
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        self.setItemDelegate(NoDash())

        self.setColumnCount(9)
        self.setRowCount(1)

        self.setStyleSheet("""
            QComboBox {
                max-height : 30px;
            }
            QLineEdit {
                max-height : 30px;
            }
            QPushButton {
                max-height: 30px;
            }
            QTableWidget{
                selection-background-color : transparent;
            }
        """)

        self.add_buttons = []

        switch = QLineEdit()
        default_var = QLineEdit()

        add_button = QPushButton("&Add")
        add_button.clicked.connect(self.addCase)

        self.add_buttons.append(add_button)

        self.setCellWidget(0, 1, QLabel("Switch"))
        self.setCellWidget(0, 4, switch)
        self.setCellWidget(0, 6, add_button)

        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 10)
        self.setColumnWidth(4, 400)
        self.setColumnWidth(5, 10)
        self.setColumnWidth(6, 30)

    def addCase(self):
        try:
            if self.rowCount() < SwitchCondition.MAX_CONDITION_COUNT:
                self.insertRow(self.index)
                var = QLineEdit()
                add_button = QPushButton("Add")
                add_button.clicked.connect(self.addCase)

                self.add_buttons.insert(self.index, add_button)

                self.setCellWidget(self.index, 2, QLabel(f"case{self.index}"))
                self.setCellWidget(self.index, 4, var)
                self.setCellWidget(self.index, 6, add_button)
                self.add_case.emit(self.index)
                self.index += 1
        except Exception as e:
            print("error {} happens in add condition. [condition/conditionArea.py]".format(e))


