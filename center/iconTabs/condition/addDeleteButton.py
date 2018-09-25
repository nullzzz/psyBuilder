from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class AddDeleteButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, button_type='add'):
        super(AddDeleteButton, self).__init__(parent)

        pixmap = None
        if button_type == 'add':
            pixmap = QPixmap('image/add.png')
        elif button_type == 'delete':
            pixmap = QPixmap('image/delete.png')
        pixmap.scaled(32, 32)
        self.setPixmap(pixmap)
        self.setFixedSize(32, 32)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
