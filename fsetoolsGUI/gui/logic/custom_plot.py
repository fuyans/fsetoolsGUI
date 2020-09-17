from os import path

import matplotlib.pyplot as plt
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtWidgets import QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QFrame, QSpacerItem

import fsetoolsGUI

try:
    qt_css = open(path.join(fsetoolsGUI.__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    qt_css = None

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


class App(QtWidgets.QDialog):
    def __init__(self, parent=None, title: str = None, show_toolbar: bool = False):

        super().__init__(parent=parent)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        # ======================
        # instantiate UI objects
        # ======================
        self.setStyleSheet(qt_css)

        if title:
            self.setWindowTitle(title)

        self.p0_layout = QVBoxLayout()
        self.p0_layout.setSpacing(0), self.p0_layout.setContentsMargins(0, 0, 0, 10)
        self.frame = QFrame()
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.p0_layout.addWidget(self.frame)

        self.p3_layout = QHBoxLayout()
        self.p3_refresh = QPushButton('Refresh')
        self.p3_refresh.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_save_figure = QPushButton('Save')
        self.p3_save_figure.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')

        self.p3_layout.addItem(QSpacerItem(2, 2, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.p3_layout.addWidget(self.p3_refresh)
        self.p3_layout.addSpacing(5)
        self.p3_layout.addWidget(self.p3_save_figure)
        self.p3_layout.addSpacing(15)

        self.p0_layout.addLayout(self.p3_layout)

        self.setLayout(self.p0_layout)

        # =========================================
        # Instantiate figure and associated objects
        # =========================================
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('None')

        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.frame_layout.addWidget(self.figure_canvas)
        if show_toolbar:
            self.toolbar = NavigationToolbar(self.figure_canvas, self)
            self.frame_layout.addWidget(self.toolbar)

        self.p3_refresh.clicked.connect(self.refresh_figure)
        self.p3_save_figure.clicked.connect(self.save_figure)

        self.resize(380, 380)

    def add_subplots(self, *args, **kwargs) -> plt.Axes:
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


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(title='Example')
    app.show()

    ax = app.add_subplots()
    ax.fill_between([0, 1], [0, 1], [0, 0.5], facecolor='grey', alpha=0.2, label='area between lines')
    ax.plot([0, 1], [0, 1], label='line 1')
    ax.plot([0, 1], [0, 0.5], label='line 2')
    ax.set_xlabel('x label', fontsize='small')
    ax.set_ylabel('y label', fontsize='small')
    ax.tick_params(axis='both', labelsize='small')
    ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='x-small').set_visible(True)
    ax.grid(which='major', linestyle=':', linewidth=0.5, color='black')
    app.figure.tight_layout()

    qapp.exec_()
