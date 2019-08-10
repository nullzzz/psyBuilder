import sys

from PyQt5.QtCore import pyqtSignal, Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QFont, QColor, QIntValidator, QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QToolButton, QButtonGroup, QMainWindow, QMenu, QAction, \
    QGridLayout, QLabel, QComboBox, QColorDialog
from quamash import QApplication

from app.center.widget_tabs.events.newSlider.button import LeftBox
from app.center.widget_tabs.events.newSlider.item.diaItem import DiaItem
from app.center.widget_tabs.events.newSlider.item.pixItem import PixItem

from app.center.widget_tabs.events.newSlider.property import SliderProperty
from app.center.widget_tabs.events.newSlider.scene import Scene
from app.func import Func


class Slider(QMainWindow):
    propertiesChange = pyqtSignal(str)
    InsertTextButton = 10

    def __init__(self, widget_id):
        super(Slider, self).__init__()
        self.widget_id = widget_id
        self.current_wid = widget_id
        self.attributes: list = []
        self.scene = Scene()
        self.scene.itemAdd.connect(self.addItem)

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

        self.delete_action = QAction(QIcon(Func.getImage("delete.png")), "&Delete", self)
        self.delete_action.setToolTip("Delete item from diagram")
        self.delete_action.triggered.connect(self.deleteItem)

        # self.itemMenu = QMenu()
        # self.itemMenu.addAction(self.delete_action)
        # self.itemMenu.addSeparator()
        # self.itemMenu.addAction(self.front_action)
        # self.itemMenu.addAction(self.back_action)

        self.setting = self.addToolBar('Setting')
        self.setting.addAction(self.open_action)
        self.setting.addAction(self.delete_action)
        self.setting.addAction(self.front_action)
        self.setting.addAction(self.back_action)

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
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"),
                                           Qt.white))

        self.line_color_bt = QToolButton()
        self.line_color_bt.setPopupMode(QToolButton.MenuButtonPopup)
        self.line_color_bt.setMenu(
            self.createColorMenu(self.lineColorChanged, Qt.black))
        self.lineAction = self.line_color_bt.menu().defaultAction()
        self.line_color_bt.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"),
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

        # self.pointerToolbar = self.addToolBar("Pointer type")
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
        self.scene.setSceneRect(0, 0, 2000, 2000)

        self.left_box = LeftBox()
        self.left_box.clicked.connect(self.addItem)
        self.setUI()

    def addItem(self):
        self.pointer_bt.setChecked(True)
        self.scene.setMode(Scene.InsertItem)

    def setUI(self):
        self.setWindowTitle("Slider")
        layout = QHBoxLayout()
        layout.addWidget(self.left_box, 1)
        layout.addWidget(self.view, 2)
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

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

    def selectDiaItem(self, d):
        self.fill_color_bt.setIcon(
            self.createColorToolButtonIcon(Func.getImage("floodfill.png"), QColor(d['itemcolor'])))
        self.line_color_bt.setIcon(
            self.createColorToolButtonIcon(Func.getImage("linecolor.png"), QColor(d['linecolor'])))
        self.line_wid_com.setCurrentText(str(d['linewidth']))

    def deleteItem(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

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

    #
    # def itemInserted(self, item):
    #     self.pointer_group.button(DiagramScene.MoveItem).setChecked(True)
    #     self.scene.setMode(self.pointer_group.checkedId())
    #     self.buttonGroup.button(item.diagram_type).setChecked(False)
    #
    # def pixitemInserted(self, item):
    #     self.pointer_group.button(DiagramScene.MoveItem).setChecked(True)
    #     self.scene.setMode(self.pointer_group.checkedId())
    #     self.buttonGroup.button(item.diagram_type).setChecked(False)

    def itemColorChanged(self):
        self.fillAction = self.sender()
        if self.fillAction.data() == 'More..':
            color = QColorDialog.getColor()
            if color.isValid():
                self.fill_color_bt.setIcon(
                    self.createColorToolButtonIcon(Func.getImage("floodfill.png"), color))
                self.scene.setItemColor(color)
        else:
            self.fill_color_bt.setIcon(
                self.createColorToolButtonIcon(Func.getImage("floodfill.png"),
                                               QColor(self.fillAction.data())))
            self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        if self.lineAction.data() == 'More..':
            color = QColorDialog.getColor()
            self.line_color_bt.setIcon(
                self.createColorToolButtonIcon(Func.getImage("linecolor.png"), color))
            self.scene.setLineColor(color)
        else:
            self.line_color_bt.setIcon(
                self.createColorToolButtonIcon(Func.getImage('linecolor.png'),
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

    # def about(self):
    #     QMessageBox.about(self, "About Diagram Scene",
    #                       "The <b>Diagram Scene</b> example shows use of the graphics framework.")

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.pro_window.show()

    def refresh(self):
        pass

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

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
        colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

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

    #
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

    # def restore(self, properties: dict):
    #     for d in properties:
    #         if d == 'default_properties':
    #             self.pro_window.setProperties(properties[d])
    #         else:
    #             dic = properties[d]
    #             if dic['name'] == 'text':
    #                 item = DiagramTextItem()
    #                 item.restore(dic)
    #                 item.setZValue(dic['z'])
    #                 self.scene.addItem(item)
    #                 item.setPos(QPoint(dic['x_pos'], dic['y_pos']))
    #             elif dic['name'] < 4:
    #                 item = DiagramItem(dic['name'], self.itemMenu, self.attributes)
    #                 self.scene.addItem(item)
    #                 item.restore(dic)
    #                 item.setZValue(dic['z'])
    #                 item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
    #             elif dic['name'] == 4:
    #                 p1 = QPointF(int(dic['P1 X']), int(dic['P1 Y']))
    #                 p2 = QPointF(int(dic['P2 X']), int(dic['P2 Y']))
    #                 p3 = QPointF((p1.x() - p2.x()) / 2, (p1.y() - p2.y()) / 2)
    #                 p4 = QPointF(-(p1.x() - p2.x()) / 2, -(p1.y() - p2.y()) / 2)
    #                 item = DiagramItem(dic['name'], self.itemMenu, self.attributes, p3, p4)
    #                 self.scene.addItem(item)
    #                 item.restore(dic)
    #                 item.setZValue(dic['z'])
    #                 # print(QPoint(int(dic['Center X']), int(dic['Center Y'])))
    #                 item.setPos(QPoint(int(dic['Center X']), int(dic['Center Y'])))
    #             else:
    #                 item = DiagramPixmapItem(dic['name'], self.itemMenu, self.attributes)
    #                 item.restore(dic)
    #                 self.scene.addItem(item)
    #                 item.setZValue(dic['z'])
    #                 item.setPos(QPoint(dic['x_pos'], dic['y_pos']))

    # def clone(self, widget_id: str):
    #     """
    #     根据传入的widget_id，复制一个widget
    #     :param widget_id:
    #     :return:
    #     """
    #     slider = Slider(widget_id=widget_id)
    #     slider.pro_window.setProperties(self.pro_window.getInfo())
    #     for item in self.scene.items():
    #         item1 = item.clone()
    #         slider.scene.addItem(item1)
    #         item1.setPos(item.scenePos())
    #         slider.scene.update()
    #     return slider

    def changeWidgetId(self, new_widget_id: str):
        """
        修改widget的wid
        :param new_widget_id:
        :return:
        """
        self.widget_id = new_widget_id


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = Slider("11")
    t.show()
    sys.exit(app.exec_())
