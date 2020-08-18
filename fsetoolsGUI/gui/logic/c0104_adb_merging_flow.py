from os.path import join

from PySide2 import QtWidgets
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QLabel, QCheckBox

import fsetoolsGUI
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass


def clause_2_23_merging_flow(N: float, S: float, D: float, W_SE: float) -> tuple:
    """Calculation follows section 2.23 and diagram 2.6 in Approved Document B vol. 2 (2019)"""

    if N > 60 and D < 2:
        condition = True
        W = S + W_SE
    else:
        condition = False
        W = ((N / 2.5) + (60 * S)) / 80

    return W, condition


class App(AppBaseClass):
    app_id = '0104'
    app_name_short = 'ADB\nmerging\nflow'
    app_name_long = 'ADB merging flow at final exit level'

    def __init__(self, parent=None, post_stats: bool = True):

        # instantiation
        super().__init__(parent, post_stats)

        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p1_description = QLabel(
            'This sheet calculates the merging flow at final exit level in accordance with Section 2.23 in '
            'Approved Document B, Volume 2'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.label_image_figure = QLabel()
        self.ui.label_image_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0104-1.png'))
        self.ui.p1_layout.addWidget(self.ui.label_image_figure)

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'p2_in_S_up', 'S<sub>up</sub>, upper stair width', 'mm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'p2_in_D', 'D, door separation', 'm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'p2_in_W_SE', 'W<sub>SE</sub>, door width from current level', 'mm')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_in_N', 'N, no. pers. from exit level', 'person')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 5, 0, 1, 3)
        self.ui.p2_out_check = QCheckBox('Are "D>2" and "N>60" all true?')
        self.ui.p2_out_check.setDisabled(True)
        self.ui.p2_layout.addWidget(self.ui.p2_out_check, 6, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_out_W_FE', 'W<sub>FE</sub>, solved min. exit width', 'mm')
        self.ui.p2_out_W_FE.setReadOnly(True)

        # set up context image
        self.ui.label_image_figure.setPixmap(self.make_pixmap_from_fp(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0104-1.png')))

    def example(self):
        self.ui.p2_in_D.setText('1.9')
        self.ui.p2_in_S_up.setText('1200')
        self.ui.p2_in_W_SE.setText('1050')
        self.ui.p2_in_N.setText('61')

        self.repaint()

    @property
    def input_parameters(self):

        # ====================
        # parse values from ui
        # ====================

        def str2float(v):
            try:
                return float(v)
            except Exception as e:
                return None

        try:
            S_up = str2float(self.ui.p2_in_S_up.text())
            if S_up is not None:
                S_up /= 1e3
            W_SE = str2float(self.ui.p2_in_W_SE.text())
            if W_SE is not None:
                W_SE /= 1e3
            D = str2float(self.ui.p2_in_D.text())
            N = str2float(self.ui.p2_in_N.text())
        except Exception as e:
            raise e

        # =============================================
        # check if enough input parameters are provided
        # =============================================

        try:
            assert all([i is not None for i in [S_up, W_SE, D, N]])
        except Exception:
            raise ValueError('Not enough input parameters are provided')

        # ====================================
        # validate individual input parameters
        # ====================================

        if S_up is not None:
            self.validate(S_up, 'unsigned float', 'Stair width to upper levels should be an unsigned float')
        if W_SE is not None:
            self.validate(W_SE, 'unsigned float', 'Door width from exit level should be an unsigned float')
        if D is not None:
            self.validate(D, 'unsigned float', 'Distance between doors should be an unsigned float')
        if N is not None:
            self.validate(N, 'unsigned float', 'No. of persons from final exit level should be an unsigned float')

        return dict(S_up=S_up, D=D, N=N, W_SE=W_SE)

    @property
    def output_parameters(self):
        return

    @output_parameters.setter
    def output_parameters(self, v):

        try:
            W_FE = v['W_FE']
            condition_check = v['condition_check']
        except KeyError:
            raise KeyError('Not enough parameters to self.output_parameters')

        self.ui.p2_out_check.setChecked(condition_check)
        self.ui.p2_out_W_FE.setText(f'{W_FE * 1e3:.1f}')

    @staticmethod
    def __calculate_merging_flow(S_up, D, N, W_SE):

        try:
            W_FE, condition_check = clause_2_23_merging_flow(
                N=N,
                D=D,
                S=S_up,
                W_SE=W_SE,
            )
        except Exception as e:
            raise e

        return dict(W_FE=W_FE, condition_check=condition_check)

    def ok(self):

        # clear ui output fields
        self.ui.p2_out_check.setChecked(False)
        self.ui.p2_out_W_FE.clear()

        # parse inputs from ui
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to parse input parameters. {str(e)}')
            return

        # calculate
        try:
            output_parameters = self.__calculate_merging_flow(**input_parameters)
        except Exception as e:
            self.statusBar().showMessage(f'Calculation error. {str(e)}')
            return

        # results to ui
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'Unable to cast results to UI. {str(e)}')
            return

        self.repaint()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
