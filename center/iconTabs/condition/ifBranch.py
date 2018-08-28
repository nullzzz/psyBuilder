from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGroupBox, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap

from .iconChoose import IconChoose
from .conditionArea import ConditionArea
from ..image import getImage


class IfBranch(QWidget):
    tabClose = pyqtSignal()
    propertiesChange = pyqtSignal(dict)
    # 发送给structure (self.value, value, name, type)
    nodeChange = pyqtSignal(str, str, QPixmap, str, str)
    # (self.value, value)
    # nodeDelete = pyqtSignal(str, str)
    def __init__(self, parent=None, value=''):
        super(IfBranch, self).__init__(parent)

        self.condition_area = ConditionArea(self)
        self.true_icon_choose = IconChoose(self)
        self.false_icon_choose = IconChoose(self)

        self.value = value

        self.type_value = {'T' : '', 'F' : ''}

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
            "properties" : "none"
        }

    def clickOk(self):
        self.clickApply()
        self.tabClose.emit()
        self.close()

    def clickCancel(self):
        self.tabClose.emit()
        self.close()

    def clickApply(self):
        try:
            # add node
            icon_true_value = self.true_icon_choose.icon.value
            print(icon_true_value)
            if not icon_true_value.startswith('Other') and icon_true_value != self.type_value['T']:
                icon_true_name = "[T]" + self.true_icon_choose.icon_name.text()
                self.nodeChange.emit(self.value, icon_true_name, getImage(icon_true_value.split('.')[0], 'pixmap'), icon_true_value, 'T')
                self.type_value['T'] = icon_true_value

            icon_false_value = self.false_icon_choose.icon.value
            if not icon_false_value.startswith('Other') and icon_false_value != self.type_value['F']:
                icon_false_name = "[F]" + self.false_icon_choose.icon_name.text()
                self.nodeChange.emit(self.value, icon_false_name, getImage(icon_false_value.split('.')[0], 'pixmap'), icon_false_value, 'F')
                self.type_value['F'] = icon_false_value
            # properties
            self.propertiesChange.emit(self.getInfo())
        except Exception as e:
            print("error {} happens in apple if-else. [condition/ifBranch.py]".format(e))
