from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFontMetrics, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout

from app.func import Func

# this is only for mac Only
class AboutRunForMacOnly(QWidget):
    def __init__(self, parent=None):
        super(AboutRunForMacOnly, self).__init__(parent=parent)

        self.setWindowTitle("About developers of PsyBuilder 0.1")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)

        self.setPalette(p)

        info = QTextEdit(self)
        info.setReadOnly(True)
        info.setTextInteractionFlags(Qt.NoTextInteraction)
        info.setFrameShape(QFrame.NoFrame)

        # info.setTextBackgroundColor()
        info.setHtml("<b>PsyBuilder (ver 0.1)</b> for Psychtoolbox 3 under MATLAB "
                     "was developed by the group leaded by Prof. "
                     "<a style='color: blue;' href=\"http://web.suda.edu.cn/yzhangpsy/index.html\">Yang Zhang</a> "
                     "at Attention and Perception lab at Soochow university, Suzhou, China. "
                     "<br><br><b>PsyBuilder 0.1</b> are provided as is, no warranty for their "
                     "correctness or usefulness for any purpose is made or implied by "
                     "the authors of the software, or by anyone else. This software "
                     "is designed for research purposes only and not to be used for "
                     "any business purpose, such as, but not limited to, business training)."
                     )

        cP = info.palette()
        cP.setColor(QPalette.Base,QColor(255,255,255,0))
        info.setPalette(cP)

        info.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setFixedHeight(QFontMetrics(info.font()).lineSpacing() * 11)

        layout = QVBoxLayout()
        layout.addWidget(info, 2)
        self.setLayout(layout)
