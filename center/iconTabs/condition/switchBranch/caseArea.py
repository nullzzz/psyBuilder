from PyQt5.QtWidgets import QComboBox, QLabel, QGridLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal

from .case import Case
import copy


class CaseArea(QScrollArea):
    MAX_CASE_COUNT = 9
    caseAdd = pyqtSignal(Case)

    def __init__(self, parent=None):
        super(CaseArea, self).__init__(parent)

        # data
        self.switch_value = ''
        self.cases = []
        # case_num, [case{case title, case value, case icon value, case name}]
        self.case_data_backup = {}
        case_1 = Case(title='Case 1', can_add=True, can_delete=False)
        case_2 = Case(title='Case 2', can_add=True, can_delete=False)
        case_3 = Case(title='Otherwise', can_add=False, can_delete=False)
        self.linkCaseSignals(case_1)
        self.linkCaseSignals(case_2)
        self.linkCaseSignals(case_3)
        self.cases.append(case_1)
        self.cases.append(case_2)
        self.cases.append(case_3)
        self.switch = QComboBox()

        self.grid_layout = QGridLayout()

        self.label = QLabel("Switch:")
        self.label.setAlignment(Qt.AlignRight)
        self.grid_layout.addWidget(self.label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.switch, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.cases[0], 1, 0, 1, 1)
        self.grid_layout.addWidget(self.cases[1], 1, 1, 1, 1)
        self.grid_layout.addWidget(self.cases[2], 1, 2, 1, 1)

        self.widget = QWidget()
        self.widget.setLayout(self.grid_layout)

        self.setWidget(self.widget)
        self.setWidgetResizable(True)

    def linkCaseSignals(self, case: Case):
        case.add_button.clicked.connect(self.insertCase)
        case.delete_button.clicked.connect(self.deleteCase)

    def insertCase(self):
        try:
            index = self.getIndex(self.sender())
            if index != -1:
                add_index = index + 1
                row = add_index // 3 + 1
                col = add_index % 3
                # 不存在添加到末尾，因为末尾必定是default，而default设置为不可添加，对于其后面的case往后移动
                # 必须倒序了
                for i in range(len(self.cases), add_index, -1):
                    self.setCase(i, self.cases[i - 1])
                # 放入新case
                new_case = Case(title=f"Case {add_index + 1}", can_add=True, can_delete=True)
                self.linkCaseSignals(new_case)
                self.caseAdd.emit(new_case)
                self.cases.insert(add_index, new_case)
                if len(self.cases) > 3:
                    for case in self.cases:
                        case.delete_button.setDisabled(False)
                if len(self.cases) == CaseArea.MAX_CASE_COUNT:
                    for case in self.cases:
                        case.add_button.setDisabled(True)
                self.grid_layout.addWidget(new_case, row, col, 1, 1)
                # default case
                self.cases[-1].setTitle('Otherwise')
                self.cases[-1].add_button.setDisabled(True)
                self.cases[-1].delete_button.setDisabled(True)
                self.update()
                self.repaint()

        except Exception as e:
            print(f"error {e} happens in insert case. [switch/caseArea.py]")

    def deleteCase(self):
        try:
            index = self.getIndex(self.sender())
            if index != -1:
                self.grid_layout.removeWidget(self.cases[index])
                self.cases[index].hide()
                self.update()
                # 依次往前移动
                for i in range(index, len(self.cases) - 1):
                    row = i // 3 + 1
                    col = i % 3
                    old_case = self.cases[i + 1]
                    self.grid_layout.removeWidget(old_case)
                    # 设置在新的位置
                    self.grid_layout.addWidget(old_case, row, col, 1, 1)
                # 按钮状态变化
                self.cases.pop(index)
                for i in range(len(self.cases)):
                    self.cases[i].setTitle(f"Case {i + 1}")
                if len(self.cases) == 3:
                    for case in self.cases:
                        case.setDeleteDisabled(True)
                if len(self.cases) == 8:
                    for case in self.cases:
                        case.setAddDisabled(False)
                # default case
                self.cases[-1].setTitle('Otherwise')
                self.cases[-1].add_button.setDisabled(True)
                self.cases[-1].delete_button.setDisabled(True)
                self.update()
                self.repaint()
            else:
                print("invalid delete.")
        except Exception as e:
            print(f"error {e} happens in delete case. [switch/caseArea.py]")

    def setCase(self, index, case: Case):
        # 擦掉原来位置上的case
        self.grid_layout.removeWidget(case)
        # 要根据case改名字
        case.setTitle(f"Case {index + 1}")
        row = index // 3 + 1
        col = index % 3
        self.grid_layout.addWidget(case, row, col, 1, 1)

    def getIndex(self, btn):
        for i in range(len(self.cases)):
            if btn in (self.cases[i].add_button, self.cases[i].delete_button):
                return i
        return -1

    def backup(self):
        self.case_data_backup['case'] = []
        for case in self.cases:
            case_data = {}
            case_data['case_title'] = case.title()
            # case_data['case_value'] = case.case_comBox.currentText()
            case_data['case_icon_value'] = case.icon_choose.icon.value
            case_data['case_icon_name'] = case.icon_choose.icon_name.text()
            case_data['can_add'] = case.canAdd()
            case_data['can_delete'] = case.canDelete()
            self.case_data_backup['case'].append(case_data)

    def restore(self):
        # 先删除所有case
        for case in self.cases:
            self.grid_layout.removeWidget(case)
            case.hide()
            self.widget.update()
        self.cases.clear()
        # 增加新case
        cases = self.case_data_backup['case']
        for index in range(len(cases)):
            case = Case(title=cases[index]['case_title'], parent=None, can_add=cases[index]['can_add'],
                        can_delete=cases[index]['can_delete'])

            case.icon_choose.icon_comboBox.setCurrentText(cases[index]['case_icon_value'].split('.')[0])
            case.icon_choose.icon.changeValue(cases[index]['case_icon_value'])
            case.icon_choose.icon_name.setText(cases[index]['case_icon_name'])
            self.cases.append(case)
            row = index // 3 + 1
            col = index % 3
            self.grid_layout.addWidget(case, row, col, 1, 1)

