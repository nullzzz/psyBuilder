from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsGridLayout, QGraphicsWidget


class TimelineScene(QGraphicsScene):
    """
    real place to place items
    """

    def __init__(self):
        super(TimelineScene, self).__init__(None)
        # layout
        self.layout = QGraphicsGridLayout()
        self.layout.setRowFixedHeight(0, 100)
        # set a container widget to set layout
        self.container = QGraphicsWidget(None, Qt.Widget)
        # set container's pos, namely top left.
        self.container.setPos(0, 0)
        self.container.setLayout(self.layout)
        # add container to itself
        self.addItem(self.container)
        self.count = 0
        #

    def addTimelineItem(self, timeline_item, timeline_name_item, index: int):
        """
        add a item in its layout
        @param timeline_item:
        @param index:
        @return:
        """
        # col width
        self.layout.setColumnFixedWidth(index, 100)
        # add timeline item
        self.layout.addItem(timeline_item, 0, index, Qt.AlignCenter)
        # add text item
        self.layout.addItem(timeline_name_item, 2, index, Qt.AlignCenter)

    def deleteTimelineItem(self, index: int):
        """
        delete a item through its index
        @param index:
        @return:
        """
