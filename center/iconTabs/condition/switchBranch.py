from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout

from getImage import getImage
from .iconChoose import IconChoose
from .switchCondition import SwitchCondition


class SwitchBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)
    # 发送给structure, iconTabs (self.value, name, pixmap, value, properties window)
    nodeChange = pyqtSignal(str, str, QPixmap, str, QWidget)
    # (self.value, value)
    nodeDelete = pyqtSignal(str, str)
    # (parent_value, value, name)
    nodeNameChange = pyqtSignal(str, str, str)
    # 直接借助深拷贝的机制(properties widget)
    iconPropertiesChange = pyqtSignal(QWidget)
    # 将icon的value, 发送iconTabs (properties)
    iconPropertiesShow = pyqtSignal(dict)

    def __init__(self, parent=None, value=''):
        super(SwitchBranch, self).__init__(parent)

        self.condition_area = SwitchCondition()
        self.condition_area.add_case.connect(self.addCase)

        # 存放case的event对象
        self.icons = []

        self.default_icon_choose = IconChoose(self)
        self.default_icon_choose.propertiesShow.connect(self.showIconProperties)
        self.icons.append(self.default_icon_choose)

        self.value = value
        # [value, name, properties]
        self.type_value = {'D': ['Other.10001', '', {}]}

        condition_group = QGroupBox("Condition")
        layout1 = QVBoxLayout()
        layout1.addWidget(self.condition_area, 1)
        layout1.addStretch()
        condition_group.setLayout(layout1)

        self.default_group = QGroupBox("Default")
        self.default_group.setMinimumHeight(250)
        layout2 = QVBoxLayout()
        layout2.addWidget(self.default_icon_choose)
        self.default_group.setLayout(layout2)

        self.icon_layout = QHBoxLayout()
        self.icon_layout.addWidget(self.default_group)

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

        self.layout = QVBoxLayout()
        self.layout.addWidget(condition_group, 1)
        self.layout.addStretch()
        self.layout.addLayout(self.icon_layout)
        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)

    def addCase(self, index):
        group = QGroupBox(f"case{index}")
        icon_choose = IconChoose(self)
        self.icons.insert(index, icon_choose)

        layout = QVBoxLayout()
        layout.addWidget(icon_choose)
        group.setLayout(layout)
        self.icon_layout.removeWidget(self.default_group)
        self.icon_layout.addWidget(group)
        self.icon_layout.addWidget(self.default_group)

    def showProperty(self):
        QMessageBox.warning(self, "todo", "set the properties of the event", QMessageBox.Ok)

    def getInfo(self):
        return {
            "properties": "none"
        }

    def clickOk(self):
        self.clickApply()
        self.close()
        self.tabClose.emit(self)

    def clickCancel(self):
        self.close()
        self.tabClose.emit(self)

    def clickApply(self):
        try:
            self.disposeNode('D')

            # properties
            self.propertiesChange.emit(self.getInfo())
        except Exception as e:
            print("error {} happens in apple if-else. [condition/ifBranch.py]".format(e))

    # todo:这是啥呀
    def disposeNode(self, condition_type='D'):
        # 获取当前的icon的value
        if condition_type == 'D':
            current_value = self.default_icon_choose.icon.value
            current_name = self.default_icon_choose.icon_name.text()
            current_properties_window = self.default_icon_choose.properties_window
        else:
            current_value = self.default_icon_choose.icon.value
            current_name = self.default_icon_choose.icon_name.text()
            current_properties_window = self.default_icon_choose.properties_window

        # node delete
        if not self.type_value[condition_type][0].startswith("Other.") and current_value.startswith("Other"):
            self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
            self.type_value[condition_type] = ['Other.10001' if condition_type == 'D' else "Other.10002", '', {}]
        elif not current_value.startswith("Other."):
            # new node
            if current_value != self.type_value[condition_type][0]:
                # delete old
                if not self.type_value[condition_type][0].startswith("Other"):
                    self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
                    self.type_value[condition_type] = ['Other.10001' if condition_type == 'D' else "Other.10002", '',
                                                       {}]
                # add new
                self.nodeChange.emit(self.value, "[" + condition_type + "] " + current_name,
                                     getImage(current_value.split('.')[0], 'pixmap'),
                                     current_value, current_properties_window)
                self.type_value[condition_type][0] = current_value
                self.type_value[condition_type][1] = self.default_icon_choose.icon_name.text()
            # change node
            else:
                # name change
                if current_name != self.type_value[condition_type][1]:
                    self.nodeNameChange.emit(self.value, current_value, '[{}] '.format(condition_type) + current_name)
                # properties change
                pass

    # 删除
    def deleteItem(self, value):
        try:
            # true
            if value == self.type_value['T'][0]:
                self.true_icon_choose.icon_comboBox.setCurrentIndex(0)
                self.type_value['T'] = ['Other.10001', '', {}]
            # false
            elif value == self.type_value['F'][0]:
                self.false_icon_choose.icon_comboBox.setCurrentIndex(0)
                self.type_value['F'] = ['Other.10001', '', {}]

        except Exception as e:
            print("error {} happens in delete item. [condition/ifBranch.py]".format(e))

    # 重命名
    def changeItemName(self, value, name):
        try:
            # true
            if value == self.type_value['T'][0]:
                self.true_icon_choose.icon_name.setText(name[4:])
            # false
            elif value == self.type_value['F'][0]:
                self.false_icon_choose.icon_name.setText(name[4:])
        except Exception as e:
            print("error {} happens in change item name. [condition/ifBranch.py]".format(e))

    # 事件参数
    def showIconProperties(self, properties):
        self.iconPropertiesShow.emit(properties)
