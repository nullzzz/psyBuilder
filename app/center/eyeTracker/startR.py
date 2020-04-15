from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QCompleter

from app.func import Func
from lib import VarLineEdit, VarComboBox, TabItemWidget


class StartR(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(StartR, self).__init__(widget_id, widget_name)
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)

        self.default_properties = {
            "Status Message": "",
            "Sync To Next Event Flip": "No",
            "EyeTracker Name": "",
        }
        self.status_message = VarLineEdit()
        self.sync_to_next_event_flip = VarComboBox()
        self.sync_to_next_event_flip.addItems(("No", "Yes"))

        self.using_tracker_id = ""
        self.tracker_info = Func.getDeviceInfo("tracker")
        self.tracker_name = VarComboBox()
        self.tracker_name.addItems(self.tracker_info.values())
        self.tracker_name.currentTextChanged.connect(self.changeTrackerId)

        self.bt_ok = QPushButton("OK")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)
        self.setUI()

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
        layout1.addWidget(QLabel("EyeTracker Name:"), 4, 0, 1, 1)
        layout1.addWidget(self.tracker_name, 4, 1, 1, 1)

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

    def changeTrackerId(self, tracker_name):
        for k, v in self.tracker_info.items():
            if v == tracker_name:
                self.using_tracker_id = k
                break

    def refresh(self):
        self.tracker_info = Func.getDeviceInfo("tracker")
        tracker_id = self.using_tracker_id
        self.tracker_name.clear()
        self.tracker_name.addItems(self.tracker_info.values())
        tracker_name = self.tracker_info.get(tracker_id)
        if tracker_name:
            self.tracker_name.setCurrentText(tracker_name)
            self.using_tracker_id = tracker_id

        # 更新attributes
        attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(attributes)
        self.updateInfo()

    def ok(self):
        self.apply()
        self.close()
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)

    def setAttributes(self, attributes):
        attributes = [f"[{attribute}]" for attribute in attributes]
        self.status_message.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties["Status Message"] = self.status_message.text()
        self.default_properties["Sync To Next Event Flip"] = self.sync_to_next_event_flip.currentText()
        self.default_properties["EyeTracker Name"] = self.tracker_name.currentText()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.status_message.setText(self.default_properties["Status Message"])
        self.sync_to_next_event_flip.setCurrentText(self.default_properties["Sync To Next Event Flip"])
        self.tracker_name.setCurrentText(self.default_properties["EyeTracker Name"])

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        self.refresh()
        return self.default_properties

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.default_properties

    def restore(self, properties):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name: str):
        clone_widget = StartR(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties.copy())
        return clone_widget

    def getStatusMessage(self) -> str:
        return self.status_message.text()

    def getSyncToNextEventFlip(self) -> str:
        return self.sync_to_next_event_flip.currentText()

    def getTrackerName(self) -> str:
        return self.tracker_name.currentText()
