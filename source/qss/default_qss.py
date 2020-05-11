import os
import re

from app.info import Info

# base qss
dock_widget = f"""
QDockWidget {{
    border: 1px solid rgb(206,206,206);
    titlebar-close-icon: url({os.path.join(Info.ImagePath, *re.split(r"/", "/dock_widget/hide.png"))});
}}

QDockWidget::title {{
    background: rgb(237,237,237);
    text-align: center;
    padding-top: 6px;
    padding-bottom: 6px;
}}

QDockWidget::close-button {{
    subcontrol-position: right;
    border: 0.5px solid transparent;
    background: transparent;
    margin-right: 2px;
    icon-size: 16px;
}}

QDockWidget::close-button:hover {{
    background: rgb(221,221,221);
}}
"""

tab_bar = f"""
QTabWidget::pane {{
    background-color: rgb(240,240,240);
    border: 0px solid red;
}}

QTabWidget::tab-bar {{
    left: 0px;
}}

QTabBar::tab {{
    background: rgb(246,246,246);
    border: 1px solid rgb(201,201,201);
    min-height: 27px;
    max-height: 27px;
    min-width: 100px;
    text-align: center;
}}

QTabBar::tab#TabWidget {{
    border-left: 10px solid transparent;
}}

QTabBar::tab:selected {{
    background: white;
}}

QTabBar::tab:!selected {{
    background: rgb(236,236,236);
}}

QTabBar::tab:hover {{
    background: rgb(225,225,225);
}}

QTabBar::close-button {{
    image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/tab_bar/close.png"))});
    subcontrol-position: right;
    subcontrol-origin: margin;
    position: absolute;
    icon-size: 2px;;
}}

QTabBar::close-button:hover {{
    image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/tab_bar/close_pressed.png"))});
}}

"""

# main windows' qss
center = f"""
QMainWindow::separator {{
    background: rgb(110,110,110);
    width: 1px;
    height: 1px;
}}
"""

structure = f"""
QTreeView::item {{
    border: 1px solid transparent;
}}

QTreeView::item:selected {{
    border: 1px solid transparent;
    background: rgb(186, 215, 251);
}}

QTreeView::item:hover {{
    border: 1px solid rgb(110,110,110);
}}

QTreeView::branch:selected {{
    background: rgb(186, 215, 251);
}}

QTreeView::branch:has-siblings:!adjoins-Item {{
    border-image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/structure/vertical_line.png"))}) 0;
}}

QTreeView::branch:has-siblings:adjoins-Item {{
    border-image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/structure/branch_more.png"))}) 0;
}}

QTreeView::branch:!has-children:!has-siblings:adjoins-Item {{
    border-image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/structure/branch_end.png"))}) 0;
}}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    border-image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/structure/branch_closed.png"))}) 0;
}}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    border-image: url({os.path.join(Info.ImagePath, *re.split(r"/", "/structure/branch_open.png"))}) 0;
}}
"""

# widgets' qss
timeline = """
/* IconBar */
QTabWidget::pane#IconBar {
    min-height:75px;
    max-height:75px;
}

QListView#IconList{
    border: 1px solid rgb(201,201,201);
    border-top: none;
    show-decoration-selected: 1;
    font-size: 12px;
    min-height:75px;
    max-height:75px;
}

QListView#IconList::Item{
    border-top: 10px solid transparent;
    border-bottom: 1px solid transparent;
    min-height: 64px;
    max-height: 64px;
    min-width: 100px;
}

QListView#IconList::Item:hover{
    padding-top: 9px;
    background: transparent;
    border-radius:2px;
    border: 1px solid rgb(110, 110, 110);
}

QListView#IconList::Item:selected{
    padding-top: 9px;
    background: rgb(186,215,251);
    border-radius:2px;
    border: 1px solid rgb(110, 110, 110);
}

/* Timeline Area */
QFrame#TimelineArea {
    background:white;
    border: 1px solid rgb(201,201,201);
}

QLabel#TimelineItem{
    background-color: transparent;
}

QLabel#TimelineItem:hover{
    border: 1px solid rgb(110,110,110);
    border-radius: 2px;
    padding: 2px;
}

QTableWidget#TimelineTable {
    selection-background-color:rgb(186,215,251);
}
"""

cycle = """
QToolBar#CycleToolBar {
    border: 1px solid rgb(201,201,201);
    min-height: 35px;
    max-height: 35px;
    spacing: 2px;
}
"""

# other
other = f"""
ColComboBox::drop-down {{image: url({os.path.join(Info.IMAGE_SOURCE_PATH, *re.split(r"/", "/color_down_arrow.png"))});}}
"""

default_qss = dock_widget + tab_bar + center + structure + timeline + cycle + other
