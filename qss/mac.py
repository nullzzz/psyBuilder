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
    border: 0px solid white;
}
QLineEdit#TimelineNameItem:selected{
    border: 10px solid blue;
}
"""

timeline_table = """
QTableView#TimelineTable{
    selection-background-color: white;
}
QTableView#TimelineTable::Item{
        background-color:white;
        border: 0px solid white;
}
QTableView#TimelineTable::Item:focus{
        background-color:white;
        border: 10px solid red;
}
QTableView#TimelineTable::Item:selected{
        background-color:white;
        border: 0px solid blue;
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
