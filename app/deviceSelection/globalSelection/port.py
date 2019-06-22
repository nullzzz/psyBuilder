from PyQt5.QtCore import QObject, QEvent, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QFormLayout, QLabel, QWidget


class ItemWidget(QWidget):
    portChanged = pyqtSignal(str)

    def __init__(self, item_type: str, parent=None):
        super(ItemWidget, self).__init__(parent)
        self.name_label = QLabel()
        self.port = "127.0.0.1"
        self.port_line = QLineEdit()
        self.port_line.setText(self.port)
        self.port_line.textChanged.connect(self.setPort)

        self.port_line.installEventFilter(self)

        layout = QFormLayout()
        layout.addRow("Type:", QLabel(item_type))
        layout.addRow("Name:", self.name_label)
        layout.addRow("Port:", self.port_line)
        self.setLayout(layout)

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.port_line:
            if e.type() == QEvent.FocusOut:
                port = self.port_line.text()
                if not self.checkPort(port):
                    QMessageBox.warning(self, "Warning", "Invalid Port!", QMessageBox.Ok)
                    self.port_line.setText(self.port)
                    self.port_line.setFocus()
                else:
                    if self.port_line.text() != self.port:
                        self.port = self.port_line.text()
                        self.portChanged.emit(self.port)
        return QWidget.eventFilter(self, obj, e)

    def setPort(self, port: str):
        if self.checkPort(port):
            self.port = port
            self.port_line.setText(port)

    @staticmethod
    def checkPort(port: str):
        port_list = port.split(".")
        if len(port_list) == 4:
            for i in port_list:
                if i.isdigit():
                    if int(i) < 0 or int(i) > 255:
                        return False
                else:
                    return False
            return True
        else:
            return False
