from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLayout, QStackedWidget, QGridLayout

from app.deviceSelection.describer.io import Screen, Sound, Net, Serial, Shower, Parallel
from app.deviceSelection.describer.quest import Quest
from app.deviceSelection.describer.tracker import Tracker, Action


class DefaultShow(QWidget):
    def __init__(self, parent=None):
        super(DefaultShow, self).__init__(parent)
        self.label = QLabel("Device information will show here.")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout = QGridLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class Describer(QStackedWidget):
    def __init__(self, parent=None):
        super(Describer, self).__init__(parent)
        self.face = DefaultShow()
        self.addWidget(self.face)
        self.id_widget: dict = {}

    def describe(self, device_id: str, device_info: dict):
        if device_info == {}:
            self.removeWidget(self.id_widget.get(device_id))
            self.id_widget.pop(device_id)
        else:
            if device_id in self.id_widget.keys():
                self.setCurrentWidget(self.id_widget.get(device_id))
            else:
                if device_id.startswith("screen"):
                    d = Screen()
                elif device_id.startswith("sound"):
                    d = Sound()
                elif device_id.startswith("network_port"):
                    d = Net()
                elif device_id.startswith("parallel_port"):
                    d = Parallel()
                elif device_id.startswith("serial_port"):
                    d = Serial()
                elif device_id.startswith("quest"):
                    d = Quest()
                elif device_id.startswith("tracker"):
                    d = Tracker()
                # elif device_id.startswith("action"):
                else:
                    d = Action()
                d.describe(device_info)
                self.addWidget(d)
                self.setCurrentWidget(d)
                self.id_widget[device_id] = d

    def cancel(self, device_id: str):
        self.removeWidget(self.id_widget.get(device_id))

    def changeName(self, new_name: str):
        if self.currentIndex():
            self.currentWidget().changeName(new_name)