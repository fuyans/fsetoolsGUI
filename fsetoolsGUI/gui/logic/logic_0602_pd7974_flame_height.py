from os.path import join

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QByteArray
from fsetools.lib.fse_flame_height import mean_flame_height_pd_7974
from fsetools.libstd.pd_7974_1_2019 import eq_11_dimensionless_hrr_rectangular
from fsetools.libstd.pd_7974_1_2019 import eq_12_dimensionless_hrr_line
from fsetools.libstd.pd_7974_1_2019 import eq_5_dimensionless_hrr

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import dialog_0602_context as image_context
from fsetoolsGUI.gui.images_base64 import dialog_0602_figure as image_figure
from fsetoolsGUI.gui.layout.ui0602_flame_height import Ui_MainWindow
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Dialog0602(QMainWindow):
    def __init__(self, parent=None):

        # instantiate ui
        super().__init__(
            module_id='0602',
            parent=parent,
            shortcut_Return=self.calculate,
            freeze_window_size=True,
        )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(image_context=image_context,
                                       image_figure=image_figure,)
        for k, v in self.dict_images_pixmap.items():
            ba = QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap()
            self.dict_images_pixmap[k].loadFromData(ba)

        for i in filter_objects_by_name(self.ui.frame_userio, object_types=[QtWidgets.QLineEdit], names=['_out_']):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # set up figures
        # self.ui.label_image_context.setPixmap(
        #     self.make_pixmap_from_fp(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0602-0.png')))
        self.ui.label_image_figure.setPixmap(
            self.make_pixmap_from_fp(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0602-1.png')))

        # set default values
        # todo
        self.change_fire_shape()

        # signal and slots
        self.ui.comboBox_fire_shape.currentIndexChanged.connect(self.change_fire_shape)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_ok.clicked.connect(self.calculate)

    def change_fire_shape(self):
        if self.ui.comboBox_fire_shape.currentIndex() == 0:  # circular fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText('Fire total HRR')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.label_L_A_or_D.setText("Fire diameter")
            self.ui.label_L_B.setDisabled(True)
            self.ui.lineEdit_L_B.setDisabled(True)
            self.ui.label_L_B_unit.setDisabled(True)
        elif self.ui.comboBox_fire_shape.currentIndex() == 1:  # rectangular fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText('Fire total HRR')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW')
            self.ui.label_L_A_or_D.setText(r"Fire's longer dimension")
            self.ui.label_L_B.setDisabled(False)
            self.ui.lineEdit_L_B.setDisabled(False)
            self.ui.label_L_B_unit.setDisabled(False)
        elif self.ui.comboBox_fire_shape.currentIndex() == 2:  # line fire source
            self.ui.label_Q_dot_or_Q_dot_l.setText(r'Fire total HRR per unit length')
            self.ui.label_Q_dot_or_Q_dot_l_unit.setText('kW/m')
            self.ui.label_L_A_or_D.setText(r'Fire length')
            self.ui.label_L_B.setDisabled(True)
            self.ui.lineEdit_L_B.setDisabled(True)
            self.ui.label_L_B_unit.setDisabled(True)
        else:
            self.statusBar().showMessage('Unknown fire shape')

    def example(self):
        self.ui.comboBox_fire_shape.setCurrentIndex(0)
        self.ui.comboBox_fuel_type.setCurrentIndex(0)
        self.ui.lineEdit_Q_dot_or_Q_dot_l.setText('1500')
        self.ui.lineEdit_L_A_or_D.setText('2.5')
        self.ui.lineEdit_rho_0.setText('1.2')
        self.ui.lineEdit_c_p_0.setText('1.0')
        self.ui.lineEdit_T_0.setText('293.15')
        self.ui.lineEdit_g.setText('9.81')

        self.repaint()

    def calculate(self):

        # clear ui outputs
        self.ui.lineEdit_out_Q_dot_star.clear()
        self.ui.lineEdit_out_Z_f.clear()

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

    @property
    def input_parameters(self):
        """Parse inputs from the UI."""

        # parse compulsory parameters
        try:
            Q_dot_or_Q_dot_l = float(self.ui.lineEdit_Q_dot_or_Q_dot_l.text())
            L_A_or_D = float(self.ui.lineEdit_L_A_or_D.text())
            rho_0 = float(self.ui.lineEdit_rho_0.text())
            c_p_0 = float(self.ui.lineEdit_c_p_0.text())
            T_0 = float(self.ui.lineEdit_T_0.text())
            g = float(self.ui.lineEdit_g.text())
            fire_shape = self.ui.comboBox_fire_shape.currentIndex()
            fuel_type = int(self.ui.comboBox_fuel_type.currentIndex())
        except Exception as e:
            raise ValueError(f'Unable to parse parameters from UI')

        # parse optional input parameters
        try:
            L_B = float(self.ui.lineEdit_L_B.text())
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
                flame_height = mean_flame_height_pd_7974(Q_dot_star=Q_dot_star, fuel_type=fuel_type,
                                                         fire_diameter=L_A_or_D)
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

            if flame_height <= 0:
                raise ValueError(
                    'Calculation failed due to unreasonable input parameters, make sure the inputs make a physical sense')
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
            self.ui.lineEdit_out_Q_dot_star.setText(f'{Q_dot_star:.2f}')
        else:
            self.ui.lineEdit_out_Q_dot_star.clear()

        if flame_height:
            self.ui.lineEdit_out_Z_f.setText(f'{flame_height:.2f}')
        else:
            self.ui.lineEdit_out_Z_f.clear()


if __name__ == '__main__':
    from PySide2 import QtWidgets, QtCore
    import PySide2
    import sys

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0602()
    app.show()
    qapp.exec_()
