from collections import OrderedDict

import numpy as np
from PySide2 import QtCore
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_travelling_fire import temperature_si as fire_temperature_si

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0611'
    app_name_short = 'Travelling\nfire'
    app_name_long = 'Travelling fire'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.input_symbols: OrderedDict = OrderedDict(
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

        self.__Figure = None
        self.__Figure_ax = None
        self.__Table = None
        self.__output_parameters = None

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        for k, v in self.input_symbols.items():
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

    def ok(self):
        self.output_parameters = self.calculate(self.input_parameters)
        self.show_results_in_table()
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
            # temperature=fire(**input_parameters),
            temperature=temperature,
        )

    @property
    def input_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        input_parameters = {k: str2float(getattr(self.ui, f'p2_in_{k}').text()) for k in list(self.input_symbols.keys())}
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

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [
            [float(i), float(j)] for i, j in zip(output_parameters['time'], output_parameters['temperature'] - 273.15)
        ]

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError as e:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=['time [s]', 'temperature [°C]'],
            window_title='Travelling fire numerical results',
        )

        self.activated_dialogs.append(self.__Table)

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Travelling fire plot')
            self.__Figure_ax = self.__Figure.add_subplots()
            self.activated_dialogs.append(self.__Figure)
        else:
            self.__Figure_ax.clear()

        self.__Figure_ax.plot(output_parameters['time'] / 60, output_parameters['temperature'] - 273.15, c='k')
        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Temperature [°C]')
        self.__Figure.figure.tight_layout()

        self.__Figure.figure_canvas.draw()
        self.__Figure.show()

        return True


if __name__ == '__main__':
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
