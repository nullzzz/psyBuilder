from PyQt5.QtCore import QObject, QEvent, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QMessageBox, QLineEdit


class Describer(QWidget):
    portChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Describer, self).__init__(parent=parent)
        self.device_type = QLabel("Unselected")
        self.device_name = QLabel("Unselected")
        self.device_port = QLineEdit("")
        self.port_tip = QLabel("")
        self.device_port.textEdited.connect(self.showPortTip)
        self.port: str = ""

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Port:", self.device_port)
        layout.addRow("", self.port_tip)
        self.setLayout(layout)

    def describe(self, device_type, device_name, device_port):
        self.device_type.setText(device_type)
        self.device_name.setText(device_name)

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
