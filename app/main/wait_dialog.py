from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QFrame, QLabel

from app.func import Func


class WaitDialog(QDialog):
    def __init__(self, parent=None):
        """
        init widget
        :param parent: parent widget
        """
        super(WaitDialog, self).__init__(parent)
        # ui
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # widget
        frame = QFrame(self)
        frame.setStyleSheet("background-color: transparent;border-radius:10px;")
        frame.setGeometry(0, 0, 70, 80)

        self.label = QLabel(frame)
        self.label.setStyleSheet("background-color:transparent;")
        self.label.setGeometry(10, 10, 50, 50)
        self.label.setPixmap(QIcon(Func.getImage("loading/frame-0.png")).pixmap(50, 50))
        self.label.setScaledContents(True)

        tip_label = QLabel(self)
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setText("loading...")
        tip_label.setStyleSheet("color: black;background-color: transparent;")
        tip_label.setGeometry(10, 55, 60, 15)

        # data
        self.image_index = 0
        self.image_count = 30

    def start(self):
        """
        显示等待窗口
        :return:
        """
        self.show()

    def change_image(self):
        """
        切换下一张图片
        :return:
        """
        self.image_index += 1
        self.label.setPixmap(QIcon(Func.getImage(f"loading/frame-{self.image_index}.png")).pixmap(50, 50))
        self.image_index %= self.image_count

    def stop(self):
        """
        关闭等待窗口
        :return:
        """
        self.image_index = 0
        self.close()
