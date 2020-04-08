import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QKeyEvent, QKeySequence
from PyQt5.QtWidgets import QApplication, QCompleter, QMainWindow, QTextEdit


class TextEdit(QTextEdit):
    def __init__(self):
        super(TextEdit, self).__init__()
        self.setPlainText("This TextEdit provides autocompletions for words that have more than"
                          " 3 characters. You can trigger autocompletion using " + QKeySequence("Ctrl+E").toString(
            QKeySequence.NativeText))
        self.completer: QCompleter = QCompleter(("test.1", "test.2", "test.3"), self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion: str):
        tc: QTextCursor = self.textCursor()

        extra: int = len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[extra:])

        self.setTextCursor(tc)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self.completer.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return
        super(TextEdit, self).keyPressEvent(e)
        completion_prefix = self.textUnderCursor()

        if completion_prefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completion_prefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) +
                    self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def textUnderCursor(self) -> str:
        tc: QTextCursor = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()

        self.text = TextEdit()

        self.setCentralWidget(self.text)
        self.resize(500, 300)
        self.setWindowTitle("Completer")


app = QApplication(sys.argv)
w = Win()
w.show()
sys.exit(app.exec_())
