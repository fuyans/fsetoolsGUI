from os.path import join

import numpy as np
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QRadioButton
from fsetools.lib.fse_activation_hd import heat_detector_temperature_pd7974

import fsetoolsGUI
from fsetoolsGUI import logger
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass
from fsetoolsGUI.gui.bases.custom_plot_pyqtgraph import App as PlotApp
from fsetoolsGUI.gui.bases.custom_utilities import Counter
from fsetoolsGUI.gui.images.base64 import dialog_0111_figure_1 as image_figure_1
from fsetoolsGUI.gui.images.base64 import dialog_0111_figure_2 as image_figure_2


def pd_7974_1_heat_detector_activation(
        plume_type: str,
        t_end: float,
        t_step: float,
        alpha: float,
        H: float,
        R: float,
        RTI: float,
        C: float,
        HRRPUA: float,
        C_conv: float,
        T_act: float,
):
    t_end *= 60.  # min -> s
    T_act += 273.15  # deg.C -> K
    C_conv /= 100.  # % -> fraction

    # calculate all sorts of things
    t = np.arange(0, t_end + t_step / 2., t_step)
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
    res.update(dict(
        time=t,
        gas_hrr_kW=gas_hrr_kW,
        t_act=t[np.argmin(np.abs(res['detector_temperature'] - T_act))],
        T_g_act=res['jet_temperature'][np.argmin(np.abs(res['detector_temperature'] - T_act))],
    ))

    return res


