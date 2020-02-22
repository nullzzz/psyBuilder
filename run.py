import platform
import sys

from PyQt5.QtWidgets import QApplication

from app import Psy
from app.info import Info
from app.kernel import Kernel
from qss import mac_qss
from qss import windows_qss


def compatible():
    """
    bind Kernel's varies to Info for compatible
    @return:
    @rtype: int
    """
    Info.PLATFORM = Kernel.Platform
    Info.IMAGE_LOAD_MODE = Kernel.ImageLoadMode
    Info.WID_WIDGET = Kernel.Widgets
    Info.WID_NODE = Kernel.Nodes
    Info.NAME_WID = Kernel.Names
    Info.FILE_NAME = Kernel.FileName
    Info.device_count = Kernel.DeviceCount
    Info.SLIDER_COUNT = Kernel.SliderCount


if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    # bind psy to Kernel.Psy
    Kernel.Psy = psy
    compatible()
    # init initial timeline
    psy.initInitialTimeline()
    psy.showMaximized()
    # choose qss
    if platform.system() == "Windows":
        app.setStyleSheet(windows_qss)
    else:
        app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
