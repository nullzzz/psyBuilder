import sys

from quamash import QApplication

from app import Psy

if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    psy = Psy()
    psy.showMaximized()
    # 运行
    sys.exit(app.exec_())
