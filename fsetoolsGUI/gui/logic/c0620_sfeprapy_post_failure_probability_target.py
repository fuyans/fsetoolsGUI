import numpy as np
from PySide2 import QtWidgets, QtCore
from fsetools.libstd.ec_1991_1_2 import appendix_a_parametric_fire
from os import path

from fsetoolsGUI.gui.layout.i0611_parametric_fire import Ui_MainWindow
from fsetoolsGUI.gui.logic.c0000_app_template_old import QMainWindow
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_tableview import TableWindow


class App(QMainWindow):
    __output_fire_curve = dict(
        time=None,
        temperature=None
    )
    __Table = None
    __Figure = None
    __Figure_ax = None

    def __init__(self, parent=None):
        module_id = '0611'

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(
            module_id=module_id,
            parent=parent,
            shortcut_Return=self.calculate,
            freeze_window_size=True,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # =======================
        # lineEdit default values
        # =======================
        self.ui.lineEdit_in_initial_temperature.setText('20')

        # =================
        # lineEdit tip text
        # =================
        self.ui.lineEdit_in_duration.setToolTip('Fire duration')
        self.ui.lineEdit_in_room_total_surface_area.setToolTip('Room total interior surface area, including opening')
        self.ui.lineEdit_in_room_floor_area.setToolTip('Room floor area')
        self.ui.lineEdit_in_ventilation_area.setToolTip('Room ventilation opening area')
        self.ui.lineEdit_in_ventilation_opening_height.setToolTip('Room ventilation opening weighted height')
        self.ui.lineEdit_in_fuel_density.setToolTip('Fuel load density')
        self.ui.lineEdit_in_lining_thermal_conductivity.setToolTip('Room wall/ceiling thermal conductivity')
        self.ui.lineEdit_in_lining_density.setToolTip('Room wall/ceiling density')
        self.ui.lineEdit_in_lining_thermal_heat_capacity.setToolTip('Room wall/ceiling heat capacity')
        self.ui.lineEdit_in_fire_limiting_time.setToolTip('Associated with fire growth rate.\n'
                                                          'Slow: 25 minutes\n'
                                                          'Medium: 20 minutes\nFast: 15 minutes')
        self.ui.lineEdit_in_initial_temperature.setToolTip('Initial or ambient temperature')

        # signals
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)

    def example(self):

        self.input_parameters = dict(
            room_total_surface_area=360,
            room_floor_area=100,
            ventilation_area=36,
            ventilation_opening_height=1,
            fuel_density=600e6,
            lining_thermal_conductivity=1.13,
            lining_density=2000,
            lining_thermal_heat_capacity=1000,
            fire_limiting_time=20 * 60,
            duration=2 * 60 * 60,
            initial_temperature=293.15,
        )

        self.repaint()

    @property
    def input_parameters(self):
        return

    @input_parameters.setter
    def input_parameters(self, v):
        pass

    @property
    def output_parameters(self):
        return

    @output_parameters.setter
    def output_parameters(self, v):
        pass

    @staticmethod
    def prepare_data(fp_data_csv: str):

        path_teq_csv = fp_data_csv
        with open(path_teq_csv, 'r') as f:
            header = f.readline()
        data = np.genfromtxt(fp_data_csv, skip_header=1, delimiter=',')

        print(header, '\n', data[0])
        # mcs_out = pd.read_csv(path_teq_csv)
        #
        # list_case_name = sorted(list(set(mcs_out["case_name"].values)))
        # list_t_eq = list()
        # list_weight = list()
        # list_n_simulation = list()
        # for case_name in list_case_name:
        #     teq = np.asarray(
        #         mcs_out[mcs_out["case_name"] == case_name][
        #             "solver_time_equivalence_solved"
        #         ].values,
        #         float,
        #     )
        #     teq[teq == np.inf] = np.max(teq[teq != np.inf])
        #     teq[teq == -np.inf] = np.min(teq[teq != -np.inf])
        #     teq = teq[~np.isnan(teq)]
        #     teq[teq > 18000.0] = 18000.0  # limit maximum time equivalence plot value to 5 hours
        #     list_t_eq.append(teq / 60.0)
        #     list_weight.append(
        #         np.average(
        #             mcs_out[mcs_out["case_name"] == case_name]["probability_weight"].values
        #         )
        #     )
        #     list_n_simulation.append(
        #         np.average(
        #             mcs_out[mcs_out["case_name"] == case_name]["n_simulations"].values
        #         )
        #     )

    def calculate(self):
        pass

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [[float(i), float(j)] for i, j in
                        zip(output_parameters['time'], output_parameters['temperature'])]

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
            header_col=['time [s]', 'temperature [K]'],
            window_title='Parametric fire numerical results',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Parametric fire plot')
            self.__Figure_ax = self.__Figure.add_subplots()
        else:
            self.__Figure_ax.clear()

        self.__Figure_ax.plot(output_parameters['time'] / 60, output_parameters['temperature'], c='k')
        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Temperature [°C]')
        self.__Figure.figure.tight_layout()

        self.__Figure.figure_canvas.draw()
        self.__Figure.show()

        return True


if __name__ == "__main__":
    # import sys
    #
    # qapp = QtWidgets.QApplication(sys.argv)
    # app = App()
    # app.show()
    # qapp.exec_()

    fp = r'C:\Users\ian\Downloads\mcs.out.csv'
    fp = path.realpath(fp)
    App.prepare_data(fp)
