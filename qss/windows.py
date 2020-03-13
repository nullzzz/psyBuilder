timeline_item = """
QLabel#TimelineItem{
    background-color: transparent;
}
QLabel#TimelineItem:hover{
    border: 2px solid rgb(186, 215, 251);
    border-radius: 4px;
    padding: 4px;
}
"""

icon_bar = """
QTabWidget#IconBar{
    max-height:90px;
}
"""

timeline_table = """
QTableView#TimelineTable{
    selection-background-color: rgb(204,233,255);
}
QTableView#TimelineTable::Item{
    background-color:transparent;
    border: 0px solid white;
}
QTableView#TimelineTable::Item:selected{
    color: black;
    background-color: rgb(204,233,255);
    border: 2px solid rgb(186, 215, 251);
}
"""

timeline_area = """
QFrame#TimelineArea{
    background:white;
}
"""

tab_bar = """
QTabWidget::pane {
    background-color: rgb(236,236,236);
}

QTabWidget::tab-bar {
    left: 0px;
}

QTabBar::tab {
    background: rgb(246,246,246);
    border: 1px solid rgb(201,201,201);
    min-height: 30px;
    min-width: 100px;
    text-align: center;
}

QTabBar::tab#TabWidget {
    border-left: 10px solid rgb(201,201,201);
    border-right: 5px solid rgb(201,201,201);
}

QTabBar::tab:selected{
    background: rgb(246,246,246);
    border-bottom:0px;
}

QTabBar::tab:!selected {
    background: rgb(221,221,221);
}

QTabBar::tab:hover {
    background: rgb(198,198,198);
}

QTabBar::close-button {
    image: url(images/tab_bar/close.ico);
}

QTabBar::close-button:hover {
    background: rgb(211,211,211);
}

QTabBar::close-button:pressed {
    background: rgb(201,201,201);
}
"""

icon_list = """
QListView#IconList{
    border: 1px solid rgb(204, 204, 204);
    border-radius: 4px;
    show-decoration-selected: 1;
    font-size: 12px;
    min-height:66px;
}

QListView#IconList::Item{
    min-height: 60px;
    min-width: 100px;
}

QListView#IconList::Item:hover{
    background: transparent;
    border-radius:4px;
    border: 2px solid rgb(186, 215, 251);
}

QListView#IconList::Item:selected{
    background: rgb(204,233,255);
    border-radius:4px;
    border: 2px solid rgb(186, 215, 251);
}
"""

dock_widget = """
QDockWidget::title {
    text-align: left;
    padding: 6px;
}
"""

structure_tree = """
QTreeView::item:selected {
    border: 1px solid rgb(186, 215, 251);
    background: rgb(186, 215, 251);
}

QTreeView::item:hover {
    border:1px solid rgb(186, 215, 251);
}

QTreeView::branch:selected {
    background: rgb(186, 215, 251);
}

QTreeView::branch:has-siblings:!adjoins-Item {
    border-image: url(images/structure/vertical_line.png) 0;
}

QTreeView::branch:has-siblings:adjoins-Item {
    border-image: url(images/structure/branch_more.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-Item {
    border-image: url(images/structure/branch_end.png) 0;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    border-image: none;
    image: url(images/structure/branch_closed.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings {
    border-image: none;
    image: url(images/structure/branch_open.png);
}
"""

windows_qss = timeline_item + icon_bar + icon_list + timeline_area + timeline_table + tab_bar + dock_widget + structure_tree
