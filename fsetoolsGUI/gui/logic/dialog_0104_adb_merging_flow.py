from os.path import join

from PySide2 import QtWidgets

import fsetoolsGUI
from fsetoolsGUI.gui.layout.dialog_0104_merging_flow import Ui_MainWindow
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


class Dialog0104(QMainWindow):
    fp_doc = join(fsetoolsGUI.__root_dir__, 'gui', 'docs', '0104.md')

    def __init__(self, parent=None):
        # instantiation
        super().__init__(
            module_id='0104',
            parent=parent,
            shortcut_Return=self.calculate,
            about_fp_or_md=self.fp_doc,
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
        self.ui.lineEdit_in_W_SE.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_S_up.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_D.setValidator(self._validator_unsigned_float)
        self.ui.lineEdit_in_N.setValidator(self._validator_unsigned_float)

        # signals
        self.ui.pushButton_ok.clicked.connect(self.calculate)
        self.ui.pushButton_example.clicked.connect(self.example)

    def example(self):
        self.ui.lineEdit_in_D.setText('1.9')
        self.ui.lineEdit_in_S_up.setText('1200')
        self.ui.lineEdit_in_W_SE.setText('1050')
        self.ui.lineEdit_in_N.setText('61')

        self.repaint()

    def calculate(self):

        # clear ui output fields
        self.ui.checkBox_out_check.setChecked(False)
        self.ui.lineEdit_out_W_FE.setText('')

        # parse inputs from ui
        try:
            S_up = float(self.ui.lineEdit_in_S_up.text()) * 1e-3
            W_SE = float(self.ui.lineEdit_in_W_SE.text()) * 1e-3
            D = float(self.ui.lineEdit_in_D.text())
            N = float(self.ui.lineEdit_in_N.text()) if self.ui.lineEdit_in_N.isEnabled() else None
        except Exception as e:
            self.statusBar().showMessage(f'Failed to parse input. Error: {e}.')
            self.repaint()
            raise ValueError

        # calculate
        try:
            W_FE, condition_check = clause_2_23_merging_flow(
                N=N,
                D=D,
                S=S_up,
                W_SE=W_SE,
            )
        except Exception as e:
            self.statusBar().showMessage(f'Calculation failed. Error: {e}')
            self.repaint()
            raise ValueError

        self.ui.checkBox_out_check.setChecked(condition_check)
        self.ui.lineEdit_out_W_FE.setText(f'{W_FE * 1e3:.1f}')

        self.statusBar().showMessage('Calculation complete.')
        self.repaint()


if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0104()
    app.show()
    qapp.exec_()

