from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QToolButton, QButtonGroup, QMenu, QAction, \
    QComboBox, QColorDialog, QToolBar

from app.center.events.slider.left.leftBox import LeftBox
from app.func import Func
from lib import TabItemMainWindow
from ...events.slider.item.diaItem import DiaItem
from ...events.slider.item.linItem import LineItem
from ...events.slider.item.otherItem import OtherItem
from ...events.slider.item.pixItem import PixItem
from ...events.slider.item.textItem import TextItem
from ...events.slider.property import SliderProperty
from ...events.slider.scene import Scene


class Slider(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(Slider, self).__init__(widget_id, widget_name)
        self.current_wid = widget_id

        self.pro_window = SliderProperty()

        self.scene = Scene()
        self.left_box = LeftBox()

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        # opengl = QGLWidget(QGLFormat(QGL.SampleBuffers))
        # opengl.makeCurrent()
        # self.view.setViewport(opengl)

        width, height = Func.getCurrentScreenRes(self.pro_window.getScreenId())
        self.view.setMaximumSize(width, height)
        self.scene.setSceneRect(0, 0, width, height)
        # self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)

        self.default_properties: dict = {
            "Items": {},
            "Properties": self.pro_window.default_properties
        }
        self.initMenu()
        self.linkSignal()
        self.setUI()

    def initMenu(self):
        open_action = QAction(QIcon(Func.getImage("setting")), "setting", self)
        open_action.triggered.connect(self.openPro)

        front_action = QAction(QIcon(Func.getImage("sendtoback.png")), "Bring to Front", self)
        front_action.setToolTip("Bring item to front")
        front_action.triggered.connect(self.toFront)

        back_action = QAction(QIcon(Func.getImage("bringtofront.png")), "Sendto & Back", self)
        back_action.setToolTip("Send item to back")
        back_action.triggered.connect(self.toBack)

        open_item_action = QAction(QIcon(Func.getImage("setting.png")), "Properties", self)
        open_item_action.triggered.connect(self.openItem)

        delete_action = QAction(QIcon(Func.getImage("trash.png")), "Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.setToolTip("Delete item from diagram")
        delete_action.triggered.connect(self.deleteItem)

        copy_action = QAction(QIcon(Func.getImage("copy.png")), "Copy", self)
        copy_action.setShortcut("Ctrl+D")
        copy_action.setToolTip("copy item from diagram")
        copy_action.triggered.connect(self.copyItem)

        self.item_list = QComboBox()
        self.item_list.setMinimumWidth(100)
        self.item_list.addItem("none")
        self.item_list.currentTextChanged.connect(self.selectItem)

        self.item_pro_windows = QAction(QIcon(Func.getImage("item_pro.png")), "open item properties", self)
        self.item_pro_windows.setToolTip("Open current item's properties")
        self.item_pro_windows.triggered.connect(self.openItem)
        self.item_pro_windows.setEnabled(False)

        setting = QToolBar()
        setting.addAction(open_action)
        setting.addSeparator()
        setting.addAction(delete_action)
        setting.addAction(copy_action)
        setting.addAction(front_action)
        setting.addAction(back_action)
        setting.addWidget(self.item_list)
        setting.addAction(self.item_pro_windows)

        self.fill_color_bt = QToolButton()
        self.fill_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.fill_color_bt.setMenu(
            self.createColorMenu(self.itemColorChanged, Qt.white))
        self.fill_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("floodfill.png"),
                                       Qt.white))

        self.line_color_bt = QToolButton()
        self.line_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.line_color_bt.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("linecolor.png"),
                                       Qt.black))
        # 边框宽度
        self.line_width_com = QComboBox()
        self.line_width_com.setEditable(True)
        for i in range(2, 20, 2):
            self.line_width_com.addItem(str(i))
        validator = QIntValidator(0, 20, self)
        self.line_width_com.setValidator(validator)
        self.line_width_com.currentTextChanged.connect(self.changeLineWidth)
        setting.addWidget(self.fill_color_bt)
        setting.addWidget(self.line_color_bt)
        setting.addWidget(self.line_width_com)

        self.pointer_bt = QToolButton()
        self.pointer_bt.setCheckable(True)
        self.pointer_bt.setChecked(True)
        self.pointer_bt.setIcon(QIcon(Func.getImage("pointer.png")))
        line_bt = QToolButton()
        line_bt.setCheckable(True)
        line_bt.setIcon(QIcon(Func.getImage("linepointer.png")))
        lasso_bt = QToolButton()
        lasso_bt.setCheckable(True)
        lasso_bt.setIcon(QIcon(Func.getImage("lasso.png")))

        self.pointer_group = QButtonGroup()
        self.pointer_group.addButton(self.pointer_bt, Scene.MoveItem)
        self.pointer_group.addButton(line_bt, Scene.InsertLine)
        self.pointer_group.addButton(lasso_bt, Scene.SelectItem)
        self.pointer_group.buttonClicked[int].connect(self.pointerGroupClicked)

        setting.addWidget(self.pointer_bt)
        setting.addWidget(line_bt)
        setting.addWidget(lasso_bt)
        self.background_bt = QToolButton()
        self.background_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.background_bt.setMenu(
            self.createBackgroundMenu(self.changeBackground))
        self.background_bt.setIcon(QIcon(Func.getImage("background4.png")))
        setting.addWidget(self.background_bt)

        self.addToolBar(Qt.TopToolBarArea, setting)

        self.item_menu = QMenu()
        self.item_menu.addAction(delete_action)
        self.item_menu.addAction(copy_action)
        self.item_menu.addSeparator()
        self.item_menu.addAction(front_action)
        self.item_menu.addAction(back_action)
        self.item_menu.addAction(open_item_action)
        self.scene.menu = self.item_menu

    def linkSignal(self):
        self.scene.itemAdd.connect(self.addItem)
        self.scene.selectionChanged.connect(self.changeItemList)

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def setUI(self):
        self.setWindowTitle("slider")
        layout = QHBoxLayout()
        layout.addWidget(self.left_box, 0, Qt.AlignLeft)
        layout.addWidget(self.view, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def openPro(self):
        self.pro_window.show()

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
            item_name = item.getName()
            index = self.item_list.findText(item_name, Qt.MatchExactly)
            if index != -1:
                self.item_list.removeItem(index)

    def copyItem(self):
        for item in self.scene.selectedItems():
            self.scene.copyItem(item)

    def toFront(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        z_value = 0
        for item in overlap_items:
            # if item.zValue() >= z_value: and (
            #         isinstance(item, TextItem) or isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() + 0.1
        selected_item.setZValue(z_value)

    def toBack(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        z_value = 0
        for item in overlap_items:
            if item.zValue() <= z_value: # and (
                    # isinstance(item, TextItem) or isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() - 0.1
        selected_item.setZValue(z_value)

    def selectItem(self, item_name: str):
        """
        when choose some items by item list
        :param item_name:
        :return:
        """
        self.blockSignals(True)
        self.item_pro_windows.setEnabled(item_name != "none")
        for item in self.scene.items():
            if isinstance(item, TextItem) or isinstance(item, PixItem) \
                    or isinstance(item, LineItem) \
                    or isinstance(item, OtherItem) \
                    or isinstance(item, DiaItem):
                item.setSelected(item_name == item.getName())
                if item_name == item.getName():
                    self.changeTool(item)
                    # self.view.centerOn(item)
        self.blockSignals(False)

    def openItem(self):
        items = self.scene.selectedItems()
        if items:
            items[0].openPro()

    def addItem(self, item_name: str):
        """
        change item list when item added by drag and drop
        :param item_name:
        :return:
        """
        self.pointer_bt.setChecked(True)
        self.scene.setMode(Scene.InsertItem)
        self.item_list.addItem(item_name)

    def changeItemList(self):
        self.blockSignals(True)
        items = self.scene.selectedItems()
        if items:
            if items[0].getName() != self.item_list.currentText():
                self.item_list.setCurrentText(items[0].getName())
        else:
            self.item_list.setCurrentIndex(0)
        self.blockSignals(False)

    def changeTool(self, item):
        """
        show item information such as color when selected.
        :param item: selected item
        :return:
        """
        border_width = item.properties.get("Border Width", "1")
        if not border_width.startswith("["):
            self.line_width_com.setCurrentText(border_width)

        border_color: str = item.properties.get("Border Color", "0,0,0")
        if border_color.startswith("["):
            r, g, b, a = 0, 0, 0, 255
        else:
            color = [int(x) for x in border_color.split(",")]
            if len(color) == 3:
                r, g, b = color
                a = 255
            else:
                r, g, b, a = color
        color = QColor(r, g, b, a)
        self.line_color_bt.setIcon(self.createColorButtonIcon(Func.getImage("linecolor.png"), color))

        fill_color: str = item.properties.get("Fill Color", "255,255,255")
        if fill_color.startswith("["):
            r, g, b, a = 255, 255, 255, 255
        else:
            color = [int(x) for x in fill_color.split(",")]
            if len(color) == 3:
                r, g, b = color
                a = 255
            else:
                r, g, b, a = color
        color = QColor(r, g, b, a)
        self.fill_color_bt.setIcon(self.createColorButtonIcon(Func.getImage("floodfill.png"), color))

    def refresh(self):
        self.pro_window.refresh()

        width, height = Func.getCurrentScreenRes(self.pro_window.getScreenId())
        self.setMaximumSize(width, height)
        self.scene.setSceneRect(0, 0, width, height)
        # self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)
        self.scene.setAttributes(format_attributes)

    def getInfo(self):
        self.default_properties["Items"] = self.scene.getInfo()
        self.pro_window.updateInfo()
        return self.default_properties

    def getProperties(self):
        return self.pro_window.getProperties()

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointer_group.checkedId())

    def itemColorChanged(self):
        color_data = self.sender().data()
        if color_data == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fill_color_bt.setIcon(
                    self.createColorButtonIcon(Func.getImage("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fill_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("floodfill.png"),
                                           QColor(color_data)))
            self.scene.setItemColor(QColor(color_data))

    def lineColorChanged(self):
        color_data = self.sender().data()
        if color_data == 'More..':
            color = QColorDialog.getColor()
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage('linecolor.png'),
                                           QColor(color_data)))
            self.scene.setLineColor(QColor(color_data))

    def changeLineWidth(self, width: str):
        self.scene.setLineWidth(int(width))

    def changeBackground(self):
        fn = f"background{self.sender().data()}.png"
        fp = Func.getImage(fn)
        self.background_bt.setIcon(QIcon(fp))
        self.scene.setBackgroundBrush(QBrush(QPixmap(fp)))
        self.scene.update()
        self.view.update()

    def createBackgroundMenu(self, slot):
        back_menu = QMenu(self)
        action1 = QAction(QIcon(Func.getImage("background1.png")), 'Blue Grid', self)
        action2 = QAction(QIcon(Func.getImage("background2.png")), 'White Grid', self)
        action3 = QAction(QIcon(Func.getImage("background3.png")), 'Gray Grid', self)
        action4 = QAction(QIcon(Func.getImage("background4.png")), 'No Grid', self, )
        action1.setData('1')
        action1.triggered.connect(slot)
        action2.setData('2')
        action2.triggered.connect(slot)
        action3.setData('3')
        action3.triggered.connect(slot)
        action4.setData('4')
        action4.triggered.connect(slot)
        back_menu.setDefaultAction(action4)
        back_menu.addAction(action1)
        back_menu.addAction(action2)
        back_menu.addAction(action3)
        back_menu.addAction(action4)
        return back_menu

    def createColorMenu(self, slot, default_color):
        colors = (Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow)
        names = ("black", "white", "red", "blue", "yellow")

        color_menu = QMenu(self)
        more_action = QAction('More..', self)
        more_action.setData('More..')
        more_action.triggered.connect(slot)
        for color, name in zip(colors, names):
            action = QAction(self.createColorIcon(color), name, self)
            action.triggered.connect(slot)
            action.setData(QColor(color))
            color_menu.addAction(action)
            if color == default_color:
                color_menu.setDefaultAction(action)
        color_menu.addAction(more_action)
        return color_menu

    @staticmethod
    def createColorButtonIcon(file_path, color):
        pix = QPixmap(50, 80)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        image = QPixmap(file_path)
        target = QRect(0, 0, 50, 60)
        source = QRect(0, 0, 42, 42)
        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()
        return QIcon(pix)

    @staticmethod
    def createColorIcon(color):
        pix = QPixmap(20, 20)
        painter = QPainter(pix)
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 20, 20), color)
        painter.end()
        return QIcon(pix)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.getInfo()
        # 发送信号
        self.propertiesChanged.emit(self.widget_id)

    """
     Functions that must be complete in new version
     """

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return self.getInfo()

    def restore(self, properties: dict):
        pro = properties.get("Properties")
        self.pro_window.setProperties(pro)

        items: dict = properties.get("Items")
        self.scene.setProperties(items)

        self.item_list.clear()
        self.item_list.addItems(items.keys())
        self.item_list.insertItem(0, "none")

    def clone(self, new_widget_id: str, new_widget_name):
        """
        根据传入的widget_id，复制一个widget
        :param new_widget_name:
        :param new_widget_id:
        :return:
        """
        clone_page = Slider(new_widget_id, new_widget_name)
        self.getInfo()
        clone_page.pro_window.setProperties(self.pro_window.default_properties.copy())
        clone_page.scene.setProperties(self.scene.getInfo())
        return clone_page

    ####################
    # single property
    ###################

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        返回x坐标值
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Center X")

    def getYAxisCoordinates(self) -> str:
        """
        返回y坐标值
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Center Y")

    def getWidth(self) -> str:
        """
        返回宽度
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Width")

    def getHeight(self) -> str:
        """
        返回高度
        :return:
        """
        return self.default_properties.get("Properties").get("Frame").get("Height")

    def getEnable(self) -> str:
        """
        返回frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """返回frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getBorderColor(self) -> str:
        """
        返回边框颜色
        :return:
        """
        return self.pro_window.frame.border_color.getColor()

    def getBorderWidth(self) -> str:
        """
        返回边框宽度
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameFillColor(self) -> str:
        """
        返回边框背景色
        :return:
        """
        return self.pro_window.frame.back_color.getColor()

    def getDuration(self) -> str:
        """
        返回duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        返回输出设备
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

    def getItems(self):
        return self.scene.getInfo()
