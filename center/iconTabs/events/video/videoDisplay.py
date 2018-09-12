from PyQt5.QtCore import Qt, QUrl, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QLabel

from .videoProperty import VideoProperty


class VideoDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(VideoDisplay, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.mediaStatusChanged.connect(self.loadStatue)
        self.video_widget = QVideoWidget()

        self.mediaPlayer.setVideoOutput(self.video_widget)

        self.label = QLabel()
        self.pro = VideoProperty()
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.pro.close)
        self.pro.apply_bt.clicked.connect(self.apply)

        self.file = ""
        self.startPos = 0
        self.endPos = 0
        self.back_color = "white"
        self.transparent_value = 0
        # self.stop_after = False
        # self.stop_after_mode = "OffsetTime"
        # self.is_stretch = False
        # self.stretch_mode = "Both"
        self.aspect_ration_mode = -1
        # self.end_video_action = "none"
        self.screen_name = "Display"
        self.clear_after = "Yes"

        self.x_pos = 0
        self.y_pos = 0
        self.w_size = 100
        self.h_size = 100
        self.setUI()
        self.setAttributes(["test"])

    def setUI(self):
        self.setWindowTitle("Video")
        self.label.setText("Your video will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

        tool = QToolBar()
        open_pro = QAction(QIcon("image/setting"), "setting", self)
        open_pro.triggered.connect(self.openPro)
        tool.addAction(open_pro)

        self.play_video = QAction(QIcon("image/start_video"), "start", self)
        self.play_video.triggered.connect(self.playVideo)
        tool.addAction(self.play_video)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    def playVideo(self):
        if self.file:
            # 播放状态
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.sender().setIcon(QIcon("image/start_video"))
                self.sender().setText("start")
                self.mediaPlayer.pause()
            # 暂停、停止状态
            else:
                self.sender().setIcon(QIcon("image/pause_video"))
                self.sender().setText("pause")
                self.mediaPlayer.play()
        else:
            QMessageBox.warning(self, "No Video Error", "Please load video first!", QMessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro.close()

    def apply(self):
        self.getPro()
        file_name = self.pro.general.file_name.text()
        if file_name:
            self.setCentralWidget(self.video_widget)
            if QFileInfo(file_name).isFile():
                # 判断文件是否改变，避免重复加载
                if file_name != self.file:
                    self.file = file_name
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                    self.play_video.setIcon(QIcon("image/start_video"))
                    self.play_video.setText("start")
                self.mediaPlayer.setPosition(self.getStartTime(self.startPos))
                self.video_widget.setAspectRatioMode(self.aspect_ration_mode)
            else:
                QMessageBox.warning(
                    self, "Warning", "The file path is invalid!")
        # 发送信号
        self.propertiesChange.emit(self.getInfo())

    def getPro(self):
        self.startPos = self.pro.general.startPos.text()
        self.endPos = self.pro.general.endPos.text()
        self.back_color = self.pro.general.back_color.currentText()
        self.transparent_value = self.pro.general.transparent.value()
        # isStopText = self.pro.tab1.stop_after.currentText()
        # if isStopText == "Yes":
        #     self.stop_after = True
        # else:
        #     self.stop_after = False
        # self.stop_after_mode = self.pro.tab1.stop_after_mode.currentText()

        self.aspect_ration_mode = self.pro.general.aspect_ratio.currentIndex() - 1
        # self.end_video_action = self.pro.tab1.end_video_action.currentText()
        self.screen_name = self.pro.general.screen_name.currentText()
        is_clear_after = self.pro.general.clear_after.currentText()
        if is_clear_after == "Yes":
            self.clear_after = True
        else:
            self.clear_after = False
        self.x_pos = self.pro.frame.x_pos.currentText()
        self.y_pos = self.pro.frame.y_pos.currentText()
        self.w_size = self.pro.frame.width.currentText()
        self.h_size = self.pro.frame.height.currentText()

    # 加载状态
    def loadStatue(self, media_statue):
        # 加载中、不识别状态
        if media_statue == QMediaPlayer.LoadingMedia or media_statue == QMediaPlayer.UnknownMediaStatus:
            self.play_video.setEnabled(False)
        else:
            self.play_video.setEnabled(True)
            buffer = self.mediaPlayer.mediaStream()

    @staticmethod
    def getStartTime(str_time):
        try:
            h = int(str_time[0:2])
            m = int(str_time[3:5])
            s = int(str_time[6:8])
            x = int(str_time[9:12])
            return h * 60 * 60 * 1000 + m * 60 * 1000 + s * 1000 + x
        except ValueError:
            return 0

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro.setAttributes(format_attributes)

    def getInfo(self):
        return {**self.pro.general.getInfo(), **self.pro.frame.getInfo(), **self.pro.duration.getInfo()}
