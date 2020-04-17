import numpy as np
from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QLineEdit
from fsetools.lib.fse_activation_hd import heat_detector_temperature_pd7974
from fsetools.libstd.pd_7974_1_2019 import eq_22_t_squared_fire_growth

from fsetoolsGUI.gui.images_base64 import dialog_0111_context_1 as image_context_1
from fsetoolsGUI.gui.images_base64 import dialog_0111_context_2 as image_context_2
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_1 as image_figure_1
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_2 as image_figure_2
from fsetoolsGUI.gui.layout.i0111_pd7974_heat_detector_activation import Ui_MainWindow as Ui_Dialog
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(QMainWindow):

    def __init__(self, parent=None):

        # containers, variables etc
        self.__Table = None
        self.__table_header: list = None
        self.__table_content: list = None
        self._numerical_results: dict = None

        # ========================
        # instantiate super and ui
        # ========================
        super().__init__(
            module_id='0111',
            parent=parent,
            shortcut_Return=self.calculate,
            freeze_window_size=True,
        )
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_context_1=image_context_1,
            image_context_2=image_context_2,
            image_figure_1=image_figure_1,
            image_figure_2=image_figure_2,
        )
        for k, v in self.dict_images_pixmap.items():
            ba = QtCore.QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        # set output items readonly
        for i in filter_objects_by_name(self.ui.frame_userio, object_types=[QLineEdit], names=['_out_']):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # window properties
        self.ui.pushButton_show_results_in_table.setEnabled(False)

        # default values
        self.ui.radioButton_ceiling_jet.setChecked(True)
        self.set_temperature_correlation()

        # set validators
        self.ui.lineEdit_in_t.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_alpha.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_H.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_R.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_RTI.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_C.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_HRRPUA.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_C_conv.setValidator(self.Validator.unsigned_float)
        self.ui.lineEdit_in_T_act.setValidator(self.Validator.unsigned_float)

        # signals
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.radioButton_fire_plume.toggled.connect(self.set_temperature_correlation)
        self.ui.pushButton_show_results_in_table.clicked.connect(self.show_results_in_table)

        self.init(self)

    def error(self, msg: str, stop: bool = False):
        self.statusBar().showMessage(msg)
        self.repaint()
        if stop:
            raise ValueError

    def set_temperature_correlation(self):

        # clear output
        self.ui.lineEdit_out_t_act.setText('')
        self.ui.pushButton_show_results_in_table.setEnabled(False)
        self._numerical_results = dict()

        """Set figures, disable and enable UI items accordingly."""
        if self.ui.radioButton_fire_plume.isChecked():  # plume temperature and velocity
            self.ui.lineEdit_in_R.setEnabled(False)
            self.ui.label_in_R_label.setEnabled(False)
            self.ui.label_in_R_unit.setEnabled(False)
            # self.ui.label_image_context.setPixmap(self.dict_images_pixmap['image_context_2'])
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])
            self.__table_header = [
                'Time [s]', 'HRR [kW]', 'V. Origin [m]', 'Plume T. [°C]', 'Plume Vel. [m/s]', 'Detector T. [°C]'
            ]
        else:  # ceiling jet temperature and velocity
            self.ui.lineEdit_in_R.setEnabled(True)
            self.ui.label_in_R_label.setEnabled(True)
            self.ui.label_in_R_unit.setEnabled(True)
            # self.ui.label_image_context.setPixmap(self.dict_images_pixmap['image_context_1'])
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])
            self.__table_header = [
                'Time [s]', 'HRR [kW]', 'V. Origin [m]', 'Jet T. [°C]', 'Jet Vel. [m/s]', 'Detector T. [°C]'
            ]

    def example(self):

        self.ui.lineEdit_in_t.setText('600')
        self.ui.lineEdit_in_alpha.setText('0.0117')
        self.ui.lineEdit_in_H.setText('2.4')
        self.ui.lineEdit_in_R.setText('2.75')
        self.ui.lineEdit_in_RTI.setText('115')
        self.ui.lineEdit_in_C.setText('0.4')
        self.ui.lineEdit_in_HRRPUA.setText('510')
        self.ui.lineEdit_in_C_conv.setText('66.7')
        self.ui.lineEdit_in_T_act.setText('58')

        self.repaint()

    def calculate(self):
        # clear outputs
        self.ui.pushButton_show_results_in_table.setEnabled(False)
        self.ui.lineEdit_out_t_act.setText('')

        # get data
        try:
            time = float(self.ui.lineEdit_in_t.text())
            alpha = float(self.ui.lineEdit_in_alpha.text())
            detector_to_fire_vertical_distance = float(self.ui.lineEdit_in_H.text())
            if self.ui.radioButton_ceiling_jet.isChecked():  # `detector_to_fire_horizontal_distance` may be disabled if plume temperature correlation is checked.
                detector_to_fire_horizontal_distance = float(self.ui.lineEdit_in_R.text())
            else:
                detector_to_fire_horizontal_distance = 0.
            detector_response_time_index = float(self.ui.lineEdit_in_RTI.text())
            detector_conduction_factor = float(self.ui.lineEdit_in_C.text())
            fire_hrr_density_kWm2 = float(self.ui.lineEdit_in_HRRPUA.text())
            fire_convection_fraction = float(self.ui.lineEdit_in_C_conv.text()) / 100.
            detector_activation_temperature = float(self.ui.lineEdit_in_T_act.text())
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
                force_plume_temperature_correlation=self.ui.radioButton_fire_plume.isChecked()
            )
        except Exception as e:
            self.error(str(e))
            raise e

        res['time'], res['gas_hrr_kW'] = time, gas_hrr_kW

        # work out activation time
        activation_time = time[
            np.argmin(np.abs((res['detector_temperature'] - 273.15) - detector_activation_temperature))]

        # print results (for console enabled version only)
        list_title = self.__table_header
        list_param = ['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity', 'detector_temperature']
        list_units = ['s', 'kW', 'm', '°C', 'm/s', '°C']
        for i, time_ in enumerate(time):
            fs1_ = list()
            for i_, param in enumerate(list_param):
                v = res[param][i]
                unit = list_units[i_]
                fs1_.append('{:<15.14}'.format(f'{v:<.2f} {unit:<}'))

            if i % 25 == 0:
                print('\n'+''.join(f'{i_:<15.15}' for i_ in list_title))
            print(''.join(fs1_))

        # write results to ui
        self.ui.lineEdit_out_t_act.setText(f'{activation_time:.1f}')
        # store calculated results
        self._numerical_results = res
        # status feedback
        self.statusBar().showMessage('Calculation complete.')
        # enable button to view numerical results
        self.ui.pushButton_show_results_in_table.setEnabled(True)
        # refresh ui
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
            header_col=['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity',
                        'detector_temperature'],
            window_title='Parametric fire numerical results',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0111()
    app.show()
    qapp.exec_()
