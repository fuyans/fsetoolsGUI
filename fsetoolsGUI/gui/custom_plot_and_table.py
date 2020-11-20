from os import path

import matplotlib.pyplot as plt
from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QPushButton, QSizePolicy, QSplitter
from matplotlib.backend_bases import NavigationToolbar2

import fsetoolsGUI
from fsetoolsGUI.gui.custom_table import MyDelegate, TableModel

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
    def __init__(
            self,
            parent=None,
            window_title: str = None,
            figure_show_toolbar: bool = False,
            figure_show_xy: bool = True,
            table_content: list = None,
            table_header_row: list = None,
            table_header_col: list = None,
    ):
        """
        This app consists of a figure widget (matplotlib) and a table widget (TableView).
        """

        super().__init__(parent=parent)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        self.resize(380, 380)

        # ======================
        # instantiate UI objects
        # ======================
        self.setStyleSheet(qt_css)

        if window_title:
            self.setWindowTitle(window_title)

        # Instantiate figure and setup layout
        # -----------------------------------

        # create layout for figure
        self.p1_layout_figure = QVBoxLayout()
        self.p1_layout_figure.setSpacing(0), self.p1_layout_figure.setContentsMargins(0, 0, 0, 10)

        # create matplotlib canvas object
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('None')
        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        # add matplotlib canvas object to figure layout
        self.p1_layout_figure.addWidget(self.figure_canvas)

        # create figure controls
        self.p2_layout_figure_controls = QHBoxLayout()
        self.p3_refresh = QPushButton('Refresh')
        self.p3_save_figure = QPushButton('Save')
        # create toolbar (optional) or QLable to show x and y values at mouse cursor
        if figure_show_toolbar:
            self.p2_layout_figure_controls.addSpacing(15)
            self.toolbar = NavigationToolbar(self.figure_canvas, self)
            self.p2_layout_figure_controls.addWidget(self.toolbar)
        elif figure_show_xy:
            self.p2_layout_figure_controls.addSpacing(15)
            in_xy = QLabel('')
            self.p2_layout_figure_controls.addWidget(in_xy)
            self.toolbar_fake = NavigationToolbarFake(self.figure_canvas, in_xy.setText)
        # add figure controls to layout
        self.p2_layout_figure_controls.addItem(QSpacerItem(2, 2, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.p2_layout_figure_controls.addWidget(self.p3_refresh)
        self.p2_layout_figure_controls.addSpacing(5)
        self.p2_layout_figure_controls.addWidget(self.p3_save_figure)
        self.p2_layout_figure_controls.addSpacing(15)
        self.p1_layout_figure.addLayout(self.p2_layout_figure_controls)

        # Instantiate table and setup layout
        # ----------------------------------
        # create TableView and TableModel
        self.p1_layout_table = QVBoxLayout()
        self.p1_layout_table.setSpacing(0), self.p1_layout_table.setContentsMargins(0, 0, 0, 10)

        delegate = MyDelegate()
        self.TableModel = TableModel(self)
        self.TableView = QtWidgets.QTableView()
        if table_content is not None:
            self.TableModel.update_model(content_data=table_content, row_headers=table_header_row, col_headers=table_header_col)
        self.TableView.setModel(self.TableModel)
        self.TableView.setItemDelegate(delegate)

        self.p1_layout_table.addWidget(self.TableView)
        # table_tip_text = QLabel('Ctrl+A to select all, Ctrl+C to copy selected cells.')
        # table_tip_text.setWordWrap(True)
        # table_tip_text.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # self.p1_layout_table.addWidget(table_tip_text)

        # Instantiate splitter and add figure and table
        # ---------------------------------------------
        # A splitter between the figure and table
        self.p0_splitter = QSplitter()
        figure_widget = QtWidgets.QWidget()
        figure_widget.setLayout(self.p1_layout_figure)
        table_widget = QtWidgets.QWidget()
        table_widget.setLayout(self.p1_layout_table)
        self.p0_splitter.addWidget(figure_widget)
        self.p0_splitter.addWidget(table_widget)

        # Instantiate master layout
        # -------------------------
        self.p0_layout = QHBoxLayout()
        self.p0_layout.addWidget(self.p0_splitter)
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
    app = App(window_title='Example', figure_show_xy=True, figure_show_toolbar=False)
    app.show()

    # Create plot
    ax = app.add_subplot()
    ax.fill_between([0, 1], [0, 1], [0, 0.5], facecolor='grey', alpha=0.2, label='area between lines')
    ax.plot([0, 1], [0, 1], label='line 1')
    ax.plot([0, 1], [0, 0.5], label='line 2')
    ax.set_xlabel('x label', fontsize='small')
    ax.set_ylabel('y label', fontsize='small')
    ax.tick_params(axis='both', labelsize='small')
    ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='x-small').set_visible(True)
    ax.grid(which='major', linestyle=':', linewidth=0.5, color='black')

    # Create table
    app.TableModel.update_model(
        content_data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        row_headers=['r1', 'r2', 'r3'],
        col_headers=['c1', 'c2', 'c3']
    )
    # format table
    app.TableView.setSortingEnabled(True)
    app.TableView.resizeColumnsToContents()
    app.TableView.resizeRowsToContents()

    app.refresh_figure()

    qapp.exec_()


def _test_2():
    import sys
    import numpy as np

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(window_title='Example', figure_show_xy=True)
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
    _test_1()
