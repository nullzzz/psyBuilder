timeline_item = """
QLabel#TimelineItem{
    background-color: transparent;
}
QLabel#TimelineItem:hover{
    border: 2px solid rgb(227,227,227);
    border-radius: 4px;
    padding: 2px;
}
"""

icon_bar = """
QTabWidget#IconBar{
    max-height:100px;
}
"""

timeline_name_item = """
QLineEdit#TimelineNameItem{
    border: 0px;
}
"""

timeline_table = """
QTableView{
    selection-background-color: rgb(204,232,255);
}
QTableView::Item:selected {
        background-color:white;
        border: 0px solid lightblue;
}
"""

timeline_area = """
QFrame#TimelineArea{
background:white;
}
"""

test = """
"""

mac_qss = timeline_item + icon_bar + timeline_area + timeline_name_item + timeline_table
