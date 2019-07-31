from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QLabel
from lib.psy_message_box import PsyMessageBox as QMessageBox

from app.func import Func
from .imageProperty import ImageProperty
from .view import Preview


class ImageDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, parent=None, widget_id: str = ""):
        super(ImageDisplay, self).__init__(parent)
        self.widget_id = widget_id
        self.current_wid = widget_id

        # 当前widget可引用属性
        self.attributes: list = []
        # 当前widget正引用属性
        self.using_attributes: list = []

        # 图片展示框
        self.label = QLabel()
        # 属性设置窗口
        self.pro_window = ImageProperty()
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        # 属性字典
        self.default_properties = self.pro_window.getInfo()

        # 相关可使用属性
        self.file = ""
        self.isStretch = False
        self.isUD = False
        self.isLR = False
        self.stretch_mode = "Both"
        self.frame_fill_color = "255,255,255"
        self.transparent_value = "0"

        self.x_pos = "0"
        self.y_pos = "0"
        self.w_size = "100"
        self.h_size = "100"
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Image")

        self.label.setText("Your image will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_pro.triggered.connect(self.openPro)
        pre_view = QAction(QIcon(Func.getImage("preview")), "preview", self)
        pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        tool.addAction(pre_view)

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
        self.pro_window.general.refresh()
        self.getInfo()

    # 预览图片
    def preView(self):
        if self.file:
            try:
                self.preview = Preview(self.file, self.pix, self.x_pos, self.y_pos, self.w_size, self.h_size)
                self.preview.setStyleSheet("background-color:{}".format(self.frame_fill_color))
                self.preview.setTransparent(int(self.transparent_value))
                self.preview.setWindowModality(Qt.ApplicationModal)
                self.preview.showFullScreen()
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.preview.close)
                self.timer.start(10000)
                self.timer.setSingleShot(True)
            except AttributeError:
                QMessageBox.warning(self, "No Image Error", "Please load image first!", QMessageBox.Ok)
            except Exception as e:
                print(e)
                print(type(e))
        else:
            QMessageBox.warning(self, "No Image Error", "Please load image first!", QMessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        self.parseProperties()
        self.label.setStyleSheet(f"background-color:{self.frame_fill_color}")
        # 加载图片文件
        if self.file:
            if QFileInfo(self.file).isFile():
                self.setImage()
            else:
                QMessageBox.warning(self, "Warning", "The file path is invalid!", QMessageBox.Ok)
        else:
            self.label.clear()
        # 发送信号
        self.propertiesChange.emit(self.default_properties)

    # 从pro获取参数
    def parseProperties(self):
        self.file = self.default_properties.get("File name", "")
        if self.file.startswith("[") and self.file.endswith("]"):
            self.file = ""
        self.isUD = self.pro_window.general.mirrorUD.checkState()
        self.isLR = self.pro_window.general.mirrorLR.checkState()
        self.isStretch = self.pro_window.general.stretch.checkState()
        self.stretch_mode = self.pro_window.general.stretch_mode.currentText()
        self.frame_fill_color = self.pro_window.frame.back_color.getColor()
        self.transparent_value = self.pro_window.general.transparent.text()
        self.x_pos = self.default_properties.get("X position", "0")
        self.y_pos = self.default_properties.get("Y position", "0")
        self.w_size = self.default_properties.get("Width", "100%")
        self.h_size = self.default_properties.get("Height", "100%")
        if self.x_pos.startswith("[") and self.x_pos.endswith("]"):
            self.x_pos = "0"
        if self.y_pos.startswith("[") and self.y_pos.endswith("]"):
            self.y_pos = "0"
        if self.w_size.startswith("[") and self.w_size.endswith("]"):
            self.w_size = "100%"
        if self.h_size.startswith("[") and self.h_size.endswith("]"):
            self.h_size = "100%"

    # 设置主面板的图片
    def setImage(self):
        img = QImage(self.file)
        image = img.mirrored(self.isLR, self.isUD)
        pix = QPixmap.fromImage(image)
        self.pix = pix
        # 图片反转
        if self.isStretch:
            mode = self.pro_window.general.stretch_mode.currentText()
            w = self.label.size().width()
            h = self.label.size().height()
            if mode == "Both":
                new_pix = pix.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            elif mode == "LeftRight":
                new_pix = pix.scaledToWidth(w, Qt.FastTransformation)
            else:
                new_pix = pix.scaledToHeight(h, Qt.FastTransformation)
            self.label.setPixmap(new_pix)
        else:
            self.label.setPixmap(pix)

    # 返回设置参数
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

    def setPro(self, pro: ImageProperty):
        del self.pro_window
        self.pro_window = pro
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    # 设置可选参数
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

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.pro_window.setProperties(self.default_properties)
            self.apply()

    def loadSetting(self):
        self.pro_window.setProperties(self.default_properties)

    # copy当前image对象
    def clone(self, new_id: str):
        clone_widget = ImageDisplay(widget_id=new_id)
        clone_widget.setPro(self.pro_window.clone())
        clone_widget.apply()
        return clone_widget

    # todo 弄啥嘞
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

    # def getBackColor(self) -> str:
    #     """
    #     返回背景颜色
    #     :return:
    #     """
    #     return self.back_color

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
