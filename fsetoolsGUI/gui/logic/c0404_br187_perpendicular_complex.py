from os.path import join

from PySide2.QtWidgets import QLabel, QVBoxLayout
from fsetools.lib.fse_thermal_radiation import phi_perpendicular_any_br187, linear_solver

import fsetoolsGUI
from fsetoolsGUI.gui.logic.c0400_br187_base_class import BR187ComplexBaseClass


class App(BR187ComplexBaseClass):
    app_id = '0404'
    app_name_short = 'BR 187\nperp.\neccentric'
    app_name_long = 'BR 187 perpendicular oriented rectangle emitter and eccentric receiver'

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(parent, post_stats)
        # self.ui.label_description.setWordWrap(True)
        # self.ui.label_description.setText(
        #     'This sheet calculates the thermal radiation intensity at a receiver that is perpendicular to '
        #     'a rectangular emitter. Calculation coded in this sheet follows "BR 187 External fire spread" 2nd edition.'
        # )
        # self.init()

        self.ui.p1_description = QLabel(
            'This sheet calculates the thermal radiation intensity at a receiver that is perpendicular to '
            'a rectangular emitter. Calculation coded in this sheet follows "BR 187 External fire spread" 2nd edition.'
        )
        self.ui.p1_description.setFixedWidth(350)
        self.ui.p1_description.setWordWrap(True)
        self.ui.p1_image = QLabel()
        self.ui.p1_image.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0404-1.png'))
        self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
        self.ui.p1_layout.addWidget(self.ui.p1_description)
        self.ui.p1_layout.addWidget(self.ui.p1_image)

    @property
    def input_parameters(self) -> dict:
        input_parameters = super().input_parameters

        # make sure `h` is greater or equal to zero.
        try:
            assert 'h' in input_parameters
        except AssertionError:
            raise ValueError('Missing input parameter h')

        if input_parameters['h'] < 0:
            raise ValueError('Input parameter h can not be negative')

        return input_parameters

    @staticmethod
    def phi_solver(W: float, H: float, w: float, h: float, Q: float, Q_a: float, S=None, UA=None):
        """A wrapper to `phi_perpendicular_any_br187` with error handling and customised IO"""

        # default values

        phi_solved, q_solved, S_solved, UA_solved = [None] * 4
        msg = 'Calculation complete.'
        # phi_solved, solved configuration factor
        # q_solved, solved receiver heat flux
        # S_solved, solved separation distance, surface to surface
        # UA_solved, solved permissible unprotected area
        # msg, a message to indicate calculation status if successful.

        w, h = -w, -h
        # ui convention is that w is the horizontal separation between the receiver and emitter
        # but the calculation function treats w as the x value and emitter has a positive x

        # calculate

        if S:  # to calculate maximum unprotected area
            try:
                phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S)
            except Exception as e:
                raise ValueError(f'Calculation incomplete. {e}')

            if Q:
                # if Q is provided, proceed to calculate q and UA
                q_solved = Q * phi_solved
                if q_solved == 0:
                    UA_solved = 1
                else:
                    UA_solved = max([min([Q_a / q_solved, 1]), 0])

            q_solved *= UA_solved

        # to calculate minimum separation distance to boundary
        elif UA:

            phi_target = Q_a / (Q * UA)

            try:
                S_solved = linear_solver(
                    func=phi_perpendicular_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=w, h_m=h, S_m=0),
                    x_name='S_m',
                    y_target=phi_target - 0.0005,
                    x_upper=1000,
                    x_lower=0.01,
                    y_tol=0.001,
                    iter_max=500,
                    func_multiplier=-1
                )
            except ValueError as e:
                raise ValueError(f'Calculation failed. {e}')
            if S_solved is None:
                raise ValueError('Calculation failed. Maximum iteration reached.')

            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S_solved)
            q_solved = Q * phi_solved * UA

            if S_solved < 2:
                msg = f'Calculation complete. Forced boundary separation to 1 from {S_solved:.3f} m.'
                S_solved = 2

        return phi_solved, q_solved, S_solved, UA_solved, msg

    def example(self):
        self.ui.p2_in_half_S_label.setChecked(True)
        self.change_mode_S_and_UA()
        self.ui.p2_in_W.setText('10')
        self.ui.p2_in_H.setText('6')
        self.ui.p2_in_w.setText('-5')
        self.ui.p2_in_h.setText('0')
        self.ui.p2_in_Q.setText('84')
        self.ui.p2_in_Q_crit.setText('12.6')
        self.ui.p2_in_half_S.setText('1')

        self.repaint()


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
