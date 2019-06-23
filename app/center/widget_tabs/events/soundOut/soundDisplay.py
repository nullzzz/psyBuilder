from PyQt5.QtCore import pyqtSignal, QUrl, Qt, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QToolBar, QPushButton, QMessageBox, QSlider, QWidget, \
    QGridLayout, QLabel, QVBoxLayout

from app.center.widget_tabs.events.soundOut.soundProperty import SoundProperty
from app.func import Func


class SoundDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, widget_id: str = ''):
        super(SoundDisplay, self).__init__(parent)
        self.widget_id = widget_id
        self.attributes = []

        self.file: str = ""
        self.is_loop: bool = False

        self.volume: int = 100
        self.pro_window = SoundProperty()

        self.default_properties = self.pro_window.getInfo()

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.play_bt = QPushButton("")
        self.play_bt.setIcon(QIcon(Func.getImage("start_video")))
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
        open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_pro.triggered.connect(self.openPro)

        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        # 阻塞原窗口
        # self.pro_window.setWindowModality(Qt.ApplicationModal)
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.parseProperties()
        file_name = self.pro_window.general.file_name.text()
        if file_name.startswith("["):
            file_name = ""
            self.file = ""
        if file_name:
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

    def parseProperties(self):
        if self.pro_window.general.loop.currentText() == "Yes":
            self.is_loop = True
        else:
            self.is_loop = False
        volume_control = self.pro_window.general.volume_control.checkState()
        if volume_control:
            volume_ = self.pro_window.general.volume.text()
            if volume_.isdigit():
                self.volume = int(volume_)

    def setLabel(self):
        m = int(self.player.duration() / (1000 * 60))
        s = int(self.player.duration() / 1000 - m * 60)
        x = int(self.player.duration() % 1000)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeTip(self, duration):
        m = int(duration / (1000 * 60))
        s = int(duration / 1000 - m * 60)
        x = int(duration % 1000)
        self.progress_bar.setRange(0, duration)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def playSound(self):
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

    # 拖动进度
    def setPosition(self, position):
        self.player.setPosition(position)
        m = int(position / (1000 * 60))
        s = int(position / 1000 - m * 60)
        self.tip1.setText('{:0>2d}:{:0>2d}'.format(m, s))

    # 按进度移动
    def positionChanged(self, position):
        self.progress_bar.setValue(position)
        m = int(position / (1000 * 60))
        s = int(position / 1000 - m * 60)
        x = position % 1000
        self.tip1.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeIcon(self, statue):
        if statue == QMediaPlayer.PlayingState:
            self.play_bt.setIcon(QIcon(Func.getImage("pause_video")))
        else:
            self.play_bt.setIcon(QIcon(Func.getImage("pause_video")))

    def getInfo(self):
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
            self.apply()

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setPro(self, pro: SoundProperty):
        del self.pro_window
        self.pro_window = pro
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.setProperties(self.default_properties)
            self.apply()

    def loadSetting(self):
        self.pro_window.setProperties(self.default_properties)

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        print(using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def clone(self, new_id: str):
        clone_widget = SoundDisplay(widget_id=new_id)
        clone_widget.setPro(self.pro_window.clone())
        clone_widget.apply()
        return clone_widget

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {"onsettime": 0, "acc": 0, "resp": 0, "rt": 0}
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

    # 返回各项参数
    # 大部分以字符串返回，少数点击选择按钮返回布尔值
    # 因为有些地方引用Attribute
    def getFilename(self) -> str:
        """
        返回图片文件名（绝对路径）
        :return:
        """
        return self.file

    def getBufferSize(self) -> str:
        """
        返回Buffer Size(ms)
        :return:
        """
        return self.pro_window.general.buffer_size.text()

    def getBufferMode(self) -> str:
        """
        返回Buffer Mode
        :return:
        """
        return self.pro_window.general.buffer_mode.currentText()

    def getStartOffset(self) -> str:
        """
        返回Start Offset
        :return:
        """
        return self.pro_window.general.start_offset.text()

    def getStopOffset(self) -> str:
        """
        返回Stop Offset
        :return:
        """
        return self.pro_window.general.stop_offset.text()

    def getLoop(self) -> str:
        """
        返回Loop
        :return:
        """
        return self.pro_window.general.loop.currentText()

    def getIsVolumeControl(self) -> bool:
        """
        返回音量控制
        :return:
        """
        return bool(self.pro_window.general.volume_control.checkState())

    def getVolume(self) -> str:
        """
        返回音量
        :return:
        """
        return self.pro_window.general.volume.text()

    def getIsPanControl(self) -> bool:
        """
        返回Pan控制
        :return:
        """
        return bool(self.pro_window.general.pan_control.checkState())

    def getPan(self) -> str:
        """
        返回pan
        :return:
        """
        return self.pro_window.general.pan.text()

    def getDuration(self) -> str:
        """
        返回duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        返回输出设备
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input devices", {})

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = SoundDisplay()

    t.show()

    sys.exit(app.exec())