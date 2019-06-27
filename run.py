import platform
import sys

from quamash import QApplication

from app.main.main import PsyApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy_application = PsyApplication()
    psy_application.initialize()
    psy_application.showMaximized()
    # 根据不同平台，载入不同的qss
    if platform.system() == "Windows":
        from conf.windows_qss import style_sheet
    else:
        from conf.mac_qss import style_sheet
    app.setStyleSheet(style_sheet)
    # 运行
    sys.exit(app.exec_())
