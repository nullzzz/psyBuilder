from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QLabel

from .imageProperty import ImageProperty
from .view import Preview


class ImageDisplay(QMainWindow):
    propertiesChange = pyqtSignal(dict)
    # parameter: self.attributes

    def __init__(self, parent=None, value=''):
        super(ImageDisplay, self).__init__(parent)
        self.value = value
        self.attributes = []
        self.label = QLabel()
        self.pro = ImageProperty()

        self.default_properties = self.pro.getInfo()

        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.cancel)
        # self.pro.cancel_bt.clicked.connect(self.testBt)
        self.pro.apply_bt.clicked.connect(self.apply)

        self.file = ""
        self.isStretch = False
        self.isUD = False
        self.isLR = False
        self.stretch_mode = "Both"
        self.back_color = "white"
        self.transparent_value = 0

        self.x_pos = 0
        self.y_pos = 0
        self.w_size = 100
        self.h_size = 100
        self.setUI()
        self.setAttributes(["test", "var"])

    def setUI(self):
        self.setWindowTitle("Image")

        self.label.setText("Your image will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

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
        # 阻塞原窗口
        self.pro.setWindowModality(Qt.ApplicationModal)
        self.pro.show()

    # 预览图片
    def preView(self):
        if self.file:
            try:
                self.preview = Preview(self.file, self.pix, self.x_pos, self.y_pos, self.w_size, self.h_size)
                self.preview.setStyleSheet("background-color:{}".format(self.back_color))
                self.preview.setTransparent(self.transparent_value)
                self.preview.setWindowModality(Qt.ApplicationModal)
                self.preview.showFullScreen()
                self.t = QtCore.QTimer()
                self.t.timeout.connect(self.preview.close)
                self.t.start(10000)
                self.t.setSingleShot(True)
            except AttributeError:
                QMessageBox.warning(self, "No Image Error", "Please load image first!", QMessageBox.Ok)
            except Exception as e:
                print(e)
                print(type(e))
        else:
            QMessageBox.warning(self, "No Image Error", "Please load image first!", QMessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro.close()

    def cancel(self):
        self.pro.loadSetting()

    def apply(self):
        self.getInfo()
        self.getPro()
        self.label.setStyleSheet("background-color:{}".format(self.back_color))
        # 加载图片文件
        if self.file:
            if QFileInfo(self.file).isFile():
                self.setImage()
            else:
                QMessageBox.warning(
                    self, "Warning", "The file path is invalid!")
        else:
            self.label.clear()
        # 发送信号
        self.propertiesChange.emit(self.default_properties)

    # 从pro获取参数
    def getPro(self):
        self.file = self.pro.general.file_name.text()
        self.isUD = self.pro.general.mirrorUD.checkState()
        self.isLR = self.pro.general.mirrorLR.checkState()
        self.isStretch = self.pro.general.stretch.checkState()
        self.stretch_mode = self.pro.general.stretch_mode.currentText()
        self.back_color = self.pro.general.back_color.currentText()
        self.transparent_value = self.pro.general.transparent.value()
        self.x_pos = self.pro.frame.x_pos.currentText()
        self.y_pos = self.pro.frame.y_pos.currentText()
        self.w_size = self.pro.frame.width.currentText()
        self.h_size = self.pro.frame.height.currentText()

    # 设置主面板的图片
    def setImage(self):
        img = QImage(self.file)
        image = img.mirrored(self.isLR, self.isUD)
        pix = QPixmap.fromImage(image)
        self.pix = pix
        # 图片反转
        if self.isStretch:
            mode = self.pro.general.stretch_mode.currentText()
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
        self.default_properties = self.pro.getInfo()
        return self.default_properties

    def setPro(self, pro: ImageProperty):
        del self.pro
        self.pro = pro
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.cancel)
        # self.pro.cancel_bt.clicked.connect(self.testBt)
        self.pro.apply_bt.clicked.connect(self.apply)

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

    # copy当前image对象
    def clone(self, value):
        clone_widget = ImageDisplay(value=value)
        clone_widget.setPro(self.pro.clone())
        clone_widget.apply()
        # self.pro.tab.addTab(clone_widget, "c")
        return clone_widget

    def test(self):
        self.pro_clone = self.pro.clone()
        self.pro_clone.setWindowModality(Qt.ApplicationModal)
        self.pro_clone.show()
