from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class AddAttributeDialog(QDialog):
    # (attribute, value -> cycle )
    attributeData = pyqtSignal(str, str)

    def __init__(self, parent=None, attributes_exist=()):
        super(AddAttributeDialog, self).__init__(parent)
        # data
        self.attribute_exist = attributes_exist
        # 美化
        self.setWindowTitle("Add Attribute")
        self.setModal(True)
        self.setFixedSize(300, 250)
        # widget
        self.attribute = QLineEdit()
        self.value = QLineEdit()
        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.ok)
        ok_btn.setFixedWidth(120)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(120)
        cancel_btn.clicked.connect(self.cancel)
        # layout
        layout = QFormLayout()
        layout.addRow(QLabel("Set attributes and default values."))
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
        if not attribute or not attribute[0].isalpha():
            QMessageBox.information(self, 'Warning', 'Invalid attribute name.')
        elif attribute in self.attribute_exist or attribute in ['Weight', 'Timeline']:
            QMessageBox.information(self, 'Warning', 'Attribute has already existed.')
        else:
            self.attributeData.emit(attribute, value)
            self.close()

    def cancel(self):
        self.close()