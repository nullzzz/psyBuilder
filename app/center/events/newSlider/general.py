from PyQt5.QtWidgets import QWidget, QFormLayout

from app.func import Func
from lib import VarComboBox


# slider专属页面
class SliderGeneral(QWidget):
    def __init__(self, parent=None):
        super(SliderGeneral, self).__init__(parent)

        # 当前可使用attribute
        self.attributes = []
        # 当前页面属性
        self.default_properties = {
            "Clear after": "Yes",
            "Screen name": "screen.0"
        }

        self.clear_after = VarComboBox()
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        self.using_screen_id: str = "screen.0"
        self.screen_name = VarComboBox()
        self.screen_info = Func.getScreenInfo()
        self.screen_name.addItems(self.screen_info.values())
        self.screen_name.currentTextChanged.connect(self.changeScreen)

        self.setGeneral()

    def setGeneral(self):
        layout = QFormLayout()
        layout.addRow("Screen Name:", self.screen_name)
        layout.addRow("Dont Clear After:", self.clear_after)

        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getScreenInfo()
        screen_id = self.using_screen_id
        self.screen_name.clear()
        self.screen_name.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen_name.setCurrentText(screen_name)
            self.using_screen_id = screen_id

    def setAttributes(self, attributes):
        self.attributes = attributes

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    def getInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties.clear()
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
        clone_page = SliderGeneral()
        clone_page.setProperties(self.default_properties)
        return clone_page
