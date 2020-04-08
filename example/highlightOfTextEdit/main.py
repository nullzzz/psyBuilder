from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from example import SmartTextEdit


class AttributeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(AttributeHighlighter, self).__init__(parent)

        self.__formats = self.initFormat()
        self.__rules = [QRegExp(r"\[[_\d\w]+\]"), QRegExp("@mean|@standard|@random")]

    @staticmethod
    def initFormat():
        attribute_format = QTextCharFormat()
        attribute_format.setFontFamily("courier")
        attribute_format.setFontPointSize(12)
        attribute_format.setForeground(QColor(Qt.darkBlue))
        attribute_format.setFontWeight(QFont.Bold)

        value_format = QTextCharFormat()
        value_format.setFontFamily("courier")
        value_format.setFontPointSize(12)
        value_format.setForeground(QColor(Qt.darkRed))
        value_format.setFontWeight(QFont.Bold)
        return attribute_format, value_format

    def updateRule(self, attributes: list):
        self.__rules[0] = QRegExp("|".join([r"\[%s\]" % i for i in attributes]))

    def highlightBlock(self, text):
        for rule, _format in zip(self.__rules, self.__formats):
            i = rule.indexIn(text)
            while i >= 0:
                length = rule.matchedLength()
                self.setFormat(i, length, _format)
                i = rule.indexIn(text, i + length)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QFont("Courier", 11)
        font.setFixedPitch(True)
        self.editor = SmartTextEdit()
        self.editor.setFont(font)
        self.highlighter = AttributeHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

        self.highlighter.updateRule(["[sub.age]", "[sub]"])

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
