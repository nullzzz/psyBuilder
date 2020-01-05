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
    max-height:100px;
}
"""

timeline_table = """
QTableView#TimelineTable{
    selection-background-color: transparent;
}
QTableView#TimelineTable::Item{
    background-color:transparent;
    border: 0px solid white;
}
QTableView#TimelineTable::Item:selected{
    color: black;
    background-color: transparent;
    border: 0px solid blue;
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

mac_qss = timeline_item + icon_bar + timeline_area + timeline_table + tab_bar
