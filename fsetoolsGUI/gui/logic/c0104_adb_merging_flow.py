from os.path import join

from PySide2 import QtWidgets

import fsetoolsGUI
from fsetoolsGUI.gui.layout.i0104_merging_flow import Ui_MainWindow
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


def clause_2_23_merging_flow(N: float, S: float, D: float, W_SE: float) -> tuple:
    """Calculation follows section 2.23 and diagram 2.6 in Approved Document B vol. 2 (2019)"""

    if N > 60 and D < 2:
        condition = True
        W = S + W_SE
    else:
        condition = False
        W = ((N / 2.5) + (60 * S)) / 80

    return W, condition


class App(QMainWindow):

    def __init__(self, parent=None):
        # instantiation
        super().__init__(
            module_id='0104',
            parent=parent,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

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

        # set up context image
        self.ui.label_image_figure.setPixmap(self.make_pixmap_from_fp(join(fsetoolsGUI.__root_dir__, 'gui', 'images', '0104-1.png')))

        # placeholder texts
        # self.ui.lineEdit_in_D.setPlaceholderText('1.9')
        # self.ui.lineEdit_in_S_up.setPlaceholderText('1200')
        # self.ui.lineEdit_in_W_SE.setPlaceholderText('1050')
        # self.ui.lineEdit_in_N.setPlaceholderText('61')

        # set up validators
        # DEPRECIATED, NO GOOD TO IMPOSE RESTRICTIONS WITHOUT ALERTING USER
        # self.ui.lineEdit_in_W_SE.setValidator(self._validator_unsigned_float)
        # self.ui.lineEdit_in_S_up.setValidator(self._validator_unsigned_float)
        # self.ui.lineEdit_in_D.setValidator(self._validator_unsigned_float)
        # self.ui.lineEdit_in_N.setValidator(self._validator_unsigned_float)

        # signals
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.lineEdit_in_D.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_S_up.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_W_SE.textChanged.connect(self.calculate)
        self.ui.lineEdit_in_N.textChanged.connect(self.calculate)


    def example(self):
        self.ui.lineEdit_in_D.setText('1.9')
        self.ui.lineEdit_in_S_up.setText('1200')
        self.ui.lineEdit_in_W_SE.setText('1050')
        self.ui.lineEdit_in_N.setText('61')

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
            S_up = str2float(self.ui.lineEdit_in_S_up.text())
            if S_up is not None:
                S_up /= 1e3
            W_SE = str2float(self.ui.lineEdit_in_W_SE.text())
            if W_SE is not None:
                W_SE /= 1e3
            D = str2float(self.ui.lineEdit_in_D.text())
            N = str2float(self.ui.lineEdit_in_N.text())
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

        self.ui.checkBox_out_check.setChecked(condition_check)
        self.ui.lineEdit_out_W_FE.setText(f'{W_FE * 1e3:.1f}')

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

    def calculate(self):

        # clear ui output fields
        self.ui.checkBox_out_check.setChecked(False)
        self.ui.lineEdit_out_W_FE.clear()

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
    app = App()
    app.show()
    qapp.exec_()

