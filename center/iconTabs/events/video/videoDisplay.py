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
        self.videoWidget = QVideoWidget()

        self.mediaPlayer.setVideoOutput(self.videoWidget)

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
        self.stop_after = False
        self.stop_after_mode = "OffsetTime"
        self.stretch = False
        self.stretch_mode = "Both"
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
        open_pro = QAction(QIcon(".\\.\\image\\setting"), "setting", self)
        open_pro.triggered.connect(self.open_pro)
        tool.addAction(open_pro)

        play_video = QAction(QIcon(".\\.\\image\\start_video"), "start", self)
        play_video.triggered.connect(self.playVideo)
        tool.addAction(play_video)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def open_pro(self):
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    def playVideo(self):
        if self.file:
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.sender().setIcon(QIcon(".\\.\\image\\start_video"))
                self.sender().setText("start")
                self.mediaPlayer.pause()
            elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
                self.sender().setIcon(QIcon(".\\.\\image\\pause_video"))
                self.sender().setText("pause")
                self.mediaPlayer.play()
            else:
                print("error: the media file is wrong [videoDisplay]")
        else:
            QMessageBox.warning(self, "No Video Error", "Please load video first!", QMessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro.close()

    def apply(self):
        self.getPro()
        if self.file:
            self.setCentralWidget(self.videoWidget)
            if QFileInfo(self.file).isFile():
                try:
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                    self.mediaPlayer.setPosition(self.getStartTime(self.startPos))
                except Exception as e:
                    print(e)
            else:
                QMessageBox.warning(
                    self, "Warning", "The file path is invalid!")
        # 发送信号
        self.propertiesChange.emit(self.getInfo())

    def getPro(self):
        self.file = self.pro.general.file_name.text()
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
        isStretchText = self.pro.general.stretch.currentText()
        if isStretchText == "Yes":
            self.stretch = True
        else:
            self.stretch = False
        self.stretch_mode = self.pro.general.stretch_mode.currentText()
        # self.end_video_action = self.pro.tab1.end_video_action.currentText()
        self.screen_name = self.pro.general.screen_name.currentText()
        isClearText = self.pro.general.clear_after.currentText()
        if isClearText == "Yes":
            self.clear_after = True
        else:
            self.clear_after = False
        self.x_pos = self.pro.frame.x_pos.currentText()
        self.y_pos = self.pro.frame.y_pos.currentText()
        self.w_size = self.pro.frame.width.currentText()
        self.h_size = self.pro.frame.height.currentText()

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
