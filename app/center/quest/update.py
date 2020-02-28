from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout

from app.func import Func
from lib import VarComboBox, MessageBox, TabItemWidget


class QuestUpdate(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(QuestUpdate, self).__init__(widget_id, widget_name)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.attributes = []
        self.default_properties = {"Is correct": "1"}
        self.response_variable = VarComboBox()
        self.response_variable.addItems(["1", "0"])

        self.quest_info = Func.getQuestInfo()
        self.quest_name = VarComboBox()
        self.quest_name.currentTextChanged.connect(self.changeQuestId)

        self.using_quest_id = ""

        self.resp = ""
        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(Func.getAttributes(self.widget_id))

    def changeQuestId(self, quest_name):
        for k, v in self.quest_info.items():
            if v == quest_name:
                self.using_quest_id = k
                break

    def setUI(self):
        self.setWindowTitle("Update")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("QUEST staircase next")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Updates the Quest test value based on a response")

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Is correct:"), 2, 0, 1, 1)
        layout1.addWidget(self.response_variable, 2, 1, 1, 1)
        layout1.addWidget(QLabel("Quest Name:"), 3, 0, 1, 1)
        layout1.addWidget(self.quest_name, 3, 1, 1, 1)

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
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def refresh(self):
        self.quest_info = Func.getQuestInfo()
        quest_id = self.using_quest_id

        self.quest_name.clear()
        self.quest_name.addItems(self.quest_info.values())
        quest_name = self.quest_info.get(quest_id)
        if quest_name:
            self.quest_name.setCurrentText(quest_name)
            self.using_quest_id = quest_id

        # 更新attributes
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.getInfo()

    def apply(self):
        self.resp = self.response_variable.currentText()
        self.propertiesChanged.emit(self.widget_id)

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
                MessageBox.warning(self, "Warning", "Invalid Attribute!", MessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        # self.response_variable.setCompleter(QCompleter(self.attributes))

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
        self.default_properties.clear()
        self.default_properties["Is correct"] = self.response_variable.currentText()
        self.default_properties["Quest name"] = self.quest_name.currentText()
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
        self.response_variable.setCurrentText(self.default_properties["Is correct"])
        self.quest_name.setCurrentText(self.default_properties["Quest name"])

    def clone(self, new_id: str):
        clone_widget = QuestUpdate(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {}
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

    def getResponseVariable(self) -> str:
        return self.response_variable.currentText()

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)
