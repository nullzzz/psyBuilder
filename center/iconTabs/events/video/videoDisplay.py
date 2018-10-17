from PyQt5.QtCore import Qt, QUrl, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QLabel, QSizePolicy

# from Info import Info
from Info import Info
from .videoProperty import VideoProperty


class VideoDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)
    getAttribute = pyqtSignal(str)

    def __init__(self, parent=None, value=''):
        super(VideoDisplay, self).__init__(parent)
        self.value = value

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.mediaStatusChanged.connect(self.loadStatue)
        self.mediaPlayer.bufferStatusChanged.connect(self.bufferLoad)
        self.video_widget = VideoWidget()

        self.mediaPlayer.setVideoOutput(self.video_widget)

        self.mediaPlayer.positionChanged.connect(self.stopPlaying)
        self.mediaPlayer.stateChanged.connect(self.changeIcon)

        self.label = QLabel()
        self.pro_window = VideoProperty()

        self.default_properties = self.pro_window.getInfo()

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.file = ""
        self.start_pos = 0
        self.end_pos = 9999999
        # self.back_color = "white"
        self.playback_rate = 1.0
        # self.transparent_value = 100
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
        self.video_widget.play_and_pause.connect(lambda: self.play_video.trigger())

        t = QAction(QIcon("image/test"), "test", self)
        t.triggered.connect(self.test)
        tool.addAction(t)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        self.getAttribute.emit(self.value)
        self.setAttributes(Info.VALUE_ATTRIBUTES[self.value])
        # 阻塞原窗口
        self.pro_window.setWindowModality(Qt.ApplicationModal)
        self.pro_window.show()

    def playVideo(self):
        if self.file:
            # 播放状态
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                # self.sender().setIcon(QIcon("image/start_video"))
                # self.sender().setText("start")
                self.mediaPlayer.pause()
            # 暂停、停止状态
            else:
                # self.sender().setIcon(QIcon("image/pause_video"))
                # self.sender().setText("pause")
                self.mediaPlayer.play()
        else:
            QMessageBox.warning(self, "No Video Error", "Please load video first!", QMessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getPro()
        file_name = self.pro_window.general.file_name.text()
        if file_name:
            self.setCentralWidget(self.video_widget)
            if QFileInfo(file_name).isFile():
                # 判断文件是否改变，避免重复加载
                if file_name != self.file:
                    self.file = file_name
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                    # self.play_video.setIcon(QIcon("image/start_video"))
                    # self.play_video.setText("start")
                self.mediaPlayer.setPosition(self.getStartTime(self.start_pos))
                self.video_widget.setAspectRatioMode(self.aspect_ration_mode)
                self.mediaPlayer.setPlaybackRate(self.playback_rate)
                # self.setWindowOpacity(self.transparent_value/100)
            else:
                QMessageBox.warning(
                    self, "Warning", "The file path is invalid!")
        # 发送信号
        self.propertiesChange.emit(self.getInfo())

    def getPro(self):
        self.start_pos = self.pro_window.general.start_pos.text()
        self.end_pos = self.getStartTime(self.pro_window.general.end_pos.text())
        # self.back_color = self.pro.general.back_color.currentText()
        self.playback_rate = float(self.pro_window.general.playback_rate.currentText())
        # self.transparent_value = self.pro.general.transparent.value()
        # isStopText = self.pro.tab1.stop_after.currentText()
        # if isStopText == "Yes":
        #     self.stop_after = True
        # else:
        #     self.stop_after = False
        # self.stop_after_mode = self.pro.tab1.stop_after_mode.currentText()

        self.aspect_ration_mode = self.pro_window.general.aspect_ratio.currentIndex() - 1
        # self.end_video_action = self.pro.tab1.end_video_action.currentText()
        self.screen_name = self.pro_window.general.screen_name.currentText()
        is_clear_after = self.pro_window.general.clear_after.currentText()
        if is_clear_after == "Yes":
            self.clear_after = True
        else:
            self.clear_after = False
        self.x_pos = self.pro_window.frame.x_pos.currentText()
        self.y_pos = self.pro_window.frame.y_pos.currentText()
        self.w_size = self.pro_window.frame.width.currentText()
        self.h_size = self.pro_window.frame.height.currentText()

    # 加载状态
    def loadStatue(self, media_statue):
        a = ["UnknownMediaStatus", "NoMedia", "LoadingMedia", "LoadedMedia",
             "StalledMedia", "BufferingMedia", "BufferedMedia", "EndOfMedia",
             "InvalidMedia"]
        # print(a[media_statue])
        # label = QLabel()
        # label.setAlignment(Qt.AlignCenter)
        # 不识别状态
        if media_statue == QMediaPlayer.UnknownMediaStatus:
            self.play_video.setEnabled(False)
            # self.setCentralWidget(label)
            self.play_video.setText("Unknown Media")
            # self.statusBar().showMessage("Unknown Media", 5000)

        # 没媒体
        elif media_statue == QMediaPlayer.NoMedia:
            self.play_video.setEnabled(False)
            # self.setCentralWidget(label)
            self.play_video.setText("No Media")
            # self.statusBar().showMessage("No Media", 5000)
        # 加载中
        elif media_statue == QMediaPlayer.LoadingMedia:
            self.play_video.setEnabled(False)
            # self.statusBar().showMessage("Loading", 5000)
            self.play_video.setText("Loading Media")

        # 加载完成
        elif media_statue == QMediaPlayer.LoadedMedia:
            self.play_video.setEnabled(True)
            # self.setCentralWidget(self.video_widget)
            self.play_video.setText("Start")
            # self.statusBar().showMessage("Loaded Media", 5000)
        # 缓冲失败
        elif media_statue == QMediaPlayer.StalledMedia:
            pass
        # 缓冲中
        elif media_statue == QMediaPlayer.BufferingMedia:
            pass
        # 缓冲完成
        elif media_statue == QMediaPlayer.BufferedMedia:
            pass
        # 播放完成
        elif media_statue == QMediaPlayer.EndOfMedia:
            pass
        # 无法播放
        elif media_statue == QMediaPlayer.InvalidMedia:
            self.play_video.setEnabled(False)
            # self.setCentralWidget(label)
            self.play_video.setText("Invalid Media")
            # self.statusBar().showMessage("Invalid Media", 5000)

    def bufferLoad(self, percentage: int):
        print(percentage)

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
        except Exception as e:
            print(e)
            return 0

    def setPro(self, pro: VideoProperty):
        del self.pro_window
        self.pro_window = pro
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def setVideo(self):
        self.setCentralWidget(self.video_widget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))

        self.mediaPlayer.setPosition(self.getStartTime(self.start_pos))
        self.video_widget.setAspectRatioMode(self.aspect_ration_mode)

    def stopPlaying(self, duration):
        if abs(self.end_pos - duration) < 1000:
            self.mediaPlayer.pause()

    def changeIcon(self, statue):
        if statue == QMediaPlayer.PlayingState:
            self.play_video.setIcon(QIcon("image/pause_video"))
            self.play_video.setText("pause")
        else:
            self.play_video.setIcon(QIcon("image/start_video"))
            self.play_video.setText("start")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.play_video.trigger()
            event.accept()
        else:
            super(VideoDisplay, self).keyPressEvent(event)

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def getInfo(self):
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties)
        self.apply()

    def loadSetting(self):
        self.pro_window.loadSetting()

    def clone(self, value):
        clone_widget = VideoDisplay(value=value)
        clone_widget.setPro(self.pro_window.clone())
        clone_widget.apply()
        # clone_widget.setVideo()
        # self.pro.tab.addTab(clone_widget, "c")
        return clone_widget

    def test(self):
        self.pro_clone = self.pro_window.clone()
        self.pro_clone.setWindowModality(Qt.ApplicationModal)
        self.pro_clone.show()

    def getDuration(self):
        try:
            duration = self.default_properties["Duration"]
        except KeyError:
            duration = "(Infinite)"
        return duration

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt":0
        }
        return hidden_attr


# 支持全屏显示
class VideoWidget(QVideoWidget):
    play_and_pause = pyqtSignal()

    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.play_and_pause.emit()
        # esc退出全屏
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            event.accept()
        # 这是啥？？？Alt+Enter？？？不管用呀
        elif event.key() == Qt.Key_Enter and event.modifiers() == Qt.Key_Alt:
            self.setFullScreen(not self.isFullScreen())
            event.accept()
        else:
            super(VideoWidget, self).keyPressEvent(event)

    # 双击打开退出全屏
    def mouseDoubleClickEvent(self, event):
        self.setFullScreen(not self.isFullScreen())
        event.accept()
