from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, \
    QHBoxLayout, QVBoxLayout, QCompleter

from app.center.events.duration.RM import BiggerDown, BiggerUP
from lib import VarComboBox


class DurationPage(QWidget):
    def __init__(self, parent=None):
        super(DurationPage, self).__init__(parent)

        self.attributes = []
        self.default_properties = {
            "Duration": "1000",
            "Input Devices": {},
            "Output Devices": {}
        }
        # top
        self.duration = VarComboBox()
        self.duration.setReg(r"\(Infinite\)|\d+|\d+~\d+")

        self.up = BiggerUP()
        self.down = BiggerDown()
        self.up.deviceChanged.connect(self.down.updateExternalInfo)
        self.setUI()

    # 生成duration页面
    def setUI(self):
        group0 = QGroupBox()
        self.duration.addItems(("1000", "2000", "3000", "4000", "100~500", "(Infinite)"))
        self.duration.setEditable(True)

        layout0 = QHBoxLayout()
        layout0.addWidget(QLabel("Duration(ms):"), 1)
        layout0.addWidget(self.duration, 4)
        group0.setLayout(layout0)

        layout = QVBoxLayout()
        layout.addWidget(group0, 1)
        layout.addWidget(self.up, 6)
        layout.addWidget(self.down, 6)
        self.setLayout(layout)

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.duration.setCompleter(QCompleter(self.attributes))

    # 返回参数
    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Duration"] = self.duration.currentText()
        self.default_properties["Output Devices"] = self.up.getInfo()
        self.default_properties["Input Devices"] = self.down.getInfo()
        return self.default_properties

    # 设置参数
    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.duration.setCurrentText(self.default_properties["Duration"])

    def clone(self):
        clone_page = DurationPage()
        clone_page.setProperties(self.default_properties)
        return clone_page
