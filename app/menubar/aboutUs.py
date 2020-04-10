from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFontMetrics, QPixmap, QPalette
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout

from app.func import Func


class AboutUs(QWidget):
    def __init__(self, parent=None):
        super(AboutUs, self).__init__(parent=parent)

        self.setWindowTitle("About developers of PTB Builder 0.1")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)
        self.setPalette(p)

        info = QTextEdit(self)
        info.setReadOnly(True)
        info.setFrameShape(QFrame.NoFrame)
        info.setHtml("<b>PTB Builder (ver 0.1)</b> for Psychtoolbox 3 under MATLAB "
                     "was developed by the group leaded by Prof. "
                     "<a style='color: blue;' href=\"http://web.suda.edu.cn/yzhangpsy/index.html\">Yang Zhang</a> "
                     "at Attention and Perception lab at Soochow university, Suzhou, China. "
                     "<br><br><b>PTB Builder 0.1</b> are provided as is, and no warranty for their "
                     "correctness or usefulness for any purpose is made or implied by "
                     "the authors of the software, or by anyone else. This software "
                     "is designed for research purposes only and not allowed to be used "
                     "for any business purpose (e.g., but not limited to, business training)."
                     )

        info.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setFixedHeight(QFontMetrics(info.font()).lineSpacing() * 11)

        author1 = self.getInfo("authorInfo01",
                               "Yang Zhang (张阳), Ph.D, Prof.<br>Department of Psychology, Soochow University"
                               "<br><a href='mailto:yzhangpsy@suda.edu.cn?Subject= Inquire about the usage of PTB Builder 0.1'>yzhangpsy@suda.edu.cn</a>")
        author2 = self.getInfo("authorInfo02",
                               "Zhe Yang, Ph.D, Associate Prof. <br> Department of computer science, Soochow University")

        author3 = self.getInfo("authorInfo03",
                               "ChenZhi Feng, Ph.D, Prof. <br> Department of Psychology, Soochow University")
        layout = QVBoxLayout()
        layout.addWidget(info, 2)
        layout.addLayout(author1, 1)
        layout.addLayout(author2, 1)
        layout.addLayout(author3, 1)

        self.setLayout(layout)

    def getInfo(self, name: str, info: str):
        head_portrait = QLabel()
        head_portrait.setFixedSize(QSize(100, 100))
        detail = QLabel()
        head_portrait.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        detail.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        head_portrait.setPixmap(QPixmap(Func.getImage(f"{name}.png")))
        detail.setTextFormat(Qt.RichText)
        detail.setTextInteractionFlags(Qt.TextBrowserInteraction)
        detail.setOpenExternalLinks(True)
        detail.setText(info)

        layout = QHBoxLayout()
        layout.addWidget(head_portrait, stretch=0)
        layout.addWidget(detail, stretch=1)
        return layout
