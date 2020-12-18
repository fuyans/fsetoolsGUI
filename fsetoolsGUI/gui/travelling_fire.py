from collections import OrderedDict

import numpy as np
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_travelling_fire import temperature_si as fire_temperature_si

from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.bases.custom_plot_pyqtgraph import App as FigureApp
from fsetoolsGUI.gui.bases.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0611'
    app_name_short = 'Travelling\nfire'
    app_name_long = 'SFE Travelling fire'

    __input_symbols: OrderedDict = OrderedDict(
        fire_time_duration=['Duration', 'min'],
        fire_time_step=['Time step', 's'],
        fire_load_density_MJm2=['Fuel load density', 'MJ/m<sup>2</sup>'],
        fire_hrr_density_MWm2=['HRR density', 'MW/m<sup>2</sup>'],
        room_length_m=['Room length', 'm'],
        room_width_m=['Room width', 'm'],
        fire_spread_rate_ms=['Fire spread speed', 'm/s'],
        beam_location_height_m=['Beam height', 'm'],
        beam_location_length_m=['Beam length', 'm'],
        fire_nft_limit_c=['Near field temp.', '<sup>o</sup>C'],
    )

    def __init__(self, parent=None, post_stats: bool = True):
        # instantiation
        super().__init__(parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        self.FigureApp = FigureApp(parent=self, title='Travelling fire')
        self.__figure_ax = self.FigureApp.add_subplot(0, 0, x_label='Time [minute]', y_label='Temperature [°C]')
        self.__output_parameters = None

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.__input_symbols.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c, f'p2_in_{k}', v[0], v[1])

    def example(self):
        input_kwargs = dict(
            fire_time_duration=180,
            fire_time_step=1,
            fire_load_density_MJm2=500,
            fire_hrr_density_MWm2=0.25,
            room_length_m=100,
            room_width_m=20,
            fire_spread_rate_ms=0.012,
            beam_location_height_m=3,
            beam_location_length_m=80,
            fire_nft_limit_c=1200)
        self.input_parameters = input_kwargs

    def submit(self):
        self.output_parameters = self.calculate(self.input_parameters)
        self.show_results_in_figure()

    @staticmethod
    def calculate(
            input_parameters
    ):
        input_parameters.pop('fire_time_duration')
        input_parameters.pop('fire_time_step')

        temperature = fire_temperature_si(
            t=input_parameters['t'],
            T_0=293.15,
            q_fd=input_parameters['fire_load_density_MJm2'] * 1e6,
            hrrpua=input_parameters['fire_hrr_density_MWm2'] * 1e6,
            l=input_parameters['room_length_m'],
            w=input_parameters['room_width_m'],
            s=input_parameters['fire_spread_rate_ms'],
            e_h=input_parameters['beam_location_height_m'],
            e_l=input_parameters['beam_location_length_m'],
            T_max=input_parameters['fire_nft_limit_c'] + 273.15,
        )

        return dict(
            time=input_parameters['t'],
            temperature=temperature,
        )

    @property
    def input_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        input_parameters = {k: str2float(getattr(self.ui, f'p2_in_{k}').text()) for k in list(self.__input_symbols.keys())}
        input_parameters['t'] = np.arange(0, input_parameters['fire_time_duration'] * 60, input_parameters['fire_time_step'])
        return input_parameters

    @input_parameters.setter
    def input_parameters(self, v: dict):
        def float2str(num: float):
            if num is None:
                return ''
            else:
                return f'{num:g}'

        for k, v_ in v.items():
            getattr(self.ui, f'p2_in_{k}').setText(float2str(v_))

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

    def show_results_in_figure(self):
        output_parameters = self.output_parameters

        self.__figure_ax.getPlotItem().clear()
        self.FigureApp.plot(output_parameters['time'] / 60, output_parameters['temperature'] - 273.15, ax=self.__figure_ax, name='Fire')
        self.FigureApp.show()


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
