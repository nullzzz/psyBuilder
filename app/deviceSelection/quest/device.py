from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem

from app.func import Func


class Quest(QListWidgetItem):
    def __init__(self, quest_type, quest_id: str = "", parent=None):
        super(Quest, self).__init__(quest_type, parent)

        self.quest_type = quest_type

        self.quest_id: str = quest_id
        self.estimated_threshold = "0.5"
        self.std_dev = "0.25"
        self.desired_proportion = "0.75"
        self.steepness = "3.5"
        self.proportion = "0.01"
        self.chance_level = "0.05"
        self.method = "quantile"
        self.minimum = "0"
        self.maximum = "1"
        self.is_log10_transform = "Yes"

        # 设置图标
        self.setIcon(QIcon(Func.getImagePath("{}_device.png".format(self.quest_type))))

        self.default_properties = {
            "Quest Type": self.quest_type,
            "Quest Name": quest_id,
        }

    def setName(self, name: str):
        self.setText(name)

    def getId(self) -> str:
        return self.quest_id

    def getName(self) -> str:
        return self.text()

    def getType(self) -> str:
        return self.quest_type

    def getThreshold(self) -> str:
        return self.estimated_threshold

    def setThreshold(self, threshold: str):
        self.estimated_threshold = threshold

    def setSD(self, sd: str):
        self.std_dev = sd

    def setDesired(self, desired: str):
        self.desired_proportion = desired

    def setSteep(self, steepness: str):
        self.steepness = steepness

    def setProportion(self, proportion: str):
        self.proportion = proportion

    def setChanceLevel(self, chance_level: str):
        self.chance_level = chance_level

    def setMethod(self, method: str):
        self.method = method

    def setMaximum(self, maximum: str):
        self.maximum = maximum

    def setMinimum(self, minimum: str):
        self.minimum = minimum

    def setIsTransform(self, is_transform: str):
        self.is_log10_transform = is_transform

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.setName(self.default_properties["Quest Name"])
        self.estimated_threshold = self.default_properties["Estimated threshold"]
        self.std_dev = self.default_properties["Std dev"]
        self.desired_proportion = self.default_properties["Desired proportion"]
        self.steepness = self.default_properties["Steepness"]
        self.proportion = self.default_properties["Proportion"]
        self.chance_level = self.default_properties["Chance level"]
        self.method = self.default_properties["Method"]
        self.minimum = self.default_properties["Minimum"]
        self.maximum = self.default_properties["Maximum"]
        self.is_log10_transform = self.default_properties["Is log10 transform"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Quest Name"] = self.text()
        self.default_properties["Quest Type"] = self.quest_type
        self.default_properties["Estimated threshold"] = self.estimated_threshold
        self.default_properties["Std dev"] = self.std_dev
        self.default_properties["Desired proportion"] = self.desired_proportion
        self.default_properties["Steepness"] = self.steepness
        self.default_properties["Proportion"] = self.proportion
        self.default_properties["Chance level"] = self.chance_level
        self.default_properties["Method"] = self.method
        self.default_properties["Minimum"] = self.minimum
        self.default_properties["Maximum"] = self.maximum
        self.default_properties["Is log10 transform"] = self.is_log10_transform
        return self.default_properties
