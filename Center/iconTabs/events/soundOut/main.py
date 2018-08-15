from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from .SoundOutmain import Ui_MainWindow
from .Soundout import MySound


class SoundOut(QtWidgets.QMainWindow, Ui_MainWindow):
    propertiesChange = QtCore.pyqtSignal(dict)
    def __init__(self):
        super(SoundOut, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('SoundOut')
        self.Settings = self.DefaultSettings()
        self.dia = MySound()
        self.player = QtMultimedia.QMediaPlayer()
        self.url = ''
        self.pushButton.setEnabled(False)
        # self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile('/Users/apple/Downloads/《我还有点小糊涂》.mp3')))
        self.player.positionChanged.connect(self.positionChanged)
        self.settings.triggered.connect(self.openSettings)
        self.pushButton.clicked.connect(self.playClicked)
        self.horizontalSlider.sliderMoved.connect(self.setPosition)
        self.dia.pushButton_2.clicked.connect(self.OK)
        self.dia.pushButton_3.clicked.connect(self.Cancel)
        self.player.stateChanged.connect(self.stateChanged)

    def playButton(self):
        if self.url == '':
            self.pushButton.setEnabled(False)
        else:
            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl(self.url)))
            self.pushButton.setEnabled(True)

    def Cancel(self):
        self.dia.close()

    def OK(self):
        self.saveSettings()
        self.url = self.dia.lineEdit.text()
        self.playButton()
        self.dia.close()
        if self.dia.checkBox.isChecked():
            self.player.setVolume(int(self.dia.lineEdit_2.text()))

    def setLabel(self):
        m = int(self.player.duration()/(1000*60))
        s = int(self.player.duration()/1000-m*60)
        self.label_2.setText('{:0>2d}:{:0>2d}'.format(m, s))

    def openSettings(self):
        self.loadSettings()
        self.dia.show()

    def playClicked(self):
        if self.player.state() == 1:
            self.player.pause()
        else:
            self.player.play()
            self.horizontalSlider.setRange(0, self.player.duration())
            self.setLabel()

    def stateChanged(self):
        if self.player.state() == 1:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("../images/pause_128px_535941_easyicon.net.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
            self.pushButton.setIcon(icon)
            self.pushButton.setIconSize(QtCore.QSize(50, 100))
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("../images/play_playback_48px_10946_easyicon.net.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.On)
            self.pushButton.setIcon(icon)
            self.pushButton.setIconSize(QtCore.QSize(50, 100))

    def setPosition(self, position):
        self.player.setPosition(position)
        m = int(position/(1000*60))
        s = int(position/1000-m*60)
        self.label.setText('{:0>2d}:{:0>2d}'.format(m, s))

    def positionChanged(self, position):
        self.horizontalSlider.setValue(position)
        m = int(position/(1000*60))
        s = int(position/1000-m*60)
        self.label.setText('{:0>2d}:{:0>2d}'.format(m, s))

    def DefaultSettings(self):
        x = {
            'Filename': ' ',
            'Buffer Size': '5000',
            'Buffer Mode': 'Streaming',
            'Position Time Format': 'MilliSeconds',
            'Start Offset': '0',
            'Stop Offset': '0',
            'Loop': 'No',
            'Stop After': 'Yes',
            'Stop After Mode': 'NextOnsetTime',
            'End Sound Action': '(none)',
            'VolumeC': False,
            'PanC': False,
            'Volume': '',
            'Pan': ''
        }
        return x

    def loadSettings(self):
        self.dia.lineEdit.setText(self.Settings['Filename'])
        self.dia.lineEdit_3.setText(self.Settings['Buffer Size'])
        self.dia.comboBox.setCurrentText(self.Settings['Buffer Mode'])
        self.dia.comboBox_2.setCurrentText(self.Settings['Position Time Format'])
        self.dia.lineEdit_4.setText(self.Settings['Start Offset'])
        self.dia.lineEdit_5.setText(self.Settings['Stop Offset'])
        self.dia.comboBox_3.setCurrentText(self.Settings['Loop'])
        self.dia.comboBox_4.setCurrentText(self.Settings['Stop After'])
        self.dia.comboBox_5.setCurrentText(self.Settings['Stop After Mode'])
        self.dia.comboBox_6.setCurrentText(self.Settings['End Sound Action'])
        self.dia.checkBox.setChecked(self.Settings['VolumeC'])
        self.dia.checkBox_2.setChecked(self.Settings['PanC'])
        self.dia.lineEdit_2.setText(self.Settings['Volume'])
        self.dia.lineEdit_6.setText(self.Settings['Pan'])

    def saveSettings(self):
        self.Settings = {
            'Filename': self.dia.lineEdit.text(),
            'Buffer Size': self.dia.lineEdit_3.text(),
            'Buffer Mode': self.dia.comboBox.currentText(),
            'Position Time Format': self.dia.comboBox_2.currentText(),
            'Start Offset': self.dia.lineEdit_4.text(),
            'Stop Offset': self.dia.lineEdit_5.text(),
            'Loop': self.dia.comboBox_3.currentText(),
            'Stop After': self.dia.comboBox_4.currentText(),
            'Stop After Mode': self.dia.comboBox_5.currentText(),
            'End Sound Action': self.dia.comboBox_6.currentText(),
            'VolumeC': self.dia.checkBox.isChecked(),
            'PanC': self.dia.checkBox_2.isChecked(),
            'Volume': self.dia.lineEdit_2.text(),
            'Pan': self.dia.lineEdit_6.text()
        }
        self.propertiesChange.emit(self.getProperties())

    def getProperties(self):
        return self.Settings