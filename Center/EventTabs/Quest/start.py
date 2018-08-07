from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QComboBox, QFormLayout)


class QuestStart(QWidget):
    propertiesChanged = pyqtSignal(dict)
    closed = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(QuestStart, self).__init__(parent)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()

        self.estimated_threshold = QLineEdit()
        self.std_dev = QLineEdit()
        self.desired_proportion = QLineEdit()
        self.steepness = QLineEdit()
        self.proportion = QLineEdit()
        self.chance_level = QLineEdit()
        self.method = QComboBox()
        self.minimum = QLineEdit()
        self.maximum = QLineEdit()
        self.experimental = QLineEdit()

        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()
        self.estimated_threshold.setFocus()

    def setUI(self):
        self.setWindowTitle("Start")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("QUEST staircase init")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Initializes a new Quest staircase procedure")
        self.estimated_threshold.setText("0.5")
        self.std_dev.setText("0.25")
        self.desired_proportion.setText("0.75")
        self.steepness.setText("3.5")
        self.proportion.setText("0.01")
        self.chance_level.setText("0.05")
        self.method.addItems(["quantile", "mean", "mode"])
        self.minimum.setText("0")
        self.maximum.setText("1")
        self.experimental.setText("quest_test_value")

        layout1 = QFormLayout()
        layout1.addRow(self.tip1)
        layout1.addRow(self.tip2)
        layout1.addRow("Estimated threshold (used for starting test value)", self.estimated_threshold)
        layout1.addRow("Std. dev. of estimated threshold", self.std_dev)
        layout1.addRow("Desired proportion of correct responses", self.desired_proportion)
        layout1.addRow("Steepness of the Weibull psychometric function(β)", self.steepness)
        layout1.addRow("Proportion of random responses at maximum stimulus intensity(σ)", self.proportion)
        layout1.addRow("Chance level (γ)", self.chance_level)
        layout1.addRow("Method to determine optimal test value", self.method)
        layout1.addRow("Minimum test value", self.minimum)
        layout1.addRow("Maximum test value", self.maximum)
        layout1.addRow("Experimental variable for test value", self.experimental)
        layout1.setLabelAlignment(Qt.AlignRight)

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
        # 关闭信号
        self.closed.emit(self)

    def cancel(self):
        self.close()
        # 关闭信号
        self.closed.emit(self)

    def apply(self):
        self.propertiesChanged.emit(self.getInfo())

    def getInfo(self):
        return {
            "Estimated threshold": self.estimated_threshold.text(),
            "Std. dev. of estimated threshold": self.std_dev.text(),
            "Desired proportion of correct responses": self.desired_proportion.text(),
            "Steepness of the Weibull psychometric function(β)": self.steepness.text(),
            "Proportion of random responses at maximum stimulus intensity(σ)": self.proportion.text(),
            "Chance level (γ)": self.chance_level.text(),
            "Method to determine optimal test value": self.method.currentText(),
            "Minimum test value": self.minimum.text(),
            "Maximum test value": self.maximum.text(),
            "Experimental variable for test value": self.experimental.text(),
        }
