from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel

from app.lib import QLineEdit, QComboBox


class Describer(QWidget):
    estimatedThresholdChanged = pyqtSignal(str)
    stdDevChanged = pyqtSignal(str)
    desiredProportionChanged = pyqtSignal(str)
    steepnessChanged = pyqtSignal(str)
    proportionChanged = pyqtSignal(str)
    chanceLevelChanged = pyqtSignal(str)
    methodChanged = pyqtSignal(str)
    minimumChanged = pyqtSignal(str)
    maximumChanged = pyqtSignal(str)
    isTransformChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Describer, self).__init__(parent)

        self.quest_name = QLabel()
        self.estimated_threshold = QLineEdit()
        self.estimated_threshold.setToolTip("Used For Starting Test Value")
        self.estimated_threshold.textChanged.connect(lambda x: self.estimatedThresholdChanged.emit(x))

        self.std_dev = QLineEdit()
        self.std_dev.setToolTip("Of Estimated Threshold")
        self.std_dev.textChanged.connect(lambda x: self.stdDevChanged.emit(x))

        self.desired_proportion = QLineEdit()
        self.desired_proportion.setToolTip("Of Correct Responses")
        self.desired_proportion.textChanged.connect(lambda x: self.desiredProportionChanged.emit(x))

        self.steepness = QLineEdit()
        self.steepness.setToolTip("Of The Weibull Psychometric Function")
        self.steepness.textChanged.connect(lambda x: self.steepnessChanged.emit(x))

        self.proportion = QLineEdit()
        self.proportion.setToolTip("Of Random Responses At Maximum Stimulus Intensity")
        self.proportion.textChanged.connect(lambda x: self.proportionChanged.emit(x))

        self.chance_level = QLineEdit()
        self.chance_level.textChanged.connect(lambda x: self.chanceLevelChanged.emit(x))

        self.method = QComboBox()
        self.method.addItems(("quantile", "mean", "mode"))
        self.method.setToolTip("To Determine Optimal Test Value")
        self.method.currentTextChanged.connect(lambda x: self.methodChanged.emit(x))

        self.minimum = QLineEdit()
        self.minimum.textChanged.connect(lambda x: self.minimumChanged.emit(x))
        self.maximum = QLineEdit()
        self.maximum.textChanged.connect(lambda x: self.maximumChanged.emit(x))
        self.is_log10_transform = QComboBox()
        self.is_log10_transform.addItems(("yes", "no"))
        self.is_log10_transform.currentTextChanged.connect(lambda x: self.isTransformChanged.emit(x))

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Quest Name:", self.quest_name)
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

    def describe(self, quest_name, **kwargs):
        self.quest_name.setText(quest_name)
        self.estimated_threshold.setText(kwargs.get("Estimated threshold", ""))
        self.std_dev.setText(kwargs.get("Std dev", ""))
        self.desired_proportion.setText(kwargs.get("Desired proportion", ""))
        self.steepness.setText(kwargs.get("Steepness", ""))
        self.proportion.setText(kwargs.get("Proportion", ""))
        self.chance_level.setText(kwargs.get("Chance level", ""))
        self.method.setCurrentText(kwargs.get("Method", ""))
        self.minimum.setText(kwargs.get("Minimum", ""))
        self.maximum.setText(kwargs.get("Maximum", ""))
        self.is_log10_transform.setCurrentText(kwargs.get("Is log10 transform", ""))

    def changeName(self, name: str):
        self.quest_name.setText(name)

    def getInfo(self):
        self.default_properties["Quest Name"] = self.quest_name.text()
        # self.default_properties["Device Type"] = "quest"
        self.default_properties["Estimated threshold"] = self.estimated_threshold.text()
        self.default_properties["Std dev"] = self.std_dev.text()
        self.default_properties["Desired proportion"] = self.desired_proportion.text()
        self.default_properties["Steepness"] = self.steepness.text()
        self.default_properties["Proportion"] = self.proportion.text()
        self.default_properties["Chance level"] = self.chance_level.text()
        self.default_properties["Method"] = self.method.currentText()
        self.default_properties["Minimum"] = self.minimum.text()
        self.default_properties["Maximum"] = self.maximum.text()
        self.default_properties["Is log10 transform"] = self.is_log10_transform.currentText()
        return self.default_properties

    def loadSetting(self):
        self.quest_name.setText(self.quest_name["Quest Name"])
        self.estimated_threshold.setText(self.default_properties["Estimated threshold"])
        self.std_dev.setText(self.default_properties["Std dev"])
        self.desired_proportion.setText(self.default_properties["Desired proportion"])
        self.steepness.setText(self.default_properties["Steepness"])
        self.proportion.setText(self.default_properties["Proportion"])
        self.chance_level.setText(self.default_properties["Chance level"])
        self.method.setCurrentText(self.default_properties["Method"])
        self.minimum.setText(self.default_properties["Minimum"])
        self.maximum.setText(self.default_properties["Maximum"])
        self.is_log10_transform.setCurrentText(self.default_properties["Is log10 transform"])
