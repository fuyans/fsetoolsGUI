from os import path

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import QLabel, QGridLayout, QGroupBox, QWidget, QScrollArea

import fsetoolsGUI
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass


class UI(object):
    def setupUi(self, main_window):
        # TREE:
        # label ->
        # (scroll_area_widget_content_layout, scroll_area_widget_content) ->
        # scroll_area ->
        # (page_2, p2_layout) ->
        # (central_widget, p0_layout) ->
        # main_window

        self.central_widget = QWidget(main_window)
        self.page_2 = QGroupBox(self.central_widget)

        # create scroll area content
        self.scroll_area_widget_content = QWidget()
        self.label = QLabel()
        self.scroll_area_widget_content_layout = QGridLayout(self.scroll_area_widget_content)
        self.scroll_area_widget_content_layout.addWidget(self.label, 1, 0, 1, 1)

        # create scroll area
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setWidget(self.scroll_area_widget_content)

        self.p2_layout = QGridLayout(self.page_2)
        self.p2_layout.addWidget(self.scroll_area, 0, 0, 1, 1)

        self.p0_layout = QGridLayout(self.central_widget)
        self.p0_layout.addWidget(self.page_2, 0, 0, 1, 1)

        self.p0_layout.setSpacing(0), self.p0_layout.setContentsMargins(0, 0, 0, 0)
        self.p2_layout.setSpacing(0), self.p2_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_content_layout.setSpacing(0), self.scroll_area_widget_content_layout.setContentsMargins(0, 0, 0, 0)

        main_window.setCentralWidget(self.central_widget)


class AppBaseClassScrollableContent(AppBaseClass):
    app_id = None
    app_name_short = None
    app_name_long = None

    def __init__(self, fp_image: str, parent=None, post_stats: bool = True, ui=UI):

        super().__init__(parent=parent, post_stats=post_stats, ui=ui)

        self.mscroll_last_move_y = 0
        self.mscroll_last_move_x = 0

        self.ui.label.setPixmap(QtGui.QPixmap(fp_image))

        self.scroll_geo = self.ui.scroll_area.geometry
        self.scroll_vbar = self.ui.scroll_area.verticalScrollBar()
        self.scroll_hbar = self.ui.scroll_area.horizontalScrollBar()

    def mouseMoveEvent(self, event):

        geo = self.scroll_geo
        x = event.pos().x()
        y = event.pos().y()
        left, right, top, bottom = geo().left(), geo().right(), geo().top(), geo().bottom()

        if left < x < right and top < y < bottom:
            if self.mscroll_last_move_x == 0:
                self.mscroll_last_move_x = x
            if self.mscroll_last_move_y == 0:
                self.mscroll_last_move_y = y

            dx = self.mscroll_last_move_x - x
            dy = self.mscroll_last_move_y - y

            self.scroll_hbar.setValue(self.scroll_hbar.value() + dx)
            self.scroll_vbar.setValue(self.scroll_vbar.value() + dy)

            self.mscroll_last_move_x = x
            self.mscroll_last_move_y = y

    def mouseReleaseEvent(self, event):
        self.mscroll_last_move_x = 0
        self.mscroll_last_move_y = 0

    def eventFilter(self, source, event):

        x = event.pos().x()
        y = event.pos().y()

        print(x, y)

        if event.type() == QtCore.QEvent.MouseMove:
            print(x, y)

            if self.mscroll_last_move_x == 0:
                self.mscroll_last_move_x = x
            if self.mscroll_last_move_y == 0:
                self.mscroll_last_move_y = y

            dx = self.mscroll_last_move_x - x
            dy = self.mscroll_last_move_y - y

            self.scroll_hbar.setValue(self.scroll_hbar.value() + dx)
            self.scroll_vbar.setValue(self.scroll_vbar.value() + dy)

            self.mscroll_last_move_x = x
            self.mscroll_last_move_y = y

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.mscroll_last_move_y = 0
            self.mscroll_last_move_x = 0

        return QtWidgets.QWidget.eventFilter(self, source, event)


class AppTest(AppBaseClassScrollableContent):
    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(
            fp_image=path.join(fsetoolsGUI.__root_dir__, 'gui', '../images', '0101-0.png'),
            parent=parent,
            ui=UI,
            post_stats=post_stats
        )


if __name__ == '__main__':
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = AppTest(post_stats=False)
    app.show()
    qapp.exec_()
