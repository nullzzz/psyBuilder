import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QApplication, QTextEdit

"""
https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html
https://stackoverflow.com/questions/58251763/how-to-construct-custom-auto-completion-completion-with-partial-matches-like-in
"""


class SmartCompleter(QCompleter):
    def __init__(self, words: tuple = ("@mean", "@mode", "@median"), parent=None):
        super().__init__(words, parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitive)

        self.highlighted.connect(self.func)

        self.current_completion: str = ""

    def func(self, text):
        self.current_completion = text


class SmartTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completer = SmartCompleter()
        self.completer.setWidget(self)

        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        if completion == self.completer.completionPrefix():
            return
        text_cursor = self.textCursor()
        last_chars = len(completion) - len(self.completer.completionPrefix())
        text_cursor.insertText(completion[-last_chars:])
        self.setTextCursor(text_cursor)

    def textBeforeCursor(self):
        text_cursor = self.textCursor()
        text_cursor.select(QtGui.QTextCursor.LineUnderCursor)
        selected_text = text_cursor.selectedText()
        if "@" in selected_text:
            return "@" + selected_text.split("@")[-1]
        return selected_text

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if self.completer.popup().isVisible():
            key = e.key()
            if key in (Qt.Key_Enter, Qt.Key_Return):
                e.ignore()
                return
        super().keyPressEvent(e)

        text_before_cursor = self.textBeforeCursor()
        if text_before_cursor != self.completer.currentCompletion():
            if text_before_cursor != self.completer.completionPrefix():
                self.completer.setCompletionPrefix(text_before_cursor)
                self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))
                cursor_rectangle = self.cursorRect()
                popup = self.completer.popup()
                cursor_rectangle.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
                self.completer.complete(cursor_rectangle)
        else:
            self.completer.popup().hide()


class SmartEditWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_vertical_layout = QVBoxLayout()
        self.setLayout(main_vertical_layout)

        main_horizontal_layout = QHBoxLayout()
        main_vertical_layout.addLayout(main_horizontal_layout)

        text_edit = SmartTextEdit()
        main_horizontal_layout.addWidget(text_edit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)

    smart_edit_widget = SmartEditWidget()
    smart_edit_widget.showNormal()

    sys.exit(app.exec())
