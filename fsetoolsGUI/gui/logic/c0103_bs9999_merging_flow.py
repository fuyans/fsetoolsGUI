from os.path import join

from PySide2 import QtWidgets, QtGui
from fsetools.libstd.bs_9999_2017 import (
    clause_15_6_6_e_merging_flow_1, clause_15_6_6_e_merging_flow_2, clause_15_6_6_e_merging_flow_3
)

import fsetoolsGUI
from fsetoolsGUI.gui.layout.i0103_merging_flow import Ui_MainWindow
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Dialog0103(QMainWindow):

    def __init__(self, parent=None):
        module_id = '0103'

        # instantiation
        super().__init__(
            module_id=module_id,
            parent=parent,
            shortcut_Return=self.calculate,
            freeze_window_size=True,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_figure_1=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{module_id}-1-1.png'),
            image_figure_2=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{module_id}-1-2.png'),
            image_figure_3=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{module_id}-1-3.png'),
        )
        for k, v in self.dict_images_pixmap.items():
            # ba = QtCore.QByteArray.fromBase64(v)
            self.dict_images_pixmap[k] = QtGui.QPixmap(v)
            # self.dict_images_pixmap[k].loadFromData(ba)

        # set all outputs lineedit to readonly
        for i in filter_objects_by_name(
                self.ui.frame_userio,
                object_types=[QtWidgets.QLineEdit, QtWidgets.QCheckBox],
                names=['_out_']
        ):
            try:
                i.setReadOnly(True)
            except AttributeError:
                i.setEnabled(False)

        # entry default values
        self.ui.radioButton_opt_scenario_1.setChecked(True)
        self.change_option_scenarios()

        # placeholder texts
        # self.ui.lineEdit_in_S_up.setPlaceholderText('mm')
        # self.ui.lineEdit_in_S_dn.setPlaceholderText('mm')
        # self.ui.lineEdit_in_W_SE.setPlaceholderText('mm')
        # self.ui.lineEdit_in_D.setPlaceholderText('m')
        # self.ui.lineEdit_in_B.setPlaceholderText('person')
        # self.ui.lineEdit_in_N.setPlaceholderText('person')
        # self.ui.lineEdit_in_X.setPlaceholderText('mm/person')

        # signals
        self.ui.radioButton_opt_scenario_1.toggled.connect(self.change_option_scenarios)
        self.ui.radioButton_opt_scenario_2.toggled.connect(self.change_option_scenarios)
        self.ui.radioButton_opt_scenario_3.toggled.connect(self.change_option_scenarios)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_about.clicked.connect(self.show_about)

        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.lineEdit_in_S_up.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_S_dn.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_W_SE.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_D.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_B.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_N.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_X.textChanged.connect(self.calculate)

    def change_option_scenarios(self):
        """When mode changes, turn off (grey them out) not required inputs and clear their value."""

        # enable everything in input group to start with.
        # ui items will be disabled for scenario 1 or 2 (if applicable) below.
        list_obj = filter_objects_by_name(
            self.ui.frame_userio, [QtWidgets.QLabel, QtWidgets.QLineEdit],
            ['_in_S_dn', '_in_W_SE', '_in_B', '_in_N']
        )
        for i in list_obj:
            i.setEnabled(True)
            if isinstance(i, QtWidgets.QLineEdit):
                if i.text() == ' ':
                    i.setText('')

        # disable items in accordance with the selected mode
        if self.ui.radioButton_opt_scenario_1.isChecked():  # scenario 1, flow from upper levels + ground floor
            # get items that to be processed
            list_obj = filter_objects_by_name(
                self.ui.frame_userio, [QtWidgets.QLabel, QtWidgets.QLineEdit], ['_in_S_dn', '_in_B']
            )
            # disable items that are not required in scenario 1
            for i in list_obj:
                if isinstance(i, QtWidgets.QLineEdit):
                    i.setText(' ')
                i.setEnabled(False)
            # set figure to scenario 1
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])

        elif self.ui.radioButton_opt_scenario_2.isChecked():  # scenario 2, flow from upper levels + basement
            list_obj = filter_objects_by_name(
                self.ui.frame_userio, [QtWidgets.QLabel, QtWidgets.QLineEdit], ['_in_W_SE', '_in_N']
            )
            for i in list_obj:
                i.setEnabled(False)
                if isinstance(i, QtWidgets.QLineEdit):
                    i.setText(' ')
            # set figure to scenario 2
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])

        else:
            # set figure to scenario 3
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_3'])

        self.repaint()

    def example(self):
        self.ui.lineEdit_in_X.setText('3.06')
        self.ui.lineEdit_in_D.setText('2.1')
        self.ui.lineEdit_in_S_up.setText('1400')
        self.ui.lineEdit_in_N.setText('270')
        self.ui.lineEdit_in_W_SE.setText('1050')

        self.ui.radioButton_opt_scenario_1.setChecked(True)

        self.repaint()

    @property
    def input_parameters(self):
        """parse input parameters from ui."""

        S_up, S_dn, B, X, D, N, W_SE, scenario = [None] * 8

        def str2float(v):
            try:
                return float(v)
            except Exception as e:
                return None

        # parse values from ui
        try:
            S_up = str2float(self.ui.lineEdit_in_S_up.text())
            if S_up is not None:
                S_up /= 1e3
            S_dn = str2float(self.ui.lineEdit_in_S_dn.text())
            if S_dn is not None:
                S_dn /= 1e3
            B = str2float(self.ui.lineEdit_in_B.text())
            X = str2float(self.ui.lineEdit_in_X.text())
            if X is not None:
                X /= 1e3
            D = str2float(self.ui.lineEdit_in_D.text())
            N = str2float(self.ui.lineEdit_in_N.text())
            W_SE = str2float(self.ui.lineEdit_in_W_SE.text())
            if W_SE is not None:
                W_SE /= 1e3
        except Exception as e:
            raise e

        # verify necessary input parameters
        try:
            if self.ui.radioButton_opt_scenario_1.isChecked():
                assert all([i is not None for i in [S_up, W_SE, D, N, X]])
                scenario = 1
            elif self.ui.radioButton_opt_scenario_2.isChecked():
                assert all([i is not None for i in [S_up, S_dn, D, B, X]])
                scenario = 2
            elif self.ui.radioButton_opt_scenario_3.isChecked():
                assert all([i is not None for i in [S_up, S_dn, W_SE, D, B, N, X]])
                scenario = 3
        except Exception as e:
            raise ValueError('Not enough input parameters provided')

        # validate individual input parameters
        if S_up is not None:
            self.validate(S_up, 'unsigned float', 'Stair width to upper levels should be an unsigned float')
        if S_dn is not None:
            self.validate(S_dn, 'unsigned float', 'Stair width to lower levels should be an unsigned float')
        if W_SE is not None:
            self.validate(W_SE, 'unsigned float', 'Door width from exit level should be an unsigned float')
        if D is not None:
            self.validate(D, 'unsigned float', 'Distance between doors should be an unsigned float')
        if B is not None:
            self.validate(B, 'unsigned float', 'No. of persons from lower levels should be an unsigned float')
        if N is not None:
            self.validate(N, 'unsigned float', 'No. of persons from final exit level should be an unsigned float')
        if X is not None:
            self.validate(X, 'unsigned float', 'Exit capacity factor should be an unsigned float')

        return dict(S_up=S_up, S_dn=S_dn, B=B, X=X, D=D, N=N, W_SE=W_SE, scenario=scenario)

    @staticmethod
    def __calculate_merging_flow(S_up, S_dn, B, X, D, N, W_SE, scenario):
        """A wrapper function for `clause_15_6_6_e_merging_flow_1` with error handling etc"""

        W_FE, condition_check = None, None

        # calculate
        if scenario == 1:
            W_FE, condition_check = clause_15_6_6_e_merging_flow_1(
                N=N,
                X=X,
                D=D,
                S_up=S_up,
                W_SE=W_SE,
            )
        elif scenario == 2:
            print(B, D)
            W_FE, condition_check = clause_15_6_6_e_merging_flow_2(
                B=B,
                X=X,
                D=D,
                S_up=S_up,
                S_dn=S_dn,
            )
            print(W_FE, condition_check)
        elif scenario == 3:
            W_FE, condition_check = clause_15_6_6_e_merging_flow_3(
                B=B,
                X=X,
                D=D,
                S_up=S_up,
                S_dn=S_dn,
                N=N,
                W_SE=W_SE,
            )

        if W_FE is None and condition_check is None:
            raise ValueError('Unknown scenario.')

        return dict(W_FE=W_FE, condition_check=condition_check)

    @property
    def output_parameters(self):
        return

    @output_parameters.setter
    def output_parameters(self, v):

        condition_check = v['condition_check']
        W_FE = v['W_FE']

        self.ui.checkBox_out_check.setChecked(condition_check)
        self.ui.lineEdit_out_W_FE.setText(f'{W_FE * 1e3:.1f}')

    def calculate(self):

        # clear ui output fields
        self.ui.checkBox_out_check.setChecked(False)
        self.ui.lineEdit_out_W_FE.clear()

        # parse inputs from ui
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input. Error: {str(e)}.')
            return

        # calculate
        try:
            output_parameters = self.__calculate_merging_flow(**input_parameters)
            self.statusBar().showMessage('Calculation complete.')
        except Exception as e:
            self.statusBar().showMessage(f'Error: {str(e)}')
            return

        # cast outputs to ui
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to cast results to UI. Error: {str(e)}')

        self.repaint()


if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0103()
    app.show()
    qapp.exec_()

