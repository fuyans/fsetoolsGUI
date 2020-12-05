import numpy as np
import pyqtgraph as pg
from PySide2 import QtCore, QtWidgets, QtGui


class App(QtWidgets.QDialog):
    cm = [
        (31, 120, 180),
        (166, 206, 227),
        (51, 160, 44),
        (178, 223, 138),
        (227, 26, 28),
        (251, 154, 153),
        (255, 127, 0),
        (253, 191, 111),
        (106, 61, 154),
        (202, 178, 214),
        (177, 89, 40),
        (255, 255, 153),
    ]

    def __init__(self, parent=None, title: str = None, antialias: bool = False):

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOptions(antialias=antialias)

        super().__init__(parent=parent)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)

        self.axes = list()

        self.resize(350, 350)

        # ======================
        # instantiate UI objects
        # ======================
        # self.setStyleSheet(qt_css)

        if title:
            self.setWindowTitle(title)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def plot(
            self,
            x: np.ndarray,
            y: np.ndarray,
            ax: pg.PlotWidget = None,
            pen: QtGui.QPen = None,
            pen_colour: tuple = None,
            pen_width: float = None,
            *args,
            **kwargs
    ):

        if ax is None:
            ax = self.axes[-1]

        if pen is None:
            if pen_colour is None:
                pen_colour = self.cm[len(ax.getPlotItem().items) % len(self.cm)]
            if pen_width is None:
                pen_width = 2
            pen = pg.mkPen(color=pen_colour, style=QtCore.Qt.SolidLine, width=pen_width)

        return ax.plot(x=x, y=y, pen=pen, *args, **kwargs)

    def add_subplot(
            self,
            row: int,
            col: int,
            row_span: int = 1,
            col_span: int = 1,
            x_label: str = None,
            y_label: str = None,
            *args,
            **kwargs,
    ):

        ax = pg.PlotWidget(parent=self, *args, **kwargs)
        ax.setLabel('bottom', x_label)
        ax.setLabel('left', y_label)
        ax.showGrid(x=True, y=True)
        self.layout.addWidget(ax, row, col, row_span, col_span)
        self.axes.append(ax)
        return ax


def _test_1():
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(title='Example', antialias=False)

    x1 = np.linspace(1, 50, 1000)
    x2 = np.linspace(2, 50, 1000)
    x3 = np.linspace(3, 50, 1000)
    x4 = np.linspace(4, 50, 1000)
    x5 = np.linspace(5, 50, 1000)
    x6 = np.linspace(6, 50, 1000)

    y1 = 1.5 * np.sin(x1 - 1) * (x1 / max(x1) * 2)
    y2 = 1.5 * np.sin(x2 - 2) * (x2 / max(x2) * 2)
    y3 = 1.5 * np.sin(x3 - 3) * (x3 / max(x3) * 2)
    y4 = 1.5 * np.sin(x4 - 4) * (x4 / max(x4) * 2)
    y5 = 1.5 * np.sin(x5 - 5) * (x5 / max(x5) * 2)
    y6 = 1.5 * np.sin(x6 - 6) * (x6 / max(x6) * 2)

    ax1 = app.add_subplot(0, 0, x_label='x axis', y_label='y axis')

    app.plot(x1, y1, ax=ax1)
    app.plot(x2, y2, ax=ax1)
    app.plot(x3, y3, ax=ax1)
    app.plot(x4, y4, ax=ax1)
    app.plot(x5, y5, ax=ax1)
    app.plot(x6, y6, ax=ax1)

    app.show()
    qapp.exec_()


if __name__ == '__main__':
    _test_1()
