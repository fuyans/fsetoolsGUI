from os.path import join

from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187, phi_perpendicular_any_br187, linear_solver

import fsetoolsGUI
from fsetoolsGUI.gui.layout.dialog_0403_br187_parallel_complex import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Dialog04(QMainWindow):

    __phi_func = None

    def __init__(self, module_id:str, parent=None):

        super().__init__(
            module_id=module_id,
            parent=parent,
            shortcut_Return=self.calculate,
            about_fp_or_md=join(fsetoolsGUI.__root_dir__, 'gui', 'doc', f'{module_id}.md')
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        if module_id == '0403':
            self.__phi_func = self.__phi_parallel_any_br187
        elif module_id == '0404':
            self.__phi_func = self.__phi_perpendicular_any_br187

        # set up radiation figure
        self.ui.label_image_page.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{module_id}-0.png'))
        self.ui.label_image_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{module_id}-1.png'))

        # set default values
        self.ui.radioButton_in_S.setChecked(True)
        self.change_mode_S_and_UA()

        # signals

        self.ui.lineEdit_in_W.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_H.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_w.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_h.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_Q.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_S.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_UA.textChanged.connect(self.calculate)

        self.ui.radioButton_in_S.toggled.connect(self.change_mode_S_and_UA)
        self.ui.radioButton_in_UA.toggled.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)

    def example(self):

        self.ui.radioButton_in_S.setChecked(True)
        self.ui.lineEdit_in_W.setText('50')
        self.ui.lineEdit_in_H.setText('50')
        self.ui.lineEdit_in_w.setText('0')
        self.ui.lineEdit_in_h.setText('0')
        self.ui.lineEdit_in_Q.setText('84')
        self.ui.lineEdit_in_S.setText('2')
        self.change_mode_S_and_UA()

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.radioButton_in_S.isChecked():  # to calculate separation to boundary
            self.ui.lineEdit_in_UA.setEnabled(False)  # disable UA related inputs
            self.ui.label_in_UA_unit.setEnabled(False)  # disable UA related inputs
            self.ui.lineEdit_in_S.setEnabled(True)  # enable S related inputs
            self.ui.label_in_S_unit.setEnabled(True)  # enable S related inputs
            self.ui.label_out_S_or_UA.setText('Unprotected area')
            self.ui.label_out_S_or_UA_unit.setText('%')
            self.ui.label_out_S_or_UA.setStatusTip('Solved maximum permitted unprotected area')
            self.ui.label_out_S_or_UA.setToolTip('Solved maximum permitted unprotected area')
        elif self.ui.radioButton_in_UA.isChecked():  # to calculate unprotected area percentage
            self.ui.lineEdit_in_S.setEnabled(False)  # disable S related inputs
            self.ui.label_in_S_unit.setEnabled(False)  # disable S related inputs
            self.ui.lineEdit_in_UA.setEnabled(True)  # enable UA related inputs
            self.ui.label_in_UA_unit.setEnabled(True)  # enable UA related inputs
            self.ui.label_out_S_or_UA.setText('½S, emitter to boundary')
            self.ui.label_out_S_or_UA_unit.setText('m')
            self.ui.label_out_S_or_UA.setStatusTip('Solved minimum separation distance.')
            self.ui.label_out_S_or_UA.setToolTip('Solved minimum separation distance.')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    @property
    def input_parameters(self) -> dict:
        """parse input parameters from the ui"""

        # assign default values
        Q_a = 12.6  # acceptable heat flux
        W, H, w, h, S, UA, Q = [None] * 7

        # a helper function to transform string to float with error handling
        def str2float(str: str):
            try:
                return float(str)
            except ValueError:
                return None

        # parse input parameters from ui
        W = str2float(self.ui.lineEdit_in_W.text())
        H = str2float(self.ui.lineEdit_in_H.text())
        w = str2float(self.ui.lineEdit_in_w.text())
        h = str2float(self.ui.lineEdit_in_h.text())
        if self.ui.radioButton_in_S.isChecked():
            S = str2float(self.ui.lineEdit_in_S.text())
            if S:
                # convert surface to relevant boundary to surface to surface distance
                S *= 2.
        elif self.ui.radioButton_in_UA.isChecked():
            UA = str2float(self.ui.lineEdit_in_UA.text())
            if UA:
                # convert % to absolute i.e. 98% -> 0.98
                UA /= 100.
        Q = str2float(self.ui.lineEdit_in_Q.text())

        # validate input values
        self.validate_show_statusBar_msg(W, 'unsigned float', 'W should be greater than 0')
        self.validate_show_statusBar_msg(H, 'unsigned float', 'H should be greater than 0')
        self.validate_show_statusBar_msg(w, 'unsigned float', 'w should be greater than 0')
        self.validate_show_statusBar_msg(h, 'unsigned float', 'h should be greater than 0')
        if S:
            try:
                # check if S provided is greater than S (1 m to the relevant boundary)
                assert S >= 2
            except AssertionError:
                raise ValueError('Separation to relevant boundary should be greater than 1 m')
        if UA:
            try:
                assert all((UA > 0, UA < 1))
            except AssertionError:
                raise ValueError('Unprotected area should be greater than 0 and less than 100 %')
        self.validate_show_statusBar_msg(Q, 'unsigned float', 'Q should be greater than 0')

        try:
            # check if enough inputs are provided for any calculation options
            assert all(i is not None for i in (W, H, w, h))
            # check crucial parameters for any calculation

            if UA:
                # if to calculate the required separation S for a given UA,
                # then Q is also required
                assert Q
        except AssertionError:
            raise ValueError('Not enough input parameters')

        return dict(W=W, H=H, w=w, h=h, S=S, UA=UA, Q_a=Q_a, Q=Q)

    @property
    def output_parameters(self) -> dict:
        return dict()  # currently not used

    @output_parameters.setter
    def output_parameters(self, v: dict):
        try:
            assert all([i in v for i in ('phi', 'q', 'UA', 'S')])
            phi, q, UA, S = v['phi'], v['q'], v['UA'], v['S']
        except KeyError:
            raise KeyError('Not enough output parameters')

        self.ui.lineEdit_out_Phi.setText(f'{phi:.4f}')
        self.ui.lineEdit_out_q.setText(f'{q:.2f}')
        if S:
            self.ui.lineEdit_out_S_or_UA.setText(f'{S:.2f}')
        elif UA:
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA / 2:.2f}')

    def calculate(self):

        # clear ui output fields
        self.ui.lineEdit_out_S_or_UA.clear()
        self.ui.lineEdit_out_Phi.clear()
        self.ui.lineEdit_out_q.clear()

        # --------------------
        # Parse inputs from ui
        # --------------------
        try:
            input_parameters = self.input_parameters
        except ValueError as e:
            self.statusBar().showMessage(str(e))
            self.repaint()
            return


        # Calculation

        try:
            phi, q, S, UA, msg = self.__phi_func(**input_parameters)
            self.statusBar().showMessage(msg)
            # if calculation is successful: assign to output parameters for later use and show a message to user.
        except Exception as e:
            self.statusBar().showMessage(str(e))
            self.repaint()
            return

        # Assign outputs

        try:
            self.output_parameters = dict(phi=phi, q=q, S=S, UA=UA)
        except Exception as e:
            self.statusBar().showMessage(str(e))
            self.repaint()
            return

        self. repaint()

    @staticmethod
    def __phi_perpendicular_any_br187(W:float, H:float, w:float, h:float, Q:float, Q_a:float, S=None, UA=None):
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

    @staticmethod
    def __phi_parallel_any_br187(W:float, H:float, w:float, h:float, Q:float, Q_a:float, S=None, UA=None):
        """A wrapper to `phi_parallel_any_br187` with error handling and customised IO"""

        # default values

        phi_solved, q_solved, S_solved, UA_solved = [None] * 4
        msg = 'Calculation complete.'
        # phi_solved, solved configuration factor
        # q_solved, solved receiver heat flux
        # S_solved, solved separation distance, surface to surface
        # UA_solved, solved permissible unprotected area
        # msg, a message to indicate calculation status if successful.

        if S:  # to calculate maximum unprotected area
            try:
                phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5*W+w, h_m=0.5*H+h, S_m=S)
            except Exception as e:
                raise ValueError(f'Calculation incomplete. {str(e)}')

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
                    func=phi_parallel_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=0.5*W+w, h_m=0.5*H+h, S_m=S),
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

            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5*W+w, h_m=0.5*H+h, S_m=S_solved)
            q_solved = Q * phi_solved

            if S_solved < 2:
                msg = (f'Calculation complete. Forced boundary separation to 1 from {S_solved:.3f} m.')
                S_solved = 2

        return phi_solved, q_solved, S_solved, UA_solved, msg


class Dialog0403(Dialog04):
    def __init__(self):
        super().__init__(module_id='0403')


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0403()
    app.show()
    qapp.exec_()
