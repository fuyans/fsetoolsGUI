import numpy as np
import pyqtgraph as pg
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_travelling_fire_flux import heat_flux as travelling_fire_flux

from fsetoolsGUI import logger
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.custom_utilities import Counter
from fsetoolsGUI.gui.custom_plot_pyqtgraph import App as PlotApp2


def calculate_worker(
        t_end: float,
        t_step: float,
        Q_fd: float,
        q_pua: float,
        l: float,
        w: float,
        s_fire: float,
        e_h: float,
        e_l: float,
        q_lim: float,
        q_crit: float,
        *_, **__,
):
    """
    A wrapper to `fsetools.lib.fse_travelling_fire_flux.heat_flux` to better interface with the GUI.
    Signature to match the keys of `App.symbols_inputs`
    Return dict keys to match the keys of `App.symbols.outputs`

    :param t_end: [min]
    :param t_step: [s]
    :param Q_fd: [MJ/m2]
    :param q_pua: [MW/m2]
    :param l: [m]
    :param w: [m]
    :param s_fire: [m/s]
    :param e_h: [m]
    :param e_l: [m]
    :param q_lim: [kW]
    :return heat_flux: [kW]
    """

    # Unit conversion
    t_end = t_end * 60.  # min -> s

    t = np.arange(0, t_end + t_step / 2., t_step)

    heat_flux_ = travelling_fire_flux(
        t=t,
        fire_load_density_MJm2=Q_fd,
        fire_hrr_density_MWm2=q_pua,
        room_length_m=l,
        room_width_m=w,
        fire_spread_rate_ms=s_fire,
        beam_location_height_m=e_h,
        beam_location_length_m=e_l,
        fire_nff_limit_kW=q_lim,
    )

    t_crit_array = t[heat_flux_ >= q_crit]
    t_1 = min(t_crit_array)
    t_2 = max(t_crit_array)

    t_crit = (t_2 - t_1) / 60.
    l_crit = s_fire * t_crit * 60.
    A_crit = l_crit * w

    return dict(
        time=t,
        heat_flux=heat_flux_,
        t_crit=t_crit,
        l_crit=l_crit,
        A_crit=A_crit,
        t_1=t_1,
        t_2=t_2,
    )


class App(AppBaseClass):
    app_id = '0614'
    app_name_short = 'Travelling\nfire\n(heat flux)'
    app_name_long = 'SFE Travelling fire (heat flux)'

    __pen_q_crit = pg.mkPen(color=(251, 128, 114), style=QtCore.Qt.DashLine, width=2)  # pen for drawing critical heat flux in figure

    # Keys to match signature of `heat_flux_wrapper`
    input_items = dict(
        t_end=dict(description='<i>t<sub>end</sub></i>, fire time duration', unit='min', default=75.),
        t_step=dict(description='<i>t<sub>step</sub></i>, fire time step', unit='s', default=1.),
        Q_fd=dict(description='<i>Q<sub>fd</sub></i>, fuel load density', unit='MJ/m<sup>2</sup>', default=780.),
        q_pua=dict(description='<i>q<sub>pua</sub></i>, heat release rate density', unit='MW/m<sup>2</sup>', default=0.5),
        l=dict(description='<i>l</i>, room depth', unit='m', default=40),
        w=dict(description='<i>w</i>, room breadth', unit='m', default=16),
        s_fire=dict(description='<i>s<sub>fire</sub></i>, fire spread speed', unit='m/s', default=0.018),
        e_h=dict(description='<i>e<sub>h</sub></i>, beam vertical location', unit='m', default=3.),
        e_l=dict(description='<i>e<sub>l</sub></i>, beam horizontal location', unit='m', default=24.),
        q_lim=dict(description='<i>q<sub>lim</sub></i>, max. near field heat flux', unit='kW', default=120.),
        q_crit=dict(description='<i>q<sub>crit</sub></i>, critical heat flux', unit='kW', default=12.6),
    )
    # Keys to match output keys of `heat_flux_wrapper`
    output_items = dict(
        t_crit=dict(description='<i>t<sub>crit</sub></i>, critical heat flux duration', unit='min'),
        l_crit=dict(description='<i>l<sub>crit</sub></i>, critical heat flux length', unit='m'),
        A_crit=dict(description='<i>A<sub>crit</sub></i>, critical heat flux area', unit='m<sup>2</sup>'),
    )

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.__input_parameters: dict = dict()
        self.__output_parameters: dict = dict()

        self.FigureApp = PlotApp2(parent=self, title='Travelling fire (heat flux)')
        self.__figure_ax = self.FigureApp.add_subplot(0, 0, x_label='Time [min]', y_label='Heat flux [kW]')

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.input_items.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_' + k, v['description'], v['unit'], min_width=70)

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        for k, v in self.output_items.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_' + k, v['description'], v['unit'])
            getattr(self.ui, 'p2_out_' + k).setReadOnly(True)

    def example(self):
        self.input_parameters = {k: v['default'] for k, v in self.input_items.items()}

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

        for k, v_ in self.output_items.items():
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
            assert self.show_results_in_figure()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results, {str(e)}')
            logger.error(f'Unable to show results, {str(e)}')

        self.statusBar().showMessage('Calculation complete')

    def show_results_in_figure(self):
        output_parameters = self.output_parameters
        input_parameters = self.input_parameters
        self.__figure_ax.getPlotItem().clear()
        self.FigureApp.plot(output_parameters['time'] / 60., output_parameters['heat_flux'])
        self.FigureApp.plot([output_parameters[i] / 60. for i in ['t_1', 't_2']], [input_parameters[i] for i in ['q_crit', 'q_crit']], pen=self.__pen_q_crit)
        self.FigureApp.show()

        return True


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
