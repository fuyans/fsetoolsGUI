from collections import OrderedDict

import numpy as np
from PySide2 import QtCore
from PySide2.QtWidgets import QGridLayout, QLabel
from fsetools.lib.fse_bs_en_1993_1_2_heat_transfer_c import protected_steel_eurocode
from sfeprapy.mcs0.mcs0_calc import solve_time_equivalence

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI.gui.logic.c0610_travelling_fire import App as AppTravellingFire
from fsetoolsGUI.gui.logic.c0611_ec_parametric_fire import App as AppParametricFire
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0612'
    app_name_short = 'EC\nHT\nprotected'
    app_name_long = 'BS EN 1993-1-2 Protected steel heat transfer'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.__fire = [AppParametricFire(self, post_stats=False), AppTravellingFire(self, post_stats=False)]

        self.input_symbols: OrderedDict = OrderedDict(
            beam_rho=['Steel density', 'kg/m<sup>3</sup>'],
            beam_cross_section_area=['Steel section area', 'm<sup>2</sup>'],
            protection_protected_perimeter=['Steel section protected perimeter', 'm'],
            protection_k=['Protection conductivity', 'W/m/K'],
            protection_rho=['Protection density', 'kg/m<sup>3</sup>'],
            protection_c=['Protection conductivity', 'J/K/kg'],
            protection_thickness=['Protection thickness', 'mm'],
        )
        self.output_symbols: OrderedDict = OrderedDict(
            steel_max_temperature=['Max. steel temperature', '<sup>o</sup>C'],
            steel_max_temperature_time=['Max. steel time', 'min'],
            solved_protection_thickness=['Solved protection thickness', 'mm'],
            solved_time_equivalence=['Solved time equivalence', 'min'],
        )

        self.__Figure = None
        self.__Figure_ax = None
        self.__Table = None
        self.__output_parameters = None

        # ==============
        # instantiate ui
        # ==============

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_beam_critical_temperature', 'Solve for critical temp', '<sup>o</sup>C', label_obj='QCheckBox', min_width=70)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_fire_type', 'Fire type', 'Make', unit_obj='QPushButton')
        for k, v in self.input_symbols.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c, f'p2_in_{k}', v[0], v[1])
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        for k, v in self.output_symbols.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c, f'p2_in_{k}', v[0], v[1])

        # ==============
        # default values
        # ==============

        self.ui.p2_in_beam_critical_temperature.setEnabled(False)
        self.ui.p2_in_solved_protection_thickness.setEnabled(False)
        self.ui.p2_in_solved_time_equivalence.setEnabled(False)

        # =====================
        # set signals and slots
        # =====================

        def beam_critical_temperature():
            self.ui.p2_in_beam_critical_temperature.setEnabled(self.ui.p2_in_beam_critical_temperature_label.isChecked())
            self.ui.p2_in_protection_thickness.setEnabled(not self.ui.p2_in_beam_critical_temperature_label.isChecked())
            self.ui.p2_in_solved_protection_thickness.setEnabled(self.ui.p2_in_beam_critical_temperature_label.isChecked())
            self.ui.p2_in_solved_time_equivalence.setEnabled(self.ui.p2_in_beam_critical_temperature_label.isChecked())

        def make_fire(fire_type_: int):
            self.__fire[fire_type_].show()

        self.ui.p2_in_fire_type_unit.clicked.connect(lambda: make_fire(int(self.ui.p2_in_fire_type.text())))
        self.ui.p2_in_beam_critical_temperature_label.stateChanged.connect(beam_critical_temperature)

    def example(self):
        input_kwargs = dict(
            # solve_crit_temp_check=False,
            beam_critical_temperature=550,
            fire_type=0,
            beam_rho=7850,
            beam_cross_section_area=0.017,
            protection_k=0.2,
            protection_rho=800,
            protection_c=1700,
            protection_thickness=5,
            protection_protected_perimeter=2.14,
        )
        self.input_parameters = input_kwargs

    def ok(self):

        self.output_parameters = self.calculate(**self.input_parameters)
        self.show_results_in_table()
        self.show_results_in_figure()

    @staticmethod
    def calculate(
            fire_time,
            fire_temperature,
            beam_rho,
            beam_cross_section_area,
            protection_k,
            protection_rho,
            protection_c,
            protection_thickness,
            protection_protected_perimeter,
            terminate_when_cooling=False,
            solver_temperature_goal=None,
            solver_max_iter=20,
            solver_thickness_lbound=0.0001,
            solver_thickness_ubound=0.0500,
            solver_tol=1.0,
            *_,
            **__,
    ):
        if solver_temperature_goal:
            teq_output = solve_time_equivalence(
                fire_time=fire_time,
                fire_temperature=fire_temperature,
                beam_cross_section_area=beam_cross_section_area,
                beam_rho=beam_rho,
                protection_k=protection_k,
                protection_rho=protection_rho,
                protection_c=protection_c,
                protection_protected_perimeter=protection_protected_perimeter,
                fire_time_iso834=fire_time,
                fire_temperature_iso834=(345.0 * np.log10((fire_time / 60.0) * 8.0 + 1.0) + 20.0) + 273.15,  # in [K],
                solver_temperature_goal=solver_temperature_goal,
                solver_max_iter=solver_max_iter,
                solver_thickness_ubound=solver_thickness_ubound,
                solver_thickness_lbound=solver_thickness_lbound,
                solver_tol=solver_tol,
                phi_teq=1
            )

            if not teq_output['solver_convergence_status']:
                raise ValueError('No convergence')

            protection_thickness = teq_output['solver_protection_thickness']
            time_equivalence = teq_output['solver_time_equivalence_solved']
        else:
            time_equivalence = 0

        steel_temperature = protected_steel_eurocode(
            fire_time=fire_time,
            fire_temperature=fire_temperature,
            beam_rho=beam_rho,
            beam_cross_section_area=beam_cross_section_area,
            protection_k=protection_k,
            protection_rho=protection_rho,
            protection_c=protection_c,
            protection_thickness=protection_thickness,
            protection_protected_perimeter=protection_protected_perimeter,
            terminate_when_cooling=terminate_when_cooling,
        )

        return dict(
            time=fire_time,
            fire_temperature=fire_temperature,
            steel_temperature=np.array(steel_temperature),
            steel_max_temperature=np.amax(steel_temperature),
            steel_max_temperature_time=fire_time[np.argmax(steel_temperature)],
            time_equivalence=time_equivalence,
            protection_thickness=protection_thickness,
        )

    @property
    def input_parameters(self):
        def str2float(v: str):
            try:
                return float(v)
            except ValueError:
                return None

        input_parameters = {k: str2float(getattr(self.ui, f'p2_in_{k}').text()) for k in list(self.input_symbols.keys())}
        input_parameters['fire_type'] = int(self.ui.p2_in_fire_type.text())

        fire_output = self.__fire[input_parameters['fire_type']].output_parameters

        input_parameters['fire_time'] = fire_output['time']
        input_parameters['fire_temperature'] = fire_output['temperature']

        if self.ui.p2_in_beam_critical_temperature_label.isChecked():
            input_parameters['solver_temperature_goal'] = str2float(self.ui.p2_in_beam_critical_temperature.text()) + 273.15
        else:
            input_parameters['solver_temperature_goal'] = None

        input_parameters['protection_thickness'] = input_parameters['protection_thickness'] / 1000

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

        def float2str(v_):
            try:
                return f'{v_:.2f}'
            except ValueError:
                return ''

        self.ui.p2_in_steel_max_temperature.setText(float2str(v['steel_max_temperature'] - 273.15))
        self.ui.p2_in_steel_max_temperature_time.setText(float2str(v['steel_max_temperature_time'] / 60))

        if self.ui.p2_in_beam_critical_temperature_label.isChecked():
            self.ui.p2_in_solved_protection_thickness.setText(float2str(v['protection_thickness'] * 1000))
            self.ui.p2_in_solved_time_equivalence.setText(float2str(v['time_equivalence'] / 60))

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        ijk = zip(output_parameters['time'], output_parameters['fire_temperature'] - 273.15, output_parameters['steel_temperature'] - 273.15)
        list_content = [[float(i), float(j), float(k)] for i, j, k in ijk]

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
            header_col=['Time [°C]', 'Fire temperature [°C]', 'Steep temperature [°C]'],
            window_title='Steel temperature',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Steel temperature plot')
            self.__Figure_ax = self.__Figure.add_subplots()
        else:
            self.__Figure_ax.clear()

        self.__Figure_ax.plot(output_parameters['time'] / 60, output_parameters['fire_temperature'] - 273.15, label='Fire', c='r')
        self.__Figure_ax.plot(output_parameters['time'] / 60, output_parameters['steel_temperature'] - 273.15, label='Steel', c='k')
        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Temperature [°C]')
        self.__Figure.figure.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='small').set_visible(True)
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
