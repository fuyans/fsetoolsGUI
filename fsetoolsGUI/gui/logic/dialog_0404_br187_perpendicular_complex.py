from fsetools.lib.fse_thermal_radiation import phi_perpendicular_any_br187, linear_solver

from fsetoolsGUI.gui.images_base64 import dialog_0404_figure as image_figure
from fsetoolsGUI.gui.images_base64 import dialog_0404_page as image_page
from fsetoolsGUI.gui.layout.dialog_0403_br187_parallel_complex import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Dialog0404(QMainWindow):
    maximum_acceptable_thermal_radiation_heat_flux = 12.6

    def __init__(self, parent=None):
        super().__init__(
            id='0404',
            parent=parent,
            title='BR 187 Thermal Radiation Calculator (Rectangular and Perpendicular)',
            shortcut_Return=self.calculate
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # set up radiation figure
        self.ui.label_image_figure.setPixmap(self.make_pixmap_from_base64(image_figure))
        self.ui.label_image_page.setPixmap(self.make_pixmap_from_base64(image_page))

        self.ui.comboBox_S_or_UA.currentTextChanged.connect(self.change_mode_S_and_UA)
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)

    def example(self):

        self.ui.lineEdit_W.setText('50')
        self.ui.lineEdit_H.setText('50')
        self.ui.lineEdit_w.setText('0')
        self.ui.lineEdit_h.setText('0')
        self.ui.lineEdit_Q.setText('84')
        self.ui.comboBox_S_or_UA.setCurrentIndex(0)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_S_or_UA.setText('2')

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.comboBox_S_or_UA.currentIndex() == 0:  # to calculate separation to boundary
            self.ui.label_unit_S_or_UA.setText('m')
            self.ui.label_out_S_or_UA.setText('Unprotected area')
            self.ui.label_out_S_or_UA_unit.setText('%')
            self.ui.label_out_S_or_UA.setToolTip('Unprotected area')

        elif self.ui.comboBox_S_or_UA.currentIndex() == 1:  # to calculate unprotected area percentage
            self.ui.label_unit_S_or_UA.setText('%')
            self.ui.label_out_S_or_UA.setText('½S, emitter to boundary')
            self.ui.label_out_S_or_UA_unit.setText('m')
            self.ui.label_out_S_or_UA.setToolTip('Separation distance from emitter to notional boundary')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

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
            w = float(self.ui.lineEdit_w.text())
            h = float(self.ui.lineEdit_h.text())
            Q = float(self.ui.lineEdit_Q.text())
        except ValueError:
            self.statusBar().showMessage(
                'Calculation unsuccessful. '
                'Unable to parse input parameters.'
            )
            self.repaint()
            raise ValueError

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
                phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S)
            except ValueError:
                self.statusBar().showMessage(
                    'Calculation incomplete. '
                    'Failed due to an unknown error. '
                    'Please raise this issue for further investigation.'
                )
                self.repaint()
                raise ValueError

            q_solved = Q * phi_solved
            if q_solved == 0:
                UA_solved = 100
            else:
                UA_solved = max([min([q_target / q_solved * 100, 100]), 0])
            print(phi_solved)
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

            phi_solved = phi_perpendicular_any_br187(W_m=W, H_m=H, w_m=w, h_m=h, S_m=S_solved)
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

        self.repaint()


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0404()
    app.show()
    qapp.exec_()
