from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QComboBox, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, \
    QHBoxLayout, QMessageBox, QCompleter


class EyeDC(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(EyeDC, self).__init__(parent)

        self.attributes = []

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.x_pos = QLineEdit()
        self.y_pos = QLineEdit()
        self.target_color = QLineEdit()
        self.target_style = QComboBox()

        self.x_pos.textChanged.connect(self.findVar)
        self.y_pos.textChanged.connect(self.findVar)
        self.target_color.textChanged.connect(self.findVar)
        self.x_pos.returnPressed.connect(self.finalCheck)
        self.y_pos.returnPressed.connect(self.finalCheck)
        self.target_color.returnPressed.connect(self.finalCheck)

        self.show_display_with_drift_correction_target = QCheckBox("Show Display With Drift-Correction Target")
        self.show_display_with_drift_correction_target.stateChanged.connect(self.statueChanged)
        self.fixation_triggered = QCheckBox("Fixation Triggered (No Spacebar Press Required)")
        self.fixation_triggered.stateChanged.connect(self.statueChanged)
        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(["test"])

        self.x_pos.setFocus()

    def setUI(self):
        self.setWindowTitle("DC")
        self.resize(500, 750)
        # self.setStyleSheet("background-color: white;")
        self.tip1.setStyleSheet("border-width:0; border-style:outset; background-color: transparent;")
        self.tip1.setText("Drift correct")
        # self.tip1.setFocusPolicy(Qt.NoFocus)
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0; border-style:outset; background-color: transparent;")
        self.tip2.setText("Perform eye-tracker drift correction")
        # self.tip2.setFocusPolicy(Qt.NoFocus)
        self.target_color.setText("(foreground)")
        self.target_style.addItems(["default", "large filled", "small filled", "large open", "small open", "large cross", "small cross"])
        self.target_color.setEnabled(False)
        self.target_style.setEnabled(False)

        l1 = QLabel("X Position:")
        l2 = QLabel("Y Position:")
        l3 = QLabel("Target Color:")
        l4 = QLabel("Target Style:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(l1, 2, 0, 1, 1)
        layout1.addWidget(self.x_pos, 2, 1, 1, 1)

        layout1.addWidget(l2, 3, 0, 1, 1)
        layout1.addWidget(self.y_pos, 3, 1, 1, 1)
        layout1.addWidget(l3, 4, 0, 1, 1)
        layout1.addWidget(self.target_color, 4, 1, 1, 1)

        layout1.addWidget(l4, 5, 0, 1, 1)
        layout1.addWidget(self.target_style, 5, 1, 1, 1)

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
            self.target_style.setEnabled(True)
        else:
            self.target_color.setEnabled(False)
            self.target_style.setEnabled(False)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self)

    def cancel(self):
        self.close()
        self.tabClose.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getProperties())

        # 检查变量

    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        self.x_pos.setCompleter(QCompleter(self.attributes))
        self.y_pos.setCompleter(QCompleter(self.attributes))
        self.target_color.setCompleter(QCompleter(self.attributes))

    def getProperties(self):
        x_p = self.x_pos.text()
        y_p = self.y_pos.text()
        color = self.target_color.text()
        style = self.target_style.currentText()
        a = self.show_display_with_drift_correction_target.checkState()
        b = self.fixation_triggered.checkState()
        return {
            "X position": x_p,
            "Y position": y_p,
            "Target color": color,
            "Target style": style,
            "Show display with drift correction target": a,
            "Fixation triggered": b
        }
