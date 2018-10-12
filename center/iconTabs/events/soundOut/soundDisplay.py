from PyQt5.QtCore import pyqtSignal, QUrl, Qt, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QToolBar, QPushButton, QMessageBox, QSlider, QWidget, \
    QGridLayout, QLabel, QVBoxLayout

# from Info import Info
from center.iconTabs.events.soundOut.soundProperty import SoundProperty


class SoundDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, value: str=''):
        super(SoundDisplay, self).__init__(parent)
        self.value = value
        self.file = ""
        self.attributes = []
        self.volume = 100
        self.pro = SoundProperty()

        self.default_properties = self.pro.getInfo()

        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.cancel)
        self.pro.apply_bt.clicked.connect(self.apply)

        self.play_bt = QPushButton("")
        self.play_bt.setIcon(QIcon("image/start_video"))
        self.player = QMediaPlayer()
        self.player.stateChanged.connect(self.changeIcon)
        self.player.durationChanged.connect(self.changeTip)
        self.player_list = QMediaPlaylist()

        self.play_bt.setEnabled(False)
        self.player.positionChanged.connect(self.positionChanged)
        self.play_bt.clicked.connect(self.playSound)
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
        self.tip1.setText("00:00.000")
        self.tip1.setAlignment(Qt.AlignRight)
        self.tip2.setText("00:00.000")
        center = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(""), 2)
        layout.addWidget(self.play_bt, 2, Qt.AlignHCenter)
        layout.addWidget(self.tip, 1, Qt.AlignCenter)
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
        open_pro = QAction(QIcon("image/setting"), "setting", self)
        open_pro.triggered.connect(self.openPro)

        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        # self.setAttributes(Info.getAttributes(self.value))
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    def ok(self):
        self.apply()
        self.pro.close()

    def cancel(self):
        self.pro.loadSetting()

    def apply(self):
        self.getPro()
        file_name = self.pro.general.file_name.text()
        if file_name:
            # self.play_bt.setIcon(QIcon("image/start_video"))
            if QFileInfo(file_name).isFile():
                # 音频文件名
                try:
                    audio_name = ".".join(file_name.split("/")[-1].split(".")[0:-1])
                except Exception:
                    audio_name = "audio"
                # 避免重复加载文件
                if file_name != self.file:
                    self.file = file_name
                    self.player_list.clear()
                    self.player_list.addMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                    self.player.setPlaylist(self.player_list)
                    self.tip1.setText("00:00.000")
                    self.tip2.setText("00:00.000")
                    self.progress_bar.setRange(0, 0)
                # 循环播放否
                if self.is_loop:
                    self.player_list.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
                else:
                    self.player_list.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
                self.play_bt.setEnabled(True)
                self.tip.setText(audio_name)
            else:
                QMessageBox.warning(self, "Warning", "The file path is invalid!", QMessageBox.Ok)
        else:
            self.play_bt.setEnabled(False)
            self.tip.setText("Load your audio first!")

        self.propertiesChange.emit(self.getInfo())

    def getPro(self):
        if self.pro.general.loop.currentText() == "Yes":
            self.is_loop = True
        else:
            self.is_loop = False
        volume_control = self.pro.general.volume_control.checkState()
        if volume_control:
            self.volume = self.pro.general.volume.value()

    def setLabel(self):
        m = int(self.player.duration() / (1000 * 60))
        s = int(self.player.duration() / 1000 - m * 60)
        x = int(self.player.duration() % 1000)
        print(m, s, x)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeTip(self, duration):
        m = int(duration / (1000 * 60))
        s = int(duration / 1000 - m * 60)
        x = int(duration % 1000)
        self.progress_bar.setRange(0, duration)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def playSound(self):
        # print("media statue", self.player.mediaStatus())
        # print("buffer statue", self.player.bufferStatus())
        # print("audio available", self.player.isAudioAvailable())
        if not self.player.isAudioAvailable():
            self.player_list.clear()
            QMessageBox.warning(self, "Invalid Audio File", "Please open the audio file", QMessageBox.Ok)
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
            elif self.player.state() == QMediaPlayer.PausedState:
                self.player.play()
            else:
                self.player.play()
                self.player.setVolume(self.volume)

            # self.setLabel()
            # self.play_bt.setIcon(QIcon("image/pause_video"))

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
        x = position % 1000
        self.tip1.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeIcon(self, statue):
        if statue == QMediaPlayer.PlayingState:
            self.play_bt.setIcon(QIcon("image/pause_video"))
        # elif statue == QMediaPlayer.PausedState:
        #     self.play_bt.setIcon(QIcon("image/pause_video"))
        else:
            self.play_bt.setIcon(QIcon("image/start_video"))

    def getInfo(self):
        self.default_properties = self.pro.getInfo()
        return self.default_properties

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

    def setPro(self, pro: SoundProperty):
        del self.pro
        self.pro = pro
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.cancel)
        self.pro.apply_bt.clicked.connect(self.apply)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.pro_window.loadSetting()

    def clone(self, value):
        clone_widget = SoundDisplay(value=value)
        clone_widget.setPro(self.pro.clone())
        clone_widget.apply()
        return clone_widget

    def getDuration(self):
        try:
            duration = self.default_properties["Duration"]
        except KeyError:
            duration = "(Infinite)"
        return duration

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = SoundDisplay()

    t.show()

    sys.exit(app.exec())
