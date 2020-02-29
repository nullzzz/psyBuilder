from PyQt5.QtCore import Qt, QUrl, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QSizePolicy

from app.func import Func
from lib import MessageBox, TabItemMainWindow
from .videoProperty import VideoProperty


class VideoDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(VideoDisplay, self).__init__(widget_id, widget_name)
        self.attributes: set = ()

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

        self.file: str = ""
        self.start_pos = 0
        self.end_pos = 9999999
        self.playback_rate = 1.0
        self.aspect_ration_mode = -1

        self.setUI()
        self.setAttributes(["test"])

    def setUI(self):
        self.setWindowTitle("Video")
        self.label.setText("Your video will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImagePath("setting")), "setting", self)
        open_pro.triggered.connect(self.openPro)
        tool.addAction(open_pro)

        self.play_video = QAction(QIcon(Func.getImagePath("start_video")), "start", self)
        self.play_video.triggered.connect(self.playVideo)
        tool.addAction(self.play_video)
        self.video_widget.play_and_pause.connect(lambda: self.play_video.trigger())

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        self.refresh()
        # 阻塞原窗口
        # self.pro_window.setWindowModality(Qt.ApplicationModal)
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.pro_window.refresh()
        self.getInfo()

    def playVideo(self):
        if self.file:
            # 播放状态
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            # 暂停、停止状态
            else:
                self.mediaPlayer.play()
        else:
            MessageBox.warning(self, "No Video Error", "Please load video first!", MessageBox.Ok)

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
            self.setCentralWidget(self.video_widget)
            if QFileInfo(file_name).isFile():
                # 判断文件是否改变，避免重复加载
                if file_name != self.file:
                    self.file = file_name
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                self.mediaPlayer.setPosition(self.getStartTime(self.start_pos))
                self.video_widget.setAspectRatioMode(self.aspect_ration_mode)
                self.mediaPlayer.setPlaybackRate(self.playback_rate)
            else:
                MessageBox.warning(self, "Warning", "The file path is invalid!")
        # 发送信号
        self.propertiesChanged.emit(self.getInfo())

    def parseProperties(self):
        self.start_pos = self.getStartTime(self.default_properties.get("Start position", "00:00:00.000"))
        self.end_pos = self.getStartTime(self.default_properties.get("End position", "99:99:99.999"))
        self.playback_rate = float(self.default_properties.get("Playback rate", "1"))
        self.aspect_ration_mode = self.default_properties.get("Aspect ratio", "Default")
        if self.aspect_ration_mode == "Default":
            self.aspect_ration_mode = -1
        elif self.aspect_ration_mode == "Ignore":
            self.aspect_ration_mode = 0
        elif self.aspect_ration_mode == "Keep":
            self.aspect_ration_mode = 1
        elif self.aspect_ration_mode == "KeepByExpanding":
            self.aspect_ration_mode = 2

    # 加载状态
    def loadStatue(self, media_statue):
        """
        UnknownMediaStatus, NoMedia, LoadingMedia, LoadedMedia, StalledMedia,
        BufferingMedia, BufferedMedia, EndOfMedia, InvalidMedia
        """
        # 不识别状态
        if media_statue == QMediaPlayer.UnknownMediaStatus:
            self.play_video.setEnabled(False)
            # self.setCentralWidget(label)
            self.play_video.setText("Unknown Media")  # self.statusBar().showMessage("Unknown Media", 5000)

        # 没媒体
        elif media_statue == QMediaPlayer.NoMedia:
            self.play_video.setEnabled(False)
            self.play_video.setText("No Media")
        # 加载中
        elif media_statue == QMediaPlayer.LoadingMedia:
            self.play_video.setEnabled(False)
            self.play_video.setText("Loading Media")
        # 加载完成
        elif media_statue == QMediaPlayer.LoadedMedia:
            self.play_video.setEnabled(True)
            self.play_video.setText("Start")
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
            self.play_video.setText("Invalid Media")

    def bufferLoad(self, percentage: int):
        print(percentage)

    def getShowProperties(self):
        info = self.default_properties.copy()
        info.pop("Input devices")
        info.pop("Output devices")
        return info

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
            self.play_video.setIcon(QIcon(Func.getImagePath("pause_video")))
            self.play_video.setText("pause")
        else:
            self.play_video.setIcon(QIcon(Func.getImagePath("start_video")))
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

    def getProperties(self):
        return self.getInfo()

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.setProperties(self.default_properties)
            self.apply()

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
            self.apply()

    def loadSetting(self):
        self.pro_window.setProperties(self.default_properties)

    def clone(self, new_id: str):
        clone_widget = VideoDisplay(widget_id=new_id)
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

    def getStartPosition(self) -> str:
        """
        返回开始位置（hh:mm:ss.xxx）
        :return:
        """
        return self.pro_window.general.start_pos.text()

    def getEndPosition(self) -> str:
        """
        返回结束位置（hh:mm:ss.xxx）
        :return:
        """
        return self.pro_window.general.end_pos.text()

    def getPlaybackRate(self) -> str:
        """
        返回播放速率
        :return:
        """
        return self.pro_window.general.playback_rate.currentText()

    def getAspectRatio(self) -> str:
        """
        返回图像拉伸模式
        :return:
        """
        return self.pro_window.general.aspect_ratio.currentText()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getIsClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.pro_window.frame.x_pos.currentText()

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.pro_window.frame.y_pos.currentText()

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.pro_window.frame.width.currentText()

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.pro_window.frame.height.currentText()

    def getEnable(self) -> str:
        """
        返回frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """返回frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getBorderColor(self) -> str:
        """
        返回边框颜色
        :return:
        """
        return self.pro_window.frame.border_color.currentText()

    def getBorderWidth(self) -> str:
        """
        返回边框宽度
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameBackColor(self) -> str:
        """
        返回边框背景色
        :return:
        """
        return self.pro_window.frame.back_color.getColor()

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
