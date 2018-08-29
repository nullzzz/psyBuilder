from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap

from .iconChoose import IconChoose
from .conditionArea import ConditionArea
from ..image import getImage


class IfBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)
    # 发送给structure (self.value, name, pixmap, value, type)
    nodeChange = pyqtSignal(str, str, QPixmap, str, str)
    # (self.value, value)
    nodeDelete = pyqtSignal(str, str)
    # (value, name)
    nodeNameChange = pyqtSignal(str, str)
    #
    iconPropertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, value=''):
        super(IfBranch, self).__init__(parent)

        self.condition_area = ConditionArea(self)
        self.true_icon_choose = IconChoose(self)
        self.false_icon_choose = IconChoose(self)

        self.value = value
        # [value, name, properties]
        self.type_value = {'T': ['Other.10001', '', {}], 'F': ['Other.10002', '', {}]}

        condition_group = QGroupBox("Condition")
        layout1 = QVBoxLayout()
        layout1.addWidget(self.condition_area)
        condition_group.setLayout(layout1)

        true_group = QGroupBox("True")
        true_group.setMinimumHeight(250)
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

        layout = QGridLayout()
        layout.addWidget(condition_group, 0, 0, 1, 2)
        layout.addWidget(true_group, 1, 0, 2, 1)
        layout.addWidget(false_group, 1, 1, 2, 1)
        layout.addLayout(buttons_layout, 3, 0, 1, 2)
        self.setLayout(layout)

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
            self.disposeNode('T')
            self.disposeNode('F')

            # properties
            self.propertiesChange.emit(self.getInfo())
        except Exception as e:
            print("error {} happens in apple if-else. [condition/ifBranch.py]".format(e))

    def disposeNode(self, condition_type='T'):
        # 获取当前的icon的value
        if condition_type == 'T':
            current_value = self.true_icon_choose.icon.value
            current_name = self.true_icon_choose.icon_name.text()
        else:
            current_value = self.false_icon_choose.icon.value
            current_name = self.false_icon_choose.icon_name.text()

        # node delete
        if not self.type_value[condition_type][0].startswith("Other.") and current_value.startswith("Other"):
            self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
            self.type_value[condition_type] = ['Other.10001' if condition_type == 'T' else "Other.10002", '', {}]
        elif not current_value.startswith("Other."):
            # new node
            if current_value != self.type_value[condition_type][0]:
                # delete old
                if not self.type_value[condition_type][0].startswith("Other"):
                    self.nodeDelete.emit(self.value, self.type_value[condition_type][0])
                    self.type_value[condition_type] = ['Other.10001' if condition_type == 'T' else "Other.10002", '',
                                                       {}]
                # add new
                self.nodeChange.emit(self.value, "[" + condition_type + "] " + current_name,
                                     getImage(current_value.split('.')[0], 'pixmap'),
                                     current_value, condition_type)
                self.type_value[condition_type][0] = current_value
                self.type_value[condition_type][1] = self.true_icon_choose.icon_name.text()
            # change node
            else:
                # name change
                if current_name != self.type_value[condition_type][1]:
                    self.nodeNameChange.emit(current_value, '[{}] '.format(condition_type) + current_name)
                # properties change
                pass

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