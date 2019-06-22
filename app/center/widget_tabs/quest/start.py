from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                             QCompleter)

from app.func import Func
from app.lib import PigLineEdit, PigComboBox


class QuestInit(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(QuestInit, self).__init__(parent)
        self.widget_id = widget_id
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)

        self.attributes = []
        self.default_properties = {
            "Estimated threshold": "0.5",
            "Std. dev. of estimated threshold": "0.25",
            "Desired proportion of correct responses": "0.75",
            "Steepness of the Weibull psychometric function(β)": "3.5",
            "Proportion of random responses at maximum stimulus intensity(σ)": "0.01",
            "Chance level (γ)": "0.05",
            "Method to determine optimal test value": "quantile",
            "Minimum test value": "0",
            "Maximum test value": "1",
            "Is log10 transform": "quest test value",
        }

        self.estimated_threshold = PigLineEdit()
        self.std_dev = PigLineEdit()
        self.desired_proportion = PigLineEdit()
        self.steepness = PigLineEdit()
        self.proportion = PigLineEdit()
        self.chance_level = PigLineEdit()
        self.method = PigComboBox()
        self.minimum = PigLineEdit()
        self.maximum = PigLineEdit()
        self.is_log10_transform = PigLineEdit()

        self.estimated_threshold.textChanged.connect(self.findVar)
        self.std_dev.textChanged.connect(self.findVar)
        self.desired_proportion.textChanged.connect(self.findVar)
        self.steepness.textChanged.connect(self.findVar)
        self.proportion.textChanged.connect(self.findVar)
        self.chance_level.textChanged.connect(self.findVar)
        self.minimum.textChanged.connect(self.findVar)
        self.maximum.textChanged.connect(self.findVar)
        self.is_log10_transform.textChanged.connect(self.findVar)

        self.estimated_threshold.returnPressed.connect(self.finalCheck)
        self.std_dev.returnPressed.connect(self.finalCheck)
        self.desired_proportion.returnPressed.connect(self.finalCheck)
        self.steepness.returnPressed.connect(self.finalCheck)
        self.proportion.returnPressed.connect(self.finalCheck)
        self.chance_level.returnPressed.connect(self.finalCheck)
        self.minimum.returnPressed.connect(self.finalCheck)
        self.maximum.returnPressed.connect(self.finalCheck)
        self.is_log10_transform.returnPressed.connect(self.finalCheck)

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(Func.getAttributes(self.widget_id))

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
        self.is_log10_transform.setText("quest test value")

        layout1 = QFormLayout()
        layout1.addRow(self.tip1)
        layout1.addRow(self.tip2)
        layout1.addRow("Estimated Threshold (Used For Starting Test Value):", self.estimated_threshold)
        layout1.addRow("Std. Dev. of Estimated Threshold:", self.std_dev)
        layout1.addRow("Desired Proportion of Correct Responses:", self.desired_proportion)
        layout1.addRow("Steepness of The Weibull Psychometric Function(β):", self.steepness)
        layout1.addRow("Proportion of Random Responses At Maximum Stimulus Intensity(σ):", self.proportion)
        layout1.addRow("Chance Level (γ):", self.chance_level)
        layout1.addRow("Method To Determine Optimal Test Value:", self.method)
        layout1.addRow("Minimum Test Value:", self.minimum)
        layout1.addRow("Maximum Test Value:", self.maximum)
        layout1.addRow("Is Log10 Transform:", self.is_log10_transform)
        layout1.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

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
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.propertiesChange.emit(self.getInfo())
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

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
        self.estimated_threshold.setCompleter(QCompleter(self.attributes))
        self.std_dev.setCompleter(QCompleter(self.attributes))
        self.desired_proportion.setCompleter(QCompleter(self.attributes))
        self.steepness.setCompleter(QCompleter(self.attributes))
        self.proportion.setCompleter(QCompleter(self.attributes))
        self.chance_level.setCompleter(QCompleter(self.attributes))
        self.minimum.setCompleter(QCompleter(self.attributes))
        self.maximum.setCompleter(QCompleter(self.attributes))
        self.is_log10_transform.setCompleter(QCompleter(self.attributes))

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def getInfo(self):
        self.default_properties["Estimated threshold"] = self.estimated_threshold.text()
        self.default_properties["Std. dev. of estimated threshold"] = self.std_dev.text()
        self.default_properties["Desired proportion of correct responses"] = self.desired_proportion.text()
        self.default_properties["Steepness of the Weibull psychometric function(β)"] = self.steepness.text()
        self.default_properties[
            "Proportion of random responses at maximum stimulus intensity(σ)"] = self.proportion.text()
        self.default_properties["Chance level (γ)"] = self.chance_level.text()
        self.default_properties["Method to determine optimal test value"] = self.method.currentText()
        self.default_properties["Minimum test value"] = self.minimum.text()
        self.default_properties["Maximum test value"] = self.maximum.text()
        self.default_properties["Is log10 transform"] = self.is_log10_transform.text()
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print(f"此乱诏也，{self.__class__}不奉命")

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.estimated_threshold.setText(self.default_properties["Estimated threshold"])
        self.std_dev.setText(self.default_properties["Std. dev. of estimated threshold"])
        self.desired_proportion.setText(self.default_properties["Desired proportion of correct responses"])
        self.steepness.setText(self.default_properties["Steepness of the Weibull psychometric function(β)"])
        self.proportion.setText(
            self.default_properties["Proportion of random responses at maximum stimulus intensity(σ)"])
        self.chance_level.setText(self.default_properties["Chance level (γ)"])
        self.method.setCurrentText(self.default_properties["Method to determine optimal test value"])
        self.minimum.setText(self.default_properties["Minimum test value"])
        self.maximum.setText(self.default_properties["Maximum test value"])
        self.is_log10_transform.setText(self.default_properties["Is log10 transform"])

    def clone(self, new_id: str):
        clone_widget = QuestInit(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
        }
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)
