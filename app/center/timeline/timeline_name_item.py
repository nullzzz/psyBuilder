from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QGraphicsProxyWidget, QLineEdit


class TimelineLineEdit(QLineEdit):
    """

    """

    def __init__(self, text):
        super(TimelineLineEdit, self).__init__(text)
        # set its id
        self.setObjectName("TimelineLineEdit")
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

    def mousePressEvent(self, e):
        """
        override this func.
        @param e:
        @return:
        """
        super(TimelineLineEdit, self).mousePressEvent(e)
        self.setReadOnly(False)


class TimelineNameItem(QGraphicsProxyWidget):
    """
    it is widget_type item in timeline.
    """
    # emit its content when text change
    textChanged = pyqtSignal(int, str)
    # edit
    editFinishing = pyqtSignal()

    def __init__(self, widget_id: int, widget_name: str = ""):
        """
        init item
        @param parent:
        @param widget_name: like widget_id above.
        """
        super(TimelineNameItem, self).__init__(None)
        # data
        self.widget_id = widget_id
        self.pre_text = widget_name
        self.line_edit = TimelineLineEdit(widget_name)
        self.setWidget(self.line_edit)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link necessary signals
        @return:
        """
        # emit signal when finish editing
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
        emit content of line edit when finish editing and content changed
        @return:
        """
        # if changed
        self.editFinishing.emit()
        if self.text() != self.pre_text:
            # change pre text
            self.pre_text = self.text()
            # emit change signal
            self.textChanged.emit(self.widget_id, self.text())

    def undo(self):
        """
        if name is invalid, we should redo it.
        @return:
        """
        self.line_edit.undo()
        # change pre text
        self.pre_text = self.text()
