from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from .caseArea import CaseArea
from structure.main import Structure
from getImage import getImage


class SwitchBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)
    # 将icon的value, 发送iconTabs (properties)
    iconPropertiesShow = pyqtSignal(dict)
    # 发送给structure, iconTabs (self.value, name, pixmap, value, properties window)
    caseAdd = pyqtSignal(str, str, QPixmap, str, QWidget)
    # (self.value, value)
    caseDelete = pyqtSignal(str, str)
    # (parent_value, value, name)
    caseNameChange = pyqtSignal(str, str, str)
    #
    caseTabDelete = pyqtSignal(str)

    def __init__(self, parent=None, value=''):
        super(SwitchBranch, self).__init__(parent)

        #
        self.value = value
        #
        self.case_area = CaseArea(self, self.value)
        self.case_area.caseAdd.connect(self.linkCaseSignals)
        self.case_area.linkOrinalCase()
        # icon_value : [case, name]
        self.value_case_name = {}

        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.clickOk)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.clickCancel)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.clickApply)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.apply_button)

        layout = QGridLayout()
        layout.addWidget(self.case_area, 0, 0, 3, 2)
        layout.addLayout(buttons_layout, 3, 0, 1, 2)

        self.setLayout(layout)

    def clickOk(self):
        if self.clickApply():
            self.close()
            self.tabClose.emit(self)

    def clickCancel(self):
        self.close()
        # 还原到初始设定
        self.restoreCases()
        self.tabClose.emit(self)

    def clickApply(self):
        try:
            # 采取分类处理的方法
            new_case_values = []
            change_case_values = []
            keep_case_values = []
            names_validity = True
            # 得到所有被删除的case的value，name
            delete_case_values = []
            delete_case_names = []
            current_case_values = []
            for case in self.case_area.cases:
                current_case_values.append(case.icon_choose.icon.value)
            for value in self.value_case_name:
                if value not in current_case_values:
                    delete_case_values.append(value)
                    delete_case_names.append(self.value_case_name[value][0].icon_choose.icon_name.text())
            # 先检测当前所有name
            for case in self.case_area.cases:
                name = case.icon_choose.icon_name.text()
                if name:
                    name_validity, tips = Structure.checkNameValidity(name, case.icon_choose.icon.value,
                                                                      delete_names=delete_case_names)
                    if not name_validity:
                        names_validity = False
                        QMessageBox.information(self, 'Tips', f"{case.title()}' name has error---{tips}")
                else:
                    if not case.icon_choose.icon.value.startswith('Other.'):
                        QMessageBox.information(self, 'Tips', f"{case.title()}' name can't be none.")
                        names_validity = False
            if names_validity:
                # 当前页面中的所有case
                for case in self.case_area.cases:
                    case_icon_value = case.icon_choose.icon.value
                    # 排除空的
                    if not case_icon_value.startswith('Other.'):
                        if case_icon_value in self.value_case_name:
                            # 是否命名修改
                            name = case.icon_choose.icon_name.text()
                            if name == self.value_case_name[case_icon_value][1]:
                                keep_case_values.append(case_icon_value)
                            else:
                                change_case_values.append(case_icon_value)
                        else:
                            new_case_values.append(case_icon_value)
                # 处理被删除的case
                delete_case_values = []
                for value in self.value_case_name:
                    if value not in change_case_values and value not in keep_case_values:
                        delete_case_values.append(value)
                for delete_case_value in delete_case_values:
                    self.deleteCase(delete_case_value)
                # 处理新增的case
                for new_case_value in new_case_values:
                    self.addCase(new_case_value)
                # 处理修改的case
                for change_case_value in change_case_values:
                    self.changeCase(change_case_value)
                # backup
                self.case_area.backup()
                return True
            else:
                return False
        except Exception as e:
            print("error {} happens in apply. [switchBranch/main.py]".format(e))

    def linkCaseSignals(self, case):
        case.icon_choose.propertiesShow.connect(self.showIconProperties)

    def deleteCase(self, value):
        try:
            # 删除相关数据
            del self.value_case_name[value]
            # 信号
            self.caseDelete.emit(self.value, value)
            self.caseTabDelete.emit(value)
        except Exception as e:
            print(f"error {e} happens in delete case. [switchBranch/main.py]")

    def changeCase(self, value):
        try:
            # 修改相关数据
            name = self.value_case_name[value][0].icon_choose.icon_name.text()
            self.value_case_name[value][1] = name
            # 信号
            self.caseNameChange.emit(self.value, value, name)
        except Exception as e:
            print(f"error {e} happens in change case name. [switchBranch/main.py]")

    def addCase(self, value):
        try:
            # 新增相关数据
            case = self.getCaseByValue(value)
            name = case.icon_choose.icon_name.text()
            properties_window = case.icon_choose.properties_window
            self.value_case_name[value] = [case, name]
            # 信号
            self.caseAdd.emit(self.value, name, getImage(value.split('.')[0], 'pixmap'), value, properties_window)
        except Exception as e:
            print(f"error {e} happens in add case. [switchBranch/main.py]")

    def getCaseByValue(self, value):
        for case in self.case_area.cases:
            if case.icon_choose.icon.value == value:
                return case
        return None

    def getInfo(self):
        return {"properties": "none"}

    def showIconProperties(self, properties):
        self.iconPropertiesShow.emit(properties)

    def restoreCases(self):
        try:
            self.case_area.restoreForCancel()
        except Exception as e:
            print(f"error {e} happens in restore cases. [switchBranch/main.py]")

    def deleteAndClearCase(self, value):
        try:
            # 把case变成空，不去删除了，删除太麻烦
            case_to_delete = None
            for case in self.case_area.cases:
                if case.icon_choose.icon.value == value:
                    case_to_delete = case
            if case_to_delete:
                case_to_delete.icon_choose.icon_comboBox.setCurrentText('None')
                # 删除数据
                case_title = case_to_delete.title()
                case_icon_value = case_to_delete.icon_choose.icon.value
                case_icon_name = case_to_delete.icon_choose.icon_name.text()
                index = -1
                try:
                    index = int(case_title.split(' ')[1]) - 1
                except Exception:
                    pass
                self.case_area.case_data_backup['case'][index]['case_title'] = case_title
                self.case_area.case_data_backup['case'][index]['case_icon_value'] = case_icon_value
                self.case_area.case_data_backup['case'][index]['case_icon_name'] = case_icon_name
                del self.value_case_name[value]
        except Exception as e:
            print(f"error {e} happens in delete and clear case. [switchBranch/main.py]")

    def changeCaseName(self, value, name):
        try:
            if value in self.value_case_name:
                case_to_change = self.value_case_name[value][0]
                case_to_change.icon_choose.icon_name.setText(name)
                # 相关数据
                self.value_case_name[value][1] = name
                index = -1
                try:
                    index = int(case_to_change.title().split(' ')[1]) - 1
                except Exception:
                    pass
                self.case_area.case_data_backup['case'][index]['case_icon_name'] = name
        except Exception as e:
            print(f"error {e} happens in change case name. [switchBranch/main.py]")

    def addVarComboBoxAttribute(self, new_attribute):
        self.case_area.switch.addAttribute(new_attribute)
        for case in self.case_area.cases:
            case.case_comBox.addAttribute(new_attribute)

    def changeVarComboBoxAttribute(self, old_attribute, new_attribute):
        self.case_area.switch.changeAttribute(old_attribute, new_attribute)
        for case in self.case_area.cases:
            case.case_comBox.changeAttribute(old_attribute, new_attribute)

    # todo copy
    def copy(self, value):
        try:
            switch_copy = SwitchBranch(value=value)
            # widget(case area)
            # 先获取相对应的value，name
            old_new = {}
            for case_value in self.value_case_name:
                case_new_name, case_new_value = Structure.getNameAndValueInSwitchBranchByParent(self.value, case_value,
                                                                                                value)
                old_new[case_value] = [case_new_value, case_new_name]
            self.case_area.copy(switch_copy.case_area, old_new)
            # data(value case data)
            for case in switch_copy.case_area.cases:
                switch_copy.value_case_name[case.icon_choose.icon.value] = [case, case.icon_choose.icon_name.text()]
            return switch_copy
        except Exception as e:
            print(f"error {e} happens in copy switchBranch. [switchBranch/main.py]")

    def save(self):
        return self.case_area.backup()

    def restore(self, data):
        self.case_area.restore(data)

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt":0
        }
        return hidden_attr

    def getUsingAttributes(self):
        using_attributes = []
        using_attributes.append(self.case_area.switch.currentText())
        for case in self.case_area.cases:
            using_attributes.append(case.case_comBox.currentText())
        return using_attributes
