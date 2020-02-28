from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from app.func import Func


class AddDeleteButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, button_type='add'):
        super(AddDeleteButton, self).__init__(parent)

        self.button_type = button_type
        self.can_emit = True

        self.becomeEnabled()
        self.setFixedSize(32, 32)

    def mousePressEvent(self, QMouseEvent):
        if self.can_emit:
            self.clicked.emit()
            self.becomePressed()
        else:
            self.becomeDisabled()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.can_emit:
            self.becomeEnabled()
        else:
            self.becomeDisabled()

    def setDisabled(self, disabled=False):
        if disabled:
            self.can_emit = False
            self.becomeDisabled()
        else:
            self.can_emit = True
            self.becomeEnabled()

    def becomeDisabled(self):
        if self.button_type == 'add':
            self.setPixmap(QPixmap(Func.getImage("add_disabled.png")))
        elif self.button_type == 'delete':
            self.setPixmap(QPixmap(Func.getImage("delete_disabled.png")))

    def becomeEnabled(self):
        if self.button_type == 'add':
            self.setPixmap(QPixmap(Func.getImage('add.png')))
        elif self.button_type == 'delete':
            self.setPixmap(QPixmap(Func.getImage('delete.png')))

    def becomePressed(self):
        try:
            if self.button_type == 'add':
                self.setPixmap(QPixmap(Func.getImage('add_press.png')))
            elif self.button_type == 'del':
                self.setPixmap(QPixmap(Func.getImage('delete_press.png')))
        except Exception as e:
            print(f"I can't solve {e}. [condition/addDeleteButton.py]")
