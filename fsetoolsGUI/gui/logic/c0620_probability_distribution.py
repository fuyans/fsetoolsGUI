import logging

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from PySide2 import QtWidgets
from PySide2.QtCore import Signal, Slot, QObject

from fsetoolsGUI.etc.probability_distribution import solve_dist_for_mean_std
from fsetoolsGUI.gui.layout.i0620_probabilistic_distribution import Ui_MainWindow
from fsetoolsGUI.gui.logic.common import GridDialog
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow

logger = logging.getLogger('gui')

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar


class Signals(QObject):
    __upon_distribution_selection = Signal(int)

    @property
    def upon_distribution_selection(self):
        return self.__upon_distribution_selection


class App0620(QMainWindow):

    # all implemented continuous distributions
    # https://docs.scipy.org/doc/scipy/reference/tutorial/stats/continuous.html
    __dist_available = [
        ['Anglit', 'anglit'],
        ['Arcsine', 'arcsine'],
        ['Cauchy', 'cauchy'],
        ['Cosine', 'cosine'],
        ['Exponential', 'expon'],
        ['Gilbrat', 'gilbrat'],
        ['Gumbel type I', 'gumbel_l'],
        ['Gumbel type II', 'gumbel_r'],
        ['Half Cauchy', 'halfcauchy'],
        ['Half Normal', 'halfnorm'],
        ['Half Logistic', 'halflogistic'],
        ['Hyperbolic Secant', 'hypsecant'],
        ['Laplace', 'laplace'],
        ['Levy', 'levy'],
        ['Left skewed Levy', 'levy_l'],
        ['Log normal', 'lognorm'],  # customised
        # ['1 - Log normal', 'lognorm_sf'],
        ['Logistic', 'logistic'],
        ['Maxwell', 'maxwell'],
        ['Normal', 'norm'],
        ['Rayleigh', 'rayleigh'],
        ['Semicircular', 'semicircular'],
        ['Uniform', 'uniform'],
        ['Wald', 'wald'],
    ]

    def __init__(self, parent=None, mode=None):

        self.__input_parameters = None
        self.__output_parameters = None
        self.__fig = None
        self.__ax_pdf = None
        self.__ax_cdf = None
        self.figure_canvas = None
        self.signals = Signals()
        self.__x = None
        self.__y = None

        super().__init__(
            parent=parent,
            module_id='0620',
            mode=mode
        )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        self.ui.label_in_mean.setToolTip('Mean of the distribution')
        self.ui.lineEdit_in_mean.setToolTip('Mean of the distribution')

        # instantiate figure and associated objects

        self.figure = plt.figure()
        self.figure.set_facecolor('None')
        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.ui.frame_layout.addWidget(self.figure_canvas)

        # self.ui.

        self.ui.lineEdit_in_cdf.textChanged.connect(self.__cdf_value_change)
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.__sample_value_change)

        self.ui.lineEdit_in_distribution.textChanged.connect(self.__distribution_update)
        self.ui.lineEdit_in_mean.textChanged.connect(self.__distribution_update)
        self.ui.lineEdit_in_sd.textChanged.connect(self.__distribution_update)

        self.ui.lineEdit_in_sample_value.setEnabled(False)
        self.ui.lineEdit_in_cdf.setEnabled(False)

        self.signals.upon_distribution_selection.connect(self.upon_distribution_selection)
        self.distribution_selection_dialog = GridDialog(
            labels=[i[0] for i in self.__dist_available], grid_shape=(10,3),
            signal_upon_selection=self.signals.upon_distribution_selection,
            window_title='Select a distribution',
            parent=self
        )
        self.ui.pushButton_in_select_distribution.clicked.connect(lambda: self.distribution_selection_dialog.show())
        self.ui.pushButton_in_select_distribution.adjustSize()

    @Slot(int)
    def upon_distribution_selection(self, distribution_index: int):
        self.activateWindow()
        self.ui.lineEdit_in_distribution.setText(self.__dist_available[distribution_index][1])

    def ok(self):
        """Placeholder method to be overridden by child classes.
        This method is expected to be triggered upon clicking the 'OK' or 'Calculate' button. The following comments
        are suggested procedure to be followed. This method is also connected by keyboard shortcut 'Enter'"""

        # Step 1. Get parameters from UI
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse inputs. {e}')
            return e

        # Step 2. Perform analysis
        # work out distribution
        try:
            assert hasattr(stats, input_parameters['dist_name'])
            output_parameters = self.solve_dist(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Failed to make distribution. {e}')
            logger.error(f'{e}')
            return e

        # Step 3. Cast result onto UI
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Failed to output results. {e}')
            return e

        if not self.ui.lineEdit_in_sample_value.isEnabled():
            self.ui.lineEdit_in_sample_value.setEnabled(True)
            self.ui.lineEdit_in_cdf.setEnabled(True)

        self.repaint()
        self.ui.statusbar.showMessage('Complete')

    def save_figure(self):
        path_to_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save figure',
            dir='image.png'
        )

        self.figure.savefig(path_to_file, dpi=100, transparent=True)

    def __cdf_value_change(self):

        cdf_value = self.input_parameters['cdf_value']
        dist = self.output_parameters['dist']

        sample_value = dist.ppf(cdf_value)

        self.ui.lineEdit_in_sample_value.textChanged.disconnect()
        self.ui.lineEdit_in_sample_value.setText(f'{sample_value:.5g}')
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.__sample_value_change)

    def __sample_value_change(self):

        sample_value = self.input_parameters['sample_value']
        dist = self.output_parameters['dist']

        cdf_value = dist.cdf(sample_value)

        self.ui.lineEdit_in_cdf.textChanged.disconnect()
        self.ui.lineEdit_in_cdf.setText(f'{cdf_value:.5g}')
        self.ui.lineEdit_in_cdf.textChanged.connect(self.__cdf_value_change)

    def __distribution_update(self):
        if self.__ax_pdf is not None and self.__ax_cdf is not None:
            if self.__ax_pdf.lines or self.__ax_cdf.lines:
                self.__ax_pdf.clear()
                self.__ax_pdf.set_yticks([])
                self.__ax_cdf.clear()
                self.__ax_cdf.set_xticks([])
                self.__ax_cdf.set_yticks([])
                self.figure_canvas.draw()

        if self.ui.lineEdit_in_cdf.text() != '':
            self.ui.lineEdit_in_cdf.textChanged.disconnect()
            self.ui.lineEdit_in_cdf.clear()
            self.ui.lineEdit_in_cdf.textChanged.connect(self.__cdf_value_change)
        if self.ui.lineEdit_in_sample_value.text() != '':
            self.ui.lineEdit_in_sample_value.textChanged.disconnect()
            self.ui.lineEdit_in_sample_value.clear()
            self.ui.lineEdit_in_sample_value.textChanged.connect(self.__sample_value_change)

    @property
    def figure(self):
        return self.__fig

    @figure.setter
    def figure(self, fig):
        self.__fig = fig

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

        result = solve_dist_for_mean_std(dist_name, mean, sd)

        dist = getattr(stats, dist_name)(*result.x)

        return dict(dist=dist, sample_value=sample_value, pdf_value=pdf_value, cdf_value=cdf_value)

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, output_parameters_: dict):
        """cast outputs onto gui, in this instance, only the pdf and cdf plots"""

        dist = output_parameters_['dist']

        # ------------------------------------
        # instantiate axes if not already exit
        # ------------------------------------
        if self.ax_pdf is None:
            ax_pdf = self.figure.add_subplot(211)
            ax_pdf.set_xticklabels([])
            ax_pdf.tick_params(axis='both', which='both', labelsize=8)
            self.ax_pdf = ax_pdf

        if self.ax_cdf is None:
            ax_cdf = self.figure.add_subplot(212, sharex=self.__ax_pdf)
            ax_cdf.tick_params(axis='both', which='both', labelsize=8)
            self.ax_cdf = ax_cdf

        # --------
        # plot pdf
        # --------
        x = np.linspace(dist.ppf(1e-3), dist.ppf(1 - 1e-3), 50)
        y_pdf = dist.pdf(x)
        self.ax_pdf.clear()
        self.ax_pdf.plot(x, y_pdf, c='k')
        self.ax_pdf.set_ylim(bottom=0)
        self.ax_pdf.tick_params(axis='both', direction='in', labelbottom=False)

        # --------
        # plot cdf
        # --------
        y_cdf = dist.cdf(x)
        self.ax_cdf.clear()
        self.ax_cdf.plot(x, y_cdf, c='k')
        self.ax_cdf.set_ylim(bottom=0)
        self.ax_cdf.set_yticks([0, 1])
        self.ax_cdf.tick_params(axis='both', direction='in')

        # -------------------------------------------------------------
        # highlight area under the pdf and cdf if `sample_value` exists
        # -------------------------------------------------------------
        if output_parameters_['sample_value'] is not None:
            x_ = np.linspace(x[0], output_parameters_['sample_value'], 50)
            y_pdf_, y_cdf_ = dist.pdf(x_), dist.cdf(x_)
            self.ax_pdf.fill_between(x_, y_pdf_, np.zeros_like(x_), facecolor='grey', interpolate=True)
            self.ax_cdf.fill_between(x_, y_cdf_, np.zeros_like(x_), facecolor='grey', interpolate=True)

        # ----------------------
        # finalise/format figure
        # ----------------------
        self.figure.tight_layout(pad=0.25)
        self.figure_canvas.draw()

        # -------------------------
        # assign to object property
        # -------------------------
        self.__output_parameters = output_parameters_

    @property
    def ax_cdf(self) -> plt.axis:
        return self.__ax_cdf

    @ax_cdf.setter
    def ax_cdf(self, ax):
        self.__ax_cdf = ax

    @property
    def ax_pdf(self) -> plt.axis:
        return self.__ax_pdf

    @ax_pdf.setter
    def ax_pdf(self, ax):
        self.__ax_pdf = ax

    def moveEvent(self, event):
        geo = self.distribution_selection_dialog.geometry()
        geo.setX(self.normalGeometry().x() + self.width())
        geo.setY(self.normalGeometry().y())
        self.distribution_selection_dialog.setGeometry(geo)


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0620(mode=-1)
    app.show()

    qapp.exec_()
