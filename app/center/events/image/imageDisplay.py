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
        # todo: preview of image
        QMessageBox.warning(self, "undo", "refactoring")

    def refresh(self):
        self.pro_window.refresh()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        # 发送信号
        self.updateInfo()
        self.propertiesChanged.emit(self.widget_id)

    def updateInfo(self):
        self.pro_window.updateInfo()

    def setAttributes(self, attributes: list):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setProperties(self, properties: dict):
        """
        {
        "":{}
        "":{}
        }
        :param properties:
        :return:
        """
        self.pro_window.setProperties(properties)
        self.apply()

    def getProperties(self) -> dict:
        return self.pro_window.getProperties()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        self.updateInfo()
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name: str):
        self.updateInfo()
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
        return self.default_properties.get("General").get("File Name")

    def getIsMirrorUpAndDown(self) -> bool:
        """
        返回图片是否上下镜像
        :return:
        """
        return self.default_properties.get("General").get("Mirror Up/Down")

    def getIsMirrorLeftAndRight(self) -> bool:
        """
        返回图片是否左右镜像
        :return:
        """
        return self.default_properties.get("General").get("Mirror Left/Aright")

    def getRotate(self) -> str:
        """
        返回Rotate
        :return:
        """
        return self.default_properties.get("General").get("Rotate")

    def getStretchMode(self) -> str:
        """
        返回图像拉伸模式
        未拉伸返回0
        上下拉伸返回1
        左右拉伸返回2
        全拉伸返回3
        :return: ""、Both、LeftRight、UpDown、[attr]
        """
        if self.default_properties.get("General").get("Stretch"):
            return self.default_properties.get("General").get("Stretch Mode")
        return ""

    def getTransparent(self) -> str:
        """
        返回图像透明度
        :return:
        """
        return self.default_properties.get("General").get("Transparent")

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.default_properties.get("General").get("Clear After")

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.default_properties.get("General").get("Screen Name")

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.default_properties.get("Frame").get("Center X")

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.default_properties.get("Frame").get("Center Y")

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.default_properties.get("Frame").get("Width")

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.default_properties.get("Frame").get("Height")

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
        return self.pro_window.frame.dot_color.getColor()

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
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)
