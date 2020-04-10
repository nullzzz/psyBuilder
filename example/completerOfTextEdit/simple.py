import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QCompleter, QPlainTextEdit, QMainWindow, QApplication


# https://stackoverflow.com/questions/28956693/pyqt5-qtextedit-auto-completion

class MyCompleter(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, parent=None):
        QCompleter.__init__(self, ["mean", "men", "bar"], parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected


class AwesomeTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(AwesomeTextEdit, self).__init__(parent)

        self.completer = MyCompleter()
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        print(completion)
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        # 自动补全
        if event.key() == Qt.Key_Tab and self.completer.popup().isVisible():
            self.insertCompletion(self.completer.getSelected())
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            return
        QPlainTextEdit.keyPressEvent(self, event)

        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 0:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                        + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()


class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()

        self.text = AwesomeTextEdit()

        self.setCentralWidget(self.text)
        self.resize(500, 300)
        self.setWindowTitle("Completer")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Win()
    w.show()
    sys.exit(app.exec_())
