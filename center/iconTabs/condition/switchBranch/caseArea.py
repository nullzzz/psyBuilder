from PyQt5.QtWidgets import QComboBox, QLabel, QGridLayout, QWidget, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal

from .case import Case
from ..varChoose import  VarChoose
import copy


class CaseArea(QScrollArea):
    MAX_CASE_COUNT = 9
    caseAdd = pyqtSignal(Case)

    def __init__(self, parent=None, parent_value=''):
        super(CaseArea, self).__init__(parent)

        # data
        self.parent_value = parent_value
        self.switch_value = ''
        self.cases = []
        self.cases_back_up = []
        # case_num, [case{case title, case value, case icon value, case name}]
        self.case_data_backup = {}

        self.case_1 = Case(title='Case 1', can_add=True, can_delete=False, parent_value=parent_value)
        self.case_2 = Case(title='Case 2', can_add=True, can_delete=False, parent_value=parent_value)
        self.case_3 = Case(title='Otherwise', can_add=False, can_delete=False, parent_value=parent_value)
        self.linkCaseSignals(self.case_1)
        self.linkCaseSignals(self.case_2)
        self.linkCaseSignals(self.case_3)
        self.cases.append(self.case_1)
        self.cases.append(self.case_2)
        self.cases.append(self.case_3)
        self.switch = VarChoose(parent_value=self.parent_value)
        self.backup()

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

    def linkOrinalCase(self):
        self.caseAdd.emit(self.case_1)
        self.caseAdd.emit(self.case_2)
        self.caseAdd.emit(self.case_3)

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
                new_case = Case(title=f"Case {add_index + 1}", can_add=True, can_delete=True, parent_value=self.parent_value)
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
        self.case_data_backup['switch'] = self.switch.currentText()
        self.case_data_backup['case'] = []
        self.cases_back_up.clear()
        for case in self.cases:
            self.cases_back_up.append(case.icon_choose.properties_window)
            case_data = {}
            case_data['case_title'] = case.title()
            case_data['case_value'] = case.case_comBox.currentText()
            case_data['case_icon_value'] = case.icon_choose.icon.value
            case_data['case_icon_name'] = case.icon_choose.icon_name.text()
            case_data['case_icon_properties'] = {} if not case.icon_choose.properties_window else case.icon_choose.properties_window.getInfo()
            case_data['can_add'] = case.canAdd()
            case_data['can_delete'] = case.canDelete()
            self.case_data_backup['case'].append(case_data)

    def restore(self, data):
        try:
            self.case_data_backup = data
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
                case.case_comBox.setCurrentText(cases[index]['case_value'])
                case.icon_choose.icon_comboBox.setCurrentText(cases[index]['case_icon_value'].split('.')[0])
                case.icon_choose.icon.changeValue(cases[index]['case_icon_value'])
                case.icon_choose.icon_name.setText(cases[index]['case_icon_name'])
                if cases[index]['case_icon_properties']:
                    case.icon_choose.properties_window.setProperties(cases[index]['case_icon_properties'])
                self.cases.append(case)
                row = index // 3 + 1
                col = index % 3
                self.grid_layout.addWidget(case, row, col, 1, 1)
                self.linkCaseSignals(case)
                self.caseAdd.emit(case)
        except Exception as e:
            print(f"error {e} happens in restore cases. [switchBranch/caseArea.py]")

    def restoreForCancel(self):
        try:
            # 先删除所有case
            for case in self.cases:
                self.grid_layout.removeWidget(case)
                case.hide()
                self.widget.update()
            self.cases.clear()
            # 增加新case
            print(self.cases_back_up)
            cases = self.case_data_backup['case']
            for index in range(len(cases)):
                case = Case(title=cases[index]['case_title'], parent=None, can_add=cases[index]['can_add'],
                            can_delete=cases[index]['can_delete'])
                case.case_comBox.setCurrentText(cases[index]['case_value'])
                case.icon_choose.icon_comboBox.setCurrentText(cases[index]['case_icon_value'].split('.')[0])
                case.icon_choose.icon.changeValue(cases[index]['case_icon_value'])
                case.icon_choose.icon_name.setText(cases[index]['case_icon_name'])
                case.icon_choose.properties_window = self.cases_back_up[index]
                self.cases.append(case)
                row = index // 3 + 1
                col = index % 3
                self.grid_layout.addWidget(case, row, col, 1, 1)
                self.linkCaseSignals(case)
                self.caseAdd.emit(case)
        except Exception as e:
            print(f"error {e} happens in restore cases for cancel. [switchBranch/caseArea.py]")

    def copy(self, case_area_copy, old_value:dict):
        try:
            # todo copy var
            # 先把复制者的case数调整为一致
            for i in range(3, len(self.cases)):
                row = i // 3 + 1
                col = i % 3
                new_case = Case()
                case_area_copy.grid_layout.addWidget(new_case, row, col, 1, 1)
                case_area_copy.cases.append(new_case)
                case_area_copy.caseAdd.emit(new_case)
                case_area_copy.linkCaseSignals(new_case)
            # 详细
            for i in range(len(self.cases)):
                # 修改title，buttons，value，name
                case:Case = self.cases[i]
                case_copy:Case = case_area_copy.cases[i]
                case_copy.setTitle(case.title())
                case_copy.setAddDisabled(not case.canAdd())
                case_copy.setDeleteDisabled(not case.canDelete())
                value = case.icon_choose.icon.value
                case_copy.case_comBox.setCurrentText(case.case_comBox.currentText())
                if not value.startswith('Other.'):
                    case_copy.icon_choose.icon_comboBox.setCurrentText(value.split('.')[0])
                    case_copy.icon_choose.icon.changeValue(old_value[value][0])
                    case_copy.icon_choose.icon_name.setText(old_value[value][1])
                    case_copy.icon_choose.properties_window.setProperties(case_copy.icon_choose.properties_window.getInfo())
            # backup
            case_area_copy.backup()
        except Exception as e:
            print(f"error {e} happens in copy cases. [switchBranch/caseArea.py]")