from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QFormLayout, QLabel)


class ColsAdd(QDialog):
    data = pyqtSignal(list)

    def __init__(self, parent=None, exist_name=[]):
        super(ColsAdd, self).__init__(parent)

        self.setFixedWidth(320)
        self.setWindowTitle("Add Columns")
        self.names = []
        self.values = []
        self.exist_name = exist_name
        self.form = QFormLayout(self)
        tip = QLabel("Set Names and it's default value.")
        font = QFont()
        font.setBold(True)
        tip.setFont(font)
        self.form.addRow(tip)
        self.form.addRow(QLabel(""))
        self.form.addRow(QLabel("Name: "), QLabel("Default Value: "))
        name = QLineEdit()
        name.setFixedWidth(100)
        value = QLineEdit("?")
        value.setFixedWidth(150)
        self.names.append(name)
        self.values.append(value)
        self.form.addRow(name, value)
        for i in range(0, 4):
            self.form.addRow(QLabel())

        addButton = QPushButton("add")
        okButton = QPushButton("ok")
        cancelButton = QPushButton("cancel")

        addButton.clicked.connect(self.addRow)
        okButton.clicked.connect(self.submitData)
        cancelButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(okButton)
        hBox.addWidget(addButton)
        hBox.addWidget(cancelButton)

        self.form.addRow(hBox)

        self.setLayout(self.form)

        self.count = 1

    def addRow(self):
        name = QLineEdit()
        name.setFixedWidth(100)
        value = QLineEdit("?")
        value.setFixedWidth(150)

        self.names.append(name)
        self.values.append(value)

        if self.count > 3:
            self.form.insertRow(self.count + 3, name, value)
        else:
            self.form.removeRow(3 + self.count)
            self.form.insertRow(3 + self.count, name, value)

        self.count += 1

    def submitData(self):
        data = []
        names = []
        index = -1
        for i in range(0, len(self.values)):
            name = self.names[i].text()
            if name and name not in names and name not in self.exist_name:
                names.append(name)
                data.append(name)
                data.append(self.values[i].text())
            else:
                index = i
                QMessageBox.information(self, "Tips", "No.{} row's name is none or repeat".format(index + 1))
                break

        if index == -1:
            self.data.emit(data)
            self.close()
