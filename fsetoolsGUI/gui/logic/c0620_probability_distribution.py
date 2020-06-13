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


class App0620(QMainWindow):

    def __init__(self, parent=None, mode=None):

        self.__input_parameters = None
        self.__output_parameters = None
        self.__fig = None
        self.__ax_pdf = None
        self.__ax_cdf = None

        super().__init__(
            parent=parent,
            module_id='0620',
            mode=mode
        )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # instantiate figure and associated objects

        self.__fig = plt.figure()
        self.__fig.set_facecolor('None')
        self.figure_canvas = FigureCanvas(self.__fig)
        self.figure_canvas.setStyleSheet("background-color:transparent;border:0px")  # set background transparent.
        self.ui.frame_layout.addWidget(self.figure_canvas)
        # self.toolbar = NavigationToolbar(self.figure_canvas, self)
        # self.ui.frame_layout.addWidget(self.toolbar)

        self.ui.lineEdit_in_cdf.textChanged.connect(self.__cdf_value_change)
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.__sample_value_change)

        self.ui.lineEdit_in_distribution.textChanged.connect(self.__distribution_update)
        self.ui.lineEdit_in_mean.textChanged.connect(self.__distribution_update)
        self.ui.lineEdit_in_sd.textChanged.connect(self.__distribution_update)

        self.ui.lineEdit_in_sample_value.setEnabled(False)
        self.ui.lineEdit_in_cdf.setEnabled(False)

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
        self.ui.lineEdit_in_sample_value.setText(f'{sample_value:.5g}'.rstrip('0').rstrip('.'))
        self.ui.lineEdit_in_sample_value.textChanged.connect(self.__sample_value_change)

    def __sample_value_change(self):

        sample_value = self.input_parameters['sample_value']
        dist = self.output_parameters['dist']

        cdf_value = dist.cdf(sample_value)

        self.ui.lineEdit_in_cdf.textChanged.disconnect()
        self.ui.lineEdit_in_cdf.setText(f'{cdf_value:.5g}'.rstrip('0').rstrip('.'))
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
        if self.__ax_pdf is None:
            ax_pdf = self.figure.add_subplot(211)
            ax_pdf.set_xticklabels([])
            ax_pdf.tick_params(axis='both', which='both', labelsize=8)
            self.__ax_pdf = ax_pdf

        if self.__ax_cdf is None:
            ax_cdf = self.figure.add_subplot(212, sharex=self.__ax_pdf)
            ax_cdf.tick_params(axis='both', which='both', labelsize=8)
            self.__ax_cdf = ax_cdf

        x = np.linspace(dist.ppf(1e-3), dist.ppf(1 - 1e-3), 100)
        y_pdf = dist.pdf(x)
        y_cdf = dist.cdf(x)
        self.__ax_pdf.clear()
        self.__ax_pdf.plot(x, y_pdf, c='k')
        self.__ax_pdf.tick_params(axis='both', direction='in', labelbottom=False)

        self.__ax_cdf.clear()
        self.__ax_cdf.plot(x, y_cdf, c='k')
        self.__ax_cdf.set_ylim(0, 1.1)
        self.__ax_cdf.set_yticks([0, 1])
        self.__ax_cdf.tick_params(axis='both', direction='in')

        self.figure.tight_layout(pad=0.1)
        self.figure_canvas.draw()

        # -------------------------
        # assign to object property
        # -------------------------
        self.__output_parameters = output_parameters_


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0620(mode=-1)
    app.show()

    # ax = app.add_subplots()
    # ax.plot([0, 1], [0, 1])

    qapp.exec_()
