from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsProxyWidget, QSizePolicy, QLineEdit


class TimelineLineEdit(QLineEdit):
    """

    """

    def __init__(self, text):
        super(TimelineLineEdit, self).__init__(text)
        # set its id
        self.setObjectName("TimelineLineEdit")
        # set its align
        self.setAlignment(Qt.AlignCenter)
        # link necessary signals
        self.linkSignals()

    def linkSignals(self):
        """
        link necessary signals
        @return:
        """
        # lose focus when finish editing
        self.editingFinished.connect(self.clearFocus)


class TimelineNameItem(QGraphicsProxyWidget):
    """
    it is widget_type item in timeline.
    """
    # emit content when finish editing
    editFinishing = pyqtSignal(str)

    def __init__(self, widget_name: str = ""):
        """
        init item
        @param parent:
        @param widget_type: its widget add_type, such as timeline
        @param widget_id: if widget_id has provided, we don't need to generate a new widget_id
        @param widget_name: like widget_id above.
        """
        super(TimelineNameItem, self).__init__(None)
        self.line_edit = TimelineLineEdit(widget_name)
        self.setWidget(self.line_edit)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def linkSignals(self):
        """
        link necessary signals
        @return:
        """
        # emit signal to upper level when finish editing
        self.line_edit.editingFinished.connect(self.finishEditing)

    def setText(self, text: str):
        """
        set line edit's text
        @param text:
        @return:
        """
        self.line_edit.setText(text)

    def text(self):
        """
        return its' line edit's text
        @return:
        """
        return self.line_edit.text()

    def finishEditing(self):
        """
        emit content of line edit when finish editing
        @return:
        """
        self.editFinishing.emit(self.text())
