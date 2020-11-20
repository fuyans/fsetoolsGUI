import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.libstd.bs_en_1991_1_2_2002_annex_a import appendix_a_parametric_fire

from fsetoolsGUI.gui.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.c0000_utilities import Counter
from fsetoolsGUI.gui.custom_plot_pyqtgraph import App as PlotApp


def bs_en_1991_1_2_parametric_fire(
        t_end: float,
        t_step: float,
        A_v: float,
        A_t: float,
        A_f: float,
        h_eq: float,
        q_fd: float,
        lambda_: float,
        rho: float,
        c: float,
        t_lim: float,
        temperature_initial: float,
):
    """

    :param t_end:
    :param t_step:
    :param A_v:
    :param A_t:
    :param A_f:
    :param h_eq:
    :param q_fd:
    :param lambda_:
    :param rho:
    :param c:
    :param t_lim:
    :param temperature_initial:
    :return:
    """
    t_end *= 60.  # min -> s
    q_fd *= 1e6  # MJ/m2 -> J/m2
    t_lim *= 60.  # min -> s
    temperature_initial += 273.15  # deg.C -> K

    t = np.arange(0, t_end + t_step / 2., t_step)

    T = appendix_a_parametric_fire(
        t=t,
        A_v=A_v,
        A_t=A_t,
        A_f=A_f,
        h_eq=h_eq,
        q_fd=q_fd,
        lambda_=lambda_,
        rho=rho,
        c=c,
        t_lim=t_lim,
        temperature_initial=temperature_initial,
    )

    return dict(time=t, temperature=T)


class App(AppBaseClass):
    app_id = '0610'
    app_name_short = 'BS EN 1991\nparametric\nfire'
    app_name_long = 'BS EN 1991-1-2:2002 Parametric fire'

    input_items = dict(
        t_end=dict(description='t<sub>end</sub>, duration', unit='min', default=180., tip='Fire duration'),
        t_step=dict(description='t<sub>step</sub>, time step', unit='s', default=10.),
        A_t=dict(description='A<sub>t</sub>, room total surface area', unit='m<sup>2</sup>', default=360),
        A_f=dict(description='Af, room floor area', unit='m<sup>2</sup>', default=100),
        A_v=dict(description='Av, ventilation area', unit='m<sup>2</sup>', default=36),
        h_eq=dict(description='heq, entilation opening height', unit='m', default=1),
        q_fd=dict(description='qfd, uel load density', unit='MJ/m<sup>2</sup>', default=600),
        lambda_=dict(description='lambda, ining thermal conductivity', unit='K/kg/m', default=1.13),
        rho=dict(description='Lining density', unit='kg/m<sup>3</sup>', default=2000),
        c=dict(description='Lining thermal heat capacity', unit='J/K/kg', default=1000),
        t_lim=dict(description='Limiting time t<sub>lim</sub>', unit='min', default=20),
        temperature_initial=dict(description='Initial temperature', unit='<sup>o</sup>C', default=20),
    )

    def __init__(self, parent=None, post_stats: bool = True):

        self.__input_parameters: dict = dict()
        self.__output_parameters: dict = dict()

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)
        self.FigureApp = PlotApp(parent=self, title='Parametric fire')
        self.__figure_ax = self.FigureApp.add_subplot(0, 0, x_label='Time [minute]', y_label='Temperature [°C]')

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.input_items.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_' + k, v['description'], v['unit'], min_width=70)

    def example(self):
        self.input_parameters = {k: v['default'] for k, v in self.input_items.items()}

    @property
    def input_parameters(self):

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        input_parameters = dict()
        for k, v in self.input_items.items():
            input_parameters[k] = str2float(getattr(self.ui, 'p2_in_' + k).text())

        try:
            self.__input_parameters.update(input_parameters)
        except TypeError:
            self.__input_parameters = input_parameters

        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v):

        for k, v_ in self.input_items.items():
            getattr(self.ui, 'p2_in_' + k).setText(self.num2str(v[k]))

    @property
    def output_parameters(self) -> dict:
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

    def ok(self):
        # parse inputs
        try:
            self.statusBar().showMessage('Parsing inputs from UI')
            self.repaint()
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input. {str(e)}')
            return

        # calculate
        try:
            self.statusBar().showMessage('Calculation started')
            self.repaint()
            self.output_parameters = bs_en_1991_1_2_parametric_fire(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error {str(e)}')
            return

        # outputs
        try:
            self.statusBar().showMessage('Preparing results')
            self.repaint()
            assert self.show_results_in_figure()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results. Error {str(e)}')

        self.statusBar().showMessage('Calculation complete')

    def show_results_in_figure(self):
        output_parameters = self.output_parameters
        self.__figure_ax.getPlotItem().clear()
        self.FigureApp.plot(output_parameters['time'] / 60, output_parameters['temperature'] - 273.15, ax=self.__figure_ax)
        self.FigureApp.show()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
