from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction, QTextEdit

from app.func import Func
from example.highlightOfTextEdit import AttributeHighlighter
from lib import TabItemMainWindow
from .textProperty import TextProperty


class TextDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(TextDisplay, self).__init__(widget_id, widget_name)

        self.text_label = QTextEdit()

        self.pro_window = TextProperty()
        self.default_properties = self.pro_window.default_properties

        self.html = self.pro_window.html
        self.font = self.pro_window.font

        self.pro_window.general.text_edit.setDocument(self.text_label.document())

        self.lighter = AttributeHighlighter(self.text_label.document())
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        # self.align = "Center"
        # self.A_v = "Center"
        #
        # self.fore_color = "0,0,0"
        # self.back_color = "255,255,255"
        # self.transparent_value = "100%"
        #
        # self.x_pos = "0"
        # self.y_pos = "0"
        # self.w_size = "100%"
        # self.h_size = "100%"
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will show here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)
        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        pre_view = QAction(QIcon(Func.getImage("preview")), "preview", self)
        # pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        # tool.addAction(pre_view)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def refresh(self):
        self.pro_window.refresh()

    # 预览
    # def preView(self):
    #     return
    #     try:
    #         self.preview = Preview(self.x_pos, self.y_pos, self.w_size, self.h_size)
    #         # self.preview.text.setStyleSheet("background-color:{}".format(self.back_color))
    #         self.preview.setWindowModality(Qt.ApplicationModal)
    #         self.preview.setHtml(self.html)
    #         self.preview.setFont(self.pro_window.general.text_edit.font())
    #         self.preview.showFullScreen()
    #         self.preview.moveText()
    #         self.preview.setTransparent(self.transparent_value)
    #         self.t = QtCore.QTimer()
    #         self.t.timeout.connect(self.preview.close)
    #         self.t.start(10000)
    #         self.t.setSingleShot(True)
    #     except AttributeError as ae:
    #         MessageBox.warning(self, "Unknown Error", f"Please contact the developers!", MessageBox.Ok)
    #     # except Exception as e:
    #     #     print(e)
    #     #     print(type(e))

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.pro_window.testHtml()

        # self.updateInfo()
        # self.propertiesChanged.emit(self.widget_id)

    # # 获取参数
    # def parseProperties(self):
    #     self.html = self.pro_window.html
    #     self.fore_color = self.pro_window.general.fore_color.getColor()
    #     self.back_color = self.pro_window.general.back_color.getColor()
    #     self.transparent_value = self.pro_window.general.transparent.text()
    #
    #     self.x_pos = self.default_properties.get("Center X", "0")
    #     self.y_pos = self.default_properties.get("Center Y", "0")
    #     self.w_size = self.default_properties.get("Width", "100%")
    #     self.h_size = self.default_properties.get("Height", "100%")
    #     if self.x_pos.startswith("[") and self.x_pos.endswith("]"):
    #         self.x_pos = "0"
    #     if self.y_pos.startswith("[") and self.y_pos.endswith("]"):
    #         self.y_pos = "0"
    #     if self.w_size.startswith("[") and self.w_size.endswith("]"):
    #         self.w_size = "100%"
    #     if self.h_size.startswith("[") and self.h_size.endswith("]"):
    #         self.h_size = "100%"

    # 返回设置参数
    def updateInfo(self):
        self.pro_window.updateInfo()

    def changeDisplayText(self):
        self.html = self.text_label.toHtml()
        self.pro_window.general.text_edit.setDocument(self.text_label.document())

    # 设置可选参数
    def setAttributes(self, attributes):
        self.lighter.updateRule(attributes)
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties)
        self.apply()

    def getProperties(self) -> dict:
        self.refresh()
        return self.pro_window.getProperties()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    # 返回各项参数
    # 大部分以字符串返回，少数点击选择按钮返回布尔值
    # 因为有些地方引用Attribute
    def getText(self, is_html: bool = False) -> str:
        """
        返回文本信息，纯文本(default)或者html
        :param is_html:
        :return:
        """
        if is_html:
            return self.pro_window.general.text_edit.toHtml()
        else:
            return self.pro_window.general.text_edit.toPlainText()

    def getAlignmentX(self) -> str:
        """
        返回文字对齐方式
        :return:
        """
        return self.pro_window.general.align_x.currentText()

    def getAlignmentY(self) -> str:
        """
        返回文字对齐方式
        :return:
        """
        return self.pro_window.general.align_y.currentText()

    def getForceColor(self) -> str:
        """
        返回前景色
        :return:
        """
        return self.pro_window.general.fore_color.getColor()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen.currentText()

    def getBackColor(self) -> str:
        """
        返回背景颜色
        :return:
        """
        return self.pro_window.general.back_color.getColor()

    def getTransparent(self) -> str:
        """
        返回图像透明度
        :return:
        """
        return self.pro_window.general.transparent.text()

    def getIsClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getFontFamily(self) -> str:
        """
        返回字体信息
        :return:
        """
        return self.pro_window.general.font_box.currentText()

    def getFontPointSize(self) -> str:
        """
        返回字体大小
        :return:
        """
        return self.pro_window.general.font_size_box.currentText()

    def getWrapatChar(self) -> str:
        """
        返回是否换行
        :return:
        """
        return self.pro_window.general.word_wrap.text()

    def getRightToLeft(self) -> str:
        """
        返回right to left
        :return:
        """
        return self.pro_window.general.right_to_left.currentText()

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
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)

    def get(self):
        self.property()
