from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout

from app.func import Func
from app.info import Info
from lib import TabItemWidget
from .caseArea import CaseArea
from .condition import SwitchCondition


class Switch(TabItemWidget):
    """
    {
        "switch": ""
        "case": {}
    """
    tabClose = pyqtSignal(str)
    propertiesChange = pyqtSignal(dict)

    itemAdded = pyqtSignal(str, str, str, int)
    itemDeleted = pyqtSignal(str)
    itemNameChanged = pyqtSignal(int, str, str)

    def __init__(self, widget_id: str, widget_name: str):
        super(Switch, self).__init__(widget_id, widget_name)
        #
        self.using_attributes: list = []
        #
        self.switch_area = SwitchCondition()
        self.case_area = CaseArea(self)

        self.case_area.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b, 0))
        self.case_area.itemDeleted.connect(lambda a: self.itemDeleted.emit(a))
        self.case_area.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(Info.SwitchSend, a, b))

        self.default_properties: dict = {
            "Switch": self.switch_area.getProperties(),
            "Case": self.case_area.getProperties()
        }

        self.ok_bt = QPushButton("OK")
        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt = QPushButton("Cancel")
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt = QPushButton("Apply")
        self.apply_bt.clicked.connect(self.apply)

        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

        self.setUI()

    def setUI(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.ok_bt)
        buttons_layout.addWidget(self.cancel_bt)
        buttons_layout.addWidget(self.apply_bt)

        layout = QVBoxLayout()
        layout.addWidget(self.switch_area, 1)
        layout.addWidget(self.case_area, 20)
        layout.addLayout(buttons_layout, 1)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.getProperties()
        self.propertiesChanged.emit(self.widget_id)
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.getInfo()

    def getInfo(self):
        return self.getProperties()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.switch_area.setProperties(self.default_properties.get("Switch", ""))
        self.case_area.setProperties(self.default_properties.get("Case", {}))

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

    def setAttributes(self, attributes: list):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.attributes = attributes
        self.switch_area.setAttributes(format_attributes)
        self.case_area.setAttributes(format_attributes)

    def getSwitch(self) -> str:
        return self.default_properties.get("Switch", "")

    def getCasesInfo(self) -> list:
        """
        :return: [case1, case2, ...]
        case1: dict
        """
        return self.default_properties.get("Case", "")

    def getCases(self):
        return [case.getCase() for case in self.case_area.case_list]

    def getSubWidgetId(self):
        sub_wid = []
        for c in self.case_area.case_list:
            sub_wid.append(c.widget_id)
        return sub_wid

    """
    Functions that must be complete in new version
    """

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        self.default_properties["Switch"] = self.switch_area.getProperties()
        self.default_properties["Case"] = self.case_area.getProperties()
        return self.default_properties

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.getInfo()

    def restore(self, properties):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def clone(self, new_widget_id: str, new_widget_name):
        clone_widget = Switch(new_widget_id, widget_name)
        clone_widget.setProperties(self.default_properties)
        return clone_widget
