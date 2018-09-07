from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTextOption
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QTextEdit, QLabel


class Preview(QDialog):
    def __init__(self, text: QTextEdit, start_x=0, start_y=0, width=100, height=100):
        super(Preview, self).__init__()
        self.text = QTextEdit(self)
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color: transparent;")
        self.label.resize(400, 150)

        pix = QPixmap()
        pix.load(".\\.\\image\\preview_tip")
        self.label.setPixmap(pix)
        self.text.setTextColor(text.textColor())
        self.text.setText(text.toPlainText())
        self.text.setFont(text.font())
        self.text.setReadOnly(True)
        screen = QDesktopWidget().screenGeometry()
        if "%" in start_x:
            self.start_x = int(start_x[0:-1]) * screen.width() / 100
        else:
            self.start_x = int(start_x)
        if "%" in start_y:
            self.start_y = int(start_y[0:-1]) * screen.height() / 100
        else:
            self.start_y = int(start_y)

        if "%" in width:
            self.width_factor = int(width[0:-1]) * screen.width() / 100
        else:
            self.width_factor = int(width)
        if "%" in height:
            self.height_factor = int(height[0:-1]) * screen.height() / 100
        else:
            self.height_factor = int(height)


    # 换行
    def setWrap(self, is_wrap):
        if is_wrap:
            self.text.setWordWrapMode(QTextOption.WordWrap)
        else:
            self.text.setWordWrapMode(QTextOption.NoWrap)

    # 对齐方式
    def setAlign(self, align):
        if align == "Center":
            self.text.setAlignment(Qt.AlignCenter)
        elif align == "Left":
            self.text.setAlignment(Qt.AlignLeft)
        elif align == "Right":
            self.text.setAlignment(Qt.AlignRight)
        elif align == "Justify":
            self.text.setAlignment(Qt.AlignJustify)

    # 坐标位置
    def moveText(self):
        self.text.resize(self.width_factor, self.height_factor)
        self.text.move(self.start_x, self.start_y)
        self.label.move(0, 0)

    # 透明度
    def setTransparent(self, transparent_value=80):
        self.setWindowOpacity(transparent_value / 100)

    def setStartPos(self, x, y):
        self.start_x = x
        self.start_y = y

