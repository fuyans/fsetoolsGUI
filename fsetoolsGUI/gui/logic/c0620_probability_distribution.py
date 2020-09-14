import numpy as np
import scipy.stats as stats
from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QPushButton

from fsetoolsGUI import logger
from fsetoolsGUI.etc.probability_distribution import solve_dist_for_mean_std
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import *
from fsetoolsGUI.gui.logic.common import GridDialog
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp


class Signals(QObject):
    __upon_distribution_selection = Signal(int)

    @property
    def upon_distribution_selection(self):
        return self.__upon_distribution_selection


class App(AppBaseClass):
    app_id = '0620'
    app_name_short = 'Probability\ndistribution'
    app_name_long = 'Probability distribution'

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

    def __init__(self, parent=None, post_stats: bool = True):

        self.__input_parameters = None
        self.__output_parameters = None
        self._Figure = None
        self._Figure_ax_pdf = None
        self._Figure_ax_cdf = None
        self.signals = Signals()

        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('Distribution'), c.value, 0, 1, 1)
        self.ui.p2_in_distribution = QLineEdit()
        self.ui.p2_layout.addWidget(self.ui.p2_in_distribution, c.value, 1, 1, 1)
        self.ui.p2_in_fp_inputs = QPushButton('Select')
        self.ui.p2_in_fp_inputs.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_inputs, c.count, 2, 1, 1)

        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_mean', 'Mean', '')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_sd', 'SD', '')

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_cdf', 'CDF', '')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_sample_value', 'Sample value', '')

        self.ui.p3_example.setVisible(False)
        self.ui.p3_about.setVisible(False)

        # signals and slots
        self.ui.p2_in_cdf.textChanged.connect(self.__cdf_value_change)
        self.ui.p2_in_sample_value.textChanged.connect(self.__sample_value_change)

        self.ui.p2_in_distribution.textChanged.connect(self.__distribution_update)
        self.ui.p2_in_mean.textChanged.connect(self.__distribution_update)
        self.ui.p2_in_sd.textChanged.connect(self.__distribution_update)

        self.ui.p2_in_sample_value.setEnabled(False)
        self.ui.p2_in_cdf.setEnabled(False)

        self.signals.upon_distribution_selection.connect(self.upon_distribution_selection)
        self.distribution_selection_dialog = GridDialog(
            labels=[i[0] for i in self.__dist_available], grid_shape=(10, 3),
            signal_upon_selection=self.signals.upon_distribution_selection,
            window_title='Select a distribution',
            parent=self
        )
        self.activated_dialogs.append(self.distribution_selection_dialog)
        self.ui.p2_in_fp_inputs.clicked.connect(lambda: self.distribution_selection_dialog.show())
        self.adjustSize()

    def ok(self):
        """Placeholder method to be overridden by child classes.
        This method is expected to be triggered upon clicking the 'OK' or 'Calculate' button. The following comments
        are suggested procedure to be followed. This method is also connected by keyboard shortcut 'Enter'"""

        # Step 1. Get parameters from UI
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            logger.error(f'Failed to parse inputs, {e}')
            self.statusBar().showMessage(f'Failed to parse inputs, {e}')
            return e

        # Step 2. Perform analysis
        # work out distribution
        try:
            assert hasattr(stats, input_parameters['dist_name'])
            output_parameters = self.solve_dist(**input_parameters)
        except Exception as e:
            logger.error(f'Failed to make distribution, {e}')
            self.statusBar().showMessage(f'Failed to make distribution, {e}')
            return e

        # Step 3. Cast result onto UI
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            logger.error(f'Failed to output results, {e}')
            self.statusBar().showMessage(f'Failed to output results, {e}')
            return e

        try:
            self.show_results_in_figure()
        except Exception as e:
            logger.error(f'Failed to make plots, {e}')
            self.statusBar().showMessage(f'Failed to make plots, {e}')
            return e

        if not self.ui.p2_in_sample_value.isEnabled():
            self.ui.p2_in_sample_value.setEnabled(True)
            self.ui.p2_in_cdf.setEnabled(True)

        logger.info(f'Calculation complete')
        self.ui.statusbar.showMessage('Calculation complete')
        self.repaint()

    def example(self):
        pass

    @Slot(int)
    def upon_distribution_selection(self, distribution_index: int):
        self.activateWindow()
        self.ui.p2_in_distribution.setText(self.__dist_available[distribution_index][1])

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

        self.ui.p2_in_sample_value.textChanged.disconnect()
        self.ui.p2_in_sample_value.setText(f'{sample_value:.5g}')
        self.ui.p2_in_sample_value.textChanged.connect(self.__sample_value_change)

    def __sample_value_change(self):

        sample_value = self.input_parameters['sample_value']
        dist = self.output_parameters['dist']

        cdf_value = dist.cdf(sample_value)

        self.ui.p2_in_cdf.textChanged.disconnect()
        self.ui.p2_in_cdf.setText(f'{cdf_value:.5g}')
        self.ui.p2_in_cdf.textChanged.connect(self.__cdf_value_change)

    def __distribution_update(self):
        if self._Figure_ax_pdf is not None and self._Figure_ax_cdf is not None:
            if self._Figure_ax_pdf.lines or self._Figure_ax_cdf.lines:
                self._Figure_ax_pdf.clear()
                self._Figure_ax_pdf.set_yticks([])
                self._Figure_ax_pdf.clear()
                self._Figure_ax_pdf.set_xticks([])
                self._Figure_ax_pdf.set_yticks([])
                self._Figure.figure_canvas.draw()

        if self.ui.p2_in_cdf.text() != '':
            self.ui.p2_in_cdf.textChanged.disconnect()
            self.ui.p2_in_cdf.clear()
            self.ui.p2_in_cdf.textChanged.connect(self.__cdf_value_change)
        if self.ui.p2_in_sample_value.text() != '':
            self.ui.p2_in_sample_value.textChanged.disconnect()
            self.ui.p2_in_sample_value.clear()
            self.ui.p2_in_sample_value.textChanged.connect(self.__sample_value_change)

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

        dist_name = self.ui.p2_in_distribution.text()
        mean = str2float(self.ui.p2_in_mean.text())
        sd = str2float(self.ui.p2_in_sd.text())
        sample_value = str2float(self.ui.p2_in_sample_value.text())
        pdf_value = None
        cdf_value = str2float(self.ui.p2_in_cdf.text())

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
    def output_parameters(self, v: dict):
        """cast outputs onto gui, in this instance, only the pdf and cdf plots"""
        self.__output_parameters = v

    def moveEvent(self, event):
        geo = self.distribution_selection_dialog.geometry()
        geo.setX(self.normalGeometry().x() + self.width())
        geo.setY(self.normalGeometry().y())
        self.distribution_selection_dialog.setGeometry(geo)

    def show_results_in_figure(self):
        dist = self.output_parameters['dist']

        if self._Figure is None:
            self._Figure = PlotApp(self, title='Distribution visualisation')
            self.activated_dialogs.append(self._Figure)
            self._Figure_ax_pdf = self._Figure.figure.add_subplot(211)
            self._Figure_ax_cdf = self._Figure.figure.add_subplot(212, sharex=self._Figure_ax_pdf)

            self._Figure_ax_pdf.tick_params(axis='both', which='both', labelsize=8)
            self._Figure_ax_cdf.tick_params(axis='both', which='both', labelsize=8)

        else:
            self._Figure_ax_pdf.clear()
            self._Figure_ax_cdf.clear()

        # --------
        # plot pdf
        # --------
        x = np.linspace(dist.ppf(1e-3), dist.ppf(1 - 1e-3), 50)
        y_pdf = dist.pdf(x)
        self._Figure_ax_pdf.plot(x, y_pdf, c='k')
        self._Figure_ax_pdf.set_ylim(bottom=0)
        self._Figure_ax_pdf.tick_params(axis='both', direction='in', labelbottom=False)

        # --------
        # plot cdf
        # --------
        y_cdf = dist.cdf(x)
        self._Figure_ax_cdf.plot(x, y_cdf, c='k')
        self._Figure_ax_cdf.set_ylim(bottom=0)
        self._Figure_ax_cdf.set_yticks([0, 1])
        self._Figure_ax_cdf.tick_params(axis='both', direction='in')

        # -------------------------------------------------------------
        # highlight area under the pdf and cdf if `sample_value` exists
        # -------------------------------------------------------------
        if self.input_parameters['sample_value'] is not None:
            x_ = np.linspace(x[0], self.input_parameters['sample_value'], 50)
            y_pdf_, y_cdf_ = dist.pdf(x_), dist.cdf(x_)
            self._Figure_ax_pdf.fill_between(x_, y_pdf_, np.zeros_like(x_), facecolor='grey', interpolate=True)
            self._Figure_ax_cdf.fill_between(x_, y_cdf_, np.zeros_like(x_), facecolor='grey', interpolate=True)

        # ----------------------
        # finalise/format figure
        # ----------------------
        self._Figure.figure.tight_layout(pad=0.25)
        self._Figure.figure_canvas.draw()

        return True


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
