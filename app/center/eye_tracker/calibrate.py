from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout

from app.func import Func
from lib import VarComboBox, ColorListEditor, TabItemWidget


class EyeCalibrate(TabItemWidget):
    def __init__(self, widget_id: str, widget_name: str):
        super(EyeCalibrate, self).__init__(widget_id, widget_name)
        self.attributes = []

        self.tip1 = QLineEdit()
        self.tip2 = QLineEdit()
        self.tip1.setReadOnly(True)
        self.tip2.setReadOnly(True)
        self.default_properties = {
            "Calibration type": "HV13",
            "Calibration beep": "Yes",
            "Target color": "(foreground)",
            "Target style": "default",
            "EyeTracker Name": "",
        }

        self.calibration_type = VarComboBox()
        self.calibration_beep = VarComboBox()
        self.target_color = ColorListEditor()
        self.target_color.setCurrentText("gray")

        self.target_style = VarComboBox()

        self.using_tracker_id: str = ""
        self.tracker_info = Func.getTrackerInfo()
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

        self.setAttributes(Func.getAttributes(self.widget_id))

        self.calibration_type.setFocus()

    def setUI(self):
        self.setWindowTitle("Calibration")
        self.resize(500, 750)
        self.tip1.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip1.setText("Calibration")
        self.tip1.setFont(QFont("Timers", 20, QFont.Bold))
        self.tip2.setStyleSheet("border-width:0;border-style:outset;background-color:transparent;")
        self.tip2.setText("Calibration")
        self.calibration_type.addItems(["HV9", "HV13", "HV5", "HV3"])
        self.calibration_beep.addItems(["Yes", "No"])
        self.target_style.addItems(
            ["default", "large filled", "small filled", "large open", "small open", "large cross", "small cross"])

        l1 = QLabel("Calibration Type:")
        l2 = QLabel("Calibration Beep:")
        l3 = QLabel("Target Color:")
        l4 = QLabel("Target Style:")
        l5 = QLabel("EyeTracker Name:")
        # l6 = QLabel("Screen Name:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout1 = QGridLayout()
        layout1.addWidget(self.tip1, 0, 0, 1, 4)
        layout1.addWidget(self.tip2, 1, 0, 1, 4)
        layout1.addWidget(l1, 2, 0, 1, 1)
        layout1.addWidget(self.calibration_type, 2, 1, 1, 1)
        layout1.addWidget(l2, 3, 0, 1, 1)
        layout1.addWidget(self.calibration_beep, 3, 1, 1, 1)
        layout1.addWidget(l3, 4, 0, 1, 1)
        layout1.addWidget(self.target_color, 4, 1, 1, 1)
        layout1.addWidget(l4, 5, 0, 1, 1)
        layout1.addWidget(self.target_style, 5, 1, 1, 1)
        layout1.addWidget(l5, 6, 0, 1, 1)
        layout1.addWidget(self.tracker_name, 6, 1, 1, 1)
        # layout1.addWidget(l6, 7, 0, 1, 1)
        # layout1.addWidget(self.screen, 7, 1, 1, 1)

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
        self.tabClosed.emit(self.widget_id)

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.propertiesChanged.emit(self.widget_id)

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        # self.target_color.setCompleter(QCompleter(self.attributes))

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
        self.default_properties.clear()
        self.default_properties["Calibration type"] = self.calibration_type.currentText()
        self.default_properties["Calibration beep"] = self.calibration_beep.currentText()
        self.default_properties["Target color"] = self.target_color.getColor()
        self.default_properties["Target style"] = self.target_style.currentText()
        self.default_properties["EyeTracker Name"] = self.tracker_name.currentText()
        # self.info["Screen Name"] = self.screen.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
        else:
            print("此乱诏也，恕不奉命")

    def loadSetting(self):
        self.calibration_type.setCurrentText(self.default_properties["Calibration type"])
        self.calibration_beep.setCurrentText(self.default_properties["Calibration beep"])
        self.target_color.setCurrentText(self.default_properties["Target color"])
        self.target_style.setCurrentText(self.default_properties["Target style"])
        self.tracker_name.setCurrentText(self.default_properties["EyeTracker Name"])
        # self.screen.setCurrentText(self.info["Screen Name"])

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
        }
        return hidden_attr

    def getCalibrationType(self) -> str:
        return self.calibration_type.currentText()

    def getCalibrationBeep(self) -> str:
        return self.calibration_beep.currentText()

    def getTargetColor(self) -> str:
        return self.target_color.getColor()

    def getTargetStyle(self) -> str:
        return self.target_style.currentText()

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
        clone_widget = EyeCalibrate(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        return clone_widget


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeCalibrate()

    pro.show()

    sys.exit(app.exec())
