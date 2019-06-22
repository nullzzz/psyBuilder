from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QScrollArea, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, \
    QVBoxLayout


class AddAttributesDialog(QDialog):
    # (attribute, value -> cycle )
    attributeData = pyqtSignal(list, list)

    def __init__(self, parent=None, attributes_exist=()):
        super(AddAttributesDialog, self).__init__(parent)
        # data
        self.attribute_exist = attributes_exist
        self.attribute_list = []
        # 美化
        self.setWindowTitle("Add Attribute")
        self.setModal(True)
        self.setMinimumHeight(600)
        # widget
        self.attribute_area = QScrollArea()
        self.temp_widget = QWidget()
        self.attribute_area.setWidget(self.temp_widget)
        self.attribute_area.setWidgetResizable(True)
        self.attribute = QLineEdit()
        self.value = QLineEdit()
        self.attribute_list.append([self.attribute, self.value])
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.addAttributeRow)
        add_btn.setFixedWidth(120)
        ok_btn = QPushButton("Ok")
        ok_btn.clicked.connect(self.ok)
        ok_btn.setFixedWidth(120)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedWidth(120)
        cancel_btn.clicked.connect(self.cancel)
        # layout
        v_layout = QVBoxLayout()

        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Set attribute and default value."))
        self.layout.addRow(QLabel(""))
        self.layout.addRow(QLabel("Name : "), self.attribute)
        self.layout.addRow(QLabel("Default Value : "), self.value)
        self.layout.addRow(QLabel(""))
        self.temp_widget.setLayout(self.layout)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(10)

        v_layout.addWidget(self.attribute_area)
        v_layout.addLayout(btn_layout)
        self.setLayout(v_layout)

    def addAttributeRow(self):
        attribute = QLineEdit()
        value = QLineEdit()
        self.layout.insertRow(self.layout.rowCount(), QLabel("Name : "), attribute)
        self.layout.insertRow(self.layout.rowCount(), QLabel("Default Value : "), value)
        self.layout.insertRow(self.layout.rowCount(), QLabel(""))
        self.attribute_list.append([attribute, value])

    def ok(self):
        attribute_list = []
        value_list = []
        flag = True
        for attribute_edit, value_edit in self.attribute_list:
            attribute = attribute_edit.text()
            value = value_edit.text()
            if not attribute or not attribute[0].isalpha():
                QMessageBox.information(self, 'Warning', 'Invalid attribute name.')
                flag = False
                break
            elif attribute in self.attribute_exist or attribute in ['Weight',
                                                                    'Timeline'] or attribute in attribute_list:
                QMessageBox.information(self, 'Warning', 'Attribute has already existed.')
                flag = False
                break
            attribute_list.append(attribute)
            value_list.append(value)
        if flag:
            self.attributeData.emit(attribute_list, value_list)
            self.close()

    def cancel(self):
        self.close()
