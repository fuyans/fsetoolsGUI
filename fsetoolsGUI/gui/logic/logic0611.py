import numpy as np
from PySide2 import QtWidgets, QtCore
from fsetools.libstd.ec_1991_1_2 import appendix_a_parametric_fire

from fsetoolsGUI.gui.layout.ui0611_parametric_fire import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_tableview import TableWindow


class App0611(QMainWindow):
    __output_fire_curve = dict(
        time=None,
        temperature=None
    )

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

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================
        duration = str2float(self.ui.lineEdit_in_duration.text())
        room_total_surface_area = str2float(self.ui.lineEdit_in_room_total_surface_area.text())
        room_floor_area = str2float(self.ui.lineEdit_in_room_floor_area.text())
        ventilation_area = str2float(self.ui.lineEdit_in_ventilation_area.text())
        ventilation_opening_height = str2float(self.ui.lineEdit_in_ventilation_opening_height.text())
        fuel_density = str2float(self.ui.lineEdit_in_fuel_density.text())
        lining_thermal_conductivity = str2float(self.ui.lineEdit_in_lining_thermal_conductivity.text())
        lining_density = str2float(self.ui.lineEdit_in_lining_density.text())
        lining_thermal_heat_capacity = str2float(self.ui.lineEdit_in_lining_thermal_heat_capacity.text())
        fire_limiting_time = str2float(self.ui.lineEdit_in_fire_limiting_time.text())
        initial_temperature = str2float(self.ui.lineEdit_in_initial_temperature.text())

        # ======================================================
        # check if necessary inputs are provided for calculation
        # ======================================================
        try:
            assert all([i is not None for i in [
                duration, room_total_surface_area, room_floor_area, ventilation_area, ventilation_opening_height,
                fuel_density, lining_thermal_conductivity, lining_thermal_heat_capacity, fire_limiting_time,
                initial_temperature
            ]])
        except AssertionError:
            raise ValueError('Not enough input parameters to compute')

        # ==============================
        # validate individual parameters
        # ==============================
        self.validate(duration, 'unsigned float', 'Fire duration must be a positive number')
        self.validate(room_total_surface_area, 'unsigned float', 'Room total surface area must be a positive number')
        self.validate(room_floor_area, 'unsigned float', 'Room floor area must be a positive number')
        self.validate(ventilation_area, 'unsigned float', 'Ventilation opening area must be a positive number')
        self.validate(ventilation_opening_height, 'unsigned float',
                      'Ventilation opening height must be a positive number')
        self.validate(fuel_density, 'unsigned float', 'Fuel density must be a positive number')
        self.validate(lining_thermal_conductivity, 'unsigned float',
                      'Lining thermal conductivity must be a positive number')
        self.validate(lining_density, 'unsigned float', 'Lining density must be a positive number')
        self.validate(lining_thermal_heat_capacity, 'unsigned float', 'Lining heat capacity must be a positive number')
        self.validate(fire_limiting_time, 'unsigned float', 'Limiting time must be a positive number')

        # ================
        # units conversion
        # ================
        duration *= 60  # minutes -> seconds
        fire_limiting_time *= 60  # minutes -> seconds
        initial_temperature += 273.15  # degree Celsius -> degree Kelvin

        return dict(duration=duration, room_total_surface_area=room_total_surface_area,
                    room_floor_area=room_floor_area, ventilation_area=ventilation_area,
                    ventilation_opening_height=ventilation_opening_height, fuel_density=fuel_density,
                    lining_thermal_conductivity=lining_thermal_conductivity, lining_density=lining_density,
                    lining_thermal_heat_capacity=lining_thermal_heat_capacity, fire_limiting_time=fire_limiting_time,
                    initial_temperature=initial_temperature)

    @input_parameters.setter
    def input_parameters(self, v):

        def num2str(num):
            if isinstance(num, int):
                return f'{num:g}'
            elif isinstance(num, float):
                return f'{num:.3f}'.rstrip('0').rstrip('.')
            elif isinstance(num, str):
                return v
            elif num is None:
                return ''
            else:
                return str(v)

        # units conversion
        v['duration'] /= 60  # seconds -> minutes
        v['fire_limiting_time'] /= 60  # seconds -> minutes
        v['initial_temperature'] -= 273.15  # degree Kelvin -> degree Celsius

        self.ui.lineEdit_in_duration.setText(num2str(v['duration']))
        self.ui.lineEdit_in_room_total_surface_area.setText(num2str(v['room_total_surface_area']))
        self.ui.lineEdit_in_room_floor_area.setText(num2str(v['room_floor_area']))
        self.ui.lineEdit_in_ventilation_area.setText(num2str(v['ventilation_area']))
        self.ui.lineEdit_in_ventilation_opening_height.setText(num2str(v['ventilation_opening_height']))
        self.ui.lineEdit_in_fuel_density.setText(num2str(v['fuel_density']))
        self.ui.lineEdit_in_lining_thermal_conductivity.setText(num2str(v['lining_thermal_conductivity']))
        self.ui.lineEdit_in_lining_density.setText(num2str(v['lining_density']))
        self.ui.lineEdit_in_lining_thermal_heat_capacity.setText(num2str(v['lining_thermal_heat_capacity']))
        self.ui.lineEdit_in_fire_limiting_time.setText(num2str(v['fire_limiting_time']))
        self.ui.lineEdit_in_initial_temperature.setText(num2str(v['initial_temperature']))

    @property
    def output_parameters(self):
        return self.__output_fire_curve

    @output_parameters.setter
    def output_parameters(self, v):
        self.__output_fire_curve['time'] = v['time']
        self.__output_fire_curve['temperature'] = v['temperature']

    @staticmethod
    def __calculate_ec_parametric_fire_curve(
            duration,
            room_total_surface_area,
            room_floor_area,
            ventilation_area,
            ventilation_opening_height,
            fuel_density,
            lining_thermal_conductivity,
            lining_density,
            lining_thermal_heat_capacity,
            fire_limiting_time,
            initial_temperature,
    ):
        t = np.arange(0, duration + 1, 1)
        T = appendix_a_parametric_fire(
            t=t,
            A_v=ventilation_area,
            A_t=room_total_surface_area,
            A_f=room_floor_area,
            h_eq=ventilation_opening_height,
            q_fd=fuel_density,
            lambda_=lining_thermal_conductivity,
            rho=lining_density,
            c=lining_thermal_heat_capacity,
            t_lim=fire_limiting_time,
            temperature_initial=initial_temperature,
        )

        return dict(time=t, temperature=T)

    def calculate(self):

        # clear ui output fields
        # none

        # parse inputs from ui
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input. {str(e)}.')
            return

        # calculate
        try:
            output_parameters = self.__calculate_ec_parametric_fire_curve(**input_parameters)
            self.statusBar().showMessage('Calculation complete.')
        except Exception as e:
            self.statusBar().showMessage(f'{str(e)}')
            return

        # cast outputs to ui
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to cast results to UI. Error: {str(e)}')
            return

        self.show_results_in_table()

        self.repaint()

    def show_results_in_table(self):

        output_parameters = self.output_parameters
        # output_parameters['time'] -= 273.15
        # output_parameters['temperature'] -= 273.15

        # print results (for console enabled version only)
        list_content = list(zip(output_parameters['time'], output_parameters['temperature'] - 273.15))
        list_content = [[float(i), float(j)] for i, j in list_content]
        print(list_content)

        app_ = TableWindow(
            parent=self,
            data_list=list_content,
            header=['time [s]', 'temperature [°C]'],
            window_title='Numerical Results',
            window_geometry=(300, 200, 500, 800)
        )

        app_.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        app_.TableView.resizeColumnsToContents()
        app_.show()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0611()
    app.show()
    qapp.exec_()
