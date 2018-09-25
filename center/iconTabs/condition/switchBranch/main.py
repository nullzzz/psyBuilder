from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from .caseArea import CaseArea
from structure.main import Structure


class SwitchBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)
    #
    # (value, exist_value)
    iconWidgetMerge = pyqtSignal(str, str)
    iconWidgetSplit = pyqtSignal(str, str)

    def __init__(self, parent=None, value=''):
        super(SwitchBranch, self).__init__(parent)

        #
        self.value = value
        #
        self.case_area = CaseArea(self)

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
        self.restoreIcons()
        self.tabClose.emit(self)

    def clickApply(self):
        try:
            for i in range(len(self.case_area.add_buttons)):
                # 如果发生错误
                if self.disposeCase(i):
                    return False
            return True
        except Exception as e:
            print("error {} happens in apply if-else. [ifBranch/main.py]".format(e))

    def getInfo(self):
        return {"properties" : "none"}

    def disposeCase(self, case_index):
        current_icon_choose = self.case_area.cellWidget(case_index + 1, 1).icon_choose
        current_value = current_icon_choose.icon.value
        current_name = current_icon_choose.icon_name.text()
        current_properties_window = current_icon_choose.properties_window

        has_error = False

        return has_error

    def checkCaseIconName(self, name, parent_value, value, index):
        try:
            is_valid = True
            if name:
                res, exist_value, old_exist_value = Structure.checkNameIsValid(name, parent_value, value)
                #
                if res == 0:
                    is_valid = False
                elif res == 1:
                    pass
                elif res == 2:
                    # 如果用户想重复
                    if QMessageBox.question(self, "Tips",
                                            f'Case {index}\'s name has existed in other place, are you sure to change?.',
                                            QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                        self.iconWidgetMerge.emit(value, exist_value)
                    else:
                        is_valid = False
                elif res == 3:
                    self.iconWidgetSplit.emit(value, old_exist_value)
                elif res == 4:
                    # 如果用户想重复
                    if QMessageBox.question(self, "Tips",
                                            f'Case {index}\'s name has existed in other place, are you sure to change?.',
                                            QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
                        self.iconWidgetMerge.emit(value, exist_value)
                    else:
                        is_valid = False
            else:
                is_valid = False

        except Exception as e:
            print(f"error {e} happens in check name. [switchBranch/main.py]")
