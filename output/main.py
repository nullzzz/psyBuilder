from PyQt5.QtWidgets import QDockWidget, QTextEdit


class Output(QDockWidget):
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)

        self.text_area = QTextEdit()

        self.setWidget(self.text_area)
