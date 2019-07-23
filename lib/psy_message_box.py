from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

from app.func import Func


class PsyMessageBox(QMessageBox):
    def __init__(self, *__args):
        super(PsyMessageBox, self).__init__(__args)
        # 将图标设置为psy icon
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))
