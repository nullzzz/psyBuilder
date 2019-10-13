import os
import re
import sys
import traceback

from PyQt5.QtCore import Qt, QSettings, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPalette
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QShortcut, QLabel, QGridLayout, \
    QVBoxLayout, QPushButton, QWidget, QLineEdit

from app.attributes.main import Attributes
from app.center.main import Center
from app.center.widget_tabs.events.cycle.main import Cycle
from app.center.widget_tabs.events.durationPage import DurationPage
from app.center.widget_tabs.timeline.main import Timeline
from app.deviceSelection.IODevice.globalDevices import GlobalDevice
from app.deviceSelection.progressBar import LoadingTip
from app.deviceSelection.quest.questinit import QuestInit
from app.deviceSelection.tracker.trackerinit import TrackerInit
from app.func import Func
from app.info import Info
from app.output.main import Output
from app.properties.main import Properties
from app.registry import writeToRegistry
from app.structure.main import Structure
from lib.psy_message_box import PsyMessageBox as QMessageBox
from lib.wait_dialog import WaitDialog
from .compile_PTB import compilePTB


class PsyApplication(QMainWindow):
    def __init__(self, parent=None):
        super(PsyApplication, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose, True)

        # ui
        self.setWindowTitle("Psy Builder 0.1")
        self.setWindowIcon(QIcon(Func.getImage("icon.png")))

        menu_bar = self.menuBar()

        # file menu
        file_menu = menu_bar.addMenu("&File")
        new_file_action = QAction("&New", self)
        new_file_action.triggered.connect(self.newFile)
        open_file_action = QAction("&Open", self)
        open_file_action.triggered.connect(self.loadIn)
        save_file_action = QAction("&Save", self)
        save_file_action.triggered.connect(self.save)
        save_as_file_action = QAction("&Save As", self)
        save_as_file_action.triggered.connect(self.saveAs)
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(QApplication.exit)

        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_as_file_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # view menu
        view_menu = menu_bar.addMenu("&View")
        self.attribute_action = QAction("&Attribute", self)
        self.structure_action = QAction("&Structure", self)
        self.main_action = QAction("&Main", self)
        self.property_action = QAction("&Property", self)
        self.output_action = QAction("&Output", self)

        self.save_default_action = QAction("&Save as Default", self)
        self.default_action = QAction("&Default", self)

        self.attribute_action.setData("attribute")
        self.structure_action.setData("structure")
        self.main_action.setData("main")
        self.output_action.setData("output")
        self.property_action.setData("property")

        self.attribute_action.triggered.connect(self.setDockView)
        self.structure_action.triggered.connect(self.setDockView)
        self.main_action.triggered.connect(self.setDockView)
        self.output_action.triggered.connect(self.setDockView)
        self.property_action.triggered.connect(self.setDockView)

        self.save_default_action.triggered.connect(self.updateLayout)
        self.default_action.triggered.connect(self.resetView)

        view_menu.addAction(self.attribute_action)
        view_menu.addAction(self.structure_action)
        view_menu.addAction(self.main_action)
        view_menu.addAction(self.property_action)
        view_menu.addAction(self.output_action)
        view_menu.addSeparator()
        view_menu.addAction(self.default_action)

        # devices menu
        self.input_devices = GlobalDevice(io_type=Info.INPUT_DEVICE)
        self.input_devices.setWindowModality(Qt.ApplicationModal)
        self.input_devices.ok()
        self.output_devices = GlobalDevice(io_type=Info.OUTPUT_DEVICE)
        self.output_devices.setWindowModality(Qt.ApplicationModal)
        self.output_devices.ok()
        self.quest_init = QuestInit()
        self.quest_init.setWindowModality(Qt.ApplicationModal)
        self.tracker_init = TrackerInit()
        self.tracker_init.setWindowModality(Qt.ApplicationModal)

        # self.input_devices.deviceNameChanged.connect(Func.changeCertainDeviceNameWhileUsing)
        # self.output_devices.deviceNameChanged.connect(Func.changeCertainDeviceNameWhileUsing)
        devices_menu = menu_bar.addMenu("&Devices")

        output_devices_action = QAction("&Output Devices", self)
        input_devices_action = QAction("&Input Devices", self)
        output_devices_action.triggered.connect(lambda: self.showDevices(1))
        input_devices_action.triggered.connect(lambda: self.showDevices(0))
        quest_init_action = QAction("&Quest", self)
        quest_init_action.triggered.connect(self.quest_init.show)
        tracker_init_action = QAction("&Tracker", self)
        tracker_init_action.triggered.connect(self.tracker_init.show)

        devices_menu.addAction(output_devices_action)
        devices_menu.addAction(input_devices_action)
        devices_menu.addAction(quest_init_action)
        devices_menu.addAction(tracker_init_action)

        # build menu
        build_menu = menu_bar.addMenu("&Building")
        build_menu.addSection("what")

        platform_menu = build_menu.addMenu("&Platform")

        self.linux_action = QAction("&Linux", self)
        self.linux_action.setChecked(True)

        self.windows_action = QAction("&Windows", self)
        self.mac_action = QAction("&Mac", self)

        icon = QIcon(Func.getImage("dock_visible.png"))

        self.linux_action.setIcon(icon)
        self.windows_action.setIcon(icon)
        self.windows_action.setIconVisibleInMenu(False)
        self.mac_action.setIcon(icon)
        self.mac_action.setIconVisibleInMenu(False)

        self.linux_action.triggered.connect(self.changePlatform)
        self.windows_action.triggered.connect(self.changePlatform)
        self.mac_action.triggered.connect(self.changePlatform)

        platform_menu.addAction(self.linux_action)
        platform_menu.addAction(self.windows_action)
        platform_menu.addAction(self.mac_action)



        # load image mode
        image_load_menu = build_menu.addMenu("&image Load Mode")

        self.before_event_action = QAction("&before_event", self)
        self.before_event_action.setChecked(True)

        self.before_trial_action = QAction("&before_trial", self)
        self.before_exp_action = QAction("&before_exp", self)

        # icon = QIcon(Func.getImage("dock_visible.png"))

        self.before_event_action.setIcon(icon)
        self.before_trial_action.setIcon(icon)
        self.before_trial_action.setIconVisibleInMenu(False)
        self.before_exp_action.setIcon(icon)
        self.before_exp_action.setIconVisibleInMenu(False)

        self.before_event_action.triggered.connect(self.changeImageLoadMode)
        self.before_trial_action.triggered.connect(self.changeImageLoadMode)
        self.before_exp_action.triggered.connect(self.changeImageLoadMode)

        image_load_menu.addAction(self.before_event_action)
        image_load_menu.addAction(self.before_trial_action)
        image_load_menu.addAction(self.before_exp_action)


        # compile
        compile_action = QAction("&Compile", self)
        compile_action.setShortcut("Ctrl+F5")
        compile_action.triggered.connect(self.compile)
        build_menu.addAction(compile_action)

        # help menu
        help_menu = menu_bar.addMenu("&Help")
        reg_action = QAction("&Registry", self)
        about_action = QAction("&About", self)
        about_Qt_action = QAction("&About Qt", self)
        check_for_update = QAction("&Check for updates", self)

        reg_action.triggered.connect(self.registry)
        about_action.triggered.connect(self.about)
        about_Qt_action.triggered.connect(QApplication.instance().aboutQt)
        check_for_update.triggered.connect(self.checkUpdate)

        help_menu.addAction(reg_action)
        help_menu.addAction(about_action)
        help_menu.addAction(about_Qt_action)
        help_menu.addAction(check_for_update)

        # attributes
        self.attributes = Attributes(self)
        self.attributes.setWindowTitle("Attributes")
        self.attributes.setObjectName("Attributes")
        # structure
        self.structure = Structure()
        self.structure.setWindowTitle("Structure")
        self.structure.setObjectName("Structure")
        # properties
        self.properties = Properties()
        self.properties.setWindowTitle("Properties")
        self.properties.setObjectName("Properties")
        # center
        self.center = Center()
        self.center.setWindowTitle("Main")
        self.center.setObjectName("Main")
        # output
        self.output = Output()
        # 控制台输出
        Func.log = self.output.print
        self.output.setWindowTitle("Output")
        self.output.setObjectName("Output")

        # 添加dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.structure)
        self.splitDockWidget(self.structure, self.center, Qt.Horizontal)
        self.splitDockWidget(self.center, self.attributes, Qt.Horizontal)
        self.splitDockWidget(self.structure, self.properties, Qt.Vertical)
        self.splitDockWidget(self.center, self.output, Qt.Vertical)

        self.attributes.visibilityChanged.connect(self.checkVisible)
        self.structure.visibilityChanged.connect(self.checkVisible)
        self.properties.visibilityChanged.connect(self.checkVisible)
        self.center.visibilityChanged.connect(self.checkVisible)
        self.output.visibilityChanged.connect(self.checkVisible)

        self.default_dock_widget_layout = self.saveState()

        # wait dialog
        self.wait_dialog = WaitDialog(self)

        self.linkSignals()

        # delete shortcut
        self.backspace_shortcut = QShortcut(QKeySequence("BackSpace"), self)
        self.backspace_shortcut.activated.connect(self.handle_delete_shortcut)
        self.delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        self.delete_shortcut.activated.connect(self.handle_delete_shortcut)

        # save shortcut
        self.save_shortcut = QShortcut(QKeySequence(QKeySequence.Save), self)
        self.save_shortcut.activated.connect(self.save)
        self.save_as_shortcut = QShortcut(QKeySequence(QKeySequence.SaveAs), self)
        self.save_as_shortcut.activated.connect(self.saveAs)

    def initialize(self):
        """
        开场的动画效果，及初始ui大小设置
        :return:
        """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def linkSignals(self):
        """
        初始化时需要连接的信号，包括几个大的区域和初始的timeline
        :return:
        """
        # 初始化
        self.linkWidgetSignals(f'{Info.TIMELINE}.0')
        # structure
        self.structure.widgetSignalsLink.connect(self.linkWidgetSignals)
        self.structure.widgetCreatStart.connect(self.start_wait_dialog)
        self.structure.widgetCreatEnd.connect(self.stop_wait_dialog)
        self.structure.widgetDelete.connect(self.center.widget_tabs.closeTab)
        self.structure.widgetModify.connect(self.attributes.refresh)
        self.structure.structure_tree.widgetOpen.connect(self.center.widget_tabs.openWidget)
        self.structure.structure_tree.nodeNameChange.connect(self.center.widget_tabs.changeTabName)
        # self.structure.structure_tree.nodeDelete.connect(self.center.widget_tabs.closeTab)
        # center
        self.center.widget_tabs.tabChange.connect(self.properties.showProperties)
        self.center.widget_tabs.tabChange.connect(self.attributes.showAttributes)
        # output

    def linkWidgetSignals(self, widget_id: str):
        """
        为widget连接信号
        :param widget_id: 需要连接信号的widget的widget_id
        :return:
        """
        # 1：widget_tabs
        self.center.widget_tabs.linkWidgetSignals(widget_id)
        # 2：main
        widget = Info.WID_WIDGET[widget_id]
        # 通用信号
        widget.propertiesChange.connect(self.properties.showProperties)
        # 特有信号
        widget_type = widget_id.split('.')[0]
        if widget_type == Info.TIMELINE:
            self.linkTimelineSignals(widget_id)
        elif widget_type == Info.CYCLE:
            self.linkCycleSignals(widget_id)

    def linkTimelineSignals(self, widget_id):
        """
        为timeline连接与其他dock widget的信号
        :param widget_id:
        :return:
        """
        try:
            timeline: Timeline = Info.WID_WIDGET[widget_id]
            try:
                timeline.widget_icon_area.widgetIconAdd.disconnect(self.structure.addNode)
                timeline.widget_icon_area.widgetIconAdd.connect(self.structure.addNode)
            except Exception:
                timeline.widget_icon_area.widgetIconAdd.connect(self.structure.addNode)
                timeline.widget_icon_area.widgetIconMove.connect(self.structure.moveNode)
                timeline.widget_icon_area.widgetIconMove.connect(self.attributes.showAttributes)
                timeline.widget_icon_area.widget_icon_table.propertiesShow.connect(self.properties.showProperties)
                timeline.widget_icon_area.widget_icon_table.attributesShow.connect(self.attributes.showAttributes)
                timeline.widget_icon_area.widget_icon_table.widgetIconNameChange.connect(self.structure.renameNode)
                timeline.widget_icon_area.widget_icon_table.widgetIconDelete.connect(self.structure.deleteNode)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [main/main.py]")
            Func.log(f"error {e} happens in link timeline signals. [main/main.py]")

    def linkCycleSignals(self, widget_id):
        """
        为cycle连接与其他dock widget的信号
        :param widget_id:
        :return:
        """
        try:
            cycle: Cycle = Info.WID_WIDGET[widget_id]
            try:
                cycle.timeline_table.timeline_add.disconnect(self.structure.addNode)
                cycle.timeline_table.timeline_add.connect(self.structure.addNode)
            except Exception:
                cycle.timeline_table.timeline_add.connect(self.structure.addNode)
                cycle.timeline_table.timeline_delete.connect(self.structure.deleteNode)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [main/main.py]")

    def newFile(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def save(self):
        """
        这个就是在保存之前获取一下文件名
        :return:
        """
        if Info.FILE_NAME == "":
            if self.getFileName():
                self.loadOut()
        else:
            self.loadOut()

        Info.CONFIG.setValue("directory",Info.FILE_DIRECTORY)
        # print(f"{Info.FILE_DIRECTORY}")

    def getFileName(self) -> bool:
        """
        获取文件名
        :return:
        """
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Save file", Info.FILE_DIRECTORY, "Psy Files (*.psy);")
        if save_file_name:
            # mac os下不会提供默认文件名称
            if not re.search(r"(\.psy|\.ini)$", save_file_name):
                save_file_name = save_file_name + ".psy"
            Info.FILE_NAME = save_file_name
            Info.FILE_DIRECTORY = os.path.dirname(save_file_name)
            return True
        return False

    def saveAs(self):
        self.getFileName()
        if Info.FILE_NAME:
            self.loadOut()
            Info.CONFIG.setValue("directory", Info.FILE_DIRECTORY)

    def loadIn(self):
        """
        恢复文件！
        :return:
        """
        options = QFileDialog.Options()
        open_file_name, _ = QFileDialog.getOpenFileName(self, "Choose file", Info.FILE_DIRECTORY, "Psy File (*.psy)",
                                                        options=options)
        if open_file_name:
            # 更新文件名
            Info.FILE_NAME = open_file_name
            Info.FILE_DIRECTORY = os.path.dirname(open_file_name)
            # 从文件中读取配置
            setting = QSettings(open_file_name, QSettings.IniFormat)
            # 计数恢复
            Info.WIDGET_TYPE_ID_COUNT = setting.value("WIDGET_TYPE_ID_COUNT")
            Info.WIDGET_TYPE_NAME_COUNT = setting.value("WIDGET_TYPE_NAME_COUNT")

            # 更新输入输出设备
            input_device_info = setting.value("INPUT_DEVICE_INFO")
            if input_device_info:
                self.input_devices.setProperties(input_device_info)
            Info.INPUT_DEVICE_INFO = input_device_info
            output_device_info = setting.value("OUTPUT_DEVICE_INFO")
            if output_device_info:
                self.output_devices.setProperties(output_device_info)
            Info.OUTPUT_DEVICE_INFO = output_device_info
            quest_info = setting.value("QUEST_INFO")
            if quest_info:
                self.quest_init.setProperties(quest_info)
            Info.QUEST_INFO = quest_info
            tracker_info = setting.value("TRACKER_INFO")
            if tracker_info:
                self.tracker_init.setProperties(tracker_info)
            Info.TRACKER_INFO = tracker_info
            # 恢复布局
            dock_layout = setting.value("DOCK_LAYOUT")
            if dock_layout:
                self.restoreState(dock_layout)
            # 恢复slider命名计数
            slider_count = setting.value("SLIDER_COUNT")
            if slider_count:
                Info.SLIDER_COUNT = slider_count

            platform = setting.value("PLATFORM")
            Info.PLATFORM = platform
            self.changePlatform(platform)

            image_load_mode = setting.value("IMAGE_LOAD_MODE")
            # print(f"load setting: {image_load_mode}")
            Info.IMAGE_LOAD_MODE = image_load_mode
            self.changeImageLoadMode(image_load_mode)
            # 恢复widgets
            # 复原初始的Timeline
            root_timeline: Timeline = Info.WID_WIDGET[f"{Info.TIMELINE}.0"]
            # 将其数据取出
            root_timeline_info = setting.value(f"{Info.TIMELINE}.0")
            # 恢复
            if root_timeline_info:
                root_timeline.restore(root_timeline_info)

            # 恢复name_wid
            name_wid: dict = setting.value("NAME_WID")
            if name_wid:
                Info.NAME_WID = name_wid.copy()

            # 恢复structure并恢复剩余widget
            structure_tree: list = setting.value("STRUCTURE_TREE")
            self.structure.loadStructure(structure_tree)
        Func.log(f"{Info.FILE_NAME} loaded successful!")

    def loadOut(self):
        # 导出输入设备信息
        input_device_info: dict = Info.INPUT_DEVICE_INFO.copy()
        output_device_info: dict = Info.OUTPUT_DEVICE_INFO.copy()
        quest_info: dict = Info.QUEST_INFO.copy()
        tracker_info: dict = Info.TRACKER_INFO.copy()
        # 当前布局信息
        current_dock_layout = self.saveState()
        name_wid = Info.NAME_WID.copy()
        # slider命名计数
        slider_count = Info.SLIDER_COUNT.copy()
        setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
        setting.setValue("INPUT_DEVICE_INFO", input_device_info)
        setting.setValue("OUTPUT_DEVICE_INFO", output_device_info)
        setting.setValue("QUEST_INFO", quest_info)
        setting.setValue("TRACKER_INFO", tracker_info)
        setting.setValue("DOCK_LAYOUT", current_dock_layout)
        setting.setValue("SLIDER_COUNT", slider_count)
        setting.setValue("NAME_WID", name_wid)
        setting.setValue("WIDGET_TYPE_NAME_COUNT", Info.WIDGET_TYPE_NAME_COUNT.copy())
        setting.setValue("WIDGET_TYPE_ID_COUNT", Info.WIDGET_TYPE_ID_COUNT.copy())

        structure_tree: list = self.structure.getStructure("李扬是个大瓜皮")
        self.loadOutTree(structure_tree)
        setting.setValue("STRUCTURE_TREE", structure_tree)

        # 当前输出平台
        setting.setValue("PLATFORM", Info.PLATFORM)
        setting.setValue("IMAGE_LOAD_MODE", Info.IMAGE_LOAD_MODE)
        # print(f"save setting: {Info.IMAGE_LOAD_MODE}")

        Func.log(f"{Info.FILE_NAME} saved successful!")

    def loadOutTree(self, tree):
        if isinstance(tree, list):
            for i in tree:
                self.loadOutTree(i)
        elif isinstance(tree, tuple):
            widget_id = tree[1]
            setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
            # 只保存源widget的数据，引用创建的wid没有必要保存
            if widget_id == Info.WID_WIDGET[widget_id].widget_id:
                setting.setValue(widget_id, Info.WID_WIDGET[widget_id].getInfo())

    def resetView(self):
        """
        恢复默认布局
        :return:
        """
        self.restoreState(self.default_dock_widget_layout)

    def updateLayout(self):
        """
        重新设置默认布局
        :return:
        """
        self.default_dock_widget_layout = self.saveState()

    def setDockView(self, checked):
        """
        单个dock的显示与隐藏
        :param checked:
        :return:
        """
        dock = self.sender().data()
        if dock == "attribute":
            self.attributes.setVisible(self.attributes.isHidden())
        elif dock == "structure":
            self.structure.setVisible(self.structure.isHidden())
        elif dock == "main":
            self.center.setVisible(self.center.isHidden())
        elif dock == "property":
            self.properties.setVisible(self.properties.isHidden())
        elif dock == "output":
            self.output.setVisible(self.output.isHidden())
        else:
            print(f"wtf{dock}")

    def checkVisible(self, is_visible):
        """
        通过判断dock的显示与隐藏来改变菜单栏view的图标
        :param is_visible:
        :return:
        """
        dock = self.sender().windowTitle()
        if is_visible:
            icon = QIcon(Func.getImage("dock_visible.png"))
        else:
            icon = QIcon("")
        if dock == "Attributes":
            self.attribute_action.setIcon(icon)
        elif dock == "Structure":
            self.structure_action.setIcon(icon)
        elif dock == "Main":
            self.main_action.setIcon(icon)
        elif dock == "Properties":
            self.property_action.setIcon(icon)
        elif dock == "Output":
            self.output_action.setIcon(icon)
        else:
            print(f"wtf{dock}")

    def showDevices(self, device_type):
        """
        显示设备选择框
        :param device_type:
        :return:
        """
        if device_type:
            self.output_devices.show()
        else:
            self.input_devices.show()

    @staticmethod
    def changeDevices(device_type, devices):
        # output device
        if device_type:
            DurationPage.OUTPUT_DEVICES = devices
        else:
            DurationPage.INPUT_DEVICES = devices

    def contextMenuEvent(self, QContextMenuEvent):
        super().contextMenuEvent(QContextMenuEvent)

    def changePlatform(self, c):
        if isinstance(c, bool):
            self.linux_action.setIconVisibleInMenu(self.sender() is self.linux_action)
            self.windows_action.setIconVisibleInMenu(self.sender() is self.windows_action)
            self.mac_action.setIconVisibleInMenu(self.sender() is self.mac_action)
            Info.PLATFORM = self.sender().text().lstrip("&").lower()
        elif isinstance(c, str):
            platform = c if c else "linux"
            self.linux_action.setIconVisibleInMenu(platform == "linux")
            self.windows_action.setIconVisibleInMenu(platform == "windows")
            self.mac_action.setIconVisibleInMenu(platform == "mac")


    def changeImageLoadMode(self, c):
        if isinstance(c, bool):
            self.before_event_action.setIconVisibleInMenu(self.sender() is self.before_event_action)
            self.before_trial_action.setIconVisibleInMenu(self.sender() is self.before_trial_action)
            self.before_exp_action.setIconVisibleInMenu(self.sender() is self.before_exp_action)
            Info.IMAGE_LOAD_MODE = self.sender().text().lstrip("&").lower()
        elif isinstance(c, str):
            # print(c)
            imageLoadMode = c if c else "before_event"
            self.before_event_action.setIconVisibleInMenu(imageLoadMode == "before_event")
            self.before_trial_action.setIconVisibleInMenu(imageLoadMode == "before_trial")
            self.before_exp_action.setIconVisibleInMenu(imageLoadMode == "before_exp")

    def compile(self):
        try:
            # self.structure.getStructure().print_tree()
            compilePTB(self)
        except Exception as compileError:
            Func.log(str(compileError), True, False)
            traceback.print_exc()

    def registry(self):
        if Info.IS_REGISTER == "Yes":
            QMessageBox.about(self, "Registry", "Already registry")
        else:
            try:
                writeToRegistry(Func.getPsyIconPath())
                Info.CONFIG.setValue("register", "Yes")
                QMessageBox.about(self, "Registry", "Registry Successful!")
                Info.IS_REGISTER = "Yes"
            except Exception:
                QMessageBox.about(self, "Registry", "Registry Failed!")
    def aboutWidget_ok(self):
        self.aboutWidget.close()

    def about(self):

        self.aboutWidget = QWidget()
        self.aboutWidget.setWindowTitle("About developers of PTB Builder 0.1")
        self.aboutWidget.setWindowModality(2)
        self.aboutWidget.setWindowIcon(QIcon(Func.getImage("icon.png")))
        self.aboutWidget.setWindowFlags(Qt.Window|Qt.WindowCloseButtonHint)

        self.aboutWidget.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)
        self.aboutWidget.setPalette(p)

        img00 = QLabel(self)
        lab01 = QLabel(self)

        img10 = QLabel(self)
        lab11 = QLabel(self)

        closeButton = QPushButton('&Ok')


        closeButton.clicked.connect(self.aboutWidget_ok)
        closeButton.setAutoDefault(True)

        img00.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        lab01.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        img10.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        lab11.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)

        lab01.setText("Personal info")
        lab11.setText("Personal info")
        img00.setPixmap(QPixmap(Func.getImage("authorInfo01.png")))
        img10.setPixmap(QPixmap(Func.getImage("authorInfo01.png")))

        layout1 = QGridLayout()
        layout1.addWidget(img00,0,0)
        layout1.addWidget(lab01,0,1)
        layout1.addWidget(img10,1,0)
        layout1.addWidget(lab11,1,1)

        layout2 = QVBoxLayout()
        layout2.addWidget(closeButton)
        layout2.setAlignment(Qt.AlignVCenter|Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addStretch(10)
        layout.addLayout(layout2)

        self.aboutWidget.setLayout(layout)
        self.aboutWidget.setMinimumWidth(400)
        self.aboutWidget.show()

        # self.gridGroupBox.setLayout(aboutUsBox)
        # self.gridGroupBox.setWindowIcon(QIcon(Func.getImage("icon.png")))
        # self.gridGroupBox.setWindowTitle("About the authors")
        # self.gridGroupBox.setWindowModality(2)
        #
        # self.gridGroupBox.show()

        # QMessageBox.about(self, "About PTB Builder 0.1",
        #                   "A free GUI to generate experimental codes for PTB\nDepartment of Psychology,Soochow University ")

    def checkUpdate(self):
        self.bar = LoadingTip()
        self.bar.setWindowModality(Qt.ApplicationModal)
        self.bar.show()
        self.t = QTimer()
        self.t.timeout.connect(self.re)
        self.t.start(100)

    def re(self):
        self.bar.changeValue()
        self.bar.update()
        if self.bar.bar.value == 100:
            self.t.stop()
            self.bar.close()

    def closeEvent(self, QCloseEvent):
        """
        关闭时的动画效果
        :param QCloseEvent:
        :return:
        """
        try:
            self.animation.setDuration(1000)
            self.animation.setStartValue(0)
            self.animation.setEndValue(1)
            self.animation.start()
            self.close()
        except:
            self.close()

    def start_wait_dialog(self) -> None:
        """
        启动等待窗口
        :return:
        """
        self.wait_timer = QTimer(self)
        self.wait_timer.timeout.connect(self.refresh_wait_dialog)
        self.wait_dialog.start()
        self.wait_timer.start(0)

    def refresh_wait_dialog(self) -> None:
        """
        刷新等待窗口
        :return:
        """
        self.wait_dialog.change_image()
        self.wait_timer.start(0)

    def stop_wait_dialog(self) -> None:
        """
        关闭等待窗口
        :return:
        """
        self.wait_timer.stop()
        self.wait_dialog.stop()

    def handle_delete_shortcut(self):
        """
        对于delete快捷键进行,进行判断然后调用对应功能
        :return:
        """
        # 如果是center，则是timeline的删除快捷键或者是cycle的清空，否则可能是structure的删除快捷键
        focus = self.center.isFocused()
        if focus == Info.CycleFocused:
            self.center.widget_tabs.currentWidget().timeline_table.clear_data()
        elif focus == Info.TimelineFocused:
            self.center.widget_tabs.currentWidget().widget_icon_area.widget_icon_table.deleteShortcut()
        else:
            focus = self.structure.isFocused()
            if focus == Info.StructureFocused:
                self.structure.structure_tree.deleteNode()
