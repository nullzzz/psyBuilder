from PyQt5.QtWidgets import (QTableWidget, QComboBox, QLineEdit, QPushButton, QFrame)
from noDash import NoDash


class ConditionArea(QTableWidget):
    def __init__(self, parent=None):
        super(ConditionArea, self).__init__(parent)

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

        var = QComboBox()
        compare_operator = QComboBox()
        compare_operator.addItems((">", "<", "=="))
        compare_value = QLineEdit()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.addCondition)

        self.add_buttons.append(add_button)

        self.setCellWidget(0, 2, var)
        self.setCellWidget(0, 4, compare_operator)
        self.setCellWidget(0, 6, compare_value)
        self.setCellWidget(0, 8, add_button)

        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 10)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 10)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 10)
        self.setColumnWidth(6, 500)
        self.setColumnWidth(7, 10)
        self.setColumnWidth(8, 60)

    def addCondition(self):
        try:
            index = self.getIndex(self.sender())
            if index != -1:
                print(index)
                self.insertRow(index + 1)

                and_or = QComboBox()
                and_or.addItems(("and", "or"))
                var = QComboBox()
                compare_operator = QComboBox()
                compare_operator.addItems((">", "<", "=="))
                compare_value = QLineEdit()
                add_button = QPushButton("Add")
                add_button.clicked.connect(self.addCondition)

                self.add_buttons.insert(index + 1, add_button)

                self.setCellWidget(index + 1, 0, and_or)
                self.setCellWidget(index + 1, 2, var)
                self.setCellWidget(index + 1, 4, compare_operator)
                self.setCellWidget(index + 1, 6, compare_value)
                self.setCellWidget(index + 1, 8, add_button)
        except Exception as e:
            print("error {} happens in add condition. [condition/conditionArea.py]".format(e))

    def getIndex(self, add_button):
        for i in range(0, len(self.add_buttons)):
            if add_button == self.add_buttons[i]:
                return i
        return -1