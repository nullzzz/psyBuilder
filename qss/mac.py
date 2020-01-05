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

mac_qss = timeline_item + icon_bar + timeline_area + timeline_table
