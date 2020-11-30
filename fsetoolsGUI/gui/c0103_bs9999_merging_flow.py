from os.path import join

from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QRadioButton, QCheckBox
from fsetools.libstd.bs_9999_2017 import (
    clause_15_6_6_e_merging_flow_1, clause_15_6_6_e_merging_flow_2, clause_15_6_6_e_merging_flow_3
)

import fsetoolsGUI
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass


class App(AppBaseClass):
    app_id = '0103'
    app_name_short = 'BS 9999\nmerging\nflow'
    app_name_long = 'BS 9999 Merging flow at final exit level'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_description = QLabel(
            'This sheet calculates the merging flow at final exit level in accordance with Section 15.6.6 in '
            'BS 9999:2017'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.label_image_figure = QLabel()
        self.ui.p1_layout.addWidget(self.ui.label_image_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Options</b>'), 0, 0, 1, 3)
        self.ui.p2_in_scenario_1 = QRadioButton('Scenario 1. From upper and current levels', self.ui.page_2)
        self.ui.p2_in_scenario_2 = QRadioButton('Scenario 2. From upper and lower levels', self.ui.page_2)
        self.ui.p2_in_scenario_3 = QRadioButton('Scenario 3. From all levels', self.ui.page_2)
        self.ui.p2_layout.addWidget(self.ui.p2_in_scenario_1, 1, 0, 1, 3)
        self.ui.p2_layout.addWidget(self.ui.p2_in_scenario_2, 2, 0, 1, 3)
        self.ui.p2_layout.addWidget(self.ui.p2_in_scenario_3, 3, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 4, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_in_S_up', 'S<sub>up</sub>, upper stair width', 'mm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_in_S_dn', 'S<sub>dn</sub>, lower stair width', 'mm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_in_W_SE', 'W<sub>SE</sub>, door width', 'mm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_in_D', 'D, door separation', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 9, 'p2_in_B', 'B, no. pers. from lower levels', 'person')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_in_N', 'N, no. pers. from exit level', 'person')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_in_X', 'X, exit capacity factor', 'mm/pers.')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 12, 0, 1, 3)
        self.ui.p2_out_check = QCheckBox('Are "(B+N)>60" and "D<2" all true?')
        self.ui.p2_out_check.setDisabled(True)
        self.ui.p2_out_check.setStyleSheet('QCheckBox{color:"black"}')
        self.ui.p2_layout.addWidget(self.ui.p2_out_check, 13, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 14, 'p2_out_W_FE', 'W<sub>FE</sub>, solved min. exit width', 'mm')
        self.ui.p2_out_W_FE.setReadOnly(True)

        self.ui.p2_in_X.setToolTip('A1 3.3,\tA2 3.6,\tA3 4.6\nB1 3.6,\tB2 4.1,\tB3 6.0\nC1 3.6,\tC2 4.1,\tC3 6.0')

        # construct pixmaps that are used in this app
        self.dict_images_pixmap = dict(
            image_figure_1=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1-1.png'),
            image_figure_2=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1-2.png'),
            image_figure_3=join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1-3.png'),
        )
        for k, v in self.dict_images_pixmap.items():
            self.dict_images_pixmap[k] = QtGui.QPixmap(v)

        # entry default values
        self.ui.p2_in_scenario_1.setChecked(True)
        self.change_option_scenarios()

        # signals
        self.ui.p2_in_scenario_1.toggled.connect(self.change_option_scenarios)
        self.ui.p2_in_scenario_2.toggled.connect(self.change_option_scenarios)
        self.ui.p2_in_scenario_3.toggled.connect(self.change_option_scenarios)

    def change_option_scenarios(self):
        """When mode changes, turn off (grey them out) not required inputs and clear their value."""

        self.ui.p2_out_W_FE.setText('')

        # disable items in accordance with the selected mode
        if self.ui.p2_in_scenario_1.isChecked():  # scenario 1, flow from upper levels + ground floor
            # get items that to be processed
            self.ui.p2_in_S_dn.setEnabled(False)
            self.ui.p2_in_B.setEnabled(False)
            self.ui.p2_in_W_SE.setEnabled(True)
            self.ui.p2_in_N.setEnabled(True)

            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_1'])

        elif self.ui.p2_in_scenario_2.isChecked():  # scenario 2, flow from upper levels + basement
            self.ui.p2_in_S_dn.setEnabled(True)
            self.ui.p2_in_B.setEnabled(True)
            self.ui.p2_in_W_SE.setEnabled(False)
            self.ui.p2_in_N.setEnabled(False)

            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_2'])

        else:
            # set figure to scenario 3
            self.ui.p2_in_S_dn.setEnabled(True)
            self.ui.p2_in_B.setEnabled(True)
            self.ui.p2_in_W_SE.setEnabled(True)
            self.ui.p2_in_N.setEnabled(True)
            self.ui.label_image_figure.setPixmap(self.dict_images_pixmap['image_figure_3'])

        self.repaint()

    def example(self):
        self.ui.p2_in_X.setText('3.06')
        self.ui.p2_in_D.setText('2.1')
        self.ui.p2_in_S_up.setText('1400')
        self.ui.p2_in_N.setText('270')
        self.ui.p2_in_W_SE.setText('1050')

        self.ui.p2_in_scenario_1.setChecked(True)

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
            S_up = str2float(self.ui.p2_in_S_up.text())
            if S_up is not None:
                S_up /= 1e3
            S_dn = str2float(self.ui.p2_in_S_dn.text())
            if S_dn is not None:
                S_dn /= 1e3
            B = str2float(self.ui.p2_in_B.text())
            X = str2float(self.ui.p2_in_X.text())
            if X is not None:
                X /= 1e3
            D = str2float(self.ui.p2_in_D.text())
            N = str2float(self.ui.p2_in_N.text())
            W_SE = str2float(self.ui.p2_in_W_SE.text())
            if W_SE is not None:
                W_SE /= 1e3
        except Exception as e:
            raise e

        # verify necessary input parameters
        try:
            if self.ui.p2_in_scenario_1.isChecked():
                assert all([i is not None for i in [S_up, W_SE, D, N, X]])
                scenario = 1
            elif self.ui.p2_in_scenario_2.isChecked():
                assert all([i is not None for i in [S_up, S_dn, D, B, X]])
                scenario = 2
            elif self.ui.p2_in_scenario_3.isChecked():
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

        self.ui.p2_out_check.setChecked(condition_check)
        self.ui.p2_out_W_FE.setText(f'{W_FE * 1e3:.1f}')

    def ok(self):

        # clear ui output fields
        self.ui.p2_out_check.setChecked(False)
        self.ui.p2_out_W_FE.clear()

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
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
