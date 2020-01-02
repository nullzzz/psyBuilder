timeline_label = """
QLabel#TimelineLabel{
    background-color: transparent;
}
QLabel#TimelineLabel:hover{
    border: 2px solid lightBlue;
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
}"""

test = """
"""

mac_qss = timeline_label + icon_bar + timeline_area + test + timeline_line_edit
