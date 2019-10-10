from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QGroupBox, QCompleter

from app.center.widget_tabs.condition.addDeleteButton import AddDeleteButton
from app.center.widget_tabs.condition.iconChoose import IconChoose
from app.lib import PigComboBox
from lib.psy_message_box import PsyMessageBox as QMessageBox


class Case(QGroupBox):
    """
    {
        "case value" : "",
        "stim type": "Image",
        "event name": "",
        "pro window": {}
    }
    """
    add = pyqtSignal()
    delCase = pyqtSignal(int)
    addCase = pyqtSignal(int)

    def __init__(self, title: str = "test", parent=None):
        super(Case, self).__init__(title, parent)

        self.index = 0
        for c in title[::-1]:
            if c.isdigit():
                self.index = int(c)
                break

        # case的值
        self.value: str = ""

        self.attributes: list = []

        # case
        self.values = PigComboBox()
        self.values.setEditable(True)
        self.values.setInsertPolicy(QComboBox.NoInsert)
        self.values.currentTextChanged.connect(self.changeValue)
        # icon choose
        self.icon_choose = IconChoose(self)

        self.default_properties: dict = self.icon_choose.getInfo().copy()
        self.default_properties["Case value"] = self.value

        self.add_bt = AddDeleteButton(self, "add")
        self.add_bt.clicked.connect(lambda: self.addCase.emit(self.index))
        self.del_bt = AddDeleteButton(self, "delete")
        self.del_bt.clicked.connect(lambda: self.delCase.emit(self.index))

        self.grid_layout = QGridLayout(self)
        tip = QLabel("Value:")
        tip.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout.addWidget(tip, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.values, 0, 1, 1, 5)
        self.grid_layout.addWidget(self.icon_choose, 1, 0, 3, 5)
        self.grid_layout.addWidget(self.add_bt, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.del_bt, 4, 3, 1, 1)
        self.setLayout(self.grid_layout)

        self.setMaximumHeight(300)

    # todo 现有布局略丑
    def setUI(self):
        pass

    def setNotAdd(self, no=True):
        self.add_bt.setEnabled(not no)

    def setNotDel(self, no=True):
        self.del_bt.setEnabled(not no)

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties = self.icon_choose.getProperties().copy()
        self.default_properties["Case value"] = self.value
        return self.default_properties

    def changeValue(self, new_value):
        self.value = new_value

    def loadSetting(self):
        self.icon_choose.loadSetting()
        self.values.setCurrentText(self.default_properties.get("Case value", ""))

    # 导入参数
    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.icon_choose.setProperties(self.default_properties)
            self.values.setCurrentText(self.default_properties.get("Case value", ""))
        else:
            print("No properties")

    def clone(self):
        clone_case = Case(self.title())
        clone_case.setProperties(self.default_properties)
        return clone_case

    # 以便在其之前插入新的case
    def changeTitle(self, new_title: str):
        self.setTitle(new_title)
        for c in new_title:
            if c.isdigit():
                self.index = int(c)
                break

    def updateIndex(self, step: int = 1):
        self.index += step
        self.setTitle(f"Case {self.index}")

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.values.addItems(attributes)
        self.values.setCompleter(QCompleter(attributes))

    def getCase(self) -> dict:
        return {
            "Case value": self.default_properties.get("Case value", ""),
            "Stim type": self.default_properties.get("Stim type", "None"),
            "Event name": self.default_properties.get("Event name", ""),
            "Widget": self.icon_choose.getWidget(),
            "Widget id": self.icon_choose.getWidgetId()
        }
