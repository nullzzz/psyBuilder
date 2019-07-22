from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QCompleter

from app.func import Func
from app.lib import PigLineEdit, PigComboBox


class StartR(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(StartR, self).__init__(parent)
        self.widget_id = widget_id
        self.current_wid = widget_id

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.attributes = []

        self.default_properties = {
            "Status message": "",
            "Sync to next event flip": "no",
        }
        self.status_message = PigLineEdit()
        self.sync_to_next_event_flip = PigComboBox()
        self.sync_to_next_event_flip.addItems(("no", "yes"))

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
        self.setWindowTitle("StartR")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Start recording")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Start recording of eye tracking data")
        self.status_message.setMaximumWidth(300)
        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Statue Message:"), 2, 0, 1, 1)
        layout1.addWidget(self.status_message, 2, 1, 1, 1)
        layout1.addWidget(QLabel("Sync to Next Event Flip:"), 3, 0, 1, 1)
        layout1.addWidget(self.sync_to_next_event_flip, 3, 1, 1, 1)

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
        self.msg = self.status_message.text()
        self.propertiesChange.emit(self.getInfo())
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        self.status_message.setCompleter(QCompleter(self.attributes))

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def getInfo(self):
        self.default_properties["Statue message"] = self.status_message.text()
        self.default_properties["Sync to next event flip"] = self.sync_to_next_event_flip.currentText()
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print(f"此乱诏也，{self.__class__}不奉命")

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.status_message.setText(self.default_properties["Statue message"])
        self.sync_to_next_event_flip.setText(self.default_properties["Sync to next event flip"])

    def clone(self, new_id: str):
        clone_widget = StartR(widget_id=new_id)
        clone_widget.setProperties(self.default_properties)
        return clone_widget

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
        return self.status_message.text()

    def getSyncToNextEventFlip(self) -> str:
        return self.sync_to_next_event_flip.currentText()

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)
