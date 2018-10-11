from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout

from center.iconTabs.condition.iconChoose import IconChoose
from center.iconTabs.condition.ifBranch.conditionArea import ConditionArea
from getImage import getImage
from structure.main import Structure


class IfBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)
    # 发送给structure, iconTabs (self.value, name, pixmap, value, properties window, condition_type)
    nodeAdd = pyqtSignal(str, str, QPixmap, str, QWidget, str)
    # (self.value, value)
    nodeDelete = pyqtSignal(str, str)
    # (parent_value, value, name)
    nodeNameChange = pyqtSignal(str, str, str)
    # 直接借助深拷贝的机制(properties widget)
    iconPropertiesChange = pyqtSignal(QWidget)
    # 将icon的value, 发送iconTabs (properties)
    iconPropertiesShow = pyqtSignal(dict)
    #
    iconWidgetMerge = pyqtSignal(str, str)
    iconWidgetSplit = pyqtSignal(str, str)
    # 当icon变更事，它的tab应当被关闭
    iconTabDelete = pyqtSignal(str)

    def __init__(self, parent=None, value=''):
        super(IfBranch, self).__init__(parent)

        self.condition_area = ConditionArea(self, value)
        self.true_icon_choose = IconChoose(self)
        self.true_icon_choose.propertiesShow.connect(self.showIconProperties)
        self.false_icon_choose = IconChoose(self)
        self.false_icon_choose.propertiesShow.connect(self.showIconProperties)

        self.value = value
        # [value, name, properties]

        self.type_value = {'T': ['Other.10001', '', None], 'F': ['Other.10002', '', None]}
        self.widget_type_index = {'None': 0, 'Image': 1, 'Text': 2, 'Video': 3, 'SoundOut': 4}

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
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # layout = QGridLayout()
        # layout.addWidget(condition_group, 0, 0, 3, 2)
        # layout.addWidget(true_group, 3, 0, 2, 1)
        # layout.addWidget(false_group, 3, 1, 2, 1)
        # layout.addLayout(buttons_layout, 5, 0, 1, 2)
        layout = QVBoxLayout()
        layout.addWidget(condition_group, 1)
        tf_layout = QHBoxLayout()
        tf_layout.addWidget(true_group)
        tf_layout.addWidget(false_group)
        layout.addLayout(tf_layout, 20)
        layout.addLayout(buttons_layout, 1)
        self.setLayout(layout)

    def showProperty(self):
        QMessageBox.warning(self, "todo", "set the properties of the event", QMessageBox.Ok)

    def getInfo(self):
        return {
            "properties": "none"
        }

    def restoreIcons(self):
        true_widget_type = self.type_value['T'][0].split('.')[0]
        false_widget_type = self.type_value['F'][0].split('.')[0]

        if true_widget_type != 'Other':
            self.true_icon_choose.icon_comboBox.setCurrentIndex(self.widget_type_index[true_widget_type])
            self.true_icon_choose.icon.changeValue(self.type_value['T'][0])
            self.true_icon_choose.icon_name.setText(self.type_value['T'][1])
            self.true_icon_choose.properties_window = self.type_value['T'][2]
        else:
            self.true_icon_choose.icon_comboBox.setCurrentIndex(0)

        if false_widget_type != 'Other':
            self.false_icon_choose.icon_comboBox.setCurrentIndex(self.widget_type_index[true_widget_type])
            self.false_icon_choose.icon.changeValue(self.type_value['F'][0])
            self.false_icon_choose.icon_name.setText(self.type_value['F'][1])
            self.false_icon_choose.properties_window = self.type_value['F'][2]
        else:
            self.false_icon_choose.icon_comboBox.setCurrentIndex(0)

    def clickOk(self):
        if self.clickApply():
            self.close()
            self.tabClose.emit(self)

    def clickCancel(self):
        self.close()
        # 还原到初始设定
        self.restoreIcons()
        self.tabClose.emit(self)

    def clickApply(self):
        try:
            if self.disposeIconChoose('T') or self.disposeIconChoose('F'):
                return False
            return True
        except Exception as e:
            print("error {} happens in apply if-else. [ifBranch/main.py]".format(e))

    def disposeIconChoose(self, condition_type='T'):
        if condition_type == 'T':
            current_value = self.true_icon_choose.icon.value
            current_name = self.true_icon_choose.icon_name.text()
            current_properties_window = self.true_icon_choose.properties_window
            other_value = 'Other.10001'
        else:
            current_value = self.false_icon_choose.icon.value
            current_name = self.false_icon_choose.icon_name.text()
            current_properties_window = self.false_icon_choose.properties_window
            other_value = 'Other.10002'

        has_error = False
        # 空变成有，有变成空，有变成有，空保持空
        if current_value.startswith('Other.'):
            # 空保持空
            if self.type_value[condition_type][0].startswith('Other.'):
                pass
            # 有变成空
            else:
                self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
                self.iconTabDelete.emit(self.type_value[condition_type][0])
                self.type_value[condition_type] = [other_value, '', None]
        else:
            # 空变成有
            if self.type_value[condition_type][0].startswith('Other.'):
                if self.checkIconName(current_name, self.value, current_value, condition_type):
                    self.nodeAdd.emit(self.value, current_name,
                                      getImage(current_value.split('.')[0], 'pixmap'),
                                      current_value, current_properties_window, condition_type)
                    self.type_value[condition_type][0] = current_value
                    self.type_value[condition_type][1] = current_name
                    self.type_value[condition_type][2] = current_properties_window
                else:
                    has_error = True
            # 有变成有
            else:
                # 还是原来的有
                if self.type_value[condition_type][0] == current_value:
                    # 名字改变了
                    if self.type_value[condition_type][1] != current_name:
                        if self.checkIconName(current_name, self.value, current_value, condition_type):
                            self.nodeNameChange.emit(self.value, current_value, current_name)
                        else:
                            has_error = True
                    # 名字没变
                    else:
                        pass
                # 变成另一种有
                else:
                    # delete old
                    if not self.type_value[condition_type][0].startswith("Other"):
                        self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
                        self.iconTabDelete.emit(self.type_value[condition_type][0])
                        self.type_value[condition_type] = [other_value, '', None]
                    # add new
                    if self.checkIconName(current_name, self.value, current_value, condition_type):
                        self.nodeAdd.emit(self.value, current_name, getImage(current_value.split('.')[0], 'pixmap'),
                                          current_value, current_properties_window, condition_type)
                        self.type_value[condition_type][0] = current_value
                        self.type_value[condition_type][1] = current_name
                        self.type_value[condition_type][2] = current_properties_window
                    else:
                        has_error = True

            return has_error

    # def checkIconName(self, name, parent_value, value, condition_type):
    #     try:
    #         # name非空
    #         is_valid = True
    #         if name:
    #             res, exist_value, old_exist_value = Structure.checkNameIsValid(name, parent_value, value)
    #             #
    #             if res == 0:
    #                 is_valid= False
    #             elif res == 1:
    #                 pass
    #             elif res == 2:
    #                 # 如果用户想重复
    #                 if QMessageBox.question(self, "Tips",
    #                                         'the {}  group\'s name has existed in other place, are you sure to change?.'.format(
    #                                                 'True' if condition_type == 'T' else 'False'),
    #                                         QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
    #                     self.iconWidgetMerge.emit(value, exist_value)
    #                 else:
    #                     is_valid = False
    #             elif res == 3:
    #                 self.iconWidgetSplit.emit(value, old_exist_value)
    #             elif res == 4:
    #                 # 如果用户想重复
    #                 if QMessageBox.question(self, "Tips",
    #                                         'the {}  group\'s name has existed in other place, are you sure to change?.'.format(
    #                                             'True' if condition_type == 'T' else 'False'),
    #                                         QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
    #                     self.iconWidgetMerge.emit(value, exist_value)
    #                 else:
    #                     is_valid = False
    #         else:
    #             is_valid = False
    #
    #         # is valid
    #         if is_valid:
    #             return True
    #         else:
    #             if name:
    #                 QMessageBox.information(self, 'Tips', 'the {}  group\'s name can\'t use.'.format(
    #                     'True' if condition_type == 'T' else 'False'), QMessageBox.Ok)
    #             else:
    #                 QMessageBox.information(self, 'Tips', 'the {}  group\'s name can\'t be none.'.format(
    #                     'True' if condition_type == 'T' else 'False'), QMessageBox.Ok)
    #             return False
    #     except Exception as e:
    #         print(f"error {e} happens in check icon name. [ifBranch/main.py]")

    def checkIconName(self, name, parent_value, value, condition_type):
        try:
            # name非空
            is_valid = False
            tips = ''
            if name:
                is_valid, tips = Structure.checkNameValidity(name, value)
            # is valid
            if is_valid:
                return True
            else:
                if name:
                    QMessageBox.information(self, 'Tips', 'the {}  group\'s name can\'t use, because {}'.format(
                        'True' if condition_type == 'T' else 'False', tips), QMessageBox.Ok)
                else:
                    QMessageBox.information(self, 'Tips', 'the {}  group\'s name can\'t be none.'.format(
                        'True' if condition_type == 'T' else 'False'), QMessageBox.Ok)
                return False
        except Exception as e:
            print(f"error {e} happens in check icon name. [ifBranch/main.py]")

    def deleteItem(self, value):
        try:
            # true
            if value == self.type_value['T'][0]:
                self.true_icon_choose.icon_comboBox.setCurrentIndex(0)
                self.type_value['T'] = ['Other.10001', '', {}]
            # false
            elif value == self.type_value['F'][0]:
                self.false_icon_choose.icon_comboBox.setCurrentIndex(0)
                self.type_value['F'] = ['Other.10002', '', {}]

        except Exception as e:
            print("error {} happens in delete Item. [ifBranch/main.py]".format(e))

    def changeItemName(self, value, name):
        try:
            # true
            if value == self.type_value['T'][0]:
                self.true_icon_choose.icon_name.setText(name)
                self.type_value['T'][1] = name
            # false
            elif value == self.type_value['F'][0]:
                self.false_icon_choose.icon_name.setText(name)
                self.type_value['F'][1] = name
        except Exception as e:
            print("error {} happens in change Item name. [ifBranch/main.py]".format(e))

    def showIconProperties(self, properties):
        self.iconPropertiesShow.emit(properties)

    # todo copy ifBranch (copy condition area)
    def copy(self, value):
        try:
            if_branch_copy = IfBranch(value=value)
            # data (type_value[value, name, properties_window])
            if not self.type_value['T'][0].startswith('Other.'):
                # icon_name, icon_value
                icon_name, icon_value = Structure.getNameAndValueInIfBranchByParent(value, 'T')
                if_branch_copy.type_value['T'][0] = icon_value
                if_branch_copy.type_value['T'][1] = icon_name
                if_branch_copy.true_icon_choose.icon_comboBox.setCurrentText(icon_value.split('.')[0])
                if_branch_copy.true_icon_choose.icon.changeValue(icon_value)
                if_branch_copy.true_icon_choose.icon_name.setText(icon_name)
                if_branch_copy.true_icon_choose.properties_window.setInfo(self.type_value['T'][2].getInfo())
                if_branch_copy.type_value['T'][2] = if_branch_copy.true_icon_choose.properties_window
            if not self.type_value['F'][0].startswith('Other.'):
                icon_name, icon_value = Structure.getNameAndValueInIfBranchByParent(value, 'F')
                if_branch_copy.type_value['F'][0], if_branch_copy.type_value['F'][1] = icon_value, icon_name
                if_branch_copy.false_icon_choose.icon_comboBox.setCurrentText(icon_value.split('.')[0])
                if_branch_copy.false_icon_choose.icon.changeValue(icon_value)
                if_branch_copy.false_icon_choose.icon_name.setText(icon_name)
                if_branch_copy.false_icon_choose.properties_window.setInfo(self.type_value['F'][2].getInfo())
                if_branch_copy.type_value['F'][2] = if_branch_copy.false_icon_choose.properties_window
            return if_branch_copy
        except Exception as e:
            print(f"error {e} happens in copy if branch. [ifBranch/main.py]")

    def save(self):
        return self.type_value

    def restore(self, type_value:dict):
        self.type_value = type_value
        true_widget_type = self.type_value['T'][0].split('.')[0]
        false_widget_type = self.type_value['F'][0].split('.')[0]

        if true_widget_type != 'Other':
            self.true_icon_choose.icon_comboBox.setCurrentIndex(self.widget_type_index[true_widget_type])
            self.true_icon_choose.icon.changeValue(self.type_value['T'][0])
            self.true_icon_choose.icon_name.setText(self.type_value['T'][1])
            self.true_icon_choose.properties_window = self.type_value['T'][2]
        else:
            self.true_icon_choose.icon_comboBox.setCurrentIndex(0)

        if false_widget_type != 'Other':
            self.false_icon_choose.icon_comboBox.setCurrentIndex(self.widget_type_index[true_widget_type])
            self.false_icon_choose.icon.changeValue(self.type_value['F'][0])
            self.false_icon_choose.icon_name.setText(self.type_value['F'][1])
            self.false_icon_choose.properties_window = self.type_value['F'][2]
        else:
            self.false_icon_choose.icon_comboBox.setCurrentIndex(0)

    # 获取condition\true\false参数
    def getInfo(self):
        pass