class App(AppBaseClass):
    app_id = '0111'
    app_name_short = 'PD 7974\nheat\ndetector\nactivation'
    app_name_long = 'PD 7974 heat detector device activation time'

    input_items = dict(
        t_end=dict(description='<i>t<sub>end</sub></i>, duration', unit='min', default=10),
        t_step=dict(description='<i>t<sub>step</sub></i>, time step', unit='s', default=1),
        alpha=dict(description='<i>α</i>, fire growth factor', unit='kW/s<sup>2</sup>', default=0.012),
        H=dict(description='<i>H</i>, height', unit='m', default=2.4),
        R=dict(description='<i>R</i>, radial distance', unit='m', default=2.75),
        RTI=dict(description='<i>RTI</i>, response time index', unit='m<sup>0.5</sup>s<sup>0.5</sup>', default=115),
        C=dict(description='<i>C</i>, conduction factor', unit='m<sup>0.5</sup>/s<sup>0.5</sup>', default=0.4),
        HRRPUA=dict(description='HRR density', unit='kW/m<sup>2</sup>', default=510),
        C_conv=dict(description='<i>C<sub>conv</sub></i>, convection HRR', unit='%', default=66.7),
        T_act=dict(description='<i>T<sub>act</sub></i>, detector act. temp.', unit='<sup>o</sup>C', default=68),
    )
    output_items = dict(
        t_act=dict(description='<i>t<sub>act</sub></i>, activation time', unit='s', default=''),
        T_g_act=dict(description='<i>T<sub>g,act</sub></i>, gas temp. at act.', unit='<sup>o</sup>C', default=''),
    )

    def __init__(self, parent=None, post_stats: bool = True):

        super().__init__(parent, post_stats)

        # containers, variables etc
        self.__input_parameters = dict()
        self.__output_parameters = dict()

        self.FigureApp = PlotApp(parent=self, title='PD 7974 heat detector device activation time', antialias=True)
        self.FigureApp.resize(600, 400)
        self.__figure_ax_1 = self.FigureApp.add_subplot(0, 0, x_label='Time [s]', y_label='Temperature [<sup>o</sup>C]', name='p1')
        self.__figure_ax_2 = self.FigureApp.add_subplot(1, 0, x_label='Time [s]', y_label='HRR [kW]', name='p2')
        self.__figure_ax_3 = self.FigureApp.add_subplot(0, 1, x_label='Time [s]', y_label='Jet velocity [m/s]', name='p3')
        self.__figure_ax_4 = self.FigureApp.add_subplot(1, 1, x_label='Time [s]', y_label='Virtual origin [m]', name='p4')
        self.__figure_ax_1.addLegend()
        self.__figure_ax_2.setXLink(self.__figure_ax_1)
        self.__figure_ax_3.setXLink(self.__figure_ax_1)
        self.__figure_ax_4.setXLink(self.__figure_ax_1)

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
        for k, v in self.input_items.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_' + k, v['description'], v['unit'], min_width=70)

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        for k, v in self.output_items.items():
            self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_' + k, v['description'], v['unit'], min_width=70)

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

    def set_temperature_correlation(self):

        # clear output
        for i in self.output_items.keys():
            getattr(self.ui, f'p2_out_{i}').setText('')

        """Set figures, disable and enable UI items accordingly."""
        if self.ui.p2_in_fire_plume.isChecked():  # plume temperature and velocity
            self.ui.p2_in_R.setEnabled(False)
            self.ui.p1_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])
        else:  # ceiling jet temperature and velocity
            self.ui.p2_in_R.setEnabled(True)
            self.ui.p1_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])

    def example(self):
        input_parameters = {k: v['default'] for k, v in self.input_items.items()}
        input_parameters.update(dict(plume_type='ceiling jet'))
        self.input_parameters = input_parameters

    def ok(self):
        self.output_parameters = pd_7974_1_heat_detector_activation(**self.input_parameters)
        self.show_results_in_figure()

    @property
    def input_parameters(self):

        def str2float(v):
            try:
                return float(v)
            except:
                return None

        input_parameters = dict()
        for k, v in self.input_items.items():
            input_parameters[k] = str2float(getattr(self.ui, 'p2_in_' + k).text())

        if self.ui.p2_in_fire_plume.isChecked():
            input_parameters['plume_type'] = 'fire plume'
        elif self.ui.p2_in_ceiling_jet.isChecked():
            input_parameters['plume_type'] = 'ceiling jet'
        else:
            errmsg = f'Unknown correlation type, it can be either `fire plume` or `ceiling jet`'
            logger.error(errmsg)
            raise ValueError(errmsg)

        try:
            self.__input_parameters.update(input_parameters)
        except TypeError:
            self.__input_parameters = input_parameters

        return self.__input_parameters

    @input_parameters.setter
    def input_parameters(self, v: dict):

        if 'fire plume' == v['plume_type']:
            self.ui.p2_in_fire_plume.setChecked(True)
        elif 'ceiling jet' == v['plume_type']:
            self.ui.p2_in_ceiling_jet.setChecked(True)
        else:
            errmsg = f'Unknown correlation type, it can be either `plume` or `ceiling jet`, `{v["type"]}` is given'
            logger.error(errmsg)
            raise ValueError(errmsg)

        for k, v_ in self.input_items.items():
            getattr(self.ui, 'p2_in_' + k).setText(self.num2str(v[k]))

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v: dict):
        self.__output_parameters = v
        for k, v_ in self.output_items.items():
            getattr(self.ui, 'p2_out_' + k).setText(self.num2str(v[k]))

    def show_results_in_figure(self):
        out = self.output_parameters

        self.__figure_ax_1.getPlotItem().clear()
        self.__figure_ax_2.getPlotItem().clear()
        self.__figure_ax_3.getPlotItem().clear()
        self.__figure_ax_4.getPlotItem().clear()

        self.FigureApp.plot(x=out['time'], y=out['detector_temperature'] - 273.15, ax=self.__figure_ax_1, name='Detector temp.')
        self.FigureApp.plot(x=out['time'], y=out['jet_temperature'] - 273.15, ax=self.__figure_ax_1, name='Gas temp.')
        self.FigureApp.plot(x=out['time'], y=out['gas_hrr_kW'], ax=self.__figure_ax_2)
        self.FigureApp.plot(x=out['time'], y=out['jet_velocity'], ax=self.__figure_ax_3)
        self.FigureApp.plot(x=out['time'], y=out['virtual_origin'], ax=self.__figure_ax_4)

        self.FigureApp.show()

    @staticmethod
    def str2float(v):
        try:
            return float(v)
        except:
            return None


if __name__ == '__main__':
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
