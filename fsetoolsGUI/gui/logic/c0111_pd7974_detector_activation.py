from os.path import join

import numpy as np
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QRadioButton
from fsetools.lib.fse_activation_hd import heat_detector_temperature_pd7974
from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_1 as image_figure_1
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_2 as image_figure_2
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0111'
    app_name_short = 'PD 7974\nheat\ndetector\nactivation'
    app_name_long = 'PD 7974 heat detector device activation time calculator'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        # containers, variables etc
        self.__Table = None
        self.__table_header: list = None
        self.__table_content: list = None
        self._numerical_results: dict = None

        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This app estimates the activation time of a heat detection element '
            '(e.g. heat detector, sprinkler head etc.) located above a fire bed.\n\n'
            'Calculation follows '
            '"PD 7974-1:2019 Application of fire safety engineering principles to the design of buildings. '
            'Part 1: Initiation and development of fire within the enclosure of origin (Sub-system 1)".'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), 0, 0, 1, 3)
        self.ui.p2_in_ceiling_jet = QRadioButton('Use ceiling jet equations', self.ui.page_2)
        self.ui.p2_in_fire_plume = QRadioButton('Use plume equations', self.ui.page_2)
        self.ui.p2_layout.addWidget(self.ui.p2_in_ceiling_jet, 1, 0, 1, 3)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fire_plume, 2, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 3, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_in_t', 't, fire duration', 's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_in_alpha', 'α, fire growth factor', 'kW/m<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_in_H', 'H, height', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_in_R', 'R, radial distance', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_in_RTI', 'RTI, response time index',
                                'm<sup>0.5</sup>s<sup>0.5</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'p2_in_C', 'C, conduction factor',
                                'm<sup>0.5</sup>/s<sup>0.5</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_in_HRRPUA', 'HRR per unit area', 'kW/m<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_in_C_conv', 'C<sub>conv</sub> convection HRR', '%')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 12, 'p2_in_t_act', 'detector act. temp.', '<sup>o</sup>C')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 13, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 14, 'p2_out_T_g_act', 'T<sub>g,act</sub>, gas temp.',
                                '<sup>o</sup>C')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 15, 'p2_out_t_act', 't<sub>act</sub>, detector act. time', 's')

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_figure_1=image_figure_1,
            image_figure_2=image_figure_2,
        )
        for k, v in self.dict_images_pixmap.items():
            ba = QtCore.QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        # default values
        self.ui.p2_in_ceiling_jet.setChecked(True)
        self.set_temperature_correlation()

        # signals
        self.ui.p2_in_fire_plume.toggled.connect(self.set_temperature_correlation)

    def error(self, msg: str, stop: bool = False):
        self.statusBar().showMessage(msg)
        self.repaint()
        if stop:
            raise ValueError

    def set_temperature_correlation(self):

        # clear output
        self.ui.p2_out_t_act.setText('')
        self.ui.p2_out_T_g_act.setText('')

        self._numerical_results = dict()

        """Set figures, disable and enable UI items accordingly."""
        if self.ui.p2_in_fire_plume.isChecked():  # plume temperature and velocity
            self.ui.p2_in_R.setEnabled(False)
            self.ui.p1_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])
            self.__table_header = [
                'Time [s]', 'HRR [kW]', 'V. Origin [m]', 'Plume T. [°C]', 'Plume Vel. [m/s]', 'Detector T. [°C]'
            ]
        else:  # ceiling jet temperature and velocity
            self.ui.p2_in_R.setEnabled(True)
            self.ui.p1_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])
            self.__table_header = [
                'Time [s]', 'HRR [kW]', 'V. Origin [m]', 'Jet T. [°C]', 'Jet Vel. [m/s]', 'Detector T. [°C]'
            ]

    def example(self):

        self.ui.p2_in_t.setText('600')
        self.ui.p2_in_alpha.setText('0.0117')
        self.ui.p2_in_H.setText('2.4')
        self.ui.p2_in_R.setText('2.5')
        self.ui.p2_in_RTI.setText('115')
        self.ui.p2_in_C.setText('0.4')
        self.ui.p2_in_HRRPUA.setText('510')
        self.ui.p2_in_C_conv.setText('66.7')
        self.ui.p2_in_t_act.setText('68')

        self.repaint()

    def ok(self):
        self.calculate()

    def calculate(self):
        # clear outputs
        self.ui.p2_out_t_act.setText('')

        # get data
        try:
            time = float(self.ui.p2_in_t.text())
            alpha = float(self.ui.p2_in_alpha.text())
            detector_to_fire_vertical_distance = float(self.ui.p2_in_H.text())
            if self.ui.p2_in_ceiling_jet.isChecked():  # `detector_to_fire_horizontal_distance` may be disabled if plume temperature correlation is checked.
                detector_to_fire_horizontal_distance = float(self.ui.p2_in_R.text())
            else:
                detector_to_fire_horizontal_distance = 0.
            detector_response_time_index = float(self.ui.p2_in_RTI.text())
            detector_conduction_factor = float(self.ui.p2_in_C.text())
            fire_hrr_density_kWm2 = float(self.ui.p2_in_HRRPUA.text())
            fire_convection_fraction = float(self.ui.p2_in_C_conv.text()) / 100.
            detector_activation_temperature = float(self.ui.p2_in_t_act.text())
        except Exception as e:
            self.error(f'Failed to parse inputs. Error "{e}".')
            raise e

        # calculate all sorts of things
        time = np.arange(0, time, 1.)
        gas_hrr_kW = eq_22_t_squared_fire_growth(alpha, time) / 1000.

        try:
            res = heat_detector_temperature_pd7974(
                gas_time=time,
                gas_hrr_kW=gas_hrr_kW,
                detector_to_fire_vertical_distance=detector_to_fire_vertical_distance,
                detector_to_fire_horizontal_distance=detector_to_fire_horizontal_distance,
                detector_response_time_index=detector_response_time_index,
                detector_conduction_factor=detector_conduction_factor,
                fire_hrr_density_kWm2=fire_hrr_density_kWm2,
                fire_convection_fraction=fire_convection_fraction,
                force_plume_temperature_correlation=self.ui.p2_in_fire_plume.isChecked()
            )
        except Exception as e:
            self.error(str(e))
            raise e

        res['time'], res['gas_hrr_kW'] = time, gas_hrr_kW

        # work out activation time
        activation_time = time[
            np.argmin(np.abs((res['detector_temperature'] - 273.15) - detector_activation_temperature))]
        activation_gas_temperature = res['jet_temperature'][np.argmin(
            np.abs((res['detector_temperature'] - 273.15) - detector_activation_temperature))] - 273.15

        # print results (for console version only)
        list_title = self.__table_header
        list_param = ['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity', 'detector_temperature']
        list_units = ['s', 'kW', 'm', 'K', 'm/s', 'K']
        for i, time_ in enumerate(time):
            fs1_ = list()
            for i_, param in enumerate(list_param):
                v = res[param][i]
                unit = list_units[i_]
                fs1_.append('{:<15.14}'.format(f'{v:<.2f} {unit:<}'))

            if i % 25 == 0:
                print('\n' + ''.join(f'{i_:<15.15}' for i_ in list_title))
            print(''.join(fs1_))

        # write results to ui
        self.ui.p2_out_t_act.setText(f'{activation_time:.1f}')
        self.ui.p2_out_T_g_act.setText(f'{activation_gas_temperature:.1f}')
        # store calculated results
        self._numerical_results = res
        # status feedback
        self.statusBar().showMessage('Calculation complete.')
        # enable button to view numerical results
        self.show_results_in_table()
        self.repaint()

    def show_results_in_table(self):

        res = self._numerical_results
        res['jet_temperature'] -= 273.15
        res['detector_temperature'] -= 273.15

        # print results (for console enabled version only)
        list_param = ['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity', 'detector_temperature']
        list_content = list()
        for i, time_ in enumerate(self._numerical_results['time']):
            list_content_ = list()
            for i_, param in enumerate(list_param):
                v = self._numerical_results[param][i]
                list_content_.append(float(v))
            list_content.append(list_content_)

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
            header_col=self.__table_header,
            window_title='Numerical results',
        )

        # added `self.__Table` to `activated_dialogs` so it closes upon parent app close event
        self.activated_dialogs.append(self.__Table)

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
