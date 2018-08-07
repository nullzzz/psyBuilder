import sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QApplication, QComboBox, QWidget, \
    QLabel, QLineEdit, QCheckBox, QPushButton, QHBoxLayout


class SetUp(QWidget):
    propertiesChanged = pyqtSignal(dict)
    closed = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(SetUp, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.xpos = QLineEdit()
        self.ypos = QLineEdit()
        self.target_color = QLineEdit()
        self.target_stytle = QComboBox()
        self.show_display_with_drift_correction_target = QCheckBox("Show display with drift-correction target")
        self.show_display_with_drift_correction_target.stateChanged.connect(self.statueChanged)
        self.fixation_triggered = QCheckBox("Fixation triggered (no spacebar press required)")
        self.fixation_triggered.stateChanged.connect(self.statueChanged)
        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.xpos.setFocus()

    def setUI(self):
        self.setWindowTitle("Set up")
        self.resize(500, 750)
        # self.setStyleSheet("background-color: white;")
        self.tip1.setStyleSheet("border-width:0; border-style:outset; background-color: transparent;")
        self.tip1.setText("Drift_correct")
        # self.tip1.setFocusPolicy(Qt.NoFocus)
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0; border-style:outset; background-color: transparent;")
        self.tip2.setText("Perform eye-tracker drift correction")
        # self.tip2.setFocusPolicy(Qt.NoFocus)
        self.target_color.setText("(foreground)")
        self.target_stytle.addItems(["default", "large filled", "small filled", "large open", "small open", "large cross", "small cross"])
        self.target_color.setEnabled(False)
        self.target_stytle.setEnabled(False)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("X position"), 2, 0, 1, 1)
        layout1.addWidget(self.xpos, 2, 1, 1, 1)

        layout1.addWidget(QLabel("Y position"), 3, 0, 1, 1)
        layout1.addWidget(self.ypos, 3, 1, 1, 1)
        layout1.addWidget(QLabel("Target color"), 4, 0, 1, 1)
        layout1.addWidget(self.target_color, 4, 1, 1, 1)

        layout1.addWidget(QLabel("Target style"), 5, 0, 1, 1)
        layout1.addWidget(self.target_stytle, 5, 1, 1, 1)

        layout1.addWidget(self.show_display_with_drift_correction_target, 6, 1, 1, 1)
        layout1.addWidget(self.fixation_triggered, 7, 1, 1, 1)

        layout1.setContentsMargins(30, 10, 30, 0)
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

    def statueChanged(self):
        a = self.show_display_with_drift_correction_target.checkState()
        b = self.fixation_triggered.checkState()
        if a:
            self.target_color.setEnabled(True)
            self.target_stytle.setEnabled(True)
        else:
            self.target_color.setEnabled(False)
            self.target_stytle.setEnabled(False)

    def ok(self):
        self.apply()
        self.close()
        self.closed.emit(self)

    def cancel(self):
        self.close()
        self.closed.emit(self)

    def apply(self):
        self.propertiesChanged.emit(self.getProperties())

    def getProperties(self):
        x_p = self.xpos.text()
        y_p = self.ypos.text()
        color = self.target_color.text()
        style = self.target_stytle.currentText()
        a = self.show_display_with_drift_correction_target.checkState()
        b = self.fixation_triggered.checkState()
        return {
            "X position": x_p,
            "Y position": y_p,
            "Target color": color,
            "Target style": style,
            "show display with drift correction target": a,
            "fixation triggered": b
        }


if __name__ == "__main__":
    app = QApplication(sys.argv)

    t = SetUp()

    t.show()

    sys.exit(app.exec())
