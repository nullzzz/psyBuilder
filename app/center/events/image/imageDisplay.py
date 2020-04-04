from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QMessageBox

from app.func import Func
from lib import TabItemMainWindow
from .imageProperty import ImageProperty


class ImageDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(ImageDisplay, self).__init__(widget_id, widget_name)
        # 图片展示框
        self.label = QLabel()
        # 属性设置窗口
        self.pro_window = ImageProperty()
        self.default_properties = self.pro_window.default_properties
        # 相关可使用属性
        # self.file = ""
        # self.isStretch = False
        # self.isUD = False
        # self.isLR = False
        # self.stretch_mode = "Both"
        # self.frame_fill_color = "255,255,255"
        # self.transparent_value = "0"
        #
        # self.x_pos = "50%"
        # self.y_pos = "50%"
        # self.w_size = "100%"
        # self.h_size = "100%"
        self.setUI()
        self.linkSignal()

    def setUI(self):
        """
        UI part, necessary
        :return:
        """
        self.setWindowTitle("Image")

        self.label.setText("Your image will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        preview = QAction(QIcon(Func.getImage("preview")), "preview", self)
        preview.triggered.connect(self.preview)
        tool.addAction(open_pro)
        tool.addAction(preview)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def linkSignal(self):
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def preview(self):
        QMessageBox.warning(self, "undo", "refactoring")

    def refresh(self):
        """
        refresh some information that may change such device name.
        this function will be called when the properties window opened or getting the properties.
        :return:
        """
        self.pro_window.refresh()

    # 预览图片
    # def preView(self):
    #     if self.file:
    #         try:
    #             self.preview = Preview(self.file, self.pix, self.x_pos, self.y_pos, self.w_size, self.h_size)
    #             self.preview.setStyleSheet("background-color:{}".format(self.frame_fill_color))
    #             self.preview.setTransparent(int(self.transparent_value))
    #             self.preview.setWindowModality(Qt.ApplicationModal)
    #             self.preview.showFullScreen()
    #             self.timer = QtCore.QTimer()
    #             self.timer.timeout.connect(self.preview.close)
    #             self.timer.start(10000)
    #             self.timer.setSingleShot(True)
    #         except AttributeError:
    #             MessageBox.warning(self, "No Image Error", "Please load image first!", MessageBox.Ok)
    #         except Exception as e:
    #             print(e)
    #             print(type(e))
    #     else:
    #         MessageBox.warning(self, "No Image Error", "Please load image first!", MessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        # 发送信号
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)

    # 从pro获取参数
    # def parseProperties(self):
    #     self.file = self.info.get("File name", "")
    #     if self.file.startswith("[") and self.file.endswith("]"):
    #         self.file = ""
    #     self.isUD = self.pro_window.general.mirrorUD.checkState()
    #     self.isLR = self.pro_window.general.mirrorLR.checkState()
    #     self.isStretch = self.pro_window.general.stretch.checkState()
    #     self.stretch_mode = self.pro_window.general.stretch_mode.currentText()
    #     self.frame_fill_color = self.pro_window.frame.back_color.getColor()
    #     self.transparent_value = self.pro_window.general.transparent.text()
    #     self.x_pos = self.info.get("Center X", "50%")
    #     self.y_pos = self.info.get("Center Y", "50%")
    #     self.w_size = self.info.get("Width", "100%")
    #     self.h_size = self.info.get("Height", "100%")
    #     if self.x_pos.startswith("[") and self.x_pos.endswith("]"):
    #         self.x_pos = "50%"
    #     if self.y_pos.startswith("[") and self.y_pos.endswith("]"):
    #         self.y_pos = "50%"
    #     if self.w_size.startswith("[") and self.w_size.endswith("]"):
    #         self.w_size = "100%"
    #     if self.h_size.startswith("[") and self.h_size.endswith("]"):
    #         self.h_size = "100%"

    # 设置主面板的图片
    # def setImage(self):
    #     img = QImage(self.file)
    #     image = img.mirrored(self.isLR, self.isUD)
    #     pix = QPixmap.fromImage(image)
    #     self.pix = pix
    #     # 图片反转
    #     if self.isStretch:
    #         mode = self.pro_window.general.stretch_mode.currentText()
    #         w = self.label.size().width()
    #         h = self.label.size().height()
    #         if mode == "Both":
    #             new_pix = pix.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    #         elif mode == "LeftRight":
    #             new_pix = pix.scaledToWidth(w, Qt.FastTransformation)
    #         else:
    #             new_pix = pix.scaledToHeight(h, Qt.FastTransformation)
    #         self.label.setPixmap(new_pix)
    #     else:
    #         self.label.setPixmap(pix)

    def updateInfo(self):
        self.pro_window.updateInfo()

    def setProperties(self, properties: dict):
        """
        {
        "":{}
        "":{}
        }
        :param properties:
        :return:
        """
        self.default_properties.update(properties)
        self.pro_window.setProperties(self.default_properties)
        self.apply()

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        self.refresh()
        properties = {}
        for k, v in self.pro_window.getProperties().items():
            if not isinstance(v, dict):
                properties[k] = v
        return properties

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name: str):
        clone_widget = ImageDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        clone_widget.apply()
        return clone_widget

    ##########################################
    # return single attribute
    # most of them return string
    # you can see this as a document。
    ##########################################
    def getFilename(self) -> str:
        """
        返回图片文件名（绝对路径）
        :return:
        """
        return self.file

    def getIsMirrorUpAndDown(self) -> bool:
        """
        返回图片是否上下镜像
        :return:
        """
        return self.isUD

    def getIsMirrorLeftAndRight(self) -> bool:
        """
        返回图片是否左右镜像
        :return:
        """
        return self.isLR

    def getStretchMode(self) -> str:
        """
        返回图像拉伸模式
        未拉伸返回0
        上下拉伸返回1
        左右拉伸返回2
        全拉伸返回3
        :return: ""、Both、LeftRight、UpDown、[attr]
        """
        if self.isStretch:
            return self.stretch_mode
        return ""

    def getTransparent(self) -> str:
        """
        返回图像透明度
        :return:
        """
        return self.transparent_value

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getRotate(self) -> str:
        """
        返回Rotate
        :return:
        """
        return self.pro_window.general.rotate.text()

    def getEnable(self) -> str:
        """
        返回frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """返回frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.x_pos

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.y_pos

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.w_size

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.h_size

    def getBorderColor(self) -> str:
        """
        返回边框颜色
        :return:
        """
        return self.pro_window.frame.border_color.getColor()

    def getBorderWidth(self) -> str:
        """
        返回边框宽度
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameFillColor(self) -> str:
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
