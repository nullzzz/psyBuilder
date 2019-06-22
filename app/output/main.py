import sys

import datetime
from PyQt5.QtWidgets import QDockWidget, QTextEdit


class Output(QDockWidget):
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

        self.text_area = QTextEdit()
        # self.text_area.setEnabled(False)

        self.setWidget(self.text_area)

    def print(self, text, error: bool = False, timer: bool = True):
        if timer:
            self.text_area.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if error:
            self.text_area.append(sys._getframe().f_code.co_filename)
            self.text_area.append(f"line {sys._getframe().f_back.f_lineno}")
        self.text_area.append(text)
