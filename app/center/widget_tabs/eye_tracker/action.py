from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QComboBox

from app.func import Func


class EyeAction(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(EyeAction, self).__init__(parent)
        self.widget_id = widget_id

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.status_message = QComboBox()

        self.default_properties = {
            "Status Message": "Saccade start"
        }
        self.msg = ""
        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

        self.setAttributes(Func.getAttributes(self.widget_id))

        self.status_message.setFocus()

    def setUI(self):
        self.setWindowTitle("Action")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Wait")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Waits for an eye-tracker event")
        self.status_message.addItems(
            ["Saccade start", "Saccade end", "Fixation start", "Fixation end", "Blink start", "Blink end"])

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Status Message:"), 2, 0, 1, 1)
        layout1.addWidget(self.status_message, 2, 1, 1, 1)

        layout2 = QHBoxLayout()
        layout2.addStretch(10)
        layout2.addWidget(self.bt_ok)
        layout2.addWidget(self.bt_cancel)
        layout2.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)
        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.msg = self.status_message.currentText()
        self.propertiesChange.emit(self.getInfo())

    def getInfo(self):
        self.default_properties["Status Message"] = self.status_message.currentText()
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print("此乱诏也，恕不奉命")

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.status_message.setCurrentText(self.default_properties["Statue Message"])

    def clone(self, new_id: str):
        clone_widget = EyeAction(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

    def setAttributes(self, attributes):
        pass

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        return using_attributes

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
        }
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

    def getStatusMessage(self) -> str:
        return self.status_message.currentText()

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeAction()

    pro.show()

    sys.exit(app.exec())
