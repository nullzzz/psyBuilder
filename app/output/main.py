import datetime

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QTextEdit

from lib import DockWidget


class Output(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self, parent=None):
        super(Output, self).__init__(parent)
        # main widget is a widget_name edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        # first str is work path of this software
        self.text_edit.setHtml(f"<b>{QDir().currentPath()}</b>")
        self.text_edit.append('<p style="font:5px;color:white">none</p>')
        self.setWidget(self.text_edit)

        # todo delete, test here
        self.print("test information.")
        self.print("test information.", 1)
        self.print("test information.", 1)
        self.print("test information.", 1)
        self.print("test information.", 2)
        self.print("test information.", 1)
        self.print("test information.", 2)
        self.print("test information.", 2)
        self.print("test information.", 1)
        self.print("test information.", 1)
        self.print("test information.", 2)

    def print(self, information: str, information_type: int = 0) -> None:
        """
        print information in its widget_name edit
        @param information:
        @param information_type: 0 none
                                 1 success
                                 2 fail
        @return:
        """
        self.text_edit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # none
        if information_type == 0:
            self.text_edit.append(f"<p>{information}</p>")
        elif information_type == 1:
            self.text_edit.append(f'<b style="color:rgb(73,156,84)">[success]</b> {information}')
        else:
            self.text_edit.append(f'<b style="color:rgb(199,84,80)">[fail]</b> {information}')
        self.text_edit.append('<p style="font:5px;color:white">none</p>')
