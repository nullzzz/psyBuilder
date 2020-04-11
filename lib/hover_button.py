from PyQt5.QtWidgets import QPushButton

from app.func import Func


class HoverButton(QPushButton):
    def __init__(self, button_type: str, text: str = ""):
        super(HoverButton, self).__init__()
        self.button_type = button_type
        self.setIcon(Func.getImageObject(f"{self.button_type}.png", 1))
        self.text = text
        if text:
            self.setText(text)
        self.setStyleSheet("""
        QPushButton{
            border:none;
            background:transparent;
        }
        """)

    def enterEvent(self, QEvent):
        super(HoverButton, self).enterEvent(QEvent)
        self.setIcon(Func.getImageObject(f"{self.button_type}_pressed.png", 1))
        if self.text:
            self.setStyleSheet("""
                            QPushButton{
                                border:none;
                                color:rgb(59,120,181);
                                background:transparent;
                            }
                            """)

    def leaveEvent(self, QEvent):
        super(HoverButton, self).leaveEvent(QEvent)
        self.setIcon(Func.getImageObject(f"{self.button_type}.png", 1))
        if self.text:
            self.setStyleSheet("""
                            QPushButton{
                                border:none;
                                background:transparent;
                            }
                            """)
