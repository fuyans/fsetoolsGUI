from os.path import join

import numpy as np
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QRadioButton
from fsetools.lib.fse_activation_hd import heat_detector_temperature_pd7974

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_1 as image_figure_1
from fsetoolsGUI.gui.images_base64 import dialog_0111_figure_2 as image_figure_2
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0111'
    app_name_short = 'PD 7974\nheat\ndetector\nactivation'
    app_name_long = 'PD 7974 heat detector device activation time calculator'

    def __init__(self, parent=None, post_stats: bool = True):

        super().__init__(parent, post_stats)

        # containers, variables etc
        self.TableApp = TableWindow(parent=self, window_title='Numerical results')
        self.__output_parameters = None

        # ==============
        # Instantiate UI
        # ==============
        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This app estimates the activation time of a heat detection element '
            '(e.g. heat detector, sprinkler head etc.) located above a fire bed.\n\n'
            'Calculation follows '
            '"PD 7974-1:2019 Application of fire safety engineering principles to the design of buildings. '
            'Part 1: Initiation and development of fire within the enclosure of origin (Sub-system 1)".'
        )
        self.ui.p1_description.setFixedWidth(350), self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)
        c = Counter()

        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), c.count, 0, 1, 3)
        self.ui.p2_in_ceiling_jet = QRadioButton('Use ceiling jet equations', self.ui.page_2)
        self.ui.p2_in_fire_plume = QRadioButton('Use plume equations', self.ui.page_2)
        self.ui.p2_layout.addWidget(self.ui.p2_in_ceiling_jet, c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fire_plume, c.count, 0, 1, 3)

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_t', 't, fire duration', 's')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_alpha', 'α, fire growth factor', 'kW/m<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_H', 'H, height', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_R', 'R, radial distance', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_RTI', 'RTI, response time index', 'm<sup>0.5</sup>s<sup>0.5</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_C', 'C, conduction factor', 'm<sup>0.5</sup>/s<sup>0.5</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_HRRPUA', 'HRR per unit area', 'kW/m<sup>2</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_C_conv', 'C<sub>conv</sub> convection HRR', '%')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_in_T_act', 'T<sub>act</sub> detector act. temp.', '<sup>o</sup>C')

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_T_g_act', 'T<sub>g</sub>, gas temp.', '<sup>o</sup>C')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c, 'p2_out_t_act', 't<sub>act</sub>, detector act. time', 's')

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_figure_1=image_figure_1,
            image_figure_2=image_figure_2,
        )
        for k, v in self.dict_images_pixmap.items():
            ba = QtCore.QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        # =====================
        # Assign default values
        # =====================
        self.ui.p2_in_ceiling_jet.setChecked(True)
        self.set_temperature_correlation()

        # ========================
        # Define slots and signals
        # ========================
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
        self.ui.p2_in_T_act.setText('68')

        self.repaint()

    def ok(self):
        self.output_parameters = self.calculate(**self.input_parameters)
        self.show_results_in_table(self.output_parameters)

    @staticmethod
    def calculate(
            plume_type: str,
            t: float,
            alpha: float,
            H: float,
            R: float,
            RTI: float,
            C: float,
            HRRPUA: float,
            C_conv: float,
            T_act: float,
    ):
        # calculate all sorts of things
        t = np.arange(0, t + 1., 1.)
        gas_hrr_kW = alpha * (t ** 2)

        res = heat_detector_temperature_pd7974(
            gas_time=t,
            gas_hrr_kW=gas_hrr_kW,
            detector_to_fire_vertical_distance=H,
            detector_to_fire_horizontal_distance=R,
            detector_response_time_index=RTI,
            detector_conduction_factor=C,
            fire_hrr_density_kWm2=HRRPUA,
            fire_convection_fraction=C_conv,
            force_plume_temperature_correlation='fire plume' == plume_type
        )

        # work out activation time
        T_diff = np.abs((res['detector_temperature'] - 273.15) - T_act)
        res.update(dict(
            time=t,
            gas_hrr_kW=gas_hrr_kW,
            activation_time=t[np.argmin(T_diff)],
            activation_gas_temperature=res['jet_temperature'][np.argmin(T_diff)] - 273.15,
        ))

        return res

    @property
    def input_parameters(self):
        return dict(
            plume_type='ceiling jet' if self.ui.p2_in_ceiling_jet.isChecked() else 'fire plume',
            t=self.str2float(self.ui.p2_in_t.text()),
            alpha=self.str2float(self.ui.p2_in_alpha.text()),
            H=self.str2float(self.ui.p2_in_H.text()),
            R=self.str2float(self.ui.p2_in_R.text()),
            RTI=self.str2float(self.ui.p2_in_RTI.text()),
            C=self.str2float(self.ui.p2_in_C.text()),
            HRRPUA=self.str2float(self.ui.p2_in_HRRPUA.text()),
            C_conv=self.str2float(self.ui.p2_in_C_conv.text()) * 1e-2,
            T_act=self.str2float(self.ui.p2_in_T_act.text()),
        )

    @input_parameters.setter
    def input_parameters(self, v: dict):

        if 'fire plume' == v['plume_type']:
            self.ui.p2_in_fire_plume.setChecked(True)
        elif 'ceiling jet' == v['plume_type']:
            self.ui.p2_in_ceiling_jet.setChecked(True)
        else:
            raise ValueError(f'Unknown correlation type, it can be either `plume` or `ceiling jet`, `{v["type"]}` is given')

        self.ui.p2_in_t.setText(self.num2str(v['t']))
        self.ui.p2_in_alpha.setText(self.num2str(v['alpha']))
        self.ui.p2_in_H.setText(self.num2str(v['H']))
        self.ui.p2_in_R.setText(self.num2str(v['R']))
        self.ui.p2_in_RTI.setText(self.num2str(v['RTI']))
        self.ui.p2_in_C.setText(self.num2str(v['C']))
        self.ui.p2_in_HRRPUA.setText(self.num2str(v['HRRPUA']))
        self.ui.p2_in_C_conv.setText(self.num2str(v['C_conv']))
        self.ui.p2_in_T_act.setText(self.num2str(v['T_act']))

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v

        self.ui.p2_out_T_g_act.setText(self.num2str(v['activation_gas_temperature']))
        self.ui.p2_out_t_act.setText(self.num2str(v['activation_time']))

    def show_results_in_table(self, v: dict):

        v['jet_temperature'] -= 273.15
        v['detector_temperature'] -= 273.15

        # print results (for console enabled version only)
        list_param = ['time', 'gas_hrr_kW', 'virtual_origin', 'jet_temperature', 'jet_velocity', 'detector_temperature']
        list_units = ['s', 'kW', 'm', 'K', 'm/s', 'K']
        list_content = list()
        for i, time_ in enumerate(v['time']):
            list_content_ = list()
            for i_, param in enumerate(list_param):
                list_content_.append(float(v[param][i]))
            list_content.append(list_content_)

        self.TableApp.update_table_content(
            content_data=list_content,
            col_headers=[f'{i1.replace("_", " ")} [{i2}]' for i1, i2 in zip(list_param, list_units)]
        )
        self.TableApp.show()

    @staticmethod
    def str2float(v):
        try:
            return float(v)
        except:
            return None

    @staticmethod
    def num2str(v):
        if isinstance(v, int):
            return f'{v:g}'
        elif isinstance(v, float):
            return f'{v:.3f}'.rstrip('0').rstrip('.')
        elif isinstance(v, str):
            return v
        elif v is None:
            return ''
        else:
            return str(v)


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
