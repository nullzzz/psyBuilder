from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QToolButton, QButtonGroup, QMenu, QAction, \
    QComboBox, QColorDialog

from app.func import Func
from lib import TabItemMainWindow
from .item.diaItem import DiaItem
from .item.linItem import LineItem
from .item.otherItem import OtherItem
from .item.pixItem import PixItem
from .item.textItem import TextItem
from .leftBox import LeftBox
from .property import SliderProperty
from .scene import Scene


class Slider(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(Slider, self).__init__(widget_id, widget_name)
        self.attributes: list = []
        self.scene = Scene()
        self.scene.itemAdd.connect(self.addItem)
        self.scene.selectionChanged.connect(self.changeItemList)

        self.pro_window = SliderProperty()
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.open_action = QAction(QIcon(Func.getImagePath("setting")), "setting", self)
        self.open_action.triggered.connect(self.openPro)

        self.front_action = QAction(QIcon(Func.getImagePath("sendtoback.png")), "Bring to Front", self)
        self.front_action.setToolTip("Bring item to front")
        self.front_action.triggered.connect(self.toFront)

        self.back_action = QAction(QIcon(Func.getImagePath("bringtofront.png")), "Sendto & Back", self)
        self.back_action.setToolTip("Send item to back")
        self.back_action.triggered.connect(self.toBack)

        self.open_item_action = QAction(QIcon(Func.getImagePath("setting.png")), "Properties", self)
        self.open_item_action.triggered.connect(self.openItem)

        self.delete_action = QAction(QIcon(Func.getImagePath("trash.png")), "Delete", self)
        self.delete_action.setShortcut("Ctrl+D")
        self.delete_action.setToolTip("Delete item from diagram")
        self.delete_action.triggered.connect(self.deleteItem)

        self.itemMenu = QMenu()
        self.itemMenu.addAction(self.delete_action)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.front_action)
        self.itemMenu.addAction(self.back_action)
        self.itemMenu.addAction(self.open_item_action)

        self.item_list = QComboBox()
        self.item_list.setMinimumWidth(100)
        self.item_list.addItem("none")
        self.item_list.currentTextChanged.connect(self.selectItem)

        self.item_pro_windows = QAction(QIcon(Func.getImagePath("item_pro.png")), "open item properties", self)
        self.item_pro_windows.setToolTip("Open current item's properties")
        self.item_pro_windows.triggered.connect(self.openItem)
        self.item_pro_windows.setEnabled(False)

        self.setting = self.addToolBar('Setting')
        self.setting.addAction(self.open_action)
        self.setting.addAction(self.delete_action)
        self.setting.addAction(self.front_action)
        self.setting.addAction(self.back_action)

        self.setting.addWidget(self.item_list)
        self.setting.addAction(self.item_pro_windows)

        # 边框宽度
        self.line_wid_com = QComboBox()
        self.line_wid_com.setEditable(True)
        for i in range(2, 20, 2):
            self.line_wid_com.addItem(str(i))
        validator = QIntValidator(0, 20, self)
        self.line_wid_com.setValidator(validator)
        self.line_wid_com.currentIndexChanged.connect(self.changeLineWidth)

        self.fill_color_bt = QToolButton()
        self.fill_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.fill_color_bt.setMenu(
            self.createColorMenu(self.itemColorChanged, Qt.white))
        self.fillAction = self.fill_color_bt.menu().defaultAction()
        self.fill_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImagePath("floodfill.png"),
                                       Qt.white))

        self.line_color_bt = QToolButton()
        self.line_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.line_color_bt.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.lineAction = self.line_color_bt.menu().defaultAction()
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImagePath("linecolor.png"),
                                       Qt.black))
        self.line_color_bt.clicked.connect(self.lineButtonTriggered)

        self.setting.addWidget(self.fill_color_bt)
        self.setting.addWidget(self.line_color_bt)
        self.setting.addWidget(self.line_wid_com)

        self.pointer_bt = QToolButton()
        self.pointer_bt.setCheckable(True)
        self.pointer_bt.setChecked(True)
        self.pointer_bt.setIcon(QIcon(Func.getImagePath("pointer.png")))
        line_bt = QToolButton()
        line_bt.setCheckable(True)
        line_bt.setIcon(QIcon(Func.getImagePath("linepointer.png")))
        lasso_bt = QToolButton()
        lasso_bt.setCheckable(True)
        lasso_bt.setIcon(QIcon(Func.getImagePath("lasso.png")))

        self.pointer_group = QButtonGroup()
        self.pointer_group.addButton(self.pointer_bt, Scene.MoveItem)
        self.pointer_group.addButton(line_bt, Scene.InsertLine)
        self.pointer_group.addButton(lasso_bt, Scene.SelectItem)
        self.pointer_group.buttonClicked[int].connect(self.pointerGroupClicked)

        self.setting.addWidget(self.pointer_bt)
        self.setting.addWidget(line_bt)
        self.setting.addWidget(lasso_bt)
        self.background_bt = QToolButton()
        self.background_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.background_bt.setMenu(
            self.createBackgroundMenu(self.changeBackground))
        self.background_bt.setIcon(QIcon(Func.getImagePath("background4.png")))
        self.background_bt.clicked.connect(self.fillButtonTriggered)
        self.setting.addWidget(self.background_bt)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        width, height = Func.getCurrentScreenRes(self.pro_window.general.using_screen_id)

        self.view.setMaximumSize(width / 2, height / 2)
        self.scene.setSceneRect(0, 0, width, height)
        self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)

        self.scene.menu = self.itemMenu

        self.left_box = LeftBox()

        self.default_properties: dict = {
            "items": {},
            "pro": self.pro_window.getInfo()
        }
        self.setUI()

    def addItem(self, item_name: str):
        self.pointer_bt.setChecked(True)
        self.scene.setMode(Scene.InsertItem)
        if item_name:
            self.item_list.addItem(item_name)

    def changeItemList(self):
        items = self.scene.selectedItems()
        if items:
            if items[0].getName() != self.item_list.currentText():
                self.item_list.setCurrentText(items[0].getName())
        else:
            self.item_list.setCurrentIndex(0)

    def selectItem(self, item_name: str):
        self.scene.selectionChanged.disconnect()
        self.item_pro_windows.setEnabled(item_name != "none")
        for item in self.scene.items():
            if isinstance(item, TextItem) or isinstance(item, PixItem) \
                    or isinstance(item, LineItem) \
                    or isinstance(item, OtherItem) \
                    or isinstance(item, DiaItem):
                item.setSelected(item_name == item.getName())
                if item_name == item.getName():
                    self.changeTool(item)
        self.scene.selectionChanged.connect(self.changeItemList)

    def changeTool(self, item):
        border_width = item.default_properties.get("Border width", "2")
        if not border_width.startswith("["):
            self.line_wid_com.setCurrentText(border_width)

        border_color: str = item.default_properties.get("Border color", "0,0,0")
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
        self.line_color_bt.setIcon(self.createColorButtonIcon(Func.getImagePath("linecolor.png"), color))

        fill_color: str = item.default_properties.get("Fill color", "0,0,0")
        if fill_color.startswith("["):
            r, g, b, a = 0, 0, 0, 255
        else:
            color = [int(x) for x in fill_color.split(",")]
            if len(color) == 3:
                r, g, b = color
                a = 255
            else:
                r, g, b, a = color
        color = QColor(r, g, b, a)
        self.fill_color_bt.setIcon(self.createColorButtonIcon(Func.getImagePath("floodfill.png"), color))

    def setUI(self):
        self.setWindowTitle("Slider")
        layout = QHBoxLayout()
        layout.addWidget(self.left_box, 0, Qt.AlignLeft)
        layout.addWidget(self.view, 1, Qt.AlignHCenter | Qt.AlignVCenter)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.pro_window.refresh()
        self.getInfo()

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        width, height = Func.getCurrentScreenRes(self.pro_window.general.using_screen_id)
        self.view.setMaximumSize(width / 2, height / 2)
        self.scene.setSceneRect(0, 0, width, height)
        self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)

    def getInfo(self):
        self.default_properties = {
            "items": self.scene.getInfo(),
            "pro": self.pro_window.getInfo()
        }
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    def getShowProperties(self):
        info = self.pro_window.default_properties.copy()
        info.pop("Input devices")
        info.pop("Output devices")
        return info

    def getHiddenAttribute(self):
        hidden_attr = {
            "onsettime": 0,
            "acc": 0,
            "resp": 0,
            "rt": 0
        }
        return hidden_attr

    def selectDiaItem(self, d):
        self.fill_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImagePath("floodfill.png"), QColor(d['itemcolor'])))
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImagePath("linecolor.png"), QColor(d['linecolor'])))
        self.line_wid_com.setCurrentText(str(d['linewidth']))

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
            item_name = item.getName()
            index = self.item_list.findText(item_name, Qt.MatchExactly)
            if index != -1:
                self.item_list.removeItem(index)

    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointer_group.checkedId())

    def toFront(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        z_value = 0
        for item in overlap_items:
            if item.zValue() >= z_value and (
                    isinstance(item, TextItem) or isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() + 0.1
        selected_item.setZValue(z_value)

    def toBack(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        z_value = 0
        for item in overlap_items:
            if item.zValue() <= z_value and (
                    isinstance(item, TextItem) or isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() - 0.1
        selected_item.setZValue(z_value)

    def itemColorChanged(self):
        self.fillAction = self.sender()
        if self.fillAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fill_color_bt.setIcon(
                    self.createColorButtonIcon(Func.getImagePath("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fill_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImagePath("floodfill.png"),
                                           QColor(self.fillAction.data())))
            self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        if self.lineAction.data() == 'More..':
            color = QColorDialog.getColor()
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImagePath("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImagePath('linecolor.png'),
                                           QColor(self.lineAction.data())))
            self.lineButtonTriggered()

    def changeLineWidth(self):
        self.scene.setLineWidth(int(self.line_wid_com.currentText()))

    def changeBackground(self):
        fn = f"background{self.sender().data()}.png"
        fp = Func.getImagePath(fn)
        self.background_bt.setIcon(QIcon(fp))
        self.scene.setBackgroundBrush(QBrush(QPixmap(fp)))
        self.scene.update()
        self.view.update()

    def fillButtonTriggered(self):
        self.scene.setItemColor(QColor(self.fillAction.data()))
        # self.getInfo()# after changed the color, updating the default_properties

    def lineButtonTriggered(self):
        self.scene.setLineColor(QColor(self.lineAction.data()))
        # self.getInfo()  # after changed the color, updating the default_properties

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def openItem(self):
        items = self.scene.selectedItems()
        if items:
            items[0].openPro()

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)
        self.scene.setAttributes(format_attributes)

    def createMenus(self):
        self.itemMenu = QMenu()
        self.itemMenu.addAction(self.delete_action)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.front_action)
        self.itemMenu.addAction(self.back_action)

    def createBackgroundMenu(self, slot):
        back_menu = QMenu(self)
        action1 = QAction(QIcon(Func.getImagePath("background1.png")), 'Blue Grid', self)
        action2 = QAction(QIcon(Func.getImagePath("background2.png")), 'White Grid', self)
        action3 = QAction(QIcon(Func.getImagePath("background3.png")), 'Gray Grid', self)
        action4 = QAction(QIcon(Func.getImagePath("background4.png")), 'No Grid', self, )
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
        self.propertiesChanged.emit(self.pro_window.default_properties)

    def restore(self, properties: dict):
        if isinstance(properties, dict):
            # print(f"line 446 slider: {properties}")
            self.default_properties = properties
            pro: dict = self.default_properties.get("pro")
            self.pro_window.setProperties(pro)

            items: dict = self.default_properties.get("items")
            self.scene.setProperties(items)

            self.item_list.clear()
            self.item_list.addItems(items.keys())
            self.item_list.insertItem(0, "none")

    def clone(self, widget_id: str):
        """
        根据传入的widget_id，复制一个widget
        :param widget_id:
        :return:
        """
        clone_page = Slider(widget_id=widget_id)
        clone_page.pro_window.setProperties(self.pro_window.getInfo())
        clone_page.scene.setProperties(self.scene.getInfo())
        return clone_page

    def changeWidgetId(self, new_widget_id: str):
        """
        修改widget的wid
        :param new_widget_id:
        :return:
        """
        self.widget_id = new_widget_id

    def getDuration(self) -> str:
        """
        返回duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

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

    def getOutputDevice(self) -> dict:
        """
        返回输出设备
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input devices", {})

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)