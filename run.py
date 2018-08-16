import sys

from PyQt5.QtWidgets import QApplication

from main.main import MainWindow

tabBar = """
        QTabWidget::pane { /* The tab widget frame */
        border-top: 2px solid #C2C7CB;
    }
    
    QTabWidget::tab-bar {
        left: 5px; /* move to the right by 5px */
    }
    
    /* Style the tab using the tab sub-control. Note that
        it reads QTabBar _not_ QTabWidget */
    QTabBar::tab {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border: 2px solid #C4C4C3;
        border-bottom: none;
        border-bottom-color: #C2C7CB; /* same as the pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 30ex;
        padding: 2px;
    }
    
    QTabBar::tab:selected, QTabBar::tab:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                    stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
    }
    
    QTabBar::tab:selected {
        border-color: #9B9B9B;
        border-bottom-color: #C2C7CB; /* same as pane color */
    }
    
    QTabBar::tab:!selected {
        margin-top: 2px; /* make non-selected tabs look smaller */
    }

    QTabBar::close-button  {
        image: url(image/close.png);
        background: transparent;
    }

    QTabBar::close-button:hover
    {
        image: url(image/close-hover.png);
        background: transparent;
    }

    QTabBar::close-button:pressed {
        image: url(image/close-pressed.png);
        background: transparent;
    }"""

dockWidget = """
    QDockWidget {
        background-color: rgba(100,149,237);
        border: 1px solid #403F3F;
        titlebar-close-icon: url(image/close.png);
        titlebar-normal-icon: url(image/undock.png);
    }

    QDockWidget::close-button, QDockWidget::float-button {
        border: 1px solid transparent;
        border-radius: 2px;
        background: transparent;
    }

    QDockWidget::close-button:hover {
        image: url(image/close-hover.png);
        background: transparent;
    }

    QDockWidget::float-button:hover {
        background: rgba(255, 255, 255, 10);
    }

    QDockWidget::close-button:pressed {
        image: url(image/close-pressed.png);
        background: transparent;
    }

    QDockWidget::float-button:pressed {
        padding: 1px -1px -1px 1px;
        background: rgba(255, 255, 255, 10);
    }"""

mainWindow = """
    QMainWindow::separator
    {
        background-color: white;
        color: white;
        padding-left: 4px;
        spacing: 2px;
        border: 1px  #76797C;
    }

    QMainWindow::separator:hover
    {
        background-color: #d3d3cf;
        color: white;
        padding-left: 4px;
        border: 1px solid #76797C;
        spacing: 2px;
    }

    QMenu::separator
    {
        height: 1px;
        background-color: #76797C;
        color: white;
        padding-left: 4px;
        margin-left: 10px;
        margin-right: 5px;
    }"""

scrollBar = """
    QScrollBar:horizontal
    {
        height: 20px;
        margin: 3px 15px 3px 15px;
        border: 1px transparent #2A2929;
        border-radius: 4px;
        background-color: lightGray;
    }

    QScrollBar::handle:horizontal
    {
        background-color: Gray;
        min-width: 5px;
        border-radius: 4px;
    }

    QScrollBar::add-line:horizontal
    {
        margin: 0px 3px 0px 3px;
        border-image: url(image/right_arrow_disabled.png);
        width: 10px;
        height: 10px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:horizontal
    {
        margin: 0px 3px 0px 3px;
        border-image: url(image/left_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
    {
        border-image: url(image/right_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }


    QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
    {
        border-image: url(image/left_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
    {
        background: none;
    }


    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
    {
        background: none;
    }

    QScrollBar:vertical
    {
        background-color: lightGray;
        width: 18px;
        margin: 15px 3px 15px 3px;
        border: 1px transparent #2A2929;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical
    {
        background-color: gray;
        min-height: 5px;
        border-radius: 4px;
    }

    QScrollBar::sub-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(image/up_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(image/down_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
    {

        border-image: url(image/up_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }


    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
    {
        border-image: url(image/down_arrow.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }"""

