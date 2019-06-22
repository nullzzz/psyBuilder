from PyQt5.QtCore import QObject, QEvent, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QMessageBox, QLineEdit

from app.lib import ColorListEditor


class Describer(QWidget):
    portChanged = pyqtSignal(str)
    colorChanged = pyqtSignal(str)
    sampleChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Describer, self).__init__(parent=parent)
        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")
        self.device_port = QLineEdit("")
        self.port_tip = QLabel("")

        self.device_port.textEdited.connect(self.showPortTip)
        self.port: str = ""

        self.is_describing_screen: bool = False

        self.setUI()

    def setUI(self):
        self.layout = QFormLayout()
        self.layout.setLabelAlignment(Qt.AlignRight)
        self.layout.addRow("Device Type:", self.device_type)
        self.layout.addRow("Device Name:", self.device_name)
        self.layout.addRow("Device Port:", self.device_port)
        self.layout.addRow("", self.port_tip)
        self.setLayout(self.layout)

    def describe(self, device_type, device_name, device_port, color="0,0,0", sample="0"):
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)

        if device_type == "screen":
            if not self.is_describing_screen:
                self.bg_color = ColorListEditor()
                self.bg_color.colorChanged.connect(self.changeColor)
                self.bg_color.setCurrentText(color)
                self.multi_sample = QLineEdit(sample)
                self.multi_sample.textEdited.connect(self.changeSample)
                self.layout.insertRow(3, "Back Color:", self.bg_color)
                self.layout.insertRow(4, "Multi Sample:", self.multi_sample)
            else:
                self.bg_color.setCurrentText(color)
                self.multi_sample.setText(sample)
            self.is_describing_screen = True
        else:
            if self.is_describing_screen:
                self.layout.removeRow(4)
                self.layout.removeRow(3)
                self.is_describing_screen = False

        if device_type in ("mouse", "keyboard", "game pad"):
            self.device_port.setText("Invalid")
            self.device_port.setEnabled(False)
        else:
            self.device_port.setEnabled(True)
            self.device_port.setText(device_port)
            self.port = device_port
            self.showPortTip(self.port)

    def changeName(self, name):
        self.device_name.setText(name)

    def eventFilter(self, obj: QObject, e: QEvent):
        print(e)
        if obj == self.device_port:
            if e.type() == QEvent.FocusOut:
                port = self.device_port.text()
                if not self.checkPort(port):
                    QMessageBox.warning(self, "Warning", "Invalid Port!", QMessageBox.Ok)
                    self.device_port.setText(self.port)
                    self.device_port.setFocus()
                else:
                    if self.port_line.text() != self.port:
                        self.port = self.port_line.text()
                        self.portChanged.emit(self.port)
        # print(e.type())
        # if e.type() == QEvent.FocusOut:
        #     if obj == self.device_port:
        #         port = self.device_port.text()
        #         if not self.checkPort(port):
        #             QMessageBox.warning(self, "Warning", "Invalid Port!", QMessageBox.Ok)
        #             self.device_port.setText(self.port)
        #             self.device_port.setFocus()
        #         else:
        #             if self.port_line.text() != self.port:
        #                 self.port = self.port_line.text()
        #                 self.portChanged.emit(self.port)
        #     elif obj == self.bg_color:
        #         self.colorChanged.emit(self.bg_color.currentText())
        #     elif obj == self.multi_sample:
        #         print("emit sample")
        #         self.sampleChanged.emit(self.multi_sample.text())
        return QWidget.eventFilter(self, obj, e)

    def showPortTip(self, port: str):
        """
        端口有效性提示
        :param port:
        :return:
        """
        flag: bool = self.checkPort(port)

        if flag is False:
            self.port_tip.setText("Invalid Port")
        else:
            self.port_tip.setText("")
            self.portChanged.emit(port)

    def checkPort(self, port: str):
        flag: bool = True
        device_type: str = self.device_type.text()
        if device_type == "screen":
            if not port.isdigit() or int(port) > 10:
                flag = False
        elif device_type == "network_port":
            port_list = port.split(".")
            if len(port_list) == 4:
                for i in port_list:
                    if i.isdigit():
                        if int(i) < 0 or int(i) > 255:
                            flag = False
                    else:
                        flag = False
            else:
                flag = False
        elif device_type == "serial_port":
            if port.startswith("com") and port[3:].isdigit():
                pass
            else:
                flag = False
        elif device_type == "parallel_port":
            flag = port == "D010"
        return flag

    def changeSample(self, sample):
        self.sampleChanged.emit(sample)

    def changeColor(self, color):
        self.colorChanged.emit(color)
