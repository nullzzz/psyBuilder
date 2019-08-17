from PyQt5.QtCore import pyqtSignal, QPointF, QRect, QSize, QPoint, Qt, QByteArray, QDataStream, QIODevice, QMimeData
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QIntValidator, QPainter, QPixmap, QDrag
from PyQt5.QtWidgets import (QAction, QButtonGroup, QComboBox, QFontComboBox, QGraphicsView, QGridLayout,
                             QHBoxLayout, QLabel, QMainWindow, QMenu, QMessageBox, QSizePolicy, QToolBox, QToolButton,
                             QWidget, QPushButton, QColorDialog, QDesktopWidget)

from app.center.widget_tabs.events.slider.item.diaItem import DiaItem
from app.center.widget_tabs.events.slider.item.diagramTextItem import DiagramTextItem
from app.center.widget_tabs.events.slider.item.pixItem import PixItem

from app.center.widget_tabs.events.slider.property import SliderProperty
from app.center.widget_tabs.events.slider.scene import Scene
from app.func import Func
from app.info import Info
from lib.psy_message_box import PsyMessageBox as QMessageBox


class Button(QPushButton):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        icon = self.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << icon
        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_()


class Slider(QMainWindow):
    propertiesChange = pyqtSignal(str)
    InsertTextButton = 10

    def __init__(self, widget_id):
        super(Slider, self).__init__()
        self.widget_id = widget_id
        self.current_wid = widget_id
        self.attributes = []
        try:
            self.attributes = Func.getAttributes(self.widget_id)
        except KeyError:
            # condition下的slider在此出错
            pass

        self.createActions()
        self.createMenus()
        self.createToolBox()

        self.scene = Scene(self.itemMenu, self.attributes)

        self.scene.itemInserted.connect(self.itemInserted)
        self.scene.pixItemInserted.connect(self.pixitemInserted)
        self.scene.textInserted.connect(self.textInserted)
        self.scene.itemSelected.connect(self.itemSelected)
        self.scene.DitemSelected.connect(self.DitemSelected)

        self.createToolbars()

        layout = QHBoxLayout()
        layout.addWidget(self.toolBox)
        self.view = QGraphicsView(self.scene)
        scr_Rect = QDesktopWidget().screenGeometry()

        # print(f"screen: {scr_Rect}")

        self.scene.setSceneRect(0, 0, scr_Rect.width(), scr_Rect.height())
        self.view.fitInView(0, 0, scr_Rect.width() / 2, scr_Rect.height() / 2, Qt.KeepAspectRatio)

        layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Slider")

        self.pro_window = SliderProperty()
        self.setAttributes(self.attributes)
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def getProperties(self):
        return {'none': 'none'}

    def getHiddenAttribute(self):
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt": 0
        }
        return hidden_attr

    def DitemSelected(self, d):
        self.fillColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"), QColor(d['itemcolor'])))
        self.lineColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"), QColor(d['linecolor'])))
        self.lineWidthCombo.setCurrentText(str(d['linewidth']))

    # 左边工具栏按钮事件
    def buttonGroupPressed(self, id):
        self.pointerTypeGroup.button(3).setChecked(False)
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)
        print(f"line 119: {id}")
        if id == self.InsertTextButton:
            self.scene.setMode(Scene.InsertText)
        else:
            self.scene.setItemType(id)
            self.scene.setMode(Scene.InsertItem)

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if item.zValue() >= zValue and (isinstance(item, DiaItem) or isinstance(item, PixItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and (isinstance(item, DiaItem) or isinstance(item, PixItem))):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.pointerTypeGroup.button(Scene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def pixitemInserted(self, item):
        self.pointerTypeGroup.button(Scene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def textInserted(self, item):
        self.buttonGroup.button(self.InsertTextButton).setChecked(False)
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def currentFontChanged(self, font):
        self.handleFontChange()

    def fontSizeChanged(self, font):
        self.handleFontChange()

    def textColorChanged(self):
        self.textAction = self.sender()
        if self.textAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fontColorToolButton.setIcon(
                    self.createColorToolButtonIcon(Func.getImage("textpointer.png"), color))
                self.scene.setTextColor(color)
        else:
            self.fontColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("textpointer.png"),
                                               QColor(self.textAction.data())))
            self.textButtonTriggered()

    def itemColorChanged(self):
        self.fillAction = self.sender()
        if self.fillAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fillColorToolButton.setIcon(
                    self.createColorToolButtonIcon(Func.getImage("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fillColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("floodfill.png"),
                                               QColor(self.fillAction.data())))
            self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        if self.lineAction.data() == 'More..':
            color = QColorDialog.getColor()
            self.lineColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.lineColorToolButton.setIcon(
                self.createColorToolButtonIcon(Func.getImage('linecolor.png'),
                                               QColor(self.lineAction.data())))
            self.lineButtonTriggered()

    def lineWidthChanged(self):
        self.scene.setLineWidth(int(self.lineWidthCombo.currentText()))

    def backChanged(self):
        self.backAction = self.sender()
        if self.backAction.data() == '1':
            self.backToolButton.setIcon(QIcon(Func.getImage("background1.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background1.png"))))
        elif self.backAction.data() == '2':
            self.backToolButton.setIcon(QIcon(Func.getImage("background2.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background2.png"))))
        elif self.backAction.data() == '3':
            self.backToolButton.setIcon(QIcon(Func.getImage("background3.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background3.png"))))
        elif self.backAction.data() == '4':
            self.backToolButton.setIcon(QIcon(Func.getImage("background4.png")))
            self.scene.setBackgroundBrush(QBrush(QPixmap(Func.getImage("background4.png"))))
        self.scene.update()
        self.view.update()

    def textButtonTriggered(self):
        # print(2)
        self.scene.setTextColor(QColor(self.textAction.data()))

    def fillButtonTriggered(self):
        self.scene.setItemColor(QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QColor(self.lineAction.data()))

    def handleFontChange(self):
        font = self.fontCombo.currentFont()
        # BUG
        # font.setPointSize(self.fontSizeCombo.currentText().toInt()[0])
        font.setPointSize(int(self.fontSizeCombo.currentText()))
        if self.bold_action.isChecked():
            font.setWeight(QFont.Bold)
        else:
            font.setWeight(QFont.Normal)
        font.setItalic(self.italic_action.isChecked())
        font.setUnderline(self.underline_action.isChecked())

        self.scene.setFont(font)

    def itemSelected(self, item):
        font = item.font()
        color = item.defaultTextColor()
        self.fontCombo.setCurrentFont(font)
        self.fontSizeCombo.setEditText(str(font.pointSize()))
        self.bold_action.setChecked(font.weight() == QFont.Bold)
        self.italic_action.setChecked(font.italic())
        self.underline_action.setChecked(font.underline())

    def about(self):
        QMessageBox.about(self, "About Diagram Scene",
                          "The <b>Diagram Scene</b> example shows use of the graphics framework.")

    def openPro(self):
        try:
            self.attributes = Func.getAttributes(self.widget_id)
            self.setAttributes(self.attributes)
        except KeyError as e:
            # condition下的slider在这里出错
            pass
        screen_devices = Func.getScreen()
        self.pro_window.general.setScreen(screen_devices)

        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        try:
            self.pro_window.setAttributes(format_attributes)
        except Exception as e:
            print(e)

    # 视图左边的工具栏
    def createToolBox(self):
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(False)
        self.buttonGroup.buttonPressed[int].connect(self.buttonGroupPressed)

        layout = QGridLayout()
        layout.addWidget(self.createCellWidget("Polygon", DiaItem.Polygon), 0, 0)
        layout.addWidget(self.createCellWidget("Circle", DiaItem.Circle), 1, 0)
        layout.addWidget(self.createCellWidget("Arc", DiaItem.Arc), 2, 0)
        layout.addWidget(self.createCellWidget("Rect", DiaItem.Rect), 3, 0)

        textButton = Button()
        self.buttonGroup.addButton(textButton, self.InsertTextButton)
        textButton.setIcon(QIcon(QPixmap(Func.getImage("textpointer.png")).scaled(50, 50)))
        textButton.setIconSize(QSize(50, 50))
        videoButton = Button()
        self.buttonGroup.addButton(videoButton, PixItem.Video)
        videoButton.setIcon(QIcon(QPixmap(Func.getImage("video.png")).scaled(50, 50)))
        videoButton.setIconSize(QSize(50, 50))
        pictureButton = Button()
        self.buttonGroup.addButton(pictureButton, PixItem.Image)
        pictureButton.setIcon(QIcon(QPixmap(Func.getImage("Picture.png")).scaled(50, 50)))
        pictureButton.setIconSize(QSize(50, 50))
        soundButton = Button()
        self.buttonGroup.addButton(soundButton, PixItem.Sound)
        soundButton.setIcon(QIcon(QPixmap(Func.getImage("music.png")).scaled(50, 50)))
        soundButton.setIconSize(QSize(50, 50))
        snowButton = Button()
        self.buttonGroup.addButton(snowButton, PixItem.Snow)
        snowButton.setIcon(QIcon(QPixmap(Func.getImage("snow.png")).scaled(50, 50)))
        snowButton.setIconSize(QSize(50, 50))
        gaborButton = Button()
        self.buttonGroup.addButton(gaborButton, PixItem.Gabor)
        gaborButton.setIcon(QIcon(QPixmap(Func.getImage("Gabor.png")).scaled(50, 50)))
        gaborButton.setIconSize(QSize(50, 50))

        textLayout = QGridLayout()
        videoLayout = QGridLayout()
        pictureLayout = QGridLayout()
        soundLayout = QGridLayout()
        snowLayout = QGridLayout()
        gaborLayout = QGridLayout()

        textLayout.addWidget(textButton, 0, 0, Qt.AlignHCenter)
        textLayout.addWidget(QLabel("Text"), 1, 0, Qt.AlignCenter)
        videoLayout.addWidget(videoButton, 0, 0, Qt.AlignHCenter)
        videoLayout.addWidget(QLabel("Video"), 1, 0, Qt.AlignCenter)
        pictureLayout.addWidget(pictureButton, 0, 0, Qt.AlignHCenter)
        pictureLayout.addWidget(QLabel("Picture"), 1, 0, Qt.AlignCenter)
        soundLayout.addWidget(soundButton, 0, 0, Qt.AlignHCenter)
        soundLayout.addWidget(QLabel("Sound"), 1, 0, Qt.AlignCenter)
        snowLayout.addWidget(snowButton, 0, 0, Qt.AlignHCenter)
        snowLayout.addWidget(QLabel("Snow"), 1, 0, Qt.AlignCenter)
        gaborLayout.addWidget(gaborButton, 0, 0, Qt.AlignHCenter)
        gaborLayout.addWidget(QLabel("Gabor"), 1, 0, Qt.AlignCenter)

        textWidget = QWidget()
        textWidget.setLayout(textLayout)
        videoWidget = QWidget()
        videoWidget.setLayout(videoLayout)
        pictureWidget = QWidget()
        pictureWidget.setLayout(pictureLayout)
        soundWidget = QWidget()
        soundWidget.setLayout(soundLayout)
        snowWidget = QWidget()
        snowWidget.setLayout(snowLayout)
        gaborWidget = QWidget()
        gaborWidget.setLayout(gaborLayout)

        layout.setRowStretch(5, 10)

        itemWidget = QWidget()
        itemWidget.setLayout(layout)

        # self.backgroundButtonGroup = QButtonGroup()
        # self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

        backgroundLayout = QGridLayout()
        backgroundLayout.addWidget(textWidget, 0, 0)
        backgroundLayout.addWidget(videoWidget, 1, 0)
        backgroundLayout.addWidget(pictureWidget, 2, 0)
        backgroundLayout.addWidget(soundWidget, 3, 0)
        backgroundLayout.addWidget(snowWidget, 4, 0)
        backgroundLayout.addWidget(gaborWidget, 5, 0)

        backgroundLayout.setRowStretch(6, 10)

        backgroundWidget = QWidget()
        backgroundWidget.setLayout(backgroundLayout)

        self.toolBox = QToolBox()
        self.toolBox.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))
        self.toolBox.setMinimumWidth(itemWidget.sizeHint().width())
        self.toolBox.addItem(itemWidget, "Basic Geometries")
        self.toolBox.addItem(backgroundWidget, "Stimuli")

    def createActions(self):
        self.to_front_action = QAction(QIcon(Func.getImage("sendtoback.png")), "Bring to &Front", self)
        self.to_front_action.setShortcut("Ctrl+F")
        self.to_front_action.setToolTip("Bring item to front")
        self.to_front_action.triggered.connect(self.bringToFront)

        self.to_back_action = QAction(QIcon(Func.getImage("bringtofront.png")), "Send to &Back", self)
        self.to_back_action.setShortcut("Ctrl+B")
        self.to_back_action.setToolTip("Send item to back")
        self.to_back_action.triggered.connect(self.sendToBack)

        self.delete_action = QAction(QIcon(Func.getImage("delete.png")), "&Delete", self)
        self.delete_action.setShortcut("Ctrl+D")
        self.delete_action.setToolTip("Delete item from diagram")
        self.delete_action.triggered.connect(self.deleteItem)

        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+X")
        self.exit_action.setToolTip("Quit Scenediagram example")
        self.exit_action.triggered.connect(self.close)

        self.bold_action = QAction(QIcon(Func.getImage("bold.png")), "Bold", self)
        self.bold_action.setShortcut("Ctrl+Shift+B")
        self.bold_action.setToolTip("Bold")
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.handleFontChange)

        self.italic_action = QAction(QIcon(Func.getImage("italic.png")), "Italic", self)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.setToolTip("Italic")
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.handleFontChange)

        self.underline_action = QAction(QIcon(Func.getImage("underline.png")), "underline", self)
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.setToolTip("underline")
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.handleFontChange)

        self.about_action = QAction("Ab&out", self)
        self.about_action.setShortcut("Ctrl+O")
        self.about_action.setToolTip("underline")
        self.about_action.triggered.connect(self.about)

        self.open_pro = QAction(QIcon(Func.getImage("setting.png")), "setting", self)
        # self.open_pro.setShortcut("Ctrl+O")
        self.open_pro.setToolTip("setting")
        self.open_pro.triggered.connect(self.openPro)

        # self.open_pro = QAction(QIcon(Func.getImage("setting")), "setting", self, triggered=self.openPro)

        # 工具栏删除，顶层底层

    def createMenus(self):
        self.itemMenu = QMenu()
        self.itemMenu.addAction(self.delete_action)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.to_front_action)
        self.itemMenu.addAction(self.to_back_action)

    # 上方工具栏
    def createToolbars(self):
        self.settingToolBar = self.addToolBar('Setting')
        self.settingToolBar.addAction(self.open_pro)

        # self.editToolBar = self.addToolBar("Edit")
        self.settingToolBar.addAction(self.delete_action)
        self.settingToolBar.addAction(self.to_front_action)
        self.settingToolBar.addAction(self.to_back_action)

        self.fontCombo = QFontComboBox()
        self.fontCombo.currentFontChanged.connect(self.currentFontChanged)

        # 字体大小
        self.fontSizeCombo = QComboBox()
        self.fontSizeCombo.setEditable(True)
        for iFontSize in range(8, 30, 2):
            self.fontSizeCombo.addItem(str(iFontSize))

        validator = QIntValidator(2, 64, self)

        self.fontSizeCombo.setValidator(validator)
        self.fontSizeCombo.currentIndexChanged.connect(self.fontSizeChanged)

        # 边框宽度
        self.lineWidthCombo = QComboBox()
        self.lineWidthCombo.setEditable(True)
        for iLineWidth in range(2, 20, 2):
            self.lineWidthCombo.addItem(str(iLineWidth))

        validator = QIntValidator(0, 20, self)
        self.lineWidthCombo.setValidator(validator)
        self.lineWidthCombo.currentIndexChanged.connect(self.lineWidthChanged)

        # 字体颜色
        self.fontColorToolButton = QToolButton()
        self.fontColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.fontColorToolButton.setMenu(
            self.createColorMenu(self.textColorChanged, Qt.black))
        self.textAction = self.fontColorToolButton.menu().defaultAction()
        self.fontColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("textpointer.png"),
                                           Qt.black))
        # self.fontColorToolButton.setAutoFillBackground(True)
        try:
            self.fontColorToolButton.clicked.connect(self.textButtonTriggered)
        except Exception as e:
            print(e)

        self.fillColorToolButton = QToolButton()
        self.fillColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.fillColorToolButton.setMenu(
            self.createColorMenu(self.itemColorChanged, Qt.white))
        self.fillAction = self.fillColorToolButton.menu().defaultAction()
        self.fillColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"), Qt.white))
        self.fillColorToolButton.clicked.connect(self.fillButtonTriggered)

        self.lineColorToolButton = QToolButton()
        self.lineColorToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.lineColorToolButton.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.lineAction = self.lineColorToolButton.menu().defaultAction()
        self.lineColorToolButton.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"), Qt.black))
        self.lineColorToolButton.clicked.connect(self.lineButtonTriggered)

        # ?
        # self.textToolBar = self.addToolBar("Font")
        self.settingToolBar.addWidget(self.fontCombo)
        self.settingToolBar.addWidget(self.fontSizeCombo)
        self.settingToolBar.addAction(self.bold_action)
        self.settingToolBar.addAction(self.italic_action)
        self.settingToolBar.addAction(self.underline_action)

        # self.colorToolBar = self.addToolBar("Color")
        self.settingToolBar.addWidget(self.fontColorToolButton)
        self.settingToolBar.addWidget(self.fillColorToolButton)
        self.settingToolBar.addWidget(self.lineColorToolButton)
        self.settingToolBar.addWidget(self.lineWidthCombo)

        pointerButton = QToolButton()
        pointerButton.setCheckable(True)
        pointerButton.setChecked(True)
        pointerButton.setIcon(QIcon(Func.getImage("pointer.png")))
        linePointerButton = QToolButton()
        linePointerButton.setCheckable(True)
        linePointerButton.setIcon(QIcon(Func.getImage("linepointer.png")))

        self.pointerTypeGroup = QButtonGroup()
        self.pointerTypeGroup.addButton(pointerButton, Scene.MoveItem)
        self.pointerTypeGroup.addButton(linePointerButton, Scene.InsertLine)
        self.pointerTypeGroup.buttonClicked[int].connect(self.pointerGroupClicked)

        # self.pointerToolbar = self.addToolBar("Pointer type")
        self.settingToolBar.addWidget(pointerButton)
        self.settingToolBar.addWidget(linePointerButton)

        self.backToolButton = QToolButton()
        self.backToolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.backToolButton.setMenu(
            self.createBackgroundMenu(self.backChanged))
        # self.fillAction = self.fillColorToolButton.menu().defaultAction()
        self.backToolButton.setIcon(QIcon(Func.getImage("background4.png")))
        self.backToolButton.clicked.connect(self.fillButtonTriggered)

        self.settingToolBar.addWidget(self.backToolButton)

        # 左边工具栏添加图形本文

    def createCellWidget(self, text, diagramType):
        item = DiaItem(diagramType, self.itemMenu)
        icon = QIcon(item.image())

        button = Button()
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setCheckable(True)
        self.buttonGroup.addButton(button, diagramType)

        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(text), 1, 0, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def createColorMenu(self, slot, defaultColor):
        colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

        colorMenu = QMenu(self)
        action1 = QAction('More..', self, triggered=slot)
        action1.setData('More..')
        for color, name in zip(colors, names):
            action = QAction(self.createColorIcon(color), name, self, triggered=slot)
            action.setData(QColor(color))
            colorMenu.addAction(action)
            if color == defaultColor:
                colorMenu.setDefaultAction(action)
        colorMenu.addAction(action1)
        return colorMenu

    def createBackgroundMenu(self, slot):
        backMenu = QMenu(self)
        action1 = QAction(QIcon(Func.getImage("background1.png")), 'Blue Grid', self, triggered=slot)
        action2 = QAction(QIcon(Func.getImage("background2.png")), 'White Grid', self, triggered=slot)
        action3 = QAction(QIcon(Func.getImage("background3.png")), 'Gray Grid', self, triggered=slot)
        action4 = QAction(QIcon(Func.getImage("background4.png")), 'No Grid', self, triggered=slot)
        action1.setData('1')
        action2.setData('2')
        action3.setData('3')
        action4.setData('4')
        backMenu.setDefaultAction(action4)
        backMenu.addAction(action1)
        backMenu.addAction(action2)
        backMenu.addAction(action3)
        backMenu.addAction(action4)
        return backMenu

    def createColorToolButtonIcon(self, imageFile, color):
        pixmap = QPixmap(50, 80)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        image = QPixmap(imageFile)
        target = QRect(0, 0, 50, 60)
        source = QRect(0, 0, 42, 42)
        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()

        return QIcon(pixmap)

    def createColorIcon(self, color):
        pixmap = QPixmap(20, 20)
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 20, 20), color)
        painter.end()

        return QIcon(pixmap)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getinfo()
        # 发送信号
        # self.propertiesChange.emit(self.default_properties)

    # 设置输入输出设备
    def setDevices(self, in_devices, out_devices):
        self.setInDevices(in_devices)
        self.setOutDevices(out_devices)

    # 设置输出设备
    def setOutDevices(self, devices):
        self.pro_window.duration.out_devices_dialog.addDevices(devices)

    # 设置输入设备
    def setInDevices(self, devices):
        self.pro_window.duration.in_devices_dialog.addDevices(devices)

    def getinfo(self):
        self.default_properties = self.pro_window.getInfo()
        return self.default_properties

    def getInfo(self):
        self.all_properties = {'default_properties': self.pro_window.default_properties}
        for i in range(len(self.scene.items())):
            try:
                self.scene.items()[i].setProperties()
                self.all_properties[i + 1] = self.scene.items()[i].default_properties
            except Exception as e:
                print(e)

        return self.all_properties

    def restore(self, properties: dict):
        for d in properties:
            if d == 'default_properties':
                self.pro_window.setProperties(properties[d])
            else:
                dic = properties[d]
                if dic['name'] == 'text':
                    item = DiagramTextItem()
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    self.scene.addItem(item)
                    item.setPos(QPoint(dic['x_pos'], dic['y_pos']))
                elif dic['name'] < 4:
                    item = DiaItem(dic['name'], self.itemMenu, self.attributes)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                elif dic['name'] == 4:
                    p1 = QPointF(int(dic['P1 X']), int(dic['P1 Y']))
                    p2 = QPointF(int(dic['P2 X']), int(dic['P2 Y']))
                    p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
                    p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
                    item = DiaItem(dic['name'], self.itemMenu, self.attributes, p3, p4)
                    self.scene.addItem(item)
                    item.restore(dic)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
                else:
                    item = PixItem(dic['name'], self.itemMenu, self.attributes)
                    item.restore(dic)
                    self.scene.addItem(item)
                    item.setZValue(dic['z'])
                    item.setPos(QPoint(dic['x_pos'], dic['y_pos']))

    def clone(self, widget_id: str):
        """
        根据传入的widget_id，复制一个widget
        :param widget_id:
        :return:
        """
        slider = Slider(widget_id=widget_id)
        slider.pro_window.setProperties(self.pro_window.getInfo())
        for item in self.scene.items():
            item1 = item.clone()
            slider.scene.addItem(item1)
            item1.setPos(item.scenePos())
            slider.scene.update()
        return slider

    def changeWidgetId(self, new_widget_id: str):
        """
        修改widget的wid
        :param new_widget_id:
        :return:
        """
        self.widget_id = new_widget_id
