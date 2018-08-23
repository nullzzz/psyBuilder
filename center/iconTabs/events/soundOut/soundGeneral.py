from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QCheckBox, \
    QComboBox, QSpinBox, QApplication, QFileDialog, QCompleter, QMessageBox, QFormLayout


# soundOut event专属页面
class SoundTab1(QWidget):
    def __init__(self, parent=None):
        super(SoundTab1, self).__init__(parent)
        self.attributes = []
        self.file_name = QLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.volume_control = QCheckBox("Volume control")
        self.volume_control.stateChanged.connect(self.volumeChecked)
        self.volume = QSpinBox()
        self.pan_control = QCheckBox("Pan control")
        self.pan_control.stateChanged.connect(self.panChecked)
        self.pan = QSpinBox()

        self.buffer_size = QLineEdit()

        self.buffer_mode = QComboBox()

        self.position_time_format = QComboBox()

        self.start_offset = QLineEdit()
        self.stop_offset = QLineEdit()
        self.loop = QComboBox()

        self.setGeneral()

    def setGeneral(self):
        valid_input = QRegExp("(\d+)|(\[[_\d\w]+\]")
        self.start_offset.setValidator(QRegExpValidator(valid_input, self))
        self.stop_offset.setValidator(QRegExpValidator(valid_input, self))
        self.buffer_mode.addItems(["Buffered", "Streaming"])
        self.position_time_format.addItems(["MilliSeconds", "MicroSeconds", "Bytes"])
        self.loop.addItems(["Yes", "No"])
        self.buffer_size.setText("5000")
        self.start_offset.setText("0")
        self.stop_offset.setText("0")
        self.volume.setRange(-1000, 0)
        self.volume.setEnabled(False)
        self.pan.setRange(-1000, 1000)
        self.pan.setEnabled(False)
        self.buffer_size.textChanged.connect(self.findVar)
        self.start_offset.textChanged.connect(self.findVar)
        self.stop_offset.textChanged.connect(self.findVar)
        # self.volume.textChanged.connect(self.findVar)
        # self.pan.textChanged.connect(self.findVar)
        self.buffer_size.returnPressed.connect(self.finalCheck)
        self.start_offset.returnPressed.connect(self.finalCheck)
        self.stop_offset.returnPressed.connect(self.finalCheck)
        # self.volume.returnPressed.connect(self.finalCheck)
        # self.pan.returnPressed.connect(self.finalCheck)
        l0 = QLabel("File Name:")
        l1 = QLabel("Buffer size (ms):")
        l2 = QLabel("Buffer mode:")
        l3 = QLabel("Position Time Format:")
        l4 = QLabel("Start offset (ms):")
        l5 = QLabel("Stop offset (ms):")
        l6 = QLabel("Loop:")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox()
        layout1 = QGridLayout()
        layout1.addWidget(l0, 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 2)
        layout1.addWidget(self.open_bt, 0, 3, 1, 1)

        layout1.addWidget(l1, 1, 0)
        layout1.addWidget(self.buffer_size, 1, 1)

        layout1.addWidget(l2, 2, 0)
        layout1.addWidget(self.buffer_mode, 2, 1)

        layout1.addWidget(l3, 3, 0)
        layout1.addWidget(self.position_time_format, 3, 1)
        layout1.addWidget(l4, 4, 0)
        layout1.addWidget(self.start_offset, 4, 1)
        layout1.addWidget(l5, 5, 0)
        layout1.addWidget(self.stop_offset, 5, 1)

        layout1.addWidget(l6, 6, 0)
        layout1.addWidget(self.loop, 6, 1)
        group1.setLayout(layout1)

        group2 = QGroupBox()
        layout2 = QFormLayout()
        layout2.addRow(self.volume_control)
        layout2.addRow("\tvolume:", self.volume)
        layout2.addRow(self.pan_control)
        layout2.addRow("\tpan", self.pan)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1, 2)
        layout.addWidget(group2, 1)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the sound file)", self.file_name.text(),
                                                   "Sound File (*)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def volumeChecked(self, e):
        if e == 2:
            self.volume.setEnabled(True)
        else:
            self.volume.setEnabled(False)

    def panChecked(self, e):
        if e == 2:
            self.pan.setEnabled(True)
        else:
            self.pan.setEnabled(False)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
        else:
            self.sender().setStyleSheet("color: black")

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.buffer_size.setCompleter(QCompleter(self.attributes))
        self.start_offset.setCompleter(QCompleter(self.attributes))
        self.stop_offset.setCompleter(QCompleter(self.attributes))
        self.volume.setCompleter(QCompleter(self.attributes))
        self.pan.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        return {
            "File name": self.file_name.text(),
            "Buffer size": "{}ms".format(self.buffer_size.text()),
            "Buffer mode": self.buffer_mode.currentText(),
            "Start offset": "{}ms".format(self.start_offset.text()),
            "Stop offset": "{}ms".format(self.stop_offset.text()),
            "Loop": self.loop.currentText(),
            "Volume control": bool(self.volume_control.checkState()),
            "Volume": self.volume.value(),
            "Pan control": bool(self.pan_control.checkState()),
            "Pan": self.pan.value()
        }


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = SoundTab1()

    t.show()

    sys.exit(app.exec())
