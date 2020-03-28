from app.newDevice.device import Device


class Quest(Device):
    def __init__(self, device_type: str = "quest", device_id: str = None, parent=None):
        super(Quest, self).__init__(device_type, device_id, parent)
        self.device_type = device_type

        self.quest_id: str = device_id
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
        self.setName(self.default_properties["Device Name"])
        self.estimated_threshold = self.default_properties["Threshold Value"]
        self.std_dev = self.default_properties["Std. Dev."]
        self.desired_proportion = self.default_properties["Desired Proportion"]
        self.steepness = self.default_properties["Steepness"]
        self.proportion = self.default_properties["Proportion"]
        self.chance_level = self.default_properties["Chance Level"]
        self.method = self.default_properties["Method"]
        self.minimum = self.default_properties["Minimum Test Value"]
        self.maximum = self.default_properties["Maximum Test Value"]
        self.is_log10_transform = self.default_properties["Is Log10 Transform"]

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Device Type"] = self.device_type
        self.default_properties["Device Name"] = self.text()
        self.default_properties["Threshold Value"] = self.estimated_threshold
        self.default_properties["Std. Dev."] = self.std_dev
        self.default_properties["Desired Proportion"] = self.desired_proportion
        self.default_properties["Steepness"] = self.steepness
        self.default_properties["Proportion"] = self.proportion
        self.default_properties["Chance Level"] = self.chance_level
        self.default_properties["Method"] = self.method
        self.default_properties["Minimum Test Value"] = self.minimum
        self.default_properties["Maximum Test Value"] = self.maximum
        self.default_properties["Is Log10 Transform"] = self.is_log10_transform
        return self.default_properties
