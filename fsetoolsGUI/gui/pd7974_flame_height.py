from os.path import join

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QComboBox
from fsetools.lib.fse_flame_height import mean_flame_height_pd_7974
from fsetools.libstd.pd_7974_1_2019 import eq_11_dimensionless_hrr_rectangular
from fsetools.libstd.pd_7974_1_2019 import eq_12_dimensionless_hrr_line
from fsetools.libstd.pd_7974_1_2019 import eq_5_dimensionless_hrr

import fsetoolsGUI
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass
from fsetoolsGUI.gui.images.base64 import dialog_0602_context as image_context
from fsetoolsGUI.gui.images.base64 import dialog_0602_figure as image_figure


class App(AppBaseClass):
    app_id = '0602'
    app_name_short = 'PD 7974\nflame\nheight'
    app_name_long = 'PD 7974 Flame height calculator'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This app calculates the mean flame height in accordance with '
            '"PD 7974-1:2019 Application of fire safety engineering principles to the design of buildings. Part 1: '
            'Initiation and development of fire within the enclosure of origin (Sub-system 1)".'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_figure = QLabel()
        self.ui.p1_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))
        self.ui.p1_layout.addWidget(self.ui.p1_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'p2_in_Q_dot_or_Q_dot_l', 'Total HRR', 'kW')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'p2_in_L_A_or_D', 'Fire diameter', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'p2_in_L_B', 'Fire shorter dimension', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_in_rho_0', 'Air density', 'kg/m<sup>3</sup>')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_in_c_p_0', 'Air heat capacity', 'kJ/kg/K')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_in_T_0', 'Air temperature', 'K')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_in_g', 'Gravity', 'm/s<sup>2</sup>')
        self.ui.p2_in_fire_shape = QComboBox()
        self.ui.p2_in_fire_shape.addItems(['Circular fire', 'Rectangular fire', 'Line fire'])
        self.ui.p2_layout.addWidget(self.ui.p2_in_fire_shape, 8, 0, 1, 3)
        self.ui.p2_in_fuel_type = QComboBox()
        self.ui.p2_in_fuel_type.addItems(['Natural gas (Zukoski)', 'Wood cribs', 'Gas, liquids and solids (Heskestad)'])
        self.ui.p2_layout.addWidget(self.ui.p2_in_fuel_type, 9, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 10, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_out_Q_dot_star', 'Dimensionless HRR', '')
        self.ui.p2_out_Q_dot_star.setReadOnly(True)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 12, 'p2_out_Z_f', 'Flame height', 'm')
        self.ui.p2_out_Z_f.setReadOnly(True)

        # ==============
        # instantiate ui
        # ==============
        self.ui.p2_in_Q_dot_or_Q_dot_l.setToolTip(
            'Total fire heat release rate (per unit length for line fire shape)')
        self.ui.p2_in_L_A_or_D.setToolTip('Fire longer dimension (diameter for circular fire shape)')
        self.ui.p2_in_L_B.setToolTip('Fire shorter dimension (only for rectangular fire shape)')
        self.ui.p2_out_Q_dot_star.setToolTip('Solved dimensionless heat release rate, double click to select')
        self.ui.p2_out_Z_f.setToolTip('Solved mean flame height, double click to select')

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(image_context=image_context,
                                       image_figure=image_figure, )
        for k, v in self.dict_images_pixmap.items():
            ba = QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        # set default values
        # todo
        self.change_fire_shape()

        # signal and slots
        self.ui.p2_in_fire_shape.currentIndexChanged.connect(self.change_fire_shape)

    def change_fire_shape(self):

        self.ui.p2_out_Q_dot_star.setText('')
        self.ui.p2_out_Z_f.setText('')

        if self.ui.p2_in_fire_shape.currentIndex() == 0:  # circular fire source
            self.ui.p2_in_Q_dot_or_Q_dot_l_label.setText('Total HRR')
            self.ui.p2_in_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.p2_in_L_A_or_D_label.setText("Fire diameter")
            self.ui.p2_in_L_B_label.setDisabled(True)
            self.ui.p2_in_L_B.setDisabled(True)
            self.ui.p2_in_L_B_unit.setDisabled(True)
        elif self.ui.p2_in_fire_shape.currentIndex() == 1:  # rectangular fire source
            self.ui.p2_in_Q_dot_or_Q_dot_l_label.setText('Total HRR')
            self.ui.p2_in_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.p2_in_L_A_or_D_label.setText("Fire longer dimension")
            self.ui.p2_in_L_B_label.setDisabled(False)
            self.ui.p2_in_L_B.setDisabled(False)
            self.ui.p2_in_L_B_unit.setDisabled(False)
        elif self.ui.p2_in_fire_shape.currentIndex() == 2:  # line fire source
            self.ui.p2_in_Q_dot_or_Q_dot_l_label.setText('Total HRR per unit length')
            self.ui.p2_in_Q_dot_or_Q_dot_l_unit.setText('kW/m')
            self.ui.p2_in_L_A_or_D_label.setText(r'Fire length')
            self.ui.p2_in_L_B_label.setDisabled(True)
            self.ui.p2_in_L_B.setDisabled(True)
            self.ui.p2_in_L_B_unit.setDisabled(True)
        else:
            self.statusBar().showMessage('Unknown fire shape')

    def example(self):
        self.ui.p2_in_fire_shape.setCurrentIndex(0)
        self.ui.p2_in_fuel_type.setCurrentIndex(0)
        self.ui.p2_in_Q_dot_or_Q_dot_l.setText('1500')
        self.ui.p2_in_L_A_or_D.setText('2.5')
        self.ui.p2_in_rho_0.setText('1.2')
        self.ui.p2_in_c_p_0.setText('1.0')
        self.ui.p2_in_T_0.setText('293.15')
        self.ui.p2_in_g.setText('9.81')

        self.repaint()

    def calculate(self):

        # clear ui outputs
        self.ui.p2_out_Q_dot_star.clear()
        self.ui.p2_out_Z_f.clear()

        # parse inputs from ui
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'{str(e)}')
            return

        # perform calculation
        try:
            output_parameters = self.__flame_height_func(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'{str(e)}')
            return

        # cast outputs to ui
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'{str(e)}')
            return

    def submit(self):
        self.calculate()
        self.repaint()

    @property
    def input_parameters(self):
        """Parse inputs from the UI."""

        # parse compulsory parameters
        try:
            Q_dot_or_Q_dot_l = float(self.ui.p2_in_Q_dot_or_Q_dot_l.text())
            L_A_or_D = float(self.ui.p2_in_L_A_or_D.text())
            rho_0 = float(self.ui.p2_in_rho_0.text())
            c_p_0 = float(self.ui.p2_in_c_p_0.text())
            T_0 = float(self.ui.p2_in_T_0.text())
            g = float(self.ui.p2_in_g.text())
            fire_shape = self.ui.p2_in_fire_shape.currentIndex()
            fuel_type = int(self.ui.p2_in_fuel_type.currentIndex())
        except Exception as e:
            raise ValueError(f'Unable to parse parameters from UI')

        # parse optional input parameters
        try:
            L_B = float(self.ui.p2_in_L_B.text())
        except Exception as e:
            L_B = None

        # validation, error will be raised
        self.validate(Q_dot_or_Q_dot_l, 'unsigned float', 'Heat release rate should be greater than 0')
        self.validate(L_A_or_D, 'unsigned float', 'Fire dimension should be greater than 0')
        self.validate(rho_0, 'unsigned float', 'Ambient air density should be greater than 0')
        self.validate(c_p_0, 'unsigned float', 'Ambient air heat capacity should be greater than 0')
        self.validate(T_0, 'unsigned float', 'Ambient temperature should be greater than 0')
        self.validate(g, 'unsigned float', 'Gravity should be greater than 0')
        if L_B:
            self.validate(L_B, 'unsigned float', 'Fire dimension should be greater than 0')

        # warning if input parameters maybe incorrect
        if 10 > Q_dot_or_Q_dot_l or Q_dot_or_Q_dot_l > 10000:
            self.dialog_show_message(
                title='Warning',
                msg='Heat release rate seems too low or too high.\nMake sure the input is in correct unit.'
            )

        return dict(
            Q_dot_or_Q_dot_l=Q_dot_or_Q_dot_l,
            L_A_or_D=L_A_or_D,
            rho_0=rho_0,
            c_p_0=c_p_0,
            T_0=T_0,
            g=g,
            fire_shape=fire_shape,
            fuel_type=fuel_type,
            L_B=L_B
        )

    @staticmethod
    def __flame_height_func(Q_dot_or_Q_dot_l, L_A_or_D, rho_0, c_p_0, T_0, g, fire_shape, fuel_type, L_B):
        """A wrapper to the core calculation function with additional options and error handling"""

        try:
            if fire_shape == 0:  # circular fire source
                Q_dot_star = eq_5_dimensionless_hrr(
                    Q_dot_kW=Q_dot_or_Q_dot_l,
                    rho_0=rho_0,
                    c_p_0_kJ_kg_K=c_p_0,
                    T_0=T_0,
                    g=g,
                    D=L_A_or_D,
                )
                flame_height = mean_flame_height_pd_7974(
                    Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=L_A_or_D
                )
            elif fire_shape == 1:  # rectangular fire source
                Q_dot_star = eq_11_dimensionless_hrr_rectangular(
                    Q_dot_kW=Q_dot_or_Q_dot_l,
                    rho_0=rho_0,
                    c_p_0_kJ_kg_K=c_p_0,
                    T_0=T_0,
                    g=g,
                    L_A=L_A_or_D,
                    L_B=L_B
                )
                flame_height = mean_flame_height_pd_7974(
                    Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=(L_A_or_D + L_B) / 2.
                )
            elif fire_shape == 2:  # line fire source
                Q_dot_star = eq_12_dimensionless_hrr_line(
                    Q_dot_l_kW_m=Q_dot_or_Q_dot_l,
                    rho_0=rho_0,
                    c_p_0_kJ_kg_K=c_p_0,
                    T_0=T_0,
                    g=g,
                    L_A=L_A_or_D,
                )
                flame_height = mean_flame_height_pd_7974(
                    Q_dot_star=Q_dot_star, fuel_type=fuel_type, fire_diameter=L_A_or_D
                )
            else:
                raise ValueError('Unknown fire shape')

        except Exception as e:
            raise ValueError(f'Calculation incomplete. Error: {e}.')

        return dict(Q_dot_star=Q_dot_star, flame_height=flame_height)

    @property
    def output_parameters(self):
        return  # not implemented

    @output_parameters.setter
    def output_parameters(self, v: dict):
        """cast values to ui line edits"""

        try:
            Q_dot_star = v['Q_dot_star']
            flame_height = v['flame_height']
        except Exception as e:
            raise KeyError(f'Missing output parameters. Error {str(e)}')

        if Q_dot_star:
            self.ui.p2_out_Q_dot_star.setText(f'{Q_dot_star:.2f}')
        else:
            self.ui.p2_out_Q_dot_star.clear()

        if flame_height:
            self.ui.p2_out_Z_f.setText(f'{flame_height:.2f}')
        else:
            self.ui.p2_out_Z_f.clear()


if __name__ == '__main__':
    from PySide2 import QtWidgets, QtCore
    import PySide2
    import sys

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
