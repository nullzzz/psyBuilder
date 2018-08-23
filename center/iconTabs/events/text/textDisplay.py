from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QTextOption, QColor
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QTextEdit

from center.iconTabs.events.text.textProperty import TextProperty
from center.iconTabs.events.text.view import Preview


class TextDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)
    # parameter: self.attributes

    def __init__(self, parent=None):
        super(TextDisplay, self).__init__(parent)
        self.attributes = []
        self.text_label = QTextEdit()
        self.pro = TextProperty()
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.pro.close)
        self.pro.apply_bt.clicked.connect(self.apply)

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
        open_pro = QAction(QIcon(".\\.\\image\\setting"), "setting", self)
        open_pro.triggered.connect(self.openPro)
        pre_view = QAction(QIcon(".\\.\\image\\preview"), "preview", self)
        pre_view.triggered.connect(self.preView)
        tool.addAction(open_pro)
        tool.addAction(pre_view)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def openPro(self):
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    # 预览图片
    def preView(self):
        try:
            self.preview = Preview(self.text_label, self.x_pos, self.y_pos, self.w_size, self.h_size)
            self.preview.setStyleSheet("background-color:{}".format(self.back_color))
            self.preview.text.setStyleSheet("background-color:{}".format(self.back_color))
            # self.preview.setTransparent(self.transparent_value)
            # self.preview.setWindowModality(Qt.ApplicationModal)
            self.preview.showFullScreen()
            self.preview.setAlign(self.align)
            self.preview.setWrap(self.is_wrap)
            self.preview.moveText()
            self.preview.setTransparent(self.transparent_value)
            self.t = QtCore.QTimer()
            self.t.timeout.connect(self.preview.close)
            self.t.start(10000)
            self.t.setSingleShot(True)
        except AttributeError:
            QMessageBox.warning(self, "Unknown Error", "Please contact the developer!", QMessageBox.Ok)
        except Exception as e:
            print(e)
            print(type(e))

    def ok(self):
        self.apply()
        self.pro.close()

    def apply(self):
        self.getPro()
        self.text_label.setTextColor(QColor(self.fore_color))
        self.text_label.setText(self.text)
        self.text_label.setStyleSheet("background-color: {};".format(self.back_color))

        if self.align == "Center":
            self.text_label.setAlignment(Qt.AlignCenter)
        elif self.align == "Left":
            self.text_label.setAlignment(Qt.AlignLeft)
        elif self.align == "Right":
            self.text_label.setAlignment(Qt.AlignRight)
        elif self.align == "Justify":
            self.text_label.setAlignment(Qt.AlignJustify)

        if self.is_wrap:
            self.text_label.setWordWrapMode(QTextOption.WordWrap)
        else:
            self.text_label.setWordWrapMode(QTextOption.NoWrap)

        # 发送信号
        self.propertiesChange.emit(self.getInfo())

    # 获取参数
    def getPro(self):
        self.text = self.pro.general.text.toPlainText()
        self.align = self.pro.general.align.currentText()
        self.fore_color = self.pro.general.fore_color.currentText()
        self.back_color = self.pro.general.back_color.currentText()
        self.transparent_value = self.pro.general.transparent.value()
        self.is_wrap = bool(self.pro.general.word_wrap.checkState())
        self.x_pos = self.pro.frame.x_pos.currentText()
        self.y_pos = self.pro.frame.y_pos.currentText()
        self.w_size = self.pro.frame.width.currentText()
        self.h_size = self.pro.frame.height.currentText()

    # 返回设置参数
    def getInfo(self):
        return {**self.pro.general.getInfo(), **self.pro.frame.getInfo(), **self.pro.duration.getInfo()}

    # 设置输入输出设备
    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro.duration.in_devices_dialog.addDevices(devices)

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro.setAttributes(format_attributes)


if __name__ == "__main__":
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)

    t = TextDisplay()

    t.show()

    sys.exit(app.exec())