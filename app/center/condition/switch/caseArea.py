from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QWidget, QScrollArea

from app.center.condition.switch.case import Case
from app.func import Func


class CaseArea(QScrollArea):
    """
    {
        "case 1": ...,
        "case 2": ...,
        ...
        "Default": ...
        }
    """
    MAX_CASE_COUNT = 9
    MIN_CASE_COUNT = 3

    itemAdded = pyqtSignal(str, str)
    itemDeleted = pyqtSignal(str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(CaseArea, self).__init__(parent)

        self.attributes: list = []

        self.case_0 = Case(title='Default')

        self.case_list: list = [Case(title='Case 1'), Case(title='Case 2'), self.case_0]
        self.case_list[0].addCase.connect(self.insertCase)
        self.case_list[1].addCase.connect(self.insertCase)
        self.case_list[0].delCase.connect(self.delCase)
        self.case_list[1].delCase.connect(self.delCase)

        self.default_properties: dict = {
            "Default": self.case_0.getProperties(),
            "Case 1": self.case_list[0].getProperties(),
            "Case 2": self.case_list[1].getProperties()
        }
        for c in self.case_list:
            c.icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(a, b))
            c.icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(a))
            c.icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.setUI()

    def setUI(self):
        self.layout = QGridLayout()
        self.layout.addWidget(self.case_list[0], 0, 0)
        self.layout.addWidget(self.case_list[1], 0, 1)
        self.layout.addWidget(self.case_0, 0, 2)
        self.whiteboard = QWidget()
        self.whiteboard.setLayout(self.layout)
        self.setWidget(self.whiteboard)
        self.setWidgetResizable(True)

    def insertCase(self, index):
        # 更新case的index
        for case in self.case_list[index:-1]:
            case.updateIndex(1)
            self.layout.removeWidget(case)

        self.layout.removeWidget(self.case_0)
        new_case = Case(f"Case {index + 1}")
        new_case.setAttributes(self.attributes)
        new_case.addCase.connect(self.insertCase)
        new_case.delCase.connect(self.delCase)

        new_case.icon_choose.itemAdded.connect(lambda a, b: self.itemAdded.emit(a, b))
        new_case.icon_choose.itemDeleted.connect(lambda a: self.itemDeleted.emit(a))
        new_case.icon_choose.itemNameChanged.connect(lambda a, b: self.itemNameChanged.emit(a, b))

        self.case_list.insert(index, new_case)
        for case in self.case_list[index:-1]:
            self.addCase(case)
        cnt = len(self.case_list)
        self.layout.addWidget(self.case_0, (cnt - 1) // 3, (cnt - 1) % 3)
        self.noAdd(cnt >= CaseArea.MAX_CASE_COUNT)
        self.noDel(cnt <= CaseArea.MIN_CASE_COUNT)
        self.update()
        self.repaint()

    def delCase(self, index):
        del_case: Case = self.case_list.pop(index - 1)
        self.layout.removeWidget(del_case)
        del_case.hide()
        for case in self.case_list[index - 1:-1]:
            case.updateIndex(-1)
            self.layout.removeWidget(case)
        self.layout.removeWidget(self.case_0)
        for case in self.case_list[index - 1:-1]:
            self.addCase(case)
        cnt = len(self.case_list)
        self.layout.addWidget(self.case_0, (cnt - 1) // 3, (cnt - 1) % 3)
        self.noAdd(cnt >= CaseArea.MAX_CASE_COUNT)
        self.noDel(cnt <= CaseArea.MIN_CASE_COUNT)
        self.update()
        self.repaint()

        del_widget_id = del_case.widget_id
        if del_widget_id != "":
            # 发送给ly删掉wid_node
            self.itemDeleted.emit(del_widget_id)
            # 删掉wid_widget
            Func.delWidget(del_widget_id)

    def addCase(self, case: Case):
        index = case.index
        row = (index - 1) // 3
        col = (index - 1) % 3
        self.layout.addWidget(case, row, col)

    def noAdd(self, no=True):
        for case in self.case_list:
            case.setNotAdd(no)

    def noDel(self, no=True):
        """
        :param no: T=
        :return:
        """
        for case in self.case_list:
            case.setNotDel(no)

    def getProperties(self):
        self.default_properties.clear()
        for case in self.case_list:
            self.default_properties[case.title()] = case.getProperties()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        old_cnt = len(self.default_properties)
        new_cnt = len(self.case_list)
        if old_cnt > new_cnt:
            for i in range(old_cnt - new_cnt):
                self.insertCase(new_cnt + i - 1)
        else:
            for i in range(new_cnt - old_cnt):
                self.delCase(old_cnt - 1)
        for case in self.case_list:
            case.setProperties(self.default_properties.get(case.title(), {}))

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        for case in self.case_list:
            case.setAttributes(self.attributes)

    def clone(self):
        clone_case_area = CaseArea()
        clone_case_area.setProperties(self.default_properties)
        return clone_case_area
