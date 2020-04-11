from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QGraphicsView


class View(QGraphicsView):
    def __init__(self, *args):
        super(View, self).__init__(*args)

        self.screen_width: int = 1920
        self.screen_height: int = 1080

        self.ratio: float = 1920 / 1080

    def updateRatio(self, new_width: int, new_height: int):
        self.screen_width = new_width
        self.screen_height = new_height
        self.ratio = new_width / new_height

    def resizeEvent(self, event: QResizeEvent) -> None:
        w, h = event.size().width(), event.size().height()

        super(View, self).resizeEvent(event)
