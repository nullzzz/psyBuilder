from PyQt5.QtWidgets import QMessageBox


class MessageBox(QMessageBox):
    """
    通过重写，自定义QMessageBox的icon和样式
    """
    def __init__(self, *__args):
        super(MessageBox, self).__init__(*__args)
        # 自定义icon和样式
