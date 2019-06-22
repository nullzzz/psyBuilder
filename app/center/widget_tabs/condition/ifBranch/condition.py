from PyQt5.QtWidgets import QFormLayout, QLabel, QWidget

from app.center.widget_tabs.condition.ifBranch.eachCondition import EachCondition


class ConditionArea(QWidget):
    """
    properties:
    {
        "condition 0":  {
                            "op": "and",
                            "var": "",
                            "compare": ">"
                            "var varlue": ""
                            }
        "condition 1": ...
    }
    """
    MAX_CONDITION_COUNT = 6

    def __init__(self, parent=None):
        super(ConditionArea, self).__init__(parent)

        self.default_properties: dict = {}
        self.default_condition = EachCondition()

        self.default_condition.op = QLabel()
        self.default_condition.op.setFixedWidth(100)
        self.default_condition.del_bt = QLabel()
        self.default_condition.del_bt.setFixedWidth(self.default_condition.add_bt.width())
        self.default_condition.add_bt.clicked.connect(self.addCondition)

        self.conditions = [self.default_condition]
        #
        self.form_layout = QFormLayout(self)
        self.form_layout.addRow(self.default_condition.getLayout())
        self.setLayout(self.form_layout)

    def addCondition(self):
        index = self.getAddButtonIndex(self.sender())
        if index != -1:

            a_condition = EachCondition()
            a_condition.add_bt.clicked.connect(self.addCondition)
            a_condition.del_bt.clicked.connect(self.delCondition)

            self.form_layout.insertRow(index + 1, a_condition.getLayout())
            self.conditions.insert(index + 1, a_condition)
            if len(self.conditions) == ConditionArea.MAX_CONDITION_COUNT:
                for c in self.conditions:
                    c.add_bt.setDisabled(True)

    def delCondition(self):
        index = self.getDeleteButtonIndex(self.sender())
        if index != -1:
            self.conditions.pop(index)
            self.form_layout.removeRow(index)
            # 修改按钮状态
            if len(self.conditions) == ConditionArea.MAX_CONDITION_COUNT - 1:
                for c in self.conditions:
                    c.add_bt.setDisabled(False)

    # todo 不优雅的，有空改掉
    def getAddButtonIndex(self, add_button):
        for i, v in enumerate(self.conditions):
            if add_button == v.add_bt:
                return i
        return -1

    def getDeleteButtonIndex(self, del_bt):
        for i, v in enumerate(self.conditions):
            if del_bt is v.del_bt:
                return i
        return -1

    # 复制
    def clone(self):
        clone_condition = ConditionArea()
        for c in self.conditions:
            clone_condition.conditions.append(c.clone())
        for c in clone_condition.conditions[1:]:
            c.add_bt.clicked.connect(clone_condition.addCondition)
            c.del_bt.clicked.connect(clone_condition.delCondition)
            clone_condition.form_layout.addRow(c.getLayout())
        return clone_condition

    def getInfo(self):
        self.default_properties.clear()
        for i, c in enumerate(self.conditions):
            self.default_properties[f"condition {i}"] = c.getInfo()
        return self.default_properties

    def loadSetting(self):
        """parents' loadSetting means children' setProperties"""
        # todo 待测试
        old_cnt = len(self.default_properties)
        new_cnt = len(self.conditions)
        if old_cnt > new_cnt:
            for i in range(old_cnt - new_cnt):
                a_condition = EachCondition()
                a_condition.add_bt.clicked.connect(self.addCondition)
                a_condition.del_bt.clicked.connect(self.delCondition)
                self.form_layout.addRow(a_condition.getLayout())
                self.conditions.append(a_condition)
        else:
            for i in range(new_cnt - 1, old_cnt - 1, -1):
                self.conditions.pop()
                self.form_layout.removeRow(i)
        for i, c in enumerate(self.conditions):
            c.setProperties(self.default_properties.get(f"condition {i}", {}))

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def setAttributes(self, attributes: list):
        for c in self.conditions:
            c.setAttributes(attributes)

    def getCondition(self) -> str:
        return "".join(condition.getCondition() for condition in self.conditions)
