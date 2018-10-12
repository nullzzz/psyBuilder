from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QTextEdit

# from Info import Info
from center.iconTabs.events.text.textProperty import TextProperty
from center.iconTabs.events.text.view import Preview


class TextDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)
    # parameter: self.attributes

    def __init__(self, parent=None, value=''):
        super(TextDisplay, self).__init__(parent)
        self.value = value
        self.attributes = []
        self.text_label = QTextEdit()
        self.pro_window = TextProperty()

        self.html = self.pro_window.html
        self.font = self.pro_window.font
        self.default_properties = self.pro_window.getInfo()

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.align = "Center"
        self.A_v = "Center"

        self.fore_color = "black"
        self.back_color = "white"
        self.transparent_value = 100
        self.is_wrap = False

        self.x_pos = "0"
        self.y_pos = "0"
        self.w_size = "100%"
        self.h_size = "100%"
        self.setUI()
        self.setAttributes(["test", "var"])

    def setUI(self):
        self.setWindowTitle("Text")
        self.text_label.setText("Your text will show here")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.text_label)

        tool = QToolBar()
        open_pro = QAction(QIcon("image/setting"), "setting", self)
        open_pro.triggered.connect(self.openPro)
        pre_view = QAction(QIcon("image/preview"), "preview", self)
        pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        tool.addAction(pre_view)

        t = QAction(QIcon("image/test"), "test", self)
        t.triggered.connect(self.test)
        tool.addAction(t)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        # self.setAttributes(Info.getAttributes(self.value))
        # 阻塞原窗口
        self.pro_window.setWindowModality(Qt.ApplicationModal)
        self.pro_window.show()

    # 预览
    def preView(self):
        try:
            self.preview = Preview(self.x_pos, self.y_pos, self.w_size, self.h_size)
            # self.preview.text.setStyleSheet("background-color:{}".format(self.back_color))
            self.preview.setWindowModality(Qt.ApplicationModal)
            self.preview.setFont(self.font)
            self.preview.setHtml(self.html)
            self.preview.setWrap(self.is_wrap)
            self.preview.showFullScreen()
            self.preview.moveText()
            self.preview.setTransparent(self.transparent_value)
            self.t = QtCore.QTimer()
            self.t.timeout.connect(self.preview.close)
            self.t.start(10000)
            self.t.setSingleShot(True)
        except AttributeError as ae:
            QMessageBox.warning(self, "Unknown Error", f"Please contact the developers!", QMessageBox.Ok)
        except Exception as e:
            print(e)
            print(type(e))

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
        # self.clone()

    def apply(self):
        self.getInfo()
        self.getPro()
        self.text_label.setHtml(self.html)
        self.text_label.setFont(self.font)
        if self.is_wrap:
            self.text_label.setWordWrapMode(QTextOption.WordWrap)
        else:
            self.text_label.setWordWrapMode(QTextOption.NoWrap)
        # self.text_label.setStyleSheet("background-color: {};".format(self.back_color))
        # 发送信号
        self.propertiesChange.emit(self.default_properties)

    # 获取参数
    def getPro(self):
        self.html = self.pro_window.html
        self.font = self.pro_window.font
        self.align = self.pro_window.general.align.currentText()
        self.fore_color = self.pro_window.general.fore_color.currentText()
        self.back_color = self.pro_window.general.back_color.currentText()
        self.transparent_value = self.pro_window.general.transparent.value()
        self.is_wrap = bool(self.pro_window.general.word_wrap.checkState())
        self.x_pos = self.pro_window.frame.x_pos.currentText()
        self.y_pos = self.pro_window.frame.y_pos.currentText()
        self.w_size = self.pro_window.frame.width.currentText()
        self.h_size = self.pro_window.frame.height.currentText()

    # 返回设置参数
    def getInfo(self):
        self.html = self.pro_window.html
        self.font = self.pro_window.font
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    # 设置输入输出设备
    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro_window.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro_window.duration.in_devices_dialog.addDevices(devices)

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.pro_window.loadSetting()

    def clone(self, value):
        clone_widget = TextDisplay(value=value)
        clone_widget.setPro(self.pro_window.clone())
        clone_widget.apply()

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


if __name__ == "__main__":
    import sys

    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)

    t = TextDisplay()

    t.show()

    sys.exit(app.exec())
