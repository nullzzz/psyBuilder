from PyQt5.QtCore import Qt, QIODevice, QDataStream
from PyQt5.QtGui import QIcon, QDropEvent
from PyQt5.QtWidgets import QToolBar, QAction

from app.func import Func
from app.info import Info
from lib import TabItemMainWindow
from .lighter import AttributeHighlighter
from .smart import SmartTextEdit
from .textProperty import TextProperty


class TextDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(TextDisplay, self).__init__(widget_id, widget_name)

        self.text_label = SmartTextEdit()
        self.setAcceptDrops(True)

        self.pro_window = TextProperty()
        self.default_properties = self.pro_window.default_properties

        self.lighter = AttributeHighlighter(self.text_label.document())

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setUI()

        self.setAttributesForTextLabel()

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will appear here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)
        self.text_label.textChanged.connect(self.updateTextInRealtime)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("menu/setting.png")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent):
        data = e.mimeData().data(Info.AttributesToWidget)
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.text_label.cursor().setPos(e.pos())
        self.text_label.insertPlainText(text)

    def updateTextInRealtime(self):
        self.pro_window.general.text_edit.setHtml(self.text_label.toHtml())

    def openSettingWindow(self):
        self.pro_window.general.text_edit.setHtml(self.text_label.toHtml())
        super(TextDisplay, self).openSettingWindow()

    def refresh(self):
        self.pro_window.refresh()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()

        self.text_label.setHtml(self.default_properties.get("General").get("Html"))

    def updateInfo(self):
        self.pro_window.updateInfo()

    # ??????????????????
    def setAttributes(self, attributes):
        self.lighter.updateRule(attributes)
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)
        # self.text_label.setModelList(format_attributes)

    def setAttributesForTextLabel(self):
        attributes = Func.getWidgetAttributes(self.widget_id)
        self.lighter.updateRule(attributes)
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.text_label.setModelList(format_attributes)

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

    # ??????????????????
    # ?????????????????????????????????????????????????????????????????????
    # ????????????????????????Attribute
    def getText(self, is_html: bool = False) -> str:
        """
        ??????????????????????????????(default)??????html
        :param is_html:
        :return:
        """
        if is_html:
            return self.pro_window.general.text_edit.toHtml()
        else:
            return self.pro_window.general.text_edit.toPlainText()

    def getAlignmentX(self) -> str:
        """
        ????????????????????????
        :return:
        """
        return self.pro_window.general.align_x.currentText()

    def getAlignmentY(self) -> str:
        """
        ????????????????????????
        :return:
        """
        return self.pro_window.general.align_y.currentText()

    def getForceColor(self) -> str:
        """
        ???????????????
        :return:
        """
        return self.pro_window.general.fore_color.getRGB()

    def getScreenName(self) -> str:
        """
        ??????Screen Name
        :return:
        """
        return self.pro_window.general.screen.currentText()

    def getBackColor(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.general.back_color.getRGB()

    def getTransparent(self) -> str:
        """
        ?????????????????????
        :return:
        """
        return self.pro_window.general.transparent.text()

    def getIsClearAfter(self) -> str:
        """
        ????????????clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getFontFamily(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.general.font_box.currentText()

    def getFontPointSize(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.general.font_size_box.currentText()

    def getWrapatChar(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.general.word_wrap.text()

    def getRightToLeft(self) -> str:
        """
        ??????right to left
        :return:
        """
        return self.pro_window.general.right_to_left.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        ??????x?????????
        :return:
        """
        return self.default_properties.get("Frame").get("Center X")

    def getYAxisCoordinates(self) -> str:
        """
        ??????y?????????
        :return:
        """
        return self.default_properties.get("Frame").get("Center Y")

    def getWidth(self) -> str:
        """
        ????????????
        :return:
        """
        return self.default_properties.get("Frame").get("Width")

    def getHeight(self) -> str:
        """
        ????????????
        :return:
        """
        return self.default_properties.get("Frame").get("Height")

    def getEnable(self) -> str:
        """
        ??????frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """??????frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getBorderColor(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.frame.border_color.getRGB()

    def getBorderWidth(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameFillColor(self) -> str:
        """
        ?????????????????????
        :return:
        """
        return self.pro_window.frame.back_color.getRGB()

    def getDuration(self) -> str:
        """
        ??????duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        ??????????????????
        :return: ??????????????????
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})
