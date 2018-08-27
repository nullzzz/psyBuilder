from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QComboBox


class EyeAction(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(EyeAction, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.event = QComboBox()
        self.msg = ""
        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.event.setFocus()

    def setUI(self):
        self.setWindowTitle("Action")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Wait")
        # self.tip1.setFocusPolicy(Qt.NoFocus)
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Waits for an eye-tracker event")
        # self.tip2.setFocusPolicy(Qt.NoFocus)
        self.event.addItems(["Saccade start", "Saccade end", "Fixation start", "Fixation end", "Blink start", "Blink end"])

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Statue Message:"), 2, 0, 1, 1)
        layout1.addWidget(self.event, 2, 1, 1, 1)

        layout2 = QHBoxLayout()
        layout2.addStretch(10)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self)

    def cancel(self):
        self.close()
        self.tabClose.emit(self)

    def apply(self):
        self.msg = self.event.currentText()
        self.propertiesChange.emit(self.getProperties())

    def getProperties(self):
        return {"Statue Message": self.msg}


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeAction()

    pro.show()

    sys.exit(app.exec())
