from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QVBoxLayout, QHBoxLayout, QApplication

from app.center.widget_tabs.condition.iconChoose import IconChoose
from app.center.widget_tabs.condition.ifBranch.condition import ConditionArea
from app.func import Func


class IfBranch(QWidget):
    """
    {
        "Condition": "",
        "True": "",
        "False": ""
    }

    """
    tabClose = pyqtSignal(str)
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, widget_id: str = ''):
        super(IfBranch, self).__init__(parent)

        self.widget_id = widget_id
        self.current_wid = widget_id

        self.attributes: list = []
        self.using_attributes: list = []

        # 条件
        self.condition_area = ConditionArea()
        # 事件
        self.true_icon_choose = IconChoose()
        self.false_icon_choose = IconChoose()

        self.default_properties = {
            "Condition": self.condition_area.getInfo(),
            "True": self.true_icon_choose.getInfo(),
            "False": self.false_icon_choose.getInfo()
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

        true_group = QGroupBox("True")
        layout2 = QVBoxLayout()
        layout2.addWidget(self.true_icon_choose)
        true_group.setLayout(layout2)

        false_group = QGroupBox("False")
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
        self.default_properties["True"] = self.true_icon_choose.getInfo()
        self.default_properties["False"] = self.false_icon_choose.getInfo()
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
        self.propertiesChange.emit(self.default_properties)
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

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
        self.true_icon_choose.setProperties(self.default_properties.get("True", {}))
        self.false_icon_choose.setProperties(self.default_properties.get("False", {}))

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

    def getTrueWidget(self) -> dict:
        return {
            "stim type": self.true_icon_choose.getInfo().get("stim type", "None"),
            "event name": self.true_icon_choose.getInfo().get("event name", ""),
            "widget": self.true_icon_choose.getWidget(),
            "widget_id": self.true_icon_choose.getWidgetId()
        }

    def getFalseWidget(self) -> dict:
        return {
            "stim type": self.false_icon_choose.getInfo().get("stim type", "None"),
            "event name": self.false_icon_choose.getInfo().get("event name", ""),
            "widget": self.false_icon_choose.getWidget(),
            "widget id": self.false_icon_choose.getWidgetId()
        }


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    pro = IfBranch()

    pro.show()

    sys.exit(app.exec())
