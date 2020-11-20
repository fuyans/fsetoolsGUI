import numpy as np
import pyqtgraph as pg
import scipy.stats as stats
from PySide2.QtCore import Signal, Slot, QObject, Qt
from PySide2.QtWidgets import QGridLayout, QLineEdit, QLabel, QPushButton, QDialog, QRadioButton

from fsetoolsGUI import logger
from fsetoolsGUI.etc.probability_distribution import solve_dist_for_mean_std
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import *
from fsetoolsGUI.gui.logic.custom_plot_pyqtgraph import App as FigureApp


class Signals(QObject):
    __upon_distribution_selection = Signal(int)

    @property
    def upon_distribution_selection(self):
        return self.__upon_distribution_selection


class GridDialog(QDialog):
    def __init__(
            self,
            labels: list,
            grid_shape: tuple = None,
            parent=None,
            window_title=None,
            signal_upon_selection: Signal = None):

        self.labels = labels
        self.signal_upon_selection = signal_upon_selection

        super().__init__(parent=parent)

        # disable help
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # disable resize
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)

        if grid_shape is None:
            grid_shape = (len(labels), 1)

        if window_title:
            self.setWindowTitle(window_title)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.radio_buttons = list()
        loop_count = 0
        for j in range(grid_shape[1]):
            for i in range(grid_shape[0]):
                # create button
                self.radio_buttons.append(QRadioButton(labels[loop_count]))
                self.radio_buttons[-1].released.connect(lambda x=loop_count: self.emit_selected_index(x))
                # add to layout
                grid_layout.addWidget(self.radio_buttons[-1], i, j)

                loop_count += 1
                if loop_count >= len(labels):
                    break

            if loop_count >= len(labels):
                break

        self.adjustSize()
        self.setFixedWidth(self.width())
        self.setFixedHeight(self.height())

    def emit_selected_index(self, selected_index: int):
        if self.signal_upon_selection:
            self.signal_upon_selection.emit(selected_index)


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

        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = FigureApp(parent=self, title='Distribution', antialias=True)
        self.__figure_ax_pdf = self.FigureApp.add_subplot(row=0, col=0, x_label='Sample value', y_label='PDF')
        self.__figure_ax_cdf = self.FigureApp.add_subplot(row=1, col=0, x_label='Sample value', y_label='CDF')
        self.__figure_ax_cdf.setXLink(self.__figure_ax_pdf)

        self.__input_parameters = None
        self.__output_parameters = None
        self.signals = Signals()

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('Distribution'), c.value, 0, 1, 1)
        self.ui.p2_in_distribution = QLineEdit()
        self.ui.p2_layout.addWidget(self.ui.p2_in_distribution, c.value, 1, 1, 1)
        self.ui.p2_in_fp_inputs = QPushButton('...')
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

        # Step 4. Make plots
        try:
            self.show_results_in_figure_2()
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

    def __cdf_value_change(self):
        """Called upon change of CDF value in the output parameters"""
        cdf_value = self.input_parameters['cdf_value']
        dist = self.output_parameters['dist']
        sample_value = dist.ppf(cdf_value)
        self.ui.p2_in_sample_value.textChanged.disconnect()
        self.ui.p2_in_sample_value.setText(f'{sample_value:.5g}')
        self.ui.p2_in_sample_value.textChanged.connect(self.__sample_value_change)

    def __sample_value_change(self):
        """Called upon change of sample value in the output parameters"""
        sample_value = self.input_parameters['sample_value']
        dist = self.output_parameters['dist']
        cdf_value = dist.cdf(sample_value)
        self.ui.p2_in_cdf.textChanged.disconnect()
        self.ui.p2_in_cdf.setText(f'{cdf_value:.5g}')
        self.ui.p2_in_cdf.textChanged.connect(self.__cdf_value_change)

    def __distribution_update(self):
        """Called upon change of distribution type"""

        # Clear plots
        if self.__figure_ax_pdf is not None and self.__figure_ax_cdf is not None:
            self.__figure_ax_pdf.getPlotItem().clear()
            self.__figure_ax_cdf.getPlotItem().clear()

        # clear outputs
        if self.ui.p2_in_cdf.text() != '':
            self.ui.p2_in_cdf.textChanged.disconnect()
            self.ui.p2_in_cdf.clear()
            self.ui.p2_in_cdf.textChanged.connect(self.__cdf_value_change)
        if self.ui.p2_in_sample_value.text() != '':
            self.ui.p2_in_sample_value.textChanged.disconnect()
            self.ui.p2_in_sample_value.clear()
            self.ui.p2_in_sample_value.textChanged.connect(self.__sample_value_change)

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

    def show_results_in_figure_2(self):
        dist = self.output_parameters['dist']

        self.__figure_ax_pdf.getPlotItem().clear()
        self.__figure_ax_cdf.getPlotItem().clear()

        # --------
        # plot pdf
        # --------
        x = np.linspace(dist.ppf(1e-3), dist.ppf(1 - 1e-3), 50)
        y_pdf = dist.pdf(x)
        self.FigureApp.plot(x, y_pdf, self.__figure_ax_pdf)

        # --------
        # plot cdf
        # --------
        y_cdf = dist.cdf(x)
        self.FigureApp.plot(x, y_cdf, self.__figure_ax_cdf)

        # -------------------------------------------------------------
        # highlight area under the pdf and cdf if `sample_value` exists
        # -------------------------------------------------------------
        if self.input_parameters['sample_value'] is not None:
            x_ = np.linspace(x[0], self.input_parameters['sample_value'], 50)
            y_ = np.zeros_like(x_)
            y_pdf_, y_cdf_ = dist.pdf(x_), dist.cdf(x_)

            fill_pdf = pg.FillBetweenItem(
                self.FigureApp.plot(x_, y_pdf_, ax=self.__figure_ax_pdf, pen_width=0, pen_colour=(0, 0, 0, 1)),
                self.FigureApp.plot(x_, y_, ax=self.__figure_ax_pdf, pen_width=0, pen_colour=(0, 0, 0, 1)),
                brush=0.8
            )
            self.__figure_ax_pdf.addItem(fill_pdf)

            fill_cdf = pg.FillBetweenItem(
                self.FigureApp.plot(x_, y_cdf_, ax=self.__figure_ax_cdf, pen_width=0, pen_colour=(0, 0, 0, 1)),
                self.FigureApp.plot(x_, y_, ax=self.__figure_ax_cdf, pen_width=0, pen_colour=(0, 0, 0, 1)),
                brush=0.8
            )
            self.__figure_ax_cdf.addItem(fill_cdf)

        self.FigureApp.show()


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
