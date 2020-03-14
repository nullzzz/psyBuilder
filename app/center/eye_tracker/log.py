from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QCheckBox, QTextEdit, QListWidget, QAbstractItemView

from app.func import Func
from lib import VarLineEdit, VarComboBox, TabItemWidget


class Close(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(Close, self).__init__(widget_id, widget_name)
        self.attributes: list = Func.getAttributes(self.widget_id)

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)

        self.pause_between_msg = VarLineEdit("1")

        self.using_tracker_id = ""
        self.tracker_info = Func.getTrackerInfo()
        self.tracker_name = VarComboBox()
        self.tracker_name.addItems(self.tracker_info.values())
        self.tracker_name.currentTextChanged.connect(self.changeTrackerId)
        self.default_properties = {
            "Pause between messages": "1",
            "Automatically log all variables": 0,
            "Used attributes": [],
            "Not used attributes": [],
            "EyeTracker Name": "",
        }

        self.msg = ""
        self.automatically_log_all_variables = QCheckBox("Automatically log all variables")
        self.log_msg = QTextEdit()

        self.all_attr = QListWidget()
        self.all_attr.addItems(self.attributes)
        self.all_attr.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.refresh_bt = QPushButton("refresh")
        self.refresh_bt.clicked.connect(self.refreshAttr)
        self.select_attr = QListWidget()
        self.select_attr.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.select_all_bt = QPushButton(">>")
        self.select_all_bt.clicked.connect(self.selectAll)
        self.select_one_bt = QPushButton(">")
        self.select_one_bt.clicked.connect(self.selectOne)
        self.remove_all_bt = QPushButton("<<")
        self.remove_all_bt.clicked.connect(self.removeAll)
        self.remove_one_bt = QPushButton("<")
        self.remove_one_bt.clicked.connect(self.removeOne)

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)

        self.setUI()

        self.setAttributes(Func.getAttributes(self.widget_id))

        self.pause_between_msg.setFocus()

    def setUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Close")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Log")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Writes information to the eye-tracker logfile")

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(QLabel("Pause between messages(ms):"), 2, 0, 1, 1)
        layout1.addWidget(self.pause_between_msg, 2, 1, 1, 1)
        layout1.addWidget(self.automatically_log_all_variables, 3, 1, 1, 1)
        layout1.addWidget(QLabel("EyeTracker Name:"), 4, 0, 1, 1)
        layout1.addWidget(self.tracker_name, 4, 1, 1, 1)

        lay_bt = QVBoxLayout()
        lay_bt.addWidget(self.refresh_bt)
        lay_bt.addWidget(self.select_all_bt)
        lay_bt.addWidget(self.select_one_bt)
        lay_bt.addWidget(self.remove_one_bt)
        lay_bt.addWidget(self.remove_all_bt)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.all_attr)
        layout2.addLayout(lay_bt)
        layout2.addWidget(self.select_attr)

        layout3 = QHBoxLayout()
        layout3.addStretch(1)
        layout3.addWidget(self.bt_ok)
        layout3.addWidget(self.bt_cancel)
        layout3.addWidget(self.bt_apply)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        self.setLayout(layout)

    def changeTrackerId(self, tracker_name):
        for k, v in self.tracker_info.items():
            if v == tracker_name:
                self.using_tracker_id = k
                break

    def refresh(self):
        self.tracker_info = Func.getTrackerInfo()
        tracker_id = self.using_tracker_id
        self.tracker_name.clear()
        self.tracker_name.addItems(self.tracker_info.values())
        tracker_name = self.tracker_info.get(tracker_id)
        if tracker_name:
            self.tracker_name.setCurrentText(tracker_name)
            self.using_tracker_id = tracker_id

        # 更新attributes
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.getInfo()

    def refreshAttr(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.all_attr.clear()
        self.select_attr.clear()
        self.all_attr.addItems(self.attributes)

    def selectAll(self):
        self.all_attr.clear()
        self.select_attr.clear()
        self.select_attr.addItems(self.attributes)

    def removeAll(self):
        self.select_attr.clear()
        self.all_attr.clear()
        self.all_attr.addItems(self.attributes)

    def selectOne(self):
        its = self.all_attr.selectedItems()
        for i in its:
            it = self.all_attr.takeItem(self.all_attr.row(i))
            self.select_attr.addItem(it)

    def removeOne(self):
        its = self.select_attr.selectedItems()
        for i in its:
            it = self.select_attr.takeItem(self.select_attr.row(i))
            self.all_attr.addItem(it)

    def ok(self):
        self.apply()
        self.close()
        self.tabClose.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.propertiesChanged.emit(self.widget_id)

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print("此乱诏也，恕不奉命")

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Pause between messages"] = self.pause_between_msg.text()
        self.default_properties["Automatically log all variables"] = self.automatically_log_all_variables.checkState()
        self.default_properties["EyeTracker Name"] = self.tracker_name.currentText()
        ua = []
        for i in range(self.select_attr.count()):
            ua.append(self.select_attr.item(i).text())
        self.default_properties["Used attributes"] = ua
        nua = []
        for i in range(self.all_attr.count()):
            nua.append(self.all_attr.item(i).text())
        self.default_properties["Not used attributes"] = nua
        return self.default_properties

    def loadSetting(self):
        self.pause_between_msg.setText(self.default_properties["Pause between messages"])
        self.automatically_log_all_variables.setCheckState(self.default_properties["Automatically log all variables"])
        self.tracker_name.setCurrentText(self.default_properties["EyeTracker Name"])
        self.select_attr.clear()
        self.select_attr.addItems(self.default_properties["Used attributes"])
        self.all_attr.clear()
        self.all_attr.addItems(self.default_properties["Not used attributes"])

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

    def getPauseBetweenMessages(self) -> str:
        return self.pause_between_msg.text()

    def getIsAutomaticallyLogAllVariables(self) -> bool:
        return bool(self.automatically_log_all_variables.checkState())

    def getTrackerName(self) -> str:
        return self.tracker_name.currentText()

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)

    """
    Functions that must be complete in new version
    """

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        return self.getInfo()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.getInfo()

    def restore(self, properties):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def clone(self, new_widget_id: str, new_widget_name: str):
        clone_widget = Close(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        return clone_widget
