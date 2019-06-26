import datetime
import sys

from PyQt5.QtWidgets import QDockWidget, QTextEdit

from app.lib import SizeContainerWidget


class Output(QDockWidget):
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

        self.text_area = QTextEdit()
        size_container = SizeContainerWidget()
        size_container.setWidget(self.text_area)

        self.setWidget(size_container)

    def print(self, text, error: bool = False, timer: bool = True):
        if timer:
            self.text_area.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if error:
            self.text_area.append(sys._getframe().f_code.co_filename)
            self.text_area.append(f"line {sys._getframe().f_back.f_lineno}")
        self.text_area.append(text)
