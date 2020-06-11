import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from PySide2 import QtWidgets, QtCore

from fsetoolsGUI.etc.probability_distribution import solve_loc_scale
from fsetoolsGUI.gui.layout.i0620_probabilistic_distribution import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


class App(QMainWindow):

    def __init__(self, parent=None, mode=None):

        self.__input_parameters = None
        self.__output_parameters = None

        super().__init__(
            parent=parent,
            module_id='0620',
            mode=mode
        )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # instantiate figure and associated objects

        self.__fig, self.__ax_pdf, self.__ax_cdf = self.init_fig_ax()
        self.figure_canvas = FigureCanvas(self.__fig)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.ui.frame_layout.addWidget(self.figure_canvas)
        # self.toolbar = NavigationToolbar(self.figure_canvas, self)
        # self.ui.frame_layout.addWidget(self.toolbar)

        self.ui.lineEdit_in_cdf.textChanged.connect(self.cdf_value_change)
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.sample_value_change)

        self.ui.lineEdit_in_distribution.textChanged.connect(self.clear_plot)
        self.ui.lineEdit_in_mean.textChanged.connect(self.clear_plot)
        self.ui.lineEdit_in_sd.textChanged.connect(self.clear_plot)

    def clear_plot(self):
        if self.__ax_pdf.lines or self.__ax_cdf.lines:
            self.__ax_cdf.clear()
            self.__ax_pdf.clear()
            self.figure_canvas.draw()

    def cdf_value_change(self):

        cdf_value = self.input_parameters['cdf_value']
        dist = self.output_parameters['dist']

        sample_value = dist.ppf(cdf_value)

        self.ui.lineEdit_in_sample_value.textChanged.disconnect()
        self.ui.lineEdit_in_sample_value.setText(f'{sample_value:.5g}'.rstrip('0').rstrip('.'))
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.sample_value_change)

    def sample_value_change(self):

        sample_value = self.input_parameters['sample_value']
        dist = self.output_parameters['dist']

        cdf_value = dist.cdf(sample_value)

        self.ui.lineEdit_in_cdf.textChanged.disconnect()
        self.ui.lineEdit_in_cdf.setText(f'{cdf_value:.5g}'.rstrip('0').rstrip('.'))
        self.ui.lineEdit_in_cdf.textChanged.connect(self.cdf_value_change)

    @staticmethod
    def init_fig_ax():

        fig = plt.figure()
        fig.set_facecolor('None')

        ax_pdf = fig.add_subplot(211)
        ax_pdf.tick_params(axis='both', which='both', labelsize=8)

        ax_cdf = fig.add_subplot(212, sharex=ax_pdf)
        ax_cdf.tick_params(axis='both', which='both', labelsize=8)

        fig.tight_layout()

        return fig, ax_pdf, ax_cdf

    @property
    def input_parameters(self) -> dict:

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        dist_name = self.ui.lineEdit_in_distribution.text()
        mean = str2float(self.ui.lineEdit_in_mean.text())
        sd = str2float(self.ui.lineEdit_in_sd.text())
        sample_value = str2float(self.ui.lineEdit_in_sample_value.text())
        pdf_value = None
        cdf_value = str2float(self.ui.lineEdit_in_cdf.text())

        return dict(dist_name=dist_name, mean=mean, sd=sd, sample_value=sample_value, pdf_value=pdf_value,
                    cdf_value=cdf_value)

    @staticmethod
    def solve_dist(dist_name, mean, sd, sample_value, pdf_value, cdf_value) -> dict:

        result = solve_loc_scale(dist_name, mean, sd)

        dist = getattr(stats, dist_name)(*result.x)

        return dict(dist=dist, sample_value=sample_value, pdf_value=pdf_value, cdf_value=cdf_value)

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, output_parameters_: dict):

        dist = output_parameters_['dist']

        # -------------------------
        # make and cast plots to ui
        # -------------------------
        x = np.linspace(dist.ppf(1e-3), dist.ppf(1 - 1e-3), 100)
        y_pdf = dist.pdf(x)
        y_cdf = dist.cdf(x)
        self.__ax_pdf.clear()
        self.__ax_cdf.clear()
        self.__ax_pdf.plot(x, y_pdf, c='k')
        self.__ax_cdf.plot(x, y_cdf, c='k')

        self.figure.tight_layout()
        self.figure_canvas.draw()

        # -------------------------
        # assign to object property
        # -------------------------
        self.__output_parameters = output_parameters_

    def ok(self):
        """Placeholder method to be overridden by child classes.
        This method is expected to be triggered upon clicking the 'OK' or 'Calculate' button. The following comments
        are suggested procedure to be followed. This method is also connected by keyboard shortcut 'Enter'"""

        # Step 1. Get parameters from UI
        input_parameters = self.input_parameters

        # Step 2. Perform analysis
        # work out distribution
        output_parameters = self.solve_dist(**input_parameters)

        # Step 3. Cast result onto UI
        self.output_parameters = output_parameters

        self.repaint()
        self.ui.statusbar.showMessage('Complete')

    @property
    def figure(self):
        return self.__fig

    def add_subplots(self, *args, **kwargs) -> plt.Axes:
        ax = self.figure.add_subplot(*args, **kwargs)
        self.figure.tight_layout()
        self.figure.canvas.draw()
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
    app = App(mode=-1)
    app.show()

    # ax = app.add_subplots()
    # ax.plot([0, 1], [0, 1])

    qapp.exec_()
