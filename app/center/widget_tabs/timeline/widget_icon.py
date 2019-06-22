from PyQt5.QtWidgets import QLabel

from app.func import Func


class WidgetIcon(QLabel):
    # 把图标大小设置为固定的
    SIZE = 50

    def __init__(self, parent=None, widget_type='', widget_id=''):
        super(WidgetIcon, self).__init__(parent)
        # 美化
        self.setStyleSheet("""
                            QLabel{
                                background-color: transparent;
                            }
                            QLabel:hover{
                                border: 2px solid lightBlue;
                                border-radius: 4px;
                                padding: 2px;
                            }
                            """)
        # 通过widget_type生成widget_id，widget_id可以直接赋予
        if widget_id:
            self.widget_id = widget_id
        else:
            self.widget_id = Func.generateWidgetId(widget_type)

        # 根据widget type去生成pixmap
        self.setPixmap(Func.getWidgetImage(widget_type, 'icon').pixmap(WidgetIcon.SIZE, WidgetIcon.SIZE))

        # 当初不知干啥用的
        self.setMouseTracking(True)

    def changeWidgetId(self, widget_id) -> None:
        """
        直接去修改或命名widget_id
        :param widget_id:
        :return:
        """
        self.widget_id = widget_id
