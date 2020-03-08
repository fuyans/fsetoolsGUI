from fsetools.lib.fse_thermal_radiation import phi_parallel_any_br187, linear_solver

from fsetoolsGUI.gui.images_base64 import dialog_0401_figure as image_figure
from fsetoolsGUI.gui.layout.dialog_0401_br187_parallel_simple import Ui_MainWindow
from fsetoolsGUI.gui.logic.OFRCustom import QMainWindow


class Dialog0401(QMainWindow):
    """0401, for analysis thermal radiation between a rectangular shaped emitter and ...

    Error handling scenarios:
        1.  Input parsing failure due to inappropriate data type, i.e. height = 12.e4 will be not successfully parsed.
        2.  Calculation failure, when to solve separation distance for given unprotected area, reached upper limit of
            the predefined S.
        3.  Calculation failure, when to solve separation distance for given unprotected area, reached lower limit of
            the predefined S.
        4.  Calculation failure, no convergence found.
    """
    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        # instantiation
        super().__init__(
            title='BR 187 Thermal Radiation Calculation (Rectangular and Parallel)',
            parent=parent,
            shortcut_Return=self.calculate
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        self.change_mode_S_and_UA()

        # set up radiation figure
        self.ui.label_image_page.setPixmap(self.make_pixmap_from_base64(image_figure))

        # set up validators
        self.ui.lineEdit_W.setValidator(self._Validator_float_unsigned)
        self.ui.lineEdit_H.setValidator(self._Validator_float_unsigned)
        self.ui.lineEdit_Q.setValidator(self._Validator_float_unsigned)
        self.ui.lineEdit_S_or_UA.setValidator(self._Validator_float_unsigned)

        # signals
        self.ui.comboBox_S_or_UA.currentTextChanged.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_calculate.clicked.connect(self.calculate)
        self.ui.pushButton_test.clicked.connect(self.example)

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.comboBox_S_or_UA.currentIndex() == 0:  # to calculate separation to boundary
            self.ui.label_unit_S_or_UA.setText('m')
            self.ui.comboBox_S_or_UA.setToolTip('Separation distance from emitter to notional boundary.')
            self.ui.comboBox_S_or_UA.setStatusTip('Separation distance from emitter to notional boundary.')
            self.ui.label_out_S_or_UA.setText('Unprotected area')
            self.ui.label_out_S_or_UA_unit.setText('%')

        elif self.ui.comboBox_S_or_UA.currentIndex() == 1:  # to calculate unprotected area percentage
            self.ui.label_unit_S_or_UA.setText('%')
            self.ui.comboBox_S_or_UA.setToolTip('Unprotected area.')
            self.ui.comboBox_S_or_UA.setStatusTip('Unprotected area.')
            self.ui.label_out_S_or_UA.setText('½S, emitter to boundary')
            self.ui.label_out_S_or_UA_unit.setText('m')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    def example(self):

        self.ui.lineEdit_W.setText('10')
        self.ui.lineEdit_H.setText('10')
        self.ui.lineEdit_Q.setText('84')
        self.ui.comboBox_S_or_UA.setCurrentIndex(0)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_S_or_UA.setText('2')

        self.repaint()

    def calculate(self):

        # clear ui output fields

        self.ui.lineEdit_out_S_or_UA.setText('')
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')

        # parse inputs from ui
        try:
            W = float(self.ui.lineEdit_W.text())
            H = float(self.ui.lineEdit_H.text())
            Q = float(self.ui.lineEdit_Q.text())
        except ValueError as e:
            self.statusBar().showMessage(
                'Calculation unsuccessful. '
                'Unable to parse input parameters.'
            )
            self.repaint()
            raise ValueError(e)

        # calculate

        q_target = self.maximum_acceptable_thermal_radiation_heat_flux

        if self.ui.comboBox_S_or_UA.currentIndex() == 0:  # to calculate maximum unprotected area
            S = float(self.ui.lineEdit_S_or_UA.text()) * 2
            if S <= 2.:
                self.statusBar().showMessage(
                    'Calculation incomplete. '
                    'Separation to notional boundary should be > 1.0 m.'
                )
                self.repaint()
                raise ValueError

            try:
                phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=S)
            except ValueError:
                self.statusBar().showMessage(
                    'Calculation incomplete. '
                    'Failed due to an unknown erorr. '
                    'Please raise this issue for further investigation.'
                )
                self.repaint()
                raise ValueError

            q_solved = Q * phi_solved
            if q_solved == 0:
                UA_solved = 100
            else:
                UA_solved = max([min([q_target / q_solved * 100, 100]), 0])

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA_solved:.2f}')

            self.statusBar().showMessage('Calculation complete.')

        # to calculate minimum separation distance to boundary
        elif self.ui.comboBox_S_or_UA.currentIndex() == 1:
            UA = float(self.ui.lineEdit_S_or_UA.text()) / 100.
            if not 0 < UA <= 1:
                self.statusBar().showMessage(
                    'Calculation failed. '
                    'Unprotected area should be greater >0% and <100%.'
                )
                self.repaint()
                raise ValueError

            phi_target = q_target / (Q * UA)

            try:
                S_solved = linear_solver(
                    func=phi_parallel_any_br187,
                    dict_params=dict(W_m=W, H_m=H, w_m=0.5*W, h_m=0.5*H, S_m=0),
                    x_name='S_m',
                    y_target=phi_target,
                    x_upper=1000,
                    x_lower=0.01,
                    y_tol=0.001,
                    iter_max=500,
                    func_multiplier=-1
                )
            except ValueError:
                self.statusBar().showMessage(
                    'Calculation failed. Inspect input parameters.'
                )
                self.repaint()
                raise ValueError
            if S_solved is None:
                self.statusBar().showMessage(
                    'Calculation failed. '
                    'Maximum iteration reached.'
                )
                self.repaint()
                raise ValueError

            phi_solved = phi_parallel_any_br187(W_m=W, H_m=H, w_m=0.5 * W, h_m=0.5 * H, S_m=S_solved)
            q_solved = Q * phi_solved

            if S_solved == 1000:
                self.statusBar().showMessage(
                    'Calculation complete. '
                    'Solver\'s upper limit had reached.'
                )
            elif S_solved == 0.01:
                self.statusBar().showMessage(
                    'Calculation complete. '
                    'Solver\'s lower limit had reached and boundary separation is forced to 1.'
                )
                S_solved = 2
            elif S_solved < 2:
                self.statusBar().showMessage(
                    f'Calculation complete. '
                    f'Forced boundary separation to 1 from {S_solved:.3f} m.'
                )
                S_solved = 2
            else:
                self.statusBar().showMessage(
                    'Calculation complete.'
                )

            self.ui.lineEdit_out_Phi.setText(f'{phi_solved:.4f}')
            self.ui.lineEdit_out_q.setText(f'{q_solved:.2f}')
            self.ui.lineEdit_out_S_or_UA.setText(f'{S_solved / 2:.2f}')
        else:
            raise ValueError('Option unknown.')
        self.repaint()
