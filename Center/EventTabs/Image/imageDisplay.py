from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QMessageBox, QLabel

from .imageProperty import ImageProperty
from .view import Preview


class ImageDisplay(QMainWindow):
    propertiesChanged = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ImageDisplay, self).__init__(parent)
        self.label = QLabel()
        self.pro = ImageProperty()
        self.pro.ok_bt.clicked.connect(self.ok)
        self.pro.cancel_bt.clicked.connect(self.pro.close)
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

    def setUI(self):
        self.setWindowTitle("Image")
        self.setFixedSize(1000, 618)
        self.label.setText("Your image will show here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.label)

        tool = QToolBar()
        open_pro = QAction(QIcon(".\\.\\image\\setting"), "open", self)
        open_pro.triggered.connect(self.openPro)
        pre_view = QAction(QIcon(".\\.\\image\\preview"), "view", self)
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

    def apply(self):
        self.getPro()
        self.label.setStyleSheet("background-color:{}".format(self.back_color))
        # 加载图片文件
        if self.file:
            if QFileInfo(self.file).isFile():
                img = QImage(self.file)
                image = img.mirrored(self.isLR, self.isUD)
                pix = QPixmap.fromImage(image)
                self.pix = pix
                # 图片反转
                if self.isStretch:
                    mode = self.pro.stretch_mode.currentText()
                    w = self.label.size().width()
                    h = self.label.size().height()
                    if mode == "Both":
                        new_pix = pix.scaled(
                            w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                    elif mode == "LeftRight":
                        new_pix = pix.scaledToWidth(w, Qt.FastTransformation)
                    else:
                        new_pix = pix.scaledToHeight(h, Qt.FastTransformation)
                    self.label.setPixmap(new_pix)
                else:
                    self.label.setPixmap(pix)
            else:
                QMessageBox.warning(
                    self, "Warning", "The file path is invalid!")
        else:
            self.label.clear()
        # 发送信号
        self.propertiesChanged.emit(self.getInfo())

    # 获取参数
    def getPro(self):
        self.file = self.pro.file_name.text()
        self.isUD = self.pro.mirrorUD.checkState()
        self.isLR = self.pro.mirrorLR.checkState()
        self.isStretch = self.pro.stretch.checkState()
        self.stretch_mode = self.pro.stretch_mode.currentText()
        self.back_color = self.pro.back_color.currentText()
        self.transparent_value = self.pro.transparent.value()
        self.x_pos = self.pro.frame.xpos.currentText()
        self.y_pos = self.pro.frame.ypos.currentText()
        self.w_size = self.pro.frame.width.currentText()
        self.h_size = self.pro.frame.height.currentText()

    # 返回设置参数
    def getInfo(self):
        # isUSCK = self.pro.usck.checkState()
        # source_color = self.pro.sck.currentText()
        align_h = self.pro.align_h.currentText()
        align_v = self.pro.align_v.currentText()
        clear_after = self.pro.clear_after.currentText()
        display_name = self.pro.screen_name.currentText()

        border_color = self.pro.frame.border_color.currentText()
        border_width = self.pro.frame.border_width.value()

        duration = self.pro.duration.duration.currentText()
        in_device, out_device = self.pro.duration.getInfo()

        return {
            "File name": self.file,
            "Mirror up/down": bool(self.isUD),
            "Mirror left/right": bool(self.isLR),
            "Stretch": bool(self.isStretch),
            "Stretch mode": self.stretch_mode,
            # "use source color key": bool(isUSCK),
            # "source color": source_color,
            # "AlignHorizontal": align_h,
            # "AlignVertical": align_v,
            # "Clear after": clear_after,
            # "Back color": self.back_color,
            "Transparent": self.transparent_value,
            "Display Name": display_name,
            "X position": self.x_pos,
            "Y position": self.y_pos,
            "width": self.w_size,
            "height": self.h_size,
            "Border color": border_color,
            "Border width": border_width,
            "Duration": duration,
            "Out devices": out_device,
            "In devices": in_device
        }

    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro.duration.in_devices_dialog.addDevices(devices)