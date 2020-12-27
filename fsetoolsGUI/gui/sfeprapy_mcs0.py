import threading
from os.path import dirname

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from sfeprapy.mcs0.mcs0_calc import MCS0

from fsetoolsGUI import logger
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.bases.custom_progressbar import ProgressBar
from fsetoolsGUI.gui.bases.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0640'
    app_name_short = 'SFEPRAPY\nMCS0\nprocessor'
    app_name_long = 'SFEPRAPY Monte Carlo Simulation 0'

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
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_input', 'MCS input file', '...', unit_obj='QPushButton', min_width=200)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_n_mp', 'No. of processes', '')
        self.ui.p3_example.setText('Save example inputs')

        # ============
        # set defaults
        # ============
        self.ui.p2_in_n_mp.setText('2')

        # =================
        # signals and slots
        # =================
        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(
            lambda: self.dialog_open_file('Select a mcs0 input file', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_mcs_input.setText)
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

    def submit(self):
        try:
            self.__progress_bar.show()
            self.calculate(**self.input_parameters)
        except Exception as e:
            logger.error(f'Failed to run simulation, {e}')
            self.statusBar().showMessage(f'Failed to run simulation, {e}', timeout=60)
            raise e

    @staticmethod
    def calculate(fp_mcs_input, n_mp, qt_prog_signal_0, qt_prog_signal_1):
        # ======================
        # instantiate MCS object
        # ======================
        mcs0 = MCS0()

        # ===========
        # parse input
        # ===========
        logger.info(f'Started to parse input file ...')
        try:
            mcs0.mcs_inputs = fp_mcs_input
        except Exception as e:
            logger.error(f'Failed to parse input file as xlsx format, {e}')
        logger.info(f'Successfully parsed input file')

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
