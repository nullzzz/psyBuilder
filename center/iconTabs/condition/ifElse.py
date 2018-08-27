import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QGridLayout, QApplication
from PyQt5.QtCore import pyqtSignal

from .iconComboBox import IconComboBox


class IfElse(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(IfElse, self).__init__(parent)

        self.setWindowTitle("If-else")

        form_layout = QFormLayout()

        self.if_text = QLineEdit(self)
        form_layout.addRow(QLabel("  If:"), self.if_text)
        self.if_combo = IconComboBox(self)
        form_layout.addRow(QLabel("     "), self.if_combo)
        self.else_text = QLineEdit(self)
        form_layout.addRow(QLabel("else:"), self.else_text)
        self.else_combo = IconComboBox(self)
        form_layout.addRow(QLabel("     "), self.else_combo)

        hBox_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.clickOk)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.clickCancel)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.clickApply)
        hBox_layout.addStretch(1)
        hBox_layout.addWidget(self.ok_button)
        hBox_layout.addWidget(self.cancel_button)
        hBox_layout.addWidget(self.apply_button)

        vBox_layout = QVBoxLayout(self)
        vBox_layout.addLayout(form_layout)
        vBox_layout.addStretch(1)
        vBox_layout.addLayout(hBox_layout)

        self.setLayout(vBox_layout)

    def clickOk(self):
        self.clickApply()
        self.close()
        #
        self.tabClose.emit(self)

    def clickCancel(self):
        self.close()
        self.tabClose.emit(self)

    def clickApply(self):
        self.propertiesChange.emit(self.getProperties())

    def getProperties(self):
        return {"properties" : "none"}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = IfElse()
    demo.show()
    sys.exit(app.exec())
