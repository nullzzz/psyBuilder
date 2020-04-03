from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget, QGridLayout

from app.center.events.duration.describer.response import RespTrigger, EyeAction, RespInfo
from app.center.events.duration.describer.trigger import TriggerInfo
from app.func import Func


class DefaultShow(QWidget):
    def __init__(self, parent=None):
        super(DefaultShow, self).__init__(parent=parent)
        self.label = QLabel("Add device(s) first!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout = QGridLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class Describer(QStackedWidget):
    def __init__(self, D_TYPE, parent=None):
        super(Describer, self).__init__(parent)
        self.d_type = D_TYPE
        self.face = DefaultShow()
        self.addWidget(self.face)
        self.id_widget: dict = {
            # device_id: device_describer
        }
        self.default_properties = {

        }

    def describe(self, device_id: str, device_info: dict):
        if device_info == {}:
            self.removeWidget(self.id_widget.get(device_id))
            self.id_widget.pop(device_id)
        else:
            if device_id in self.id_widget.keys():
                self.setCurrentWidget(self.id_widget.get(device_id))
            else:
                if self.d_type == 0:
                    d = TriggerInfo()
                elif self.d_type == 1:
                    d = RespInfo()
                elif self.d_type == 2:
                    d = RespTrigger()
                else:
                    d = EyeAction()
                d.describe(device_info)
                self.addWidget(d)
                self.setCurrentWidget(d)
                self.id_widget[device_id] = d

    def cancel(self, device_id: str):
        self.removeWidget(self.id_widget.get(device_id))

    def changeName(self, old_name: str, new_name: str):
        if self.currentIndex():
            self.currentWidget().changeName(new_name)

    def updateInfo(self):
        self.default_properties.clear()
        for k, v in self.id_widget.items():
            self.default_properties[k] = v.updateInfo()
            self.default_properties[k]["Device Id"] = k

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    def updateSimpleInfo(self, info: dict):
        RespTrigger.OUTPUT_DEVICE = info
        for k, v in self.id_widget.items():
            v.updateExternalDeviceInformation(info)

    def refresh(self):
        for w, d in self.id_widget.items():
            if isinstance(d, RespInfo):
                if (new_name := Func.getDeviceNameById(w)) != "":
                    d.changeName(new_name)

    def setAttributes(self, attributes: list):
        for d in self.id_widget.values():
            d.setAttributes(attributes)
