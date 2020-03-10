from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout

from app.func import Func
from lib import PigComboBox, TabItemWidget


class EyeAction(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(EyeAction, self).__init__(widget_id, widget_name)
        self.attributes: list = []
        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.status_message = PigComboBox()

        self.using_tracker_id = ""
        self.tracker_info = Func.getTrackerInfo()
        self.tracker_name = PigComboBox()
        self.tracker_name.addItems(self.tracker_info.values())
        self.tracker_name.currentTextChanged.connect(self.changeTrackerId)

        self.default_properties = {
            "Status Message": "Saccade start",
            "EyeTracker Name": "",
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
        layout1.addWidget(QLabel("EyeTracker Name:"), 3, 0, 1, 1)
        layout1.addWidget(self.tracker_name, 3, 1, 1, 1)

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
        self.default_properties["EyeTracker Name"] = self.tracker_name.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print("此乱诏也，恕不奉命")

    def loadSetting(self):
        self.status_message.setCurrentText(self.default_properties["Status Message"])
        self.tracker_name.setCurrentText(self.default_properties["EyeTracker Name"])

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

    def getStatusMessage(self) -> str:
        return self.status_message.currentText()

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
        clone_widget = EyeAction(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        return clone_widget


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeAction()

    pro.show()

    sys.exit(app.exec())
