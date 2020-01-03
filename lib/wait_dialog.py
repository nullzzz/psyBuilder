from PyQt5.QtCore import QSize, pyqtProperty, QTimer, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QDialog


class WaitDialog(QDialog):
    Color = QColor(24, 189, 155)
    Clockwise = True
    Delta = 36

    def __init__(self):
        super(WaitDialog, self).__init__(None)
        self.angle = 0
        self._timer = QTimer(self, timeout=self.update)
        self._timer.start(1)

    def paintEvent(self, event):
        super(WaitDialog, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        painter.scale(side / 100.0, side / 100.0)
        painter.rotate(self.angle)
        painter.save()
        painter.setPen(Qt.NoPen)
        color = self.Color.toRgb()
        for i in range(11):
            color.setAlphaF(1.0 * i / 10)
            painter.setBrush(color)
            painter.drawEllipse(30, -10, 20, 20)
            painter.rotate(36)
        painter.restore()
        self.angle += self.Delta if self.Clockwise else -self.Delta
        self.angle %= 360

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self.Color

    @color.setter
    def color(self, color: QColor):
        if self.Color != color:
            self.Color = color
            self.update()

    @pyqtProperty(bool)
    def clockwise(self) -> bool:
        return self.Clockwise

    @clockwise.setter
    def clockwise(self, clockwise: bool):
        if self.Clockwise != clockwise:
            self.Clockwise = clockwise
            self.update()

    @pyqtProperty(int)
    def delta(self) -> int:
        return self.Delta

    @delta.setter
    def delta(self, delta: int):
        if self.Delta != delta:
            self.Delta = delta
            self.update()

    def sizeHint(self) -> QSize:
        return QSize(100, 100)
