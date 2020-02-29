import platform
import sys

from PyQt5.QtWidgets import QApplication

from app import Psy
from app.info import Info
from app.kernel import Kernel
from qss import mac_qss, windows_qss


def compatible():
    """
    bind kernel's varies to info
    """
    Info.FILE_NAME = Kernel.FileName
    Info.PLATFORM = Kernel.Platform
    Info.IMAGE_LOAD_MODE = Kernel.ImageLoadMode
    Info.WID_NODE = Kernel.Nodes
    Info.WID_WIDGET = Kernel.Widgets
    Info.NAME_WID = Kernel.Names
    Info.QUEST_INFO = Kernel.QuestInfo


if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    # bind psy to Kernel.Psy
    Kernel.Psy = psy
    compatible()
    # init initial timeline
    psy.showMaximized()
    # choose qss
    if platform.system() == "Windows":
        app.setStyleSheet(windows_qss)
    else:
        app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
