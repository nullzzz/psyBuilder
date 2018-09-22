from PyQt5.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from .caseTable import CaseTable


class SwitchBranch(QWidget):
    tabClose = pyqtSignal(QWidget)
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, value=''):
        super(SwitchBranch, self).__init__(parent)

        #
        self.value = value
        #
        self.case_table = CaseTable(self)

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
        layout.addWidget(self.case_table, 0, 0, 3, 2)
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
            for i in range(len(self.case_table.add_buttons)):
                if not self.disposeCase(i):
                    return False
            return True
        except Exception as e:
            print("error {} happens in apply if-else. [ifBranch/main.py]".format(e))

    def getInfo(self):
        return {"properties" : "none"}

    def disposeCase(self, case_index):
        current_icon_choose = self.case_table.cellWidget(case_index + 1, 1).icon_choose
        current_value = current_icon_choose.icon.value
        current_name = current_icon_choose.icon_name.text()
        current_properties_window = current_icon_choose.properties_window

        print(current_value, current_name)
        return True
