from PyQt5.QtWidgets import QGroupBox, QFormLayout, QLineEdit


class AttributeArea(QGroupBox):
    def __init__(self, name: str = "", value: str = ""):
        super(AttributeArea, self).__init__(None)
        # widget
        self.name_line_edit = QLineEdit(name)
        self.value_line_edit = QLineEdit(value)
        self.name_line_edit.setMinimumWidth(150)
        self.value_line_edit.setMinimumWidth(150)
        # layout
        layout = QFormLayout()
        layout.addRow("Name: ", self.name_line_edit)
        layout.addRow("Default Value: ", self.value_line_edit)
        self.setLayout(layout)

    def name(self):
        """
        return its name
        """
        return self.name_line_edit.text()

    def value(self):
        """
        return its value
        """
        return self.value_line_edit.text()

    def __str__(self):
        return f"name: {self.name()}\tvalue: {self.value()}"

    def setNameChangeable(self, changeable: bool):
        """
        set value can be changed or not
        """
        self.name_line_edit.setEnabled(changeable)

    def setValueChangeable(self, changeable: bool):
        """
        set value can be changed or not
        """
        if changeable:
            self.value_line_edit.setText("")
            self.value_line_edit.setEnabled(True)
        else:
            self.value_line_edit.setText("Sorry, you can't set it.")
            self.value_line_edit.setEnabled(False)
