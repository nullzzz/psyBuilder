from PyQt5.QtWidgets import QWidget, QFormLayout

from app.lib import PigComboBox


# slider专属页面
class SliderTab1(QWidget):
    def __init__(self, parent=None):
        super(SliderTab1, self).__init__(parent)

        # 当前可使用attribute
        self.attributes = []
        # 当前页面属性
        self.default_properties = {
            "Clear after": "Yes",
            "Screen name": "Display"
        }

        self.screen_name = PigComboBox()
        self.clear_after = PigComboBox()
        self.clear_after.addItems(("Yes", "No"))

        self.setGeneral()

    def setGeneral(self):
        layout = QFormLayout()
        layout.addRow("Screen Name:", self.screen_name)
        layout.addRow("Clear After:", self.clear_after)

        self.setLayout(layout)

    def setAttributes(self, attributes):
        self.attributes = attributes
        # self.screen_name.setCompleter(QCompleter(self.attributes))

    def setScreen(self, screen: list):
        selected = self.screen_name.currentText()
        self.screen_name.clear()
        self.screen_name.addItems(screen)
        if selected in screen:
            self.screen_name.setCurrentText(selected)

    def getInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties["Clear after"] = self.clear_after.currentText()
        self.default_properties["Screen name"] = self.screen_name.currentText()
        return self.default_properties

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        self.default_properties["Screen name"] = self.screen_name.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.screen_name.setCurrentText(self.default_properties["Screen name"])

    def clone(self):
        clone_page = SliderTab1()
        clone_page.setProperties(self.default_properties)
        return clone_page
