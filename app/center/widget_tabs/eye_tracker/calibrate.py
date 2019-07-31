from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QCompleter

from app.func import Func
from app.lib import PigComboBox, PigLineEdit
from lib.psy_message_box import PsyMessageBox as QMessageBox


class EyeCalibrate(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(str)

    def __init__(self, parent=None, widget_id=''):
        super(EyeCalibrate, self).__init__(parent)
        self.widget_id = widget_id
        self.current_wid = widget_id

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
            "Screen": "screen.0",
        }

        self.calibration_type = PigComboBox()
        self.calibration_beep = PigComboBox()
        self.target_color = PigLineEdit()
        self.target_color.textChanged.connect(self.findVar)
        self.target_color.returnPressed.connect(self.finalCheck)
        self.target_style = PigComboBox()

        self.using_tracker_id: str = ""
        self.tracker_info = Func.getTrackerInfo()
        self.tracker_name = PigComboBox()
        self.tracker_name.addItems(self.tracker_info.values())
        self.tracker_name.currentTextChanged.connect(self.changeTrackerId)

        self.using_screen_id: str = ""
        self.screen = PigComboBox()
        self.screen_info = Func.getScreenInfo()
        self.screen.addItems(self.screen_info.values())
        self.screen.currentTextChanged.connect(self.changeScreen)

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
        self.target_color.setText("(foreground)")
        self.target_style.addItems(
            ["default", "large filled", "small filled", "large open", "small open", "large cross", "small cross"])

        l1 = QLabel("Calibration Type:")
        l2 = QLabel("Calibration Beep:")
        l3 = QLabel("Target Color:")
        l4 = QLabel("Target Style:")
        l5 = QLabel("EyeTracker Name:")
        l6 = QLabel("Screen Name:")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

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
        layout1.addWidget(l6, 7, 0, 1, 1)
        layout1.addWidget(self.screen, 7, 1, 1, 1)

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

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
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
        self.screen_info = Func.getScreenInfo()
        screen_id = self.using_screen_id
        self.screen.clear()
        self.screen.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen.setCurrentText(screen_name)
            self.using_screen_id = screen_id
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
        self.propertiesChange.emit(self.getInfo())

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = [f"[{attribute}]" for attribute in attributes]
        self.target_color.setCompleter(QCompleter(self.attributes))

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
        self.default_properties["Target color"] = self.target_color.text()
        self.default_properties["Target style"] = self.target_style.currentText()
        self.default_properties["EyeTracker Name"] = self.tracker_name.currentText()
        self.default_properties["Screen Name"] = self.screen.currentText()
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
        self.calibration_type.setCurrentText(self.default_properties["Calibration type"])
        self.calibration_beep.setCurrentText(self.default_properties["Calibration beep"])
        self.target_color.setText(self.default_properties["Target color"])
        self.target_style.setCurrentText(self.default_properties["Target style"])
        self.tracker_name.setCurrentText(self.default_properties["EyeTracker Name"])
        self.screen.setCurrentText(self.default_properties["Screen Name"])

    def clone(self, new_id: str):
        clone_widget = EyeCalibrate(widget_id=new_id)
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

    def getCalibrationType(self) -> str:
        return self.calibration_type.currentText()

    def getCalibrationBeep(self) -> str:
        return self.calibration_beep.currentText()

    def getTargetColor(self) -> str:
        return self.target_color.text()

    def getTargetStyle(self) -> str:
        return self.target_style.text()

    def getTrackerName(self) -> str:
        return self.tracker_name.currentText()

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    pro = EyeCalibrate()

    pro.show()

    sys.exit(app.exec())
