from os import path

import matplotlib.pyplot as plt
from PySide2 import QtWidgets, QtCore

import fsetoolsGUI
from fsetoolsGUI.gui.layout.custom_plot import Ui_MainWindow

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


class App(QtWidgets.QMainWindow):

    def __init__(self, parent=None, title:str=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if title is not None:
            self.setWindowTitle(title)

        # instantiate figure and associated objects
        self.__fig: plt.Figure = plt.figure()
        self.__fig.patch.set_facecolor('None')

        self.figure_canvas = FigureCanvas(self.__fig)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.ui.frame_layout.addWidget(self.figure_canvas)
        # self.toolbar = NavigationToolbar(self.figure_canvas, self)
        # self.ui.frame_layout.addWidget(self.toolbar)

        self.setStyleSheet(qt_css)

        self.ui.pushButton_refresh.clicked.connect(self.refresh_figure)
        self.ui.pushButton_save_figure.clicked.connect(self.save_figure)

    @property
    def figure(self):
        return self.__fig

    def add_subplots(self, *args, **kwargs) -> plt.Axes:
        ax = self.figure.add_subplot(*args, **kwargs)
        return ax

    def save_figure(self):
        path_to_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save figure',
            dir='image.png'
        )

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
    app = App()
    app.show()

    ax = app.add_subplots()
    ax.plot([0, 1], [0, 1])

    qapp.exec_()
