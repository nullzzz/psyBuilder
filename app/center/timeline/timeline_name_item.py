from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class TimelineNameItem(QLineEdit):
    """

    """

    # emit its content when text change
    textChanged = pyqtSignal(int, str)

    def __init__(self, widget_id: int, widget_name: str = ""):
        super(TimelineNameItem, self).__init__(None)
        # data
        self.widget_id = widget_id
        self.pre_text = widget_name
        self.setText(widget_name)
        # set its id
        self.setObjectName("TimelineNameItem")
        # set its align
        self.setAlignment(Qt.AlignCenter)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        @return:
        """
        # clear its cursor when enter/return pressed
        self.editingFinished.connect(lambda: self.setReadOnly(True))
        # emit signal when finish editing
        self.editingFinished.connect(self.finishEditing)

    def mousePressEvent(self, e):
        """
        override this func.
        @param e:
        @return:
        """
        super(TimelineNameItem, self).mousePressEvent(e)
        self.setReadOnly(False)

    def finishEditing(self):
        """
        emit content of line edit when finish editing and content changed
        @return:
        """
        # if changed
        if self.text() != self.pre_text:
            # change pre text
            self.pre_text = self.text()
            # emit change signal
            self.textChanged.emit(self.widget_id, self.text())

    def setWidgetId(self, widget_id: int):
        """
        change its widget if
        @param widget_id:
        @return:
        """
        self.widget_id = widget_id

    def setWidgetName(self, widget_name: str):
        """

        @param widget_name:
        @return:
        """
        self.widget_name = widget_name
        self.setText(widget_name)
