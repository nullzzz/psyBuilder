timeline_label = """
QLabel#TimelineLabel{
    background-color: transparent;
}
QLabel#TimelineLabel:hover{
    border: 2px solid rgb(227,227,227);
    border-radius: 4px;
    padding: 2px;
}
"""

timeline_area = """
QGraphicsView#TimelineArea{
}
"""

icon_bar = """
QTabWidget#IconBar{
    max-height:100px;
}
"""

timeline_line_edit = """
QLineEdit#TimelineLineEdit{
    border: 0px;
}
QLineEdit#TimelineLineEdit:focus{
        border: 0.5px solid gray;
        border-radius: 1px;
}
"""

test = """
"""

mac_qss = timeline_label + icon_bar + timeline_area + test + timeline_line_edit
