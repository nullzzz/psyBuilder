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

test = """
QGraphicsWidget#test{
    border: 10px solid lightBlue;
}"""

icon_bar = """
QTabWidget#IconBar{
    max-height:100px;
}
"""

mac_qss = timeline_label + icon_bar + timeline_area + test
