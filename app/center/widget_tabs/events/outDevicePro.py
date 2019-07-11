from PyQt5.QtCore import QRegExp, Qt, QObject, QEvent, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QMessageBox, QCompleter

from app.lib import PigLineEdit, PigComboBox


class OutDeviceInfoAtDuration(QWidget):
    valueOrMessageChanged = pyqtSignal(str)
    pulseDurationChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.attributes = []

        self.value = PigLineEdit()
        self.value.textChanged.connect(lambda x: self.valueOrMessageChanged.emit(x))
        self.pulse_dur = PigComboBox()
        self.pulse_dur.setEditable(True)
        self.pulse_dur.setInsertPolicy(QComboBox.NoInsert)
        self.pulse_dur.addItems(["End of Duration", "10", "20", "30", "40", "50"])

        valid_num = QRegExp("\[\w+\]|\d+|End of Duration")
        self.pulse_dur.setValidator(QRegExpValidator(valid_num))
        self.pulse_dur.lineEdit().textChanged.connect(lambda x: self.pulseDurationChanged.emit(x))

        self.value.installEventFilter(self)
        self.pulse_dur.installEventFilter(self)

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Value or Msg:", self.value)
        layout.addRow("Pulse Dur:", self.pulse_dur)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 20, 10, 0)
        self.setLayout(layout)

    def showInfo(self, value: tuple):
        v, p = value
        self.value.setText(v)
        self.pulse_dur.setCurrentText(p)

    def setAttributes(self, attributes):
        self.value.setCompleter(QCompleter(self.attributes))
        self.pulse_dur.setCompleter(QCompleter(self.attributes))

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.pulse_dur:
            if e.type() == QEvent.FocusOut:
                text = self.pulse_dur.currentText()
                if text not in self.attributes:
                    if text and text[0] == "[":
                        QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                        self.pulse_dur.setCurrentIndex(0)
        return QWidget.eventFilter(self, obj, e)
