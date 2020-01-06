import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget

from .info import Info
from .kernel import Kernel


class Func(QWidget):
    """
    This class is used to store all common function.
    """

    @staticmethod
    def generateWidgetId(widget_type: int) -> int:
        """
        it' used to generate widget id which is used to discern different widget.
        @param widget_type: the add_type of widget, such as timeline.
        @return: new widget id
        """
        # get the current num of this add_type which has been created.
        count = Kernel.WidgetTypeCount[widget_type]
        # widget id = widget_type * 10000 + count
        widget_id = widget_type * Info.MaxWidgetCount + count
        # inc count of this widget type
        Kernel.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: int) -> str:
        """
        it' used to generate widget id which is used to discern different widget.
        @param widget_type: the add_type of widget, such as timeline.
        @return: new widget id
        """
        widget_type_name = Info.WidgetType[widget_type]
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type_name}_{Kernel.WidgetNameCount[widget_type]}"
            # inc count of this widget type
            Kernel.WidgetNameCount[widget_type] += 1
            # check name's validity
            if widget_name not in Kernel.Names:
                return widget_name

    @staticmethod
    def createWidget(widget_id: int, widget_name: str) -> None:
        """
        create widget according to its widget id and set its name
        @param widget_id:
        @param widget_name: its name
        @return:
        """
        widget_type = widget_id // Info.MaxWidgetCount
        # todo add other items into this function
        widget = None
        if widget_type == Info.Timeline:
            from app.center import Timeline
            widget = Timeline(widget_id, widget_name)
        elif widget_type == Info.Cycle:
            from app.center.events import Cycle
            widget = Cycle(widget_id, widget_name)
        else:
            # if fail to create widget, exit.
            exit()
        # change data set in Kernel
        Kernel.Widgets[widget_id] = widget
        Kernel.Names[widget_name] = [widget_id]

        # link necessary signals
        Func.linkWidgetSignals(widget_type, widget)

    @staticmethod
    def linkWidgetSignals(widget_type: int, widget):
        """
        link widget's signals according to its widget type.
        @param widget_type:
        @param widget:
        @return:
        """
        # It should be left to Psy
        Kernel.Psy.linkWidgetSignals(widget_type, widget)

    @staticmethod
    def checkWidgetNameValidity(widget_name: str) -> (bool, str):
        """
        check the validity of widget name.
        It should be unique, unless it's a reference.
        @param widget_name:
        @return: validity
        """
        # name should start with a letter
        if not re.match(r"^[a-zA-Z].*$", widget_name):
            return False, "Name should start with a letter."
        # name should be unique.
        if widget_name not in Kernel.Names:
            return True, ""
        return False, "Name already exists."

    @staticmethod
    def getImage(image_path: str, type: int = 0, size: QSize = None) -> QPixmap or QIcon:
        """
        get image from its relative path, return qt image object, include QPixmap or QIcon.
        @param image_path: its relative path
        @param type: 0: pixmap (default),
                     1: icon
        @return: Qt image object
        """
        path = os.path.join(Info.Image_Path, image_path)
        if not type:
            if size:
                return QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation)
            return QPixmap(path)
        return QIcon(path)

    @staticmethod
    def print(information: str, information_type: int = 0) -> None:
        """
        print information in output.
        @param information:
        @param information_type: 0 none
                                 1 success
                                 2 fail
        @return:
        """
        Kernel.Psy.output.print(information, information_type)

    @staticmethod
    def changeWidgetName(widget_id: int, widget_name: str):
        """
        change widget.widget_name
        @param widget_id:
        @param widget_name:
        @return:
        """
        widget = Kernel.Widgets[widget_id]
        widget.widget_name = widget_name
