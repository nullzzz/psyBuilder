from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from app.func import Func


class MessageBox(QMessageBox):
    def __init__(self, *__args):
        super(MessageBox, self).__init__(*__args)
        # 将图标设置为psy icon
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))
