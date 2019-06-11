from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QFrame, QLabel


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

        label = QLabel(frame)
        label.setStyleSheet("background-color:transparent;")
        label.setGeometry(10, 10, 50, 50)
        self.movie = QMovie("image/loading.gif")
        label.setScaledContents(True)
        label.setMovie(self.movie)

        tip_label = QLabel(self)
        tip_label.setAlignment(Qt.AlignCenter)
        tip_label.setText("loading...")
        tip_label.setStyleSheet("color: black;background-color: transparent;")
        tip_label.setGeometry(10, 55, 60, 15)

    def start(self):
        """
        显示等待窗口
        :return:
        """
        self.movie.start()
        self.show()

    def stop(self):
        """
        关闭等待窗口
        :return:
        """
        self.movie.stop()
        self.close()
