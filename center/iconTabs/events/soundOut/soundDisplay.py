from PyQt5.QtCore import pyqtSignal, QUrl, Qt, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QToolBar, QPushButton, QMessageBox, QSlider, QWidget, \
    QGridLayout, QLabel, QVBoxLayout

from center.iconTabs.events.soundOut.soundProperty import SoundProperty


class SoundDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(SoundDisplay, self).__init__(parent)

        self.attributes = []
        self.volume = 1
        self.pro = SoundProperty()
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.pro.close)
        self.pro.apply_bt.clicked.connect(self.apply)

        self.file = ""
        self.play_bt = QPushButton("")
        self.play_bt.setIcon(QIcon(".\\.\\image\\start_video"))
        self.player = QMediaPlayer()
        self.play_bt.setEnabled(False)
        self.player.positionChanged.connect(self.positionChanged)
        self.play_bt.clicked.connect(self.play)
        self.progress_bar = QSlider()
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.sliderMoved.connect(self.setPosition)
        self.tip = QLabel()
        self.tip1 = QLabel()
        self.tip2 = QLabel()

        self.setUI()

    def setUI(self):
        self.setWindowTitle("SoundDisplay")
        self.play_bt.setFixedSize(120, 120)
        self.play_bt.setMaximumHeight(120)
        self.play_bt.setMinimumHeight(120)
        self.play_bt.setMaximumWidth(120)
        self.play_bt.setMinimumWidth(120)
        self.tip.setMaximumHeight(20)
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.setText("Load your audio first!")
        self.tip1.setText("00:00")
        self.tip1.setAlignment(Qt.AlignRight)
        self.tip2.setText("00:00")
        center = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(""), 2)
        layout.addWidget(self.play_bt, 2, Qt.AlignHCenter)
        layout.addWidget(self.tip, 1, Qt.AlignCenter)
        # layout.setVerticalSpacing(0)
        layout2 = QGridLayout()
        layout2.addWidget(self.progress_bar, 0, 1, 1, 4)
        layout2.addWidget(self.tip1, 0, 0, 1, 1)
        layout2.addWidget(self.tip2, 0, 5, 1, 1)
        layout2.setHorizontalSpacing(10)

        layout.addLayout(layout2)
        layout.addWidget(QLabel(), 2)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 40, 10, 40)
        center.setLayout(layout)
        self.setCentralWidget(center)

        tool = QToolBar()
        open_pro = QAction(QIcon(".\\.\\image\\setting"), "setting", self)
        open_pro.triggered.connect(self.openPro)

        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    def ok(self):
        self.apply()
        self.pro.close()

    def apply(self):
        self.file = self.pro.general.file_name.text()
        volume_control = self.pro.general.volume_control.checkState()
        if volume_control:
            self.volume = self.pro.general.volume.value()
        if self.file:
            self.play_bt.setIcon(QIcon(".\\.\\image\\start_video"))
            if QFileInfo(self.file).isFile():
                # 文件名
                try:
                    file_name = ".".join(self.file.split("/")[-1].split(".")[0:-1])
                except Exception:
                    file_name = "audio"
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                self.play_bt.setEnabled(True)
                self.tip.setText(file_name)
            else:
                QMessageBox.warning(self, "Warning", "The file path is invalid!", QMessageBox.Ok)
            self.propertiesChange.emit(self.getInfo())
        else:
            self.play_bt.setEnabled(False)
            self.tip.setText("Load your audio first!")
        self.tip1.setText("00:00")
        self.tip2.setText("00:00")
        self.progress_bar.setRange(0, 0)

        self.propertiesChange.emit(self.getInfo())

    def setLabel(self):
        m = int(self.player.duration() / (1000 * 60))
        s = int(self.player.duration() / 1000 - m * 60)
        self.tip2.setText('{:0>2d}:{:0>2d}'.format(m, s))

    def play(self):
        if self.player.state() == 1:
            self.player.pause()
            self.play_bt.setIcon(QIcon(".\\.\\image\\start_video"))
        else:
            self.player.play()
            # self.player.setVolume(self.volume)
            self.progress_bar.setRange(0, self.player.duration())
            self.setLabel()
            self.play_bt.setIcon(QIcon(".\\.\\image\\pause_video"))

    # 拖动进度
    def setPosition(self, position):
        self.player.setPosition(position)
        m = int(position/(1000*60))
        s = int(position/1000-m*60)
        self.tip1.setText('{:0>2d}:{:0>2d}'.format(m, s))

    # 按进度移动
    def positionChanged(self, position):
        self.progress_bar.setValue(position)
        m = int(position/(1000*60))
        s = int(position/1000-m*60)
        self.tip1.setText('{:0>2d}:{:0>2d}'.format(m, s))

    def getInfo(self):
        return {**self.pro.general.getInfo(), **self.pro.duration.getInfo()}

    # 设置输入输出设备
    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro.duration.in_devices_dialog.addDevices(devices)

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro.setAttributes(format_attributes)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = SoundDisplay()

    t.show()

    sys.exit(app.exec())