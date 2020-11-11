import numpy as np
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_travelling_fire_flux import heat_flux as travelling_fire_flux

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI import logger
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


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

    t_crit = (max(t_crit_array) - min(t_crit_array)) / 60.
    l_crit = s_fire * t_crit * 60.
    A_crit = l_crit * w

    return dict(
        time=t,
        heat_flux=heat_flux_,
        t_crit=t_crit,
        l_crit=l_crit,
        A_crit=A_crit,
    )


class App(AppBaseClass):
    app_id = '0614'
    app_name_short = 'Travelling\nfire\n(heat flux)'
    app_name_long = 'SFE Travelling fire (heat flux)'

    # Keys to match signature of `heat_flux_wrapper`
    symbols_inputs = dict(
        t_end=dict(description='<i>t<sub>end</sub></i>, fire time duration', unit='min', default=120.),
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
    symbols_outputs = dict(
        t_crit=dict(description='<i>t<sub>crit</sub></i>, critical heat flux duration', unit='min'),
        l_crit=dict(description='<i>l<sub>crit</sub></i>, critical heat flux length', unit='m'),
        A_crit=dict(description='<i>A<sub>crit</sub></i>, critical heat flux area', unit='m<sup>2</sup>'),
    )

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = PlotApp(parent=self, title='Travelling fire (heat flux) plot')
        self.TableApp = TableWindow(parent=self, window_title='Travelling fire (heat flux) results')
        self.__figure_ax = self.FigureApp.add_subplot()
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

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        for k, v in self.symbols_outputs.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_' + k, v['description'], v['unit'])
            getattr(self.ui, 'p2_out_'+k).setReadOnly(True)

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
            assert self.show_results_in_table()
            assert self.show_results_in_figure()
        except Exception as e:
            self.statusBar().showMessage(f'Unable to show results, {str(e)}')
            logger.error(f'Unable to show results, {str(e)}')

        self.statusBar().showMessage('Calculation complete')

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [
            [float(i), float(j)] for i, j in zip(output_parameters['time'], output_parameters['heat_flux'])
        ]

        self.TableApp.update_table_content(
            content_data=list_content,
            col_headers=['time [s]', 'heat flux [kW]'],
        )
        self.TableApp.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters
        input_parameters = self.input_parameters

        self.__figure_ax.clear()
        self.__figure_ax.plot(output_parameters['time'] / 60., output_parameters['heat_flux'], c='k')
        self.__figure_ax.axhline(input_parameters['q_crit'], c='r', ls='--')
        self.__figure_ax.set_xlabel('Time [minute]', fontsize='small')
        self.__figure_ax.set_ylabel('Heat flux [kW]', fontsize='small')
        self.__figure_ax.tick_params(axis='both', labelsize='small')
        self.__figure_ax.grid(which='major', linestyle=':', linewidth='0.5', color='black')

        self.FigureApp.show()
        self.FigureApp.refresh_figure()

        return True

    @staticmethod
    def num2str(num):
        if isinstance(num, int):
            return f'{num:g}'
        elif isinstance(num, float):
            return f'{num:.3f}'.rstrip('0').rstrip('.')
        elif isinstance(num, str):
            return num
        elif num is None:
            return ''
        else:
            return str(num)


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
