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

        self.pro_window.general.text_edit.setDocument(self.text_label.document())

        self.lighter = AttributeHighlighter(self.text_label.document())
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will show here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)
        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        # pre_view = QAction(QIcon(Func.getImage("preview")), "preview", self)
        # pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        # tool.addAction(pre_view)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def refresh(self):
        self.pro_window.refresh()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()

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
        self.updateInfo()
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name):
        self.updateInfo()
        clone_widget = TextDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        clone_widget.apply()
        return clone_widget

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
        return self.pro_window.general.fore_color.getRGB()

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
        return self.pro_window.general.back_color.getRGB()

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
        return self.pro_window.frame.border_color.getRGB()

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
        return self.pro_window.frame.back_color.getRGB()

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

