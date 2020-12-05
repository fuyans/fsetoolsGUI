import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_din_en_1991_1_2_parametric_fire import temperature

from fsetoolsGUI import logger
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.custom_plot_pyqtgraph import App as FigureApp
from fsetoolsGUI.gui.custom_utilities import Counter


def calculate_worker(
        t_end: float,
        t_step: float,
        A_w: float,
        h_w: float,
        A_t: float,
        A_f: float,
        t_alpha: float,
        b: float,
        q_x_d: float,
        gamma_fi: float,
        q_ref: float,
        alpha: float,
        q_pua: float,
        *_, **__,
):
    """
    A wrapper to `fsetools.lib.fse_din_en_1991_1_2_parametric_fire.temperature` to better interface with the GUI.
    Signature to match the keys of `App.symbols_inputs`
    Return dict keys to match the keys of `App.symbols.outputs`

    :param t_end: [min]
    :param t_step: [s]
    :param A_w: [m2]
    :param h_w: [m]
    :param A_t: [m2]
    :param A_f: [m2]
    :param t_alpha: [s]
    :param b: [J/m2/s0.5/K]
    :param q_x_d: [MJ/m2]
    :param gamma_fi: []
    :param q_ref: [MJ/m2]
    :param alpha: [kW/s2]
    :param q_pua: [MW/m2]
    :return heat_flux: [kW]
    """

    # Unit conversion
    t_end = t_end * 60.  # min -> s

    t = np.arange(0, t_end + t_step / 2., t_step)

    temperature_ = temperature(
        t_array_s=t,
        A_w_m2=A_w,
        h_w_m2=h_w,
        A_t_m2=A_t,
        A_f_m2=A_f,
        t_alpha_s=t_alpha,
        b_Jm2s05K=b,
        q_x_d_MJm2=q_x_d,
        gamma_fi_Q=gamma_fi,
        q_ref=q_ref,
        alpha=alpha,
        hrrpua_MWm2=q_pua,
    )

    return dict(
        time=t,
        temperature=temperature_,
    )


class App(AppBaseClass):
    app_id = '0613'
    app_name_short = 'DIN EN 1991\nparametric\nfire'
    app_name_long = 'DIN EN 1991-1-2:2002 Parametric fire'

    # Keys to match signature of `heat_flux_wrapper`
    symbols_inputs = dict(
        t_end=dict(description='<i>t<sub>end</sub></i>, fire time duration', unit='min', default=180.),
        t_step=dict(description='<i>t<sub>step</sub></i>, fire time step', unit='s', default=1.),
        A_w=dict(description='<i>A<sub>w</sub></i>, vent. area', unit='m<sup>2</sup>', default=37.),
        h_w=dict(description='<i>h<sub>w</sub></i>, vent. weight height', unit='m', default=2.),
        A_t=dict(description='<i>A<sub>t</sub></i>, room surface area', unit='m<sup>2</sup>', default=1312.),
        A_f=dict(description='<i>A<sub>f</sub></i>, floor area', unit='m', default=500.),
        t_alpha=dict(description='<i>t<sub>α</sub></i>, fire growth factor', unit='s', default=300.),
        b=dict(description='<i>b</i>, weight thermal capacity', unit='J/m<sup>2</sup>/s<sup>0.5</sup>/K', default=720.),
        q_x_d=dict(description='<i>q<sub>x,d</sub></i>, design fuel density', unit='MJ/m<sup>2</sup>', default=600.),
        gamma_fi=dict(description='<i>Γ<sub>fi</sub></i>, partial factor', unit='', default=1.0),
        q_ref=dict(description='<i>q<sub>ref</sub></i>, ref. max. HRR', unit='', default=1300.),
        alpha=dict(description='<i>α</i>, t-square fire growth', unit='kW/s<sup>2</sup>', default=0.0117),
        q_pua=dict(description='<i>q<sub>pua</sub></i>, HRR density', unit='MW/m<sup>2</sup>', default=0.25),
    )
    # Keys to match output keys of `heat_flux_wrapper`
    symbols_outputs = dict()

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = FigureApp(parent=self, title=self.app_name_long)
        self.__figure_ax = self.FigureApp.add_subplot(0, 0, x_label='Time [min]', y_label='Temperature [°C]')
        self.__output_parameters = dict(time=None, temperature=None)
        self.__input_parameters: dict = dict()
        self.__output_parameters: dict = dict()

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.symbols_inputs.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_' + k, v['description'], v['unit'], min_width=70)

        if self.symbols_outputs:
            self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
            for k, v in self.symbols_outputs.items():
                self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_' + k, v['description'], v['unit'])
                getattr(self.ui, 'p2_out_' + k).setReadOnly(True)

    def example(self):
        self.input_parameters = {k: v['default'] for k, v in self.symbols_inputs.items()}

    @property
    def input_parameters(self):

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================
        input_parameters = dict()
        for k, v in self.symbols_inputs.items():
            input_parameters[k] = str2float(getattr(self.ui, 'p2_in_' + k).text())

        try:
            self.__input_parameters.update(input_parameters)
        except TypeError:
            self.__input_parameters = input_parameters

        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v):
        for k, v_ in self.symbols_inputs.items():
            getattr(self.ui, 'p2_in_' + k).setText(self.num2str(v[k]))

    @property
    def output_parameters(self) -> dict:
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

        for k, v_ in self.symbols_outputs.items():
            getattr(self.ui, 'p2_out_' + k).setText(self.num2str(v[k]))

    def ok(self):
        # parse inputs from ui
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
            output_parameters = calculate_worker(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error {str(e)}')
            raise e

        # cast outputs to ui
        try:
            self.statusBar().showMessage('Preparing results')
            self.repaint()
            self.output_parameters = output_parameters
            self.show_results_in_figure()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results, {str(e)}')
            logger.error(f'Unable to show results, {str(e)}')

        self.statusBar().showMessage('Calculation complete')

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        self.__figure_ax.getPlotItem().clear()
        self.FigureApp.plot(output_parameters['time'] / 60., output_parameters['temperature'] - 273.15)
        self.FigureApp.show()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
