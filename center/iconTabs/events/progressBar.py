import sys

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtWidgets import QDialog, QApplication, QFrame, QVBoxLayout


class LoadingTip(QDialog):
    def __init__(self, parent=None):
        super(LoadingTip, self).__init__(parent)
        self.bar = ProgressBar()
        layout = QVBoxLayout()
        layout.addWidget(self.bar, 1, Qt.AlignCenter)
        self.setLayout(layout)

    def setValue(self, value: int):
        self.bar.setValue(value)


class ProgressBar(QFrame):
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.value = 0
        self.setFixedSize(400, 400)

    def changeValue(self):
        self.value += 1

    def setValue(self, value: int):
        self.value = value

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        m_rotate_angle = int(360*self.value/100)
        side = 400
        out_rect = QRectF(0, 0, side, side)
        in_rect = QRectF(20, 20, side-40, side-40)
        value_str = f"{self.value}%"
        # 画外圆
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor(97, 117, 118)))
        p.drawEllipse(out_rect)
        p.setBrush(QBrush(QColor(255, 107, 107)))
        p.drawPie(out_rect, (90 - m_rotate_angle) * 16, m_rotate_angle * 16)
        p.setBrush(self.palette().window().color())
        p.drawEllipse(in_rect)
        f = QFont("Microsoft YaHei", 15, QFont.Bold)
        p.setFont(f)
        p.setFont(f)
        p.setPen(QColor("#555555"))
        p.drawText(in_rect, Qt.AlignCenter, value_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = LoadingTip()

    demo.show()

    sys.exit(app.exec_())
