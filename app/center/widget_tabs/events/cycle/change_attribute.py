from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import re

class ChangeAttributeDialog(QDialog):
    # (attribute, value -> cycle )
    attributeData = pyqtSignal(int, str, str)

    def __init__(self, parent=None, col=-1, attribute='', value='', attributes_exist=()):
        super(ChangeAttributeDialog, self).__init__(parent)
        # data
        self.old_attribute = attribute
        self.old_value = value
        self.attribute_exist = list(attributes_exist)
        self.col = col
        # 美化
        self.setWindowTitle("Add Attribute")
        self.setModal(True)
        self.setFixedSize(300, 250)
        # widget
        self.attribute = QLineEdit(attribute)
        self.value = QLineEdit(value)
        if attribute in ['Weight', 'Timeline']:
            self.attribute.setEnabled(False)
            if attribute == 'Timeline':
                self.value.setText('Sorry, you can\'set.')
                self.value.setEnabled(False)
        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.ok)
        ok_btn.setFixedWidth(120)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(120)
        cancel_btn.clicked.connect(self.cancel)
        # layout
        layout = QFormLayout()
        layout.addRow(QLabel("Set column name and default value."))
        layout.addRow(QLabel(""))
        layout.addRow(QLabel("Name : "), self.attribute)
        layout.addRow(QLabel("Default Value : "), self.value)
        layout.addRow(QLabel(""))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(10)

        layout.addRow(btn_layout)
        self.setLayout(layout)

    def ok(self):
        attribute = self.attribute.text()
        value = self.value.text()
        # 如果是weight,必须是数字
        if attribute == "Weight":
            if not re.match(r"^[0-9]+$", value):
                QMessageBox.information(self, 'Warning', 'Value must be positive number.')
                return
        if attribute == self.old_attribute:
            if value != self.old_value:
                self.attributeData.emit(self.col, attribute, value)
            self.close()
        else:
            if not attribute or not attribute[0].isalpha():
                QMessageBox.information(self, 'Warning', 'Invalid attribute name.')
            elif attribute in self.attribute_exist or attribute in ['Weight', 'Timeline']:
                QMessageBox.information(self, 'Warning', 'Attribute has already existed.')
            else:
                self.attributeData.emit(self.col, attribute, value)
                self.close()

    def cancel(self):
        self.close()
