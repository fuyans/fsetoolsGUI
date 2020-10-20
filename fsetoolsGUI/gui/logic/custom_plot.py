from os import path

import matplotlib.pyplot as plt
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QPushButton, QSizePolicy
from matplotlib.backend_bases import NavigationToolbar2

import fsetoolsGUI

plt.style.use('seaborn-paper')

try:
    qt_css = open(path.join(fsetoolsGUI.__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    qt_css = None

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ModuleNotFoundError:
    # from matplotlib.backends.backend_qt4agg import FigureCanvas
    # from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
    raise ModuleNotFoundError


class NavigationToolbarFake(NavigationToolbar2):
    def __init__(self, canvas, func_upon_move=None):
        super().__init__(canvas)
        self.func_upon_move = func_upon_move

    def mouse_move(self, event):
        self._update_cursor(event)

        if event.inaxes and event.inaxes.get_navigate() and self.func_upon_move:

            try:
                self.func_upon_move(f'{event.xdata:g}, {event.ydata:g}')
            except (ValueError, OverflowError):
                pass
        else:
            self.func_upon_move('')

    def _init_toolbar(self):
        pass


class App(QtWidgets.QDialog):
    def __init__(self, parent=None, title: str = None, show_toolbar: bool = False, show_xy: bool = True):

        super().__init__(parent=parent)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.resize(380, 380)

        # ======================
        # instantiate UI objects
        # ======================
        self.setStyleSheet(qt_css)

        if title:
            self.setWindowTitle(title)

        self.p0_layout = QVBoxLayout()
        self.p0_layout.setSpacing(0), self.p0_layout.setContentsMargins(0, 0, 0, 10)

        self.figure = plt.figure()
        self.figure.patch.set_facecolor('None')

        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.p0_layout.addWidget(self.figure_canvas)

        self.p3_layout = QHBoxLayout()
        self.p3_refresh = QPushButton('Refresh')
        self.p3_save_figure = QPushButton('Save')

        if show_toolbar:
            self.p3_layout.addSpacing(15)
            self.toolbar = NavigationToolbar(self.figure_canvas, self)
            self.p3_layout.addWidget(self.toolbar)
        elif show_xy:
            self.p3_layout.addSpacing(15)
            in_xy = QLabel('')
            self.p3_layout.addWidget(in_xy)
            self.toolbar_fake = NavigationToolbarFake(self.figure_canvas, in_xy.setText)

        self.p3_layout.addItem(QSpacerItem(2, 2, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.p3_layout.addWidget(self.p3_refresh)
        self.p3_layout.addSpacing(5)
        self.p3_layout.addWidget(self.p3_save_figure)
        self.p3_layout.addSpacing(15)

        self.p0_layout.addLayout(self.p3_layout)

        self.setLayout(self.p0_layout)

        self.p3_refresh.clicked.connect(self.refresh_figure)
        self.p3_save_figure.clicked.connect(self.save_figure)

    def resizeEvent(self, event):
        self.refresh_figure()

    def add_subplot(self, *args, **kwargs) -> plt.Axes:
        ax = self.figure.add_subplot(*args, **kwargs)
        return ax

    def save_figure(self):
        path_to_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save figure',
            dir='image.png'
        )

        if path_to_file:
            self.figure.savefig(path_to_file, dpi=100, transparent=True)

    def refresh_figure(self):
        self.figure.tight_layout()
        self.figure.canvas.draw()
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        event.accept()


def _test_1():
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(title='Example', show_xy=True, show_toolbar=True)
    app.show()

    ax = app.add_subplot()
    ax.fill_between([0, 1], [0, 1], [0, 0.5], facecolor='grey', alpha=0.2, label='area between lines')
    ax.plot([0, 1], [0, 1], label='line 1')
    ax.plot([0, 1], [0, 0.5], label='line 2')
    ax.set_xlabel('x label', fontsize='small')
    ax.set_ylabel('y label', fontsize='small')
    ax.tick_params(axis='both', labelsize='small')
    ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='x-small').set_visible(True)
    ax.grid(which='major', linestyle=':', linewidth=0.5, color='black')

    app.refresh_figure()

    qapp.exec_()


def _test_2():
    import sys
    import numpy as np

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(title='Example', show_xy=True)
    app.show()

    ax1 = app.add_subplot(121)
    ax1.fill_between([0, 1], [0, 1], [0, 0.5], facecolor='grey', alpha=0.2, label='area between line 1 and 2')
    ax1.plot([0, 1], [0, 1], label='line 1')
    ax1.plot([0, 1], [0, 0.5], label='line 2')
    ax1.set_xlabel('x label', fontsize='small')
    ax1.set_ylabel('y label', fontsize='small')
    ax1.tick_params(axis='both', labelsize='small')
    ax1.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='x-small').set_visible(True)
    ax1.grid(which='major', linestyle=':', linewidth=0.5, color='black')

    X, Y = np.meshgrid(np.arange(-3.0, 3.01, 0.1), np.arange(-3.0, 3.01, 0.1))
    Z1 = np.exp(-X ** 2 - Y ** 2)
    Z2 = np.exp(-(X - 1) ** 2 - (Y - 1) ** 2)
    Z = (Z1 - Z2) * 2

    ax2 = app.add_subplot(122)
    ax2.contourf(X, Y, Z)
    ax2.set_xlabel('x label', fontsize='small')
    ax2.set_ylabel('y label', fontsize='small')
    ax2.tick_params(axis='both', labelsize='small')
    ax2.grid(which='major', linestyle=':', linewidth=0.5, color='black')

    app.resize(680, 380)
    app.refresh_figure()

    qapp.exec_()


if __name__ == '__main__':
    _test_2()
