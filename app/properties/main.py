from lib import DockWidget


class Properties(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)

    def showProperties(self, widget_id: int):
        """
        show widget's properties
        @param widget_id:
        @return:
        """
        # todo show widget's properties
