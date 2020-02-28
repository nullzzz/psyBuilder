from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication

from app.func import Func
from lib import TabItemWidget
from .condition import ConditionArea
from ..iconChoose import IconChoose


class IfBranch(TabItemWidget):
    """
    {
        "Condition": "",
        "Yes": "",
        "No": ""
    }

    """

    itemAdded = pyqtSignal(str, str, str)
    itemDeleted = pyqtSignal(str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, widget_id: str, widget_name: str):
        super(IfBranch, self).__init__(widget_id, widget_name)

        self.attributes: list = []
        self.using_attributes: list = []

        # 条件
        self.condition_area = ConditionArea()
        # 事件

        self.true_icon_choose = IconChoose()
        self.true_icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b))
        self.true_icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(a))
        self.true_icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.false_icon_choose = IconChoose()
        self.false_icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(self.widget_id, a, b))
        self.false_icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(a))
        self.false_icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.default_properties = {
            "Condition": self.condition_area.getInfo(),
            "Yes": self.true_icon_choose.getInfo(),
            "No": self.false_icon_choose.getInfo()
        }

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.ok)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply)

        self.setAttributes(Func.getAttributes(self.widget_id))

        self.setUI()

    def setUI(self):
        condition_group = QGroupBox("Condition")
        layout1 = QVBoxLayout()
        layout1.addWidget(self.condition_area)
        condition_group.setLayout(layout1)

        true_group = QGroupBox("Yes")
        layout2 = QVBoxLayout()
        layout2.addWidget(self.true_icon_choose)
        true_group.setLayout(layout2)

        false_group = QGroupBox("No")
        layout3 = QVBoxLayout()
        layout3.addWidget(self.false_icon_choose)
        false_group.setLayout(layout3)

        buttons_layout = QHBoxLayout()

        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(condition_group, 1)
        tf_layout = QHBoxLayout()
        tf_layout.addWidget(true_group)
        tf_layout.addWidget(false_group)
        layout.addLayout(tf_layout, 20)
        layout.addLayout(buttons_layout, 1)
        self.setLayout(layout)

    def getInfo(self):
        self.default_properties["Condition"] = self.condition_area.getInfo()
        self.default_properties["Yes"] = self.true_icon_choose.getInfo()
        self.default_properties["No"] = self.false_icon_choose.getInfo()
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.getInfo()
        self.propertiesChanged.emit(self.widget_id)
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.condition_area.setProperties(self.default_properties.get("Condition", {}))
        self.true_icon_choose.setProperties(self.default_properties.get("Yes", {}))
        self.false_icon_choose.setProperties(self.default_properties.get("No", {}))

    def clone(self, new_id: str):
        clone_widget = IfBranch(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.condition_area.setAttributes(format_attributes)
        self.true_icon_choose.setAttributes(format_attributes)
        self.false_icon_choose.setAttributes(format_attributes)

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {"onsettime": 0, "acc": 0, "resp": 0, "rt": 0}
        return hidden_attr

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

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

    def getCondition(self) -> str:
        """
        返回判断条件
        :return:
        """
        return self.condition_area.getCondition()

    def getTrueWidgetInfo(self) -> dict:
        """
        获取信息，包括Event name等
        :return:
        """
        return self.true_icon_choose.getInfo()

    def getTrueWidget(self):
        return self.true_icon_choose.getWidget()

    def getFalseWidgetInfo(self) -> dict:
        return self.false_icon_choose.getInfo()

    def getFalseWidget(self):
        return self.false_icon_choose.getWidget()

    def getSubWidgetId(self):
        return self.true_icon_choose.widget_id, self.false_icon_choose.widget_id


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    pro = IfBranch()

    pro.show()

    sys.exit(app.exec())