toolBar = """
    QToolBar {
        border: 1px transparent #393838;
        background: 1px solid gray;
        font-weight: bold;
        spacing: 15px;
        qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3)
    }

    QToolBar::handle:horizontal {
        image: url(image/Hmovetoolbar.png);
    }

    QToolBar::handle:vertical {
        image: url(image/Vmovetoolbar.png);
    }

    QToolBar::separator:horizontal {
        image: url(image/Hsepartoolbar.png);
    }

    QToolBar::separator:vertical {
        image: url(image/Vsepartoolbars.png);
    }"""

lineEdit = """
    QLineEdit {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 0 8px;
        background: white;
        selection-background-color: darkgray;
        selection-border-color: darkGray;
        min-height: 30px
    }

    QLineEdit:focus {
    border-width:2px;
    border-color:rgb(51, 133, 255);
    }

    QLineEdit:!enabled {
        background-color: LightGray;
    }
    """

pushButton = """
    QPushButton {
        border: 2px solid #8f8f91;
        border-radius: 6px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde);
        min-width: 80px;
        min-height: 28px;
    }

    QPushButton:pressed {
        border-color: blue;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QPushButton:flat {
        border: none;
    }

    QPushButton:default {  
        border-color: gray;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);
    }

    QPushButton:!enabled {
        background-color: LightGray;
    }

    QPushButton:enabled {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #f6f7fa);
    }
"""

tableView = """
    QTableView
    {
        alternate-background-color: rgb(48,51,55);
        selection-background-color: rgba(204,232,255);
    }
"""

listView = """   
    QListView::item:hover, QListView::item:selected {
        border: 0.5px;
        background: lightBlue);
    }
"""

headerView = """
    QHeaderView::section
    {
        background:	#F5F5F5;
    }
"""

tree = """
    QTreeWidget::branch:has-siblings:!adjoins-item{
        border-image: url(./image/vline.png) 0;
        }

    QTreeWidget::branch:has-siblings:adjoins-item{
        border-image: url(./image/branch-more.png) 0;
        }

    QTreeWidget::branch:!has-children:!has-siblings:adjoins-item{
        border-image: url(./image/branch-end.png) 0;
        }

    QTreeWidget::branch:has-children:!has-siblings:closed, 
    QTreeWidget::branch:has-children:has-siblings:closed{
        border-image: none;
        image: url(./image/branch-closed.png);
        }

    QTreeWidget::branch:has-children:!has-siblings:open,
    QTreeWidget::branch:has-children:has-siblings:open{
        border-image: none;
        image: url(./image/branch-open.png);
        }
    """

menu = """
    QMenu {
    background-color: white;
    border: 1px solid gray;
    margin: 2px; /* some spacing around the menu */
}

QMenu::item {
    padding: 2px 25px 2px 20px;
    border: 0.5px solid gray; /* reserve space for selection border */
}

QMenu::item:selected {
    border-color: black;
    background: rgba(135,206,250);
}

QMenu::icon:checked { /* appearance of a 'checked' icon */
    background: gray;
    border: 1px inset gray;
    position: absolute;
    top: 1px;
    right: 1px;
    bottom: 1px;
    left: 1px;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 13px;
    height: 13px;
}
"""

styleSheet = dockWidget + mainWindow + scrollBar + tableView + headerView + toolBar + lineEdit + pushButton + tree + menu + listView

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = MainWindow()
    demo.resize(1600, 900)

    demo.show()
    demo.move((app.desktop().width() - demo.width()) / 2,
              (app.desktop().height() - demo.height()) / 2)
    demo.properties.my_widget.setMaximumWidth(600)

    demo.center.icon_tabs.setStyleSheet(tabBar)
    app.setStyleSheet(styleSheet)
    sys.exit(app.exec_())
