from PyQt5.QtWidgets import QComboBox


class VarChoose(QComboBox):
    def __init__(self, parent=None, parent_value=''):
        super(VarChoose, self).__init__(parent)
        self.parent_value = parent_value
        self.setInsertPolicy(QComboBox.InsertAlphabetically)
        try:
            from ..main import IconTabs
            # todo attributes
            self.addItems(IconTabs.getAttributes('Timeline.10001'))
        except Exception:
            pass