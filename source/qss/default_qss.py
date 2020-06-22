import platform
import re

from app.info import Info

source_image_path = "/".join(re.split(r'\\', Info.ImagePath))
# another_one = "/".join(re.split(r"\\", Info.IMAGE_SOURCE_PATH))


def imageURL(image_path: str, flag: int = 0):
    """
    return image url
    """

    if not flag:
        return source_image_path + image_path
    return image_path


# base qss
dock_widget = f"""
QDockWidget {{
    border: 1px solid rgb(206,206,206);
    titlebar-close-icon: url({imageURL("/dock_widget/hide.png")});
}}

QDockWidget::title {{
background: rgb(237, 237, 237);
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
background: rgb(221, 221, 221);
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
    image: url({imageURL("/tab_bar/close.png")});
    subcontrol-position: right;
    subcontrol-origin: margin;
    position: absolute;
    icon-size: 2px;;
}}

QTabBar::close-button:hover {{
    image: url({imageURL("/tab_bar/close_pressed.png")});
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
    border-image: url({imageURL("/structure/vertical_line.png")}) 0;
}}

QTreeView::branch:has-siblings:adjoins-Item {{
    border-image: url({imageURL("/structure/branch_more.png")}) 0;
}}

QTreeView::branch:!has-children:!has-siblings:adjoins-Item {{
    border-image: url({imageURL("/structure/branch_end.png")}) 0;
}}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {{
    border-image: url({imageURL("/structure/branch_closed.png")}) 0;
}}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {{
    border-image: url({imageURL("/structure/branch_open.png")}) 0;
}}
"""

# widgets' qss
if Info.OS_TYPE==2:
    tl_item_min_height = 120
    tl_min_height = 150
    tl_item_max_height = 120
    tl_max_height = 150
    tl_item_min_width = 120

    tl_item_list_font_size = 24
else:
    tl_item_min_height = 64
    tl_min_height = 75
    tl_item_max_height = 64
    tl_max_height = 75
    tl_item_min_width = 100

    tl_item_list_font_size = 12

timeline = f"""
/* IconBar */
QTabWidget::pane#IconBar {{
    min-height:{tl_min_height}px;
    max-height:{tl_max_height}px;
}}

QListView#IconList{{
    border: 1px solid rgb(201,201,201);
    border-top: none;
    show-decoration-selected: 1;
    font-size: {tl_item_list_font_size}px;
    min-height:{tl_min_height}px;
    max-height:{tl_max_height}px;
}}

QListView#IconList::Item{{
    border-top: 10px solid transparent;
    border-bottom: 1px solid transparent;
    min-height: {tl_item_min_height}px;
    max-height: {tl_item_max_height}px;
    min-width: {tl_item_min_width}px;
}}

QListView#IconList::Item:hover{{
    padding-top: 9px;
    background: transparent;
    border-radius:2px;
    border: 1px solid rgb(110, 110, 110);
}}

QListView#IconList::Item:selected{{
    padding-top: 9px;
    background: rgb(186,215,251);
    border-radius:2px;
    border: 1px solid rgb(110, 110, 110);
}}

/* Timeline Area */
QFrame#TimelineArea {{
    background:white;
    border: 1px solid rgb(201,201,201);
}}

QLabel#TimelineItem{{
    background-color: transparent;
}}

QLabel#TimelineItem:hover{{
    border: 1px solid rgb(110,110,110);
    border-radius: 2px;
    padding: 2px;
}}

QTableWidget#TimelineTable {{
    selection-background-color:rgb(186,215,251);
}}
"""
if Info.OS_TYPE==2:
    loop_min_height = 70
    loop_max_height = 70
else:
    loop_min_height = 35
    loop_max_height = 35

cycle = f"""
QToolBar#CycleToolBar {{
    border: 1px solid rgb(201,201,201);
    min-height: {loop_min_height}px;
    max-height: {loop_max_height}px;
    spacing: 2px;
}}
"""
QComboBoxStyle = ""
QLineEditStyle = ""

if Info.OS_TYPE ==0:
    menuCheck = f"""
QMenu::indicator:exclusive:checked {{
    image: url({imageURL("/menu/checked.png")});
}}

QMenu::indicator:exclusive:unchecked{{
image: none;
}}
"""
else:
    menuCheck = ""
    QComboBoxStyle = f"""
QComboBox {{  
font-family: "Helvetica";
font-size: 12pt;
}}
"""

    QLineEditStyle = f"""
QLineEdit {{  
font-family: "Helvetica";
font-size: 12pt;
}}
"""
# other
other = f"""
ColComboBox::drop-down {{image: url({imageURL("/common/color_down_arrow.png")});}}
"""

default_qss = dock_widget + tab_bar + center + structure + timeline + cycle + other + menuCheck +QComboBoxStyle +QLineEditStyle
