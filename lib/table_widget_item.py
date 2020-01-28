from PyQt5.QtWidgets import QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    """

    """

    def __init__(self, value: str = ""):
        super(TableWidgetItem, self).__init__(value)
        # save old text to redo
        self.old_text = value

    def redo(self):
        """
        redo its text, you should combine it with func save()
        @return:
        """
        self.setText(self.old_text)

    def save(self):
        """

        @return:
        """
        self.old_text = self.text()

    def setText(self, p_str):
        """

        @param p_str:
        @return:
        """
        super(TableWidgetItem, self).setText(p_str)
        self.old_text = p_str
