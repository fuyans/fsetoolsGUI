from fsetools.lib.fse_thermal_radiation import phi_perpendicular_any_br187, linear_solver

from fsetoolsGUI.gui.logic.dialog_0403_br187_parallel_complex import Dialog04


class Dialog0404(Dialog04):
    def __init__(self, parent=None):
        super().__init__(
            module_id='0404',
            parent=parent,
        )

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
                    UA_solved = 100
                else:
                    UA_solved = max([min([Q_a / q_solved * 100, 100]), 0])

        # to calculate minimum separation distance to boundary
        elif UA:

            phi_target = Q_a / (Q * UA)

            try:
                S_solved = linear_solver(
                    func=phi_perpendicular_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=w, h_m=h, S_m=0),
                    x_name='S_m',
                    y_target=phi_target,
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
            q_solved = Q * phi_solved

            if S_solved < 2:
                msg = (f'Calculation complete. Forced boundary separation to 1 from {S_solved:.3f} m.')
                S_solved = 2

        return phi_solved, q_solved, S_solved, UA_solved, msg


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0404()
    app.show()
    qapp.exec_()
