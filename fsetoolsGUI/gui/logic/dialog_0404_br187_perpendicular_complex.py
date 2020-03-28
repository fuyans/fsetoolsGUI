from os.path import join

from PySide2 import QtCore
from fsetools.lib.fse_thermal_radiation import phi_perpendicular_any_br187, linear_solver

import fsetoolsGUI
from fsetoolsGUI.gui.layout.dialog_0403_br187_parallel_complex import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Signals(QtCore.QObject):
    __calculate_silent = QtCore.Signal(bool)

    @property
    def update_progress_bar_signal(self):
        return self.__update_progress_bar_signal

    @property
    def calculation_complete(self):
        return self.__calculation_complete



class Dialog0404(QMainWindow):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6
    fp_doc = join(fsetoolsGUI.__root_dir__, 'gui', 'docs', '0404.md')  # doc file path

    def __init__(self, parent=None):
        super().__init__(
            id='0404',
            parent=parent,
            shortcut_Return=self.calculate,
            about_fp_or_md=self.fp_doc
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # set up radiation figure
        self.ui.label_image_page.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0404-0.png'))
        self.ui.label_image_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0404-1.png'))

        # set up validators
        self.ui.lineEdit_in_W.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_H.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_w.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_h.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_Q.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_S.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_UA.setValidator(self._validator_unsigned_float)

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

    def calculate(self, suppress_feedback: bool = False):
        print('hello' * 5, suppress_feedback)

        # parse inputs from ui
        try:
            W = float(self.ui.lineEdit_in_W.text())
            H = float(self.ui.lineEdit_in_H.text())
            w = float(self.ui.lineEdit_in_w.text())
            h = float(self.ui.lineEdit_in_h.text())
            if self.ui.radioButton_in_S.isChecked():
                S = float(self.ui.lineEdit_in_S.text()) * 2.
                UA = None
            elif self.ui.radioButton_in_UA.isChecked():
                S = None
                UA = float(self.ui.lineEdit_in_UA.text()) / 100.
        except ValueError as e:
            self.statusBar().showMessage(
                'Calculation unsuccessful. '
                'Unable to parse input parameters.'
            )
            self.repaint()
            raise e

        try:
            Q = float(self.ui.lineEdit_in_Q.text())
        except ValueError:
            Q = None

        # clear ui output fields

        self.ui.lineEdit_out_S_or_UA.setText('')
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')

        # Calculation

        print(Q)
        try:
            phi, q, S_or_UA, msg = self.__calculate_phi(W, H, w, h, Q, 12.6, S, UA)
            self.statusBar().showMessage(msg)

        except Exception as e:
            self.statusBar().showMessage(str(e))
            raise e

        # Assign outputs

        if self.ui.radioButton_in_S.isChecked():  # to calculate maximum unprotected area
            if phi:
                self.ui.lineEdit_out_Phi.setText(f'{phi:.4f}')
            if q:
                self.ui.lineEdit_out_q.setText(f'{q:.2f}')
            if S_or_UA:
                self.ui.lineEdit_out_S_or_UA.setText(f'{S_or_UA:.2f}')

        # to calculate minimum separation distance to boundary
        elif self.ui.radioButton_in_UA.isChecked():
            if phi:
                self.ui.lineEdit_out_Phi.setText(f'{phi:.4f}')
            if q:
                self.ui.lineEdit_out_q.setText(f'{q:.2f}')
            if S_or_UA:
                self.ui.lineEdit_out_S_or_UA.setText(f'{S_or_UA / 2:.2f}')

        self.repaint()

    @staticmethod
    def __calculate_phi(W, H, w, h, Q, q_target, S=None, UA=None):

        # calculate
        msg = None

        if S:  # to calculate maximum unprotected area
            if S <= 2.:
                raise ValueError(
                    'Calculation incomplete. '
                    'Separation to notional boundary should be > 1.0 m.')
            try:
                phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S)
            except ValueError:
                raise ValueError(
                    'Calculation incomplete. '
                    'Failed due to an unknown erorr. '
                    'Please raise this issue for further investigation.'
                )

            if Q:
                # if Q is provided, proceed to calculate q and UA
                q_solved = Q * phi_solved
                if q_solved == 0:
                    UA_solved = 100
                else:
                    UA_solved = max([min([q_target / q_solved * 100, 100]), 0])

                return phi_solved, q_solved, UA_solved, msg
            else:
                # if Q is not provided, instead of raise an error, return phi only
                return phi_solved, None, None, msg

        # to calculate minimum separation distance to boundary
        elif UA:
            if not 0 < UA <= 1:
                raise ValueError(
                    'Calculation failed. '
                    'Unprotected area should be >0 and ≤100 %.'
                )

            if Q is None:
                # if Q is not provided, raise
                raise ValueError('Calculation failed. Unable to parse Q.')

            phi_target = q_target / (Q * UA)

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
            except ValueError:
                raise ValueError(
                    'Calculation failed. Inspect input parameters.'
                )
            if S_solved is None:
                raise ValueError(
                    'Calculation failed. '
                    'Maximum iteration reached.'
                )

            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S_solved)
            q_solved = Q * phi_solved

            if S_solved == 1000:
                msg = (
                    'Calculation complete. '
                    'Solver\'s upper limit had reached.'
                )
            elif S_solved == 0.01:
                msg = (
                    'Calculation complete. '
                    'Solver\'s lower limit had reached and boundary separation is forced to 1.'
                )
                S_solved = 2
            elif S_solved < 2:
                msg = (
                    f'Calculation complete. '
                    f'Forced boundary separation to 1 from {S_solved:.3f} m.'
                )
                S_solved = 2
            else:
                msg = 'Calculation complete.'

            return phi_solved, q_solved, S_solved, msg


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0404()
    app.show()
    qapp.exec_()
