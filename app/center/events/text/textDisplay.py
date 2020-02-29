from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction, QTextEdit

from app.center.events.text.textProperty import TextProperty
from app.center.events.text.view import Preview
from app.func import Func
from lib import MessageBox, TabItemMainWindow


class TextDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(TextDisplay, self).__init__(widget_id, widget_name)
        self.attributes: list = []
        self.text_label = QTextEdit()

        self.pro_window = TextProperty()

        self.html = self.pro_window.html
        self.font = self.pro_window.font
        self.default_properties = self.pro_window.getInfo()

        self.pro_window.general.text_edit.setDocument(self.text_label.document())
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.align = "Center"
        self.A_v = "Center"

        self.fore_color = "0,0,0"
        self.back_color = "255,255,255"
        self.transparent_value = "100%"

        self.x_pos = "0"
        self.y_pos = "0"
        self.w_size = "100%"
        self.h_size = "100%"
        self.setUI()

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will show here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImagePath("setting")), "setting", self)
        open_pro.triggered.connect(self.openPro)
        pre_view = QAction(QIcon(Func.getImagePath("preview")), "preview", self)
        pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        # tool.addAction(pre_view)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        self.refresh()
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.pro_window.refresh()
        self.getInfo()

    # 预览
    def preView(self):
        try:
            self.preview = Preview(self.x_pos, self.y_pos, self.w_size, self.h_size)
            # self.preview.text.setStyleSheet("background-color:{}".format(self.back_color))
            self.preview.setWindowModality(Qt.ApplicationModal)
            self.preview.setHtml(self.html)
            self.preview.setFont(self.pro_window.general.text_edit.font())
            self.preview.showFullScreen()
            self.preview.moveText()
            self.preview.setTransparent(self.transparent_value)
            self.t = QtCore.QTimer()
            self.t.timeout.connect(self.preview.close)
            self.t.start(10000)
            self.t.setSingleShot(True)
        except AttributeError as ae:
            MessageBox.warning(self, "Unknown Error", f"Please contact the developers!", MessageBox.Ok)
        # except Exception as e:
        #     print(e)
        #     print(type(e))

    def setPro(self, pro: TextProperty):
        del self.pro_window
        self.pro_window = pro
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        self.parseProperties()
        # 发送信号
        self.propertiesChanged.emit(self.default_properties)

    # 获取参数
    def parseProperties(self):
        self.html = self.pro_window.html
        self.fore_color = self.pro_window.general.fore_color.getColor()
        self.back_color = self.pro_window.general.back_color.getColor()
        self.transparent_value = self.pro_window.general.transparent.text()

        self.x_pos = self.default_properties.get("Center X", "0")
        self.y_pos = self.default_properties.get("Center Y", "0")
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

    # 返回设置参数
    def getInfo(self):
        self.html = self.pro_window.html
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def getProperties(self):
        self.html = self.pro_window.html
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def getShowProperties(self):
        info = self.default_properties.copy()
        info.pop("Html")
        info.pop("Input devices")
        info.pop("Output devices")
        return info

    def restore(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()
            self.apply()

    def changeDisplayText(self):
        self.html = self.text_label.toHtml()
        self.pro_window.general.text_edit.setDocument(self.text_label.document())

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
            self.loadSetting()
            self.apply()

    def loadSetting(self):
        self.pro_window.setOther(self.html)
        self.pro_window.setProperties(self.default_properties)

    def clone(self, new_id):
        clone_widget = TextDisplay(widget_id=new_id)
        clone_widget.setPro(self.pro_window.clone())
        clone_widget.apply()
        return clone_widget

    def getHiddenAttribute(self):
        """
        :return:
        """
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt": 0
        }
        return hidden_attr

    def changeWidgetId(self, new_id: str):
        self.widget_id = new_id

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
        return self.x_pos

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.y_pos

    def getEnable(self) -> str:
        """
        返回frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """返回frame transparent"""
        return self.pro_window.frame.transparent.text()

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


if __name__ == "__main__":
    import sys

    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)

    t = TextDisplay()

    t.show()

    sys.exit(app.exec())