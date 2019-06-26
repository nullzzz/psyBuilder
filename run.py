import sys

from quamash import QApplication

from app.main.main import PsyApplication

tabBar = """
QTabWidget::pane { /* The tab widget frame */
    background-color: rgb(236,236,236);
}

QTabWidget::tab-bar {
    left: 0px;
}

QTabBar::tab {
    background: rgb(236,236,236);
    border: 1px solid rgb(201,201,201);
    border-left: 0.5px solid rgb(201,201,201);
    margin-top: 6px;
    min-height: 26px;
    min-width: 100px;
    text-align: center;
}

QTabBar::tab:selected{
    background: rgb(227,227,227);
    border-bottom:0px;
}

QTabBar::tab:!selected {
    background: rgb(199,199,199);
}

QTabBar::tab:hover {
    background: rgb(211,211,211);
}

QTabBar::close-button {
    image: url(image/tab_bar/close.ico);
    margin-top:3px;
}

QTabBar::close-button:hover {
    background: rgb(211,211,211);
}

QTabBar::close-button:pressed {
    background: rgb(201,201,201);
}
"""

dockWidget = """
    QDockWidget {
        background: #F5F5F5;
        border: 1px solid rgb(189,189,189);
        titlebar-close-icon: url(image/dock_widget/close.ico);
        titlebar-normal-icon: url(image/dock_widget/float.ico);
    }

    QDockWidget::close-button{
        border: 1px solid transparent;
        border-radius: 2px;
        background: transparent;
    }

    QDockWidget::close-button:hover {
        background: rgb(211,211,211);
    }
    
    QDockWidget::close-button:pressed{
        background: rgb(201,201,201);
    }
    
    QDockWidget::normal-button:hover {
        background: rgb(211,211,211);
    }
    
    QDockWidget::normal-button:pressed {
        background: rgb(201,201,201);
    }
    
    QDockWidget::title {
        text-align: center;
        background: lightgray;
    }
"""

mainWindow = """
    
"""

scrollBar = """
    QScrollBar:horizontal
    {
        height: 12px;
        margin: 3px 8px 3px 8px;
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
        width: 6px;
        height: 6px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:horizontal
    {
        margin: 0px 3px 0px 3px;
        border-image: url(image/left_arrow_disabled.png);
        height: 6px;
        width: 6px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
    {
        border-image: url(image/right_arrow.png);
        height: 6px;
        width: 6px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }


    QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
    {
        border-image: url(image/left_arrow.png);
        height: 6px;
        width: 6px;
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
        width: 12px;
        margin: 8px 3px 8px 3px;
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
    }
    """

toolBar = """
    QToolBar {
    background-color:rgb(246,246,246);
    max-height: 30px;
    spacing: 3px;
}
"""

lineEdit = """
    QLineEdit {
        border: 0.5px solid gray;
        border-radius: 0.5px;
    }

    QLineEdit:focus {
        background-color: white;
    }
    
    QLineEdit:!enabled {
        background-color: rgb(234,234,234);
        border: gray;
    }
    """

pushButton = """
    QPushButton {
        border: 0.5px solid #8f8f91;
        border-radius: 4px;
        background-color: rgb(254,254,254);
        min-width: 78px;
        min-height: 25px;
    }

    QPushButton:pressed {
        border-color: rgb(153,196,244);
    }

    QPushButton:!enabled {
        background-color: rgb(234,234,234);
        border: gray;
    }
"""

tableView = """
QTableView {
    selection-background-color: rgba(204,232,255);
}
QTableView::Item:selected {
        background-color:white;
        border-radius:1px;
        border: 2px solid lightblue;
}
"""

listView = """
    QListView {
        show-decoration-selected: 1;
    }

    QListView::Item {
        min-width: 80px;
    }

    QListView::Item:hover {
        background: transparent;
        border-radius:4px;
        border: 2px solid lightblue;
    }
    
    QListView::Item:selected {
        background: rgb(204,233,255);
        border-radius:4px;
        border: 2px solid lightblue;
    }
"""

headerView = """
    QHeaderView::section
    {
        background:	#F5F5F5;
    }
"""

tree = """
    QTreeView::branch:has-siblings:!adjoins-Item {
        border-image: url(image/vline.png) 0;
    }

    QTreeView::branch:has-siblings:adjoins-Item {
        border-image: url(image/branch-more.png) 0;
    }

    QTreeView::branch:!has-children:!has-siblings:adjoins-Item {
        border-image: url(image/branch-end.png) 0;
    }

    QTreeView::branch:has-children:!has-siblings:closed,
    QTreeView::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(image/branch-closed.png);
    }

    QTreeView::branch:open:has-children:!has-siblings,
    QTreeView::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(image/branch-open.png);
    }
    ColorListEditor::drop-down {image: url(image/color_down_arrow.png);}
    """

menu = """
QMenu {
    background-color: white;
    border: 2px solid gray;
    border-radius: 4px;
    margin: 2px;
    min-width: 78px;
}

QMenu::Item {
    padding: 2px 25px 2px 20px;
}

QMenu::Item:selected {
    border-color: transparent;
    background: rgb(153,196,244);
}

QMenu::icon:checked {
    background: rgb(210,210,210);
    border: 0.5px inset rgb(210,210,210);
    position: absolute;
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

styleSheet = tabBar + dockWidget + mainWindow + scrollBar + tableView + headerView + toolBar + pushButton + tree + menu + listView + lineEdit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy_application = PsyApplication()
    psy_application.initialize()
    psy_application.showMaximized()

    app.setStyleSheet(styleSheet)
    sys.exit(app.exec_())
