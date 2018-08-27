from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QComboBox


class EyeCalibrate(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(EyeCalibrate, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.calibration_type = QComboBox()
        self.calibration_beep = QComboBox()
        self.target_color = QLineEdit()
        self.target_style = QComboBox()

        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.calibration_type.setFocus()

    def setUI(self):
        self.setWindowTitle("Calibration")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Calibration")
        # self.tip1.setFocusPolicy(Qt.NoFocus)
        self.tip1.setFont(QFont("Timers", 20,  QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Calibration")
        # self.tip2.setFocusPolicy(Qt.NoFocus)
        self.calibration_type.addItems(["HV9", "HV13", "HV5", "HV3"])
        self.calibration_beep.addItems(["Yes", "No"])
        self.target_color.setText("(foreground)")
        self.target_style.addItems(
            ["default", "large filled", "small filled", "large open", "small open", "large cross", "small cross"])

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Calibration type:"), 2, 0, 1, 1)
        layout1.addWidget(self.calibration_type, 2, 1, 1, 1)
        layout1.addWidget(QLabel("Calibration beep:"), 3, 0, 1, 1)
        layout1.addWidget(self.calibration_beep, 3, 1, 1, 1)
        layout1.addWidget(QLabel("Target color:"), 4, 0, 1, 1)
        layout1.addWidget(self.target_color, 4, 1, 1, 1)
        layout1.addWidget(QLabel("Target style:"), 5, 0, 1, 1)
        layout1.addWidget(self.target_style, 5, 1, 1, 1)

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
        self.propertiesChange.emit(self.getProperties())

    def getProperties(self):
        return {
            "Calibration type": self.calibration_type.currentText(),
            "Calibration beep": self.calibration_beep.currentText(),
            "Target color": self.target_color.text(),
            "Target style": self.target_style.currentText()
        }


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeCalibrate()

    pro.show()

    sys.exit(app.exec())
