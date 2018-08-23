from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout)


class ColAdd(QDialog):
    data = pyqtSignal(list)

    def __init__(self, parent=None, name="", value="", col=-1, exist_name=[]):
        super(ColAdd, self).__init__(parent)

        self.setWindowTitle("Add Column")
        self.setModal(True)
        self.setFixedSize(300, 250)

        self.col = col
        self.name = QLineEdit(name, self)
        self.exist_name = exist_name
        if col in [0, 1]:
            self.name.setEnabled(False)
        self.value = QLineEdit(value, self)

        form = QFormLayout(self)
        form.addRow(QLabel("Set column name and default value."))
        form.addRow(QLabel(""))
        form.addRow(QLabel("Name : "), self.name)
        form.addRow(QLabel("Default Value : "), self.value)
        ok = QPushButton("OK")
        ok.setFixedWidth(120)
        cancel = QPushButton("Cancel")
        cancel.setFixedWidth(120)
        form.addRow(QLabel(""))
        h_box = QHBoxLayout()
        h_box.addWidget(ok)
        h_box.addWidget(cancel)
        h_box.setAlignment(Qt.AlignCenter)
        h_box.setSpacing(10)
        form.addRow(h_box)
        form.setVerticalSpacing(10)

        ok.clicked.connect(self.submitData)
        cancel.clicked.connect(self.close)

        self.setLayout(form)

    def submitData(self):
        name = self.name.text()
        value = self.value.text()
        if not name:
            QMessageBox.information(self, "Tips", "Name can't be none.")
        elif name in self.exist_name:
            QMessageBox.information(self, "Tips", "Name already exists.")
        else:
            data = [name, value]
            self.close()
            if self.col != -1:
                data.append(self.col)
            self.data.emit(data)