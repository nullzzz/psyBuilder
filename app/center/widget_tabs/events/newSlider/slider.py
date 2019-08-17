from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QToolButton, QButtonGroup, QMainWindow, QMenu, QAction, \
    QComboBox, QColorDialog

from app.center.widget_tabs.events.newSlider.item.diaItem import DiaItem
from app.center.widget_tabs.events.newSlider.item.linItem import LineItem
from app.center.widget_tabs.events.newSlider.item.otherItem import OtherItem
from app.center.widget_tabs.events.newSlider.item.pixItem import PixItem
from app.center.widget_tabs.events.newSlider.leftBox import LeftBox
from app.center.widget_tabs.events.newSlider.property import SliderProperty
from app.center.widget_tabs.events.newSlider.scene import Scene
from app.func import Func


class Slider(QMainWindow):
    propertiesChange = pyqtSignal(dict)

    def __init__(self, widget_id):
        super(Slider, self).__init__()
        self.widget_id = widget_id
        self.current_wid = widget_id
        self.attributes: list = []
        self.scene = Scene()
        self.scene.itemAdd.connect(self.addItem)
        self.scene.selectionChanged.connect(self.changeItemList)

        self.pro_window = SliderProperty()
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.open_action = QAction(QIcon(Func.getImage("setting")), "setting", self)
        self.open_action.triggered.connect(self.openPro)

        self.front_action = QAction(QIcon(Func.getImage("sendtoback.png")), "Bring to Front", self)
        self.front_action.setToolTip("Bring item to front")
        self.front_action.triggered.connect(self.toFront)

        self.back_action = QAction(QIcon(Func.getImage("bringtofront.png")), "Sendto & Back", self)
        self.back_action.setToolTip("Send item to back")
        self.back_action.triggered.connect(self.toBack)

        self.open_item_action = QAction(QIcon(Func.getImage("setting.png")), "Properties", self)
        self.open_item_action.triggered.connect(self.openItem)

        self.delete_action = QAction(QIcon(Func.getImage("delete.png")), "&Delete", self)
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

        self.item_pro_windows = QAction(QIcon(Func.getImage("item.png")), "open item properties", self)
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
            self.createColorButtonIcon(Func.getImage("floodfill.png"),
                                       Qt.white))

        self.line_color_bt = QToolButton()
        self.line_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.line_color_bt.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.lineAction = self.line_color_bt.menu().defaultAction()
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("linecolor.png"),
                                       Qt.black))
        self.line_color_bt.clicked.connect(self.lineButtonTriggered)

        self.setting.addWidget(self.fill_color_bt)
        self.setting.addWidget(self.line_color_bt)
        self.setting.addWidget(self.line_wid_com)

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

        self.setting.addWidget(self.pointer_bt)
        self.setting.addWidget(line_bt)
        self.setting.addWidget(lasso_bt)
        self.background_bt = QToolButton()
        self.background_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.background_bt.setMenu(
            self.createBackgroundMenu(self.changeBackground))
        self.background_bt.setIcon(QIcon(Func.getImage("background4.png")))
        self.background_bt.clicked.connect(self.fillButtonTriggered)
        self.setting.addWidget(self.background_bt)

        self.view = QGraphicsView(self.scene)

        width, height = Func.getCurrentScreenRes(self.pro_window.general.using_screen_id)
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
            if isinstance(item, PixItem) or isinstance(item, LineItem) or isinstance(item, OtherItem):
                item.setSelected(item_name == item.getName())
                if item_name == item.getName():
                    self.changeTool(item)
        self.scene.selectionChanged.connect(self.changeItemList)

    def changeTool(self, item):
        border_width = item.default_properties.get("Border width", "2")
        self.line_wid_com.setCurrentText(border_width)

        border_color: str = item.default_properties.get("Border color", "0,0,0")
        if border_color.startswith("["):
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(x) for x in border_color.split(",")]
        color = QColor(r, g, b)
        self.line_color_bt.setIcon(self.createColorButtonIcon(Func.getImage("linecolor.png"), color))

    def setUI(self):
        self.setWindowTitle("Slider")
        layout = QHBoxLayout()
        layout.addWidget(self.left_box, 1)
        layout.addWidget(self.view, 2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def refresh(self):
        self.attributes = Func.getAttributes(self.widget_id)
        self.setAttributes(self.attributes)
        self.pro_window.general.refresh()
        self.getInfo()

        width, height = Func.getCurrentScreenRes(self.pro_window.general.using_screen_id)
        self.scene.setSceneRect(0, 0, width, height)
        self.view.fitInView(0, 0, width / 2, height / 2, Qt.KeepAspectRatio)

    def getInfo(self):
        self.default_properties = {
            "items": self.scene.getInfo(),
            "pro": self.pro_window.getInfo()
        }
        return self.default_properties

    def getProperties(self):
        return self.default_properties

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
            self.createColorButtonIcon(Func.getImage("floodfill.png"), QColor(d['itemcolor'])))
        self.line_color_bt.setIcon(
            self.createColorButtonIcon(Func.getImage("linecolor.png"), QColor(d['linecolor'])))
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
            if item.zValue() >= z_value and (isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() + 0.1
        selected_item.setZValue(z_value)

    def toBack(self):
        if not self.scene.selectedItems():
            return
        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()
        z_value = 0
        for item in overlap_items:
            if item.zValue() <= z_value and (isinstance(item, DiaItem) or isinstance(item, PixItem)):
                z_value = item.zValue() - 0.1
        selected_item.setZValue(z_value)

    def itemColorChanged(self):
        self.fillAction = self.sender()
        if self.fillAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fill_color_bt.setIcon(
                    self.createColorButtonIcon(Func.getImage("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fill_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("floodfill.png"),
                                           QColor(self.fillAction.data())))
            self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        if self.lineAction.data() == 'More..':
            color = QColorDialog.getColor()
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.line_color_bt.setIcon(
                self.createColorButtonIcon(Func.getImage('linecolor.png'),
                                           QColor(self.lineAction.data())))
            self.lineButtonTriggered()

    def changeLineWidth(self):
        self.scene.setLineWidth(int(self.line_wid_com.currentText()))

    def changeBackground(self):
        fn = f"background{self.sender().data()}.png"
        fp = Func.getImage(fn)
        self.background_bt.setIcon(QIcon(fp))
        self.scene.setBackgroundBrush(QBrush(QPixmap(fp)))
        self.scene.update()
        self.view.update()

    def fillButtonTriggered(self):
        self.scene.setItemColor(QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QColor(self.lineAction.data()))

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
        self.propertiesChange.emit(self.pro_window.default_properties)

    def restore(self, properties: dict):
        if isinstance(properties, dict):
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
