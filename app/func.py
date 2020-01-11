import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter

from .info import Info
from .kernel import Kernel


class Func(object):
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

    @staticmethod
    def getTrackingPix(text: str) -> QPixmap:
        """
        generate pixmap from text
        @param text:
        @return:
        """
        pix = QPixmap(200, 16)
        pix.fill(QColor(0, 0, 0, 0))
        painter = QPainter(pix)
        painter.drawText(0, 0, 200, 16, Qt.TextSingleLine, text)
        return pix

    @staticmethod
    def getWidgetAttributes(widget_id: int) -> dict:
        """
        get widget's attributes and attributes' layer
        @param widget_id:
        @return: {attribute: layer}
        """
        # global attributes
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subSex": 0, "subHandness": 0, "subAge": 0}

        # todo attributes about quest, I don't know what they are.
        pass

        # get widget's hidden attributes
        hidden_attributes = Kernel.Widgets[widget_id].getHiddenAttributes()

        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Kernel.Nodes[widget_id]
        depth = -1
        while node:
            depth += 1
            node = node.parent()
        # do 1.
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.Timeline):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.Cycle):
                    for attribute in Kernel.Widgets[child_node.widget_id].getHiddenAttribute():
                        attributes[f"{child_node.text(0)}.{attribute}"] = depth
        # do 2. 3.
        first = True
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.Cycle):
                cycle = Kernel.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes[f"{cycle_name}.attr.{attribute}"] = depth
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Kernel.Widgets[node.widget_id].getHiddenAttribute()
                    for attribute in first_cycle_hidden_attributes:
                        attributes[f"{cycle_name}.{attribute}"] = depth
                    first = False
            depth -= 1
            node = node.parent()
        # return
        return attributes

    @staticmethod
    def getWidgetProperties(widget_id: int) -> dict:
        """
        get widget's properties
        @param widget_id:
        @return:
        """
        widget = Kernel.Widgets[widget_id]
        return widget.getProperties()

    @staticmethod
    def isWidgetType(widget_id: int, widget_type: int):
        """
        judge widget_id's widget type
        @param self:
        @param widget_id:
        @param widget_type:
        @return:
        """
        return widget_id // Info.MaxWidgetCount == widget_type
