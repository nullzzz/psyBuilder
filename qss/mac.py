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
    max-height:88px;
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
    border-left: 0.5px solid rgb(201,201,201);
    min-height: 26px;
    min-width: 100px;
    text-align: center;
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
    show-decoration-selected: 1;
    font-size: 12px;
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

mac_qss = timeline_item + icon_bar + icon_list + timeline_area + timeline_table + tab_bar
