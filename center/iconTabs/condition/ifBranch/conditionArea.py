from PyQt5.QtWidgets import (QComboBox, QFrame, QFormLayout, QHBoxLayout, QMessageBox, QLabel)

from ..addDeleteButton import AddDeleteButton


class ConditionArea(QFrame):
    #
    MAX_CONDITION_COUNT = 6

    def __init__(self, parent=None):
        super(ConditionArea, self).__init__(parent)
        #
        self.add_buttons = []
        self.delete_buttons = [None]
        #
        self.form_layout = QFormLayout(self)

        h_box = QHBoxLayout()
        # place holder
        self.placeholder_width = 100
        placeholder = QLabel()
        placeholder.setFixedWidth(self.placeholder_width)
        # var
        var = QComboBox()
        # compare operator
        compare_operator = QComboBox()
        compare_operator.addItems((">", "<", "=="))
        compare_operator.setFixedWidth(self.placeholder_width)
        # compare var
        compare_var = QComboBox()
        # add button
        add_button = AddDeleteButton(button_type='add')
        add_button.clicked.connect(self.addCondition)
        self.add_buttons.append(add_button)

        h_box.addWidget(placeholder)
        h_box.addWidget(var)
        h_box.addWidget(compare_operator)
        h_box.addWidget(compare_var)
        h_box.addWidget(add_button)
        placeholder_ = QLabel()
        placeholder_.setFixedWidth(add_button.width())
        h_box.addWidget(placeholder_)
        self.form_layout.addRow(h_box)

        self.setLayout(self.form_layout)

    def addCondition(self):
        try:
            if len(self.add_buttons) < ConditionArea.MAX_CONDITION_COUNT:
                index = self.getAddButtonIndex(self.sender())
                if index != -1:
                    h_box = QHBoxLayout()
                    # logical operator
                    logical_operator = QComboBox()
                    logical_operator.addItems(('and', 'or', 'xor', 'nor', 'nand', 'xnor'))
                    logical_operator.setFixedWidth(self.placeholder_width)
                    # var
                    var = QComboBox()
                    # compare_operator
                    compare_operator = QComboBox()
                    compare_operator.addItems((">", "<", "=="))
                    compare_operator.setFixedWidth(self.placeholder_width)
                    # compare var
                    compare_var = QComboBox()
                    # add button
                    add_button = AddDeleteButton(button_type='add')
                    self.add_buttons.insert(index + 1, add_button)
                    add_button.clicked.connect(self.addCondition)
                    # delete button
                    delete_button = AddDeleteButton(button_type='delete')
                    delete_button.clicked.connect(self.deleteCondition)
                    self.delete_buttons.insert(index + 1, delete_button)

                    h_box.addWidget(logical_operator)
                    h_box.addWidget(var)
                    h_box.addWidget(compare_operator)
                    h_box.addWidget(compare_var)
                    h_box.addWidget(add_button)
                    h_box.addWidget(delete_button)

                    self.form_layout.insertRow(index + 1, h_box)
            else:
                QMessageBox.information(self, 'Tips', f'you can add no more than {ConditionArea.MAX_CONDITION_COUNT}', QMessageBox.Ok)
        except Exception as e:
            print(f"error {e} happens in add condition. [ifBranch/conditionArea.py]")

    def deleteCondition(self):
        try:
            index = self.getDeleteButtonIndex(self.sender())
            if index != -1:
                self.form_layout.removeRow(index)
                # delete buttons
                self.add_buttons.pop(index)
                self.delete_buttons.pop(index)
        except Exception as e:
            print(f"error {e} happens in delete condition. [ifBranch/conditionArea.py]")

    def getAddButtonIndex(self, add_button):
        for i in range(0, len(self.add_buttons)):
            if add_button == self.add_buttons[i]:
                return i
        return -1

    def getDeleteButtonIndex(self, delete_button):
        for i in range(1, len(self.delete_buttons)):
            if delete_button == self.delete_buttons[i]:
                return i
        return -1

