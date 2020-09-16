import threading
from os.path import realpath, dirname

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QLineEdit
from sfeprapy.mcs0.mcs0_calc import MCS0

from fsetoolsGUI import logger
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter, ProgressBar


class App(AppBaseClass):
    app_id = '0640'
    app_name_short = 'PRAPY\nMCS0\nsimulator'
    app_name_long = 'SFEPRAPY MCS0 Monte Carlo Simulation method 0'

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.__progress_bar = ProgressBar('Progress', parent=self)
        self.activated_dialogs.append(self.__progress_bar)

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_in_fp_mcs_input = QLineEdit()
        self.ui.p2_in_fp_mcs_input.setMinimumWidth(150)
        self.ui.p2_in_fp_mcs_input_unit = QPushButton('...')
        self.ui.p2_in_fp_mcs_input_unit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('MCS input file'), c.value, 0, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_input, c.value, 1, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_input_unit, c.count, 2, 1, 1)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_n_mp', 'No. processes', '')
        self.ui.p3_example.setText('Input template')

        # ============
        # set defaults
        # ============
        self.ui.p2_in_n_mp.setText('2')

        # =================
        # signals and slots
        # =================
        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(
            lambda: self.get_open_file_name('Select a mcs0 input file', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_mcs_input.setText)
        )

    def example(self):
        logger.info('Saving a SFEPRAPY template input file ...')
        self.statusBar().showMessage('Saving a SFEPRAPY template input file ...')
        from sfeprapy.mcs0 import EXAMPLE_INPUT_DF
        fp = QtWidgets.QFileDialog.getSaveFileName(self, 'Save a SFEPRAPY template input file', '', '(*.xlsx *.csv)')[0]
        if fp.endswith('.csv'):
            EXAMPLE_INPUT_DF.to_csv(fp)
        elif fp.endswith('.xlsx'):
            EXAMPLE_INPUT_DF.to_excel(fp)
        else:
            logger.info('Failed to create a SFEPRAPY template input file')
            self.statusBar().showMessage('Failed to create a SFEPRAPY template input file')
            raise TypeError('Unknown file format')
        logger.info('Successfully created a SFEPRAPY template input file')
        self.statusBar().showMessage('Successfully created a SFEPRAPY template input file')

    @property
    def input_parameters(self):
        def str2num(v):
            try:
                return int(v)
            except ValueError:
                return 1

        return dict(
            fp_mcs_input=self.ui.p2_in_fp_mcs_input.text(),
            n_mp=str2num(self.ui.p2_in_n_mp.text()),
            qt_prog_signal_0=self.__progress_bar.Signals.progress_label,
            qt_prog_signal_1=self.__progress_bar.Signals.progress
        )

    @input_parameters.setter
    def input_parameters(self, v):
        pass

    @property
    def output_parameters(self):
        pass

    @output_parameters.setter
    def output_parameters(self, v):
        pass

    def ok(self):

        self.__progress_bar.show()
        self.calculate(**self.input_parameters)

    @staticmethod
    def calculate(fp_mcs_input, n_mp, qt_prog_signal_0, qt_prog_signal_1):

        # ===========
        # parse input
        # ===========
        logger.info(f'Started to parse input file ...')
        try:
            mcs_input = pd.read_csv(fp_mcs_input, index_col=0).to_dict()
        except Exception as e:
            logger.warning(f'Failed to parse input file as csv format, retry to parse in xlsx format ...')
            try:
                mcs_input = pd.read_excel(fp_mcs_input, index_col=0).to_dict()
            except Exception as e:
                logger.error(f'Failed to parse input file as xlsx format, {e}')
                raise e
        logger.info(f'Successfully parsed input file')

        # ======================
        # instantiate MCS object
        # ======================
        mcs0 = MCS0()
        mcs0.mcs_inputs = mcs_input
        mcs0.mcs_config = dict(n_threads=n_mp, cwd=dirname(fp_mcs_input))

        # ==================
        # run MCS simulation
        # ==================
        t = threading.Thread(
            target=mcs0.run_mcs,
            kwargs=dict(
                qt_prog_signal_0=qt_prog_signal_0,
                qt_prog_signal_1=qt_prog_signal_1
            )
        )
        t.start()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
