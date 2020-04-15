import os.path as path

from PySide2 import QtWidgets, QtGui, QtCore

import fsetoolsGUI
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.layout.i0101_data_sheet import Ui_MainWindow


class DialogPageDisplay(QMainWindow):
    def __init__(self, module_id: str, fp_image: str, parent=None):
        super().__init__(
            module_id=module_id,
            parent=parent,
        )

        self.mscroll_last_move_y = 0
        self.mscroll_last_move_x = 0

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setPixmap(QtGui.QPixmap(fp_image))

        self.scroll_geo = self.ui.scrollArea.geometry
        self.scroll_vbar = self.ui.scrollArea.verticalScrollBar()
        self.scroll_hbar = self.ui.scrollArea.horizontalScrollBar()

        self.init(self)

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


class App(DialogPageDisplay):
    def __init__(self, parent=None):
        super().__init__(
            module_id='0101',
            fp_image=path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0101-0.png'),
            parent=parent
        )
        self.resize(1000, 600)


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
