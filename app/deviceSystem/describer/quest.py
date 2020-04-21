from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QComboBox

from app.info import Info


class Quest(QWidget):
    def __init__(self, parent=None):
        super(Quest, self).__init__(parent)

        self.device_type = QLabel(Info.DEV_QUEST)
        self.device_name = QLabel("Unselected")
        self.estimated_threshold = QLineEdit()
        self.estimated_threshold.setToolTip("Used For Starting Test Value")

        self.std_dev = QLineEdit()
        self.std_dev.setToolTip("Of Estimated Threshold")

        self.desired_proportion = QLineEdit()
        self.desired_proportion.setToolTip("Of Correct Responses")

        self.steepness = QLineEdit()
        self.steepness.setToolTip("Of The Weibull Psychometric Function")

        self.proportion = QLineEdit()
        self.proportion.setToolTip("Of Random Responses At Maximum Stimulus Intensity")

        self.chance_level = QLineEdit()

        self.method = QComboBox()
        self.method.addItems(("quantile", "mean", "mode"))
        self.method.setToolTip("To Determine Optimal Test Value")

        self.minimum = QLineEdit()
        self.maximum = QLineEdit()
        self.is_log10_transform = QComboBox()
        self.is_log10_transform.addItems(("Yes", "No"))

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Threshold Value:", self.estimated_threshold)
        layout.addRow("Std. Dev.:", self.std_dev)
        layout.addRow("Desired Proportion:", self.desired_proportion)
        layout.addRow("Steepness(β):", self.steepness)
        layout.addRow("Proportion(σ):", self.proportion)
        layout.addRow("Chance Level (γ):", self.chance_level)
        layout.addRow("Method:", self.method)
        layout.addRow("Minimum Test Value:", self.minimum)
        layout.addRow("Maximum Test Value:", self.maximum)
        layout.addRow("Is Log10 Transform:", self.is_log10_transform)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setLayout(layout)

    def describe(self, info: dict):
        device_name = info.get("Device Name")

        self.device_name.setText(device_name)
        self.estimated_threshold.setText(info.get("Threshold Value", ""))
        self.std_dev.setText(info.get("Std. Dev.", ""))
        self.desired_proportion.setText(info.get("Desired Proportion", ""))
        self.steepness.setText(info.get("Steepness", ""))
        self.proportion.setText(info.get("Proportion", ""))
        self.chance_level.setText(info.get("Chance Level", ""))
        self.method.setCurrentText(info.get("Method", ""))
        self.minimum.setText(info.get("Minimum Test Value", ""))
        self.maximum.setText(info.get("Maximum Test Value", ""))
        self.is_log10_transform.setCurrentText(info.get("Is Log10 Transform", ""))

    def changeName(self, name: str):
        self.device_name.setText(name)

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Threshold Value": self.estimated_threshold.text(),
            "Std. Dev.": self.std_dev.text(),
            "Desired Proportion": self.desired_proportion.text(),
            "Steepness": self.steepness.text(),
            "Proportion": self.proportion.text(),
            "Chance Level": self.chance_level.text(),
            "Method": self.method.currentText(),
            "Minimum Test Value": self.minimum.text(),
            "Maximum Test Value": self.maximum.text(),
            "Is Log10 Transform": self.is_log10_transform.currentText()
        }
        return properties
