import os
import threading
from os.path import join

import matplotlib
import numpy as np
import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from tqdm import tqdm

from fsetoolsGUI import logger
from fsetoolsGUI.etc.sfeprapy_post_processor import lineplot, lineplot_matrix
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter, ProgressBar


class App(AppBaseClass):
    app_id = '0621'
    app_name_short = 'SFEPRAPY\npost-proc.'
    app_name_long = 'SFEPRAPY post-processor'

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
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_input', 'MCS input file', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_output', 'MCS output dir.', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_width', 'Plot width', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_height', 'Plot height', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_width', 'Plot mat. width', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_height', 'Plot mat. height', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_cols', 'Plot mat. cols', 'integer')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xmin', 'Plot x min.', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xmax', 'Plot x max.', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xstep', 'Plot x step', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_legend_cols', 'Plot legend cols', '')

        self.ui.p3_example.setVisible(False)
        self.ui.p3_about.setVisible(False)

        # ============
        # set defaults
        # ============
        self.ui.p2_in_figure_height.setText('3.5')
        self.ui.p2_in_figure_width.setText('3.5')
        self.ui.p2_in_figure_matrix_height.setText('1.2')
        self.ui.p2_in_figure_matrix_width.setText('1.2')
        self.ui.p2_in_figure_matrix_cols.setText('9')
        self.ui.p2_in_figure_xmin.setText('0')
        self.ui.p2_in_figure_xmax.setText('180')
        self.ui.p2_in_figure_xstep.setText('30')
        self.ui.p2_in_figure_legend_cols.setText('1')

        # =================
        # signals and slots
        # =================
        def fp_mcs_input():
            fp_input = QtWidgets.QFileDialog.getOpenFileName(self, 'Select an input file', '', '(*.csv *.xlsx)')[0]
            fp_input = os.path.realpath(fp_input)
            dir_mcs_output = os.path.join(os.path.dirname(fp_input), 'mcs.out')
            self.ui.p2_in_fp_mcs_input.setText(fp_input)
            if os.path.exists(dir_mcs_output):
                self.ui.p2_in_fp_mcs_output.setText(dir_mcs_output)
        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(fp_mcs_input)

        self.ui.p2_in_fp_mcs_output_unit.clicked.connect(
            lambda: self.ui.p2_in_fp_mcs_output.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select an input file', ''))
        )

    def example(self):
        pass

    @property
    def input_parameters(self):
        def str2int(v):
            try:
                return int(v)
            except ValueError:
                return 0

        def str2float(v):
            try:
                return float(v)
            except ValueError:
                return 0.

        return dict(
            fp_mcs_input=self.ui.p2_in_fp_mcs_input.text(),
            fp_mcs_output_dir=self.ui.p2_in_fp_mcs_output.text(),
            figure_height=str2float(self.ui.p2_in_figure_height.text()),
            figure_width=str2float(self.ui.p2_in_figure_width.text()),
            figure_matrix_height=str2float(self.ui.p2_in_figure_matrix_height.text()),
            figure_matrix_width=str2float(self.ui.p2_in_figure_matrix_width.text()),
            figure_matrix_cols=str2int(self.ui.p2_in_figure_matrix_cols.text()),
            figure_xmin=str2float(self.ui.p2_in_figure_xmin.text()),
            figure_xmax=str2float(self.ui.p2_in_figure_xmax.text()),
            figure_xstep=str2float(self.ui.p2_in_figure_xstep.text()),
            figure_legend_cols=str2int(self.ui.p2_in_figure_legend_cols.text()),
            qt_progress_signal_0=self.__progress_bar.Signals.progress,
            qt_progress_signal_1=self.__progress_bar.Signals.progress_label,
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
        try:
            threading.Thread(target=self.calculate, kwargs=self.input_parameters).start()
        except Exception as e:
            logger.error(f'Failed to post process data, {e}')
            self.statusBar().showMessage(f'Failed to post process data, {e}', timeout=60)
        self.statusBar().showMessage('Successfully post process data')

    @staticmethod
    def calculate(
            fp_mcs_input: str, fp_mcs_output_dir: str,
            figure_height: float,
            figure_width: float,
            figure_matrix_height: float,
            figure_matrix_width: float,
            figure_matrix_cols: int,
            figure_xmin: float,
            figure_xmax: float,
            figure_xstep: float,
            figure_legend_cols: int,
            qt_progress_signal_0=None, qt_progress_signal_1=None):

        matplotlib.use('agg')  # this method will be called in a thread, no GUI allowed for matplotlib
        os.chdir(os.path.dirname(fp_mcs_output_dir))

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(0)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('0/7')

        bin_width = 0.2

        # ===============
        # load input data
        # ===============
        df_input = pd.read_excel(fp_mcs_input, index_col=0)

        # ================
        # load output data
        # ================
        fp_csvs = [join(root, f) for root, dirs, files in os.walk(fp_mcs_output_dir) for f in files if f.endswith('.csv')]
        df_output: pd.DataFrame = pd.concat([pd.read_csv(fp) for fp in tqdm(fp_csvs)])
        df_output = df_output.loc[:, ~df_output.columns.str.contains('^Unnamed')]  # remove potential index column
        df_output.dropna(subset=['solver_time_equivalence_solved'], inplace=True)  # get rid of iterations without convergence for time equivalence

        # =================
        # clean output data
        # =================

        df_output.replace('', np.inf, inplace=True)
        s = df_output['solver_time_equivalence_solved']
        assert all(s.values != np.nan)  # make sure all values are numerical
        df_output.loc[df_output['solver_time_equivalence_solved'] == np.inf, 'solver_time_equivalence_solved'] = np.amax(s[s < np.inf])
        df_output.loc[df_output['solver_time_equivalence_solved'] == -np.inf, 'solver_time_equivalence_solved'] = np.amin(s[s > -np.inf])
        df_output.loc[df_output['solver_time_equivalence_solved'] == np.nan, 'solver_time_equivalence_solved'] = np.inf
        df_output.loc[df_output['solver_time_equivalence_solved'] > 18000, 'solver_time_equivalence_solved'] = 18000.
        df_output['solver_time_equivalence_solved'] = df_output['solver_time_equivalence_solved'] / 60.  # Unit from second to minute
        assert df_output['solver_time_equivalence_solved'].max() != np.inf
        assert df_output['solver_time_equivalence_solved'].max() <= 300.
        assert df_output['solver_time_equivalence_solved'].min() != -np.inf

        # =========================
        # prepare intermediate data
        # =========================

        case_names = sorted(set(df_output['case_name']))
        edges = np.arange(0, 300 + bin_width, bin_width)
        x = (edges[1:] + edges[:-1]) / 2  # make x-axis values, i.e. time equivalence

        # Calculate the PDF and CDF of time equivalence, based upon the x-axis array
        dict_teq = {case_name: s[df_output['case_name'] == case_name].values for case_name in set(df_output['case_name'])}
        dict_teq_pdf = {k: np.histogram(v, edges)[0] / len(v) for k, v in dict_teq.items()}
        dict_teq_cdf = {k: np.cumsum(v) for k, v in dict_teq_pdf.items()}

        # Calculate design failure probability due to fire for individual compartments
        dict_P = dict()
        try:
            assert all([i in df_input.index for i in ['p1', 'p2', 'p3', 'p4', 'representative_floor_area']])
            for k, teq_cdf in dict_teq_cdf.items():
                dict_P[k] = np.product([df_input.loc[i, k] for i in ['p1', 'p2', 'p3', 'p4', 'representative_floor_area']])
        except AssertionError:
            logger.warning('Failed to parse p1, p2, p3, p4 and representative_floor_area, they are not defined in the input file, a unity is assigned')
            dict_P = {k: 1 for k in dict_teq_cdf.keys()}

        dict_P_r_fi_i_weighted = {key: time_equivalence * (dict_P[key] / sum(dict_P.values())) for key, time_equivalence in dict_teq_cdf.items()}
        dict_P_f_d_i = {key: (1 - teq) * dict_P[key] for key, teq in dict_teq_cdf.items()}

        P_r_fi_i = pd.DataFrame.from_dict({'TIME [min]': x, **dict_teq_cdf}).set_index('TIME [min]')
        P_f_d_i = pd.DataFrame.from_dict({'TIME [min]': x, **dict_P_f_d_i}).set_index('TIME [min]')

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(25)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('1/7')

        # =====================
        # plot and save results
        # =====================

        # plot time equivalence in subplots matrix
        fig, ax = lineplot_matrix(dict_teq, n_cols=figure_matrix_cols, figsize=(figure_matrix_width, figure_matrix_height))
        fig.savefig('1-P_r_fi_i.png', dpi=300, bbox_inches='tight')

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(25 + 15)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('2/7')

        # plot and save time equivalence in one figure
        fig, ax = lineplot(
            x=[x] * len(case_names),
            y=[dict_teq_cdf[i] for i in case_names],
            legend_labels=case_names,
            n_legend_col=figure_legend_cols,
            xlabel='Equivalent of Time Exposure [$min$]',
            ylabel='$P_{r,fi}$ [-]',
            figsize=(figure_width, figure_height),
            xlim=(figure_xmin, figure_xmax),
            xlim_step=figure_xstep,
        )
        fig.savefig('2-P_r_fi_i.png', dpi=300, bbox_inches='tight', transparent=True)
        P_r_fi_i.iloc[[P_r_fi_i.index.get_loc(i, method='nearest') for i in [30.1, 60.1, 90.1, 120.1, 150.1, 180.1, 210.1, 240.1]]].to_csv('1-P_r_fi_i.csv')

        fig, ax = lineplot(
            x=[x],
            y=[np.sum([v for k, v in dict_P_r_fi_i_weighted.items()], axis=0)],
            legend_labels=[None],
            n_legend_col=figure_legend_cols,
            xlabel='Equivalent of Time Exposure [$min$]',
            ylabel='Combined $P_{r,fi}$ [-]',
            figsize=(figure_width, figure_height),
            xlim=(figure_xmin, figure_xmax),
            xlim_step=figure_xstep,
        )
        fig.savefig('2-P_r_fi_i_combined.png', dpi=300, bbox_inches='tight', transparent=True)

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(25 + 15 + 15)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('3/7')

        # plot failure probability due to structurally significant fire
        fig, ax = lineplot(
            x=[x] * len(case_names),
            y=[1 - dict_teq_cdf[i] for i in case_names],
            legend_labels=case_names,
            n_legend_col=figure_legend_cols,
            xlabel='Equivalent of Time Exposure [$min$]',
            ylabel='$P_{f,fi}$ [-]',
            figsize=(figure_width, figure_height),
            xlim=(figure_xmin, figure_xmax),
            xlim_step=figure_xstep,
        )
        fig.savefig('3-P_f_fi_i.png', dpi=300, bbox_inches='tight', transparent=True)

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(25 + 15 + 15 + 15)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('4/7')

        # plot failure probability due to fire
        fig, ax = lineplot(
            x=[x] * len(case_names),
            y=[dict_P_f_d_i[i] for i in case_names],
            legend_labels=case_names,
            n_legend_col=figure_legend_cols,
            xlabel='Equivalent of Time Exposure [$min$]',
            ylabel='Failure Probability [$year^{-1}$]',
            figsize=(figure_width, figure_height),
            xlim=(figure_xmin, figure_xmax),
            xlim_step=figure_xstep,
        )
        fig.savefig('4-P_fd_i.png', dpi=300, bbox_inches='tight', transparent=True)

        P_f_d_i.iloc[[P_r_fi_i.index.get_loc(i, method='nearest') for i in [30.1, 60.1, 90.1, 120.1, 150.1, 180.1, 210.1, 240.1]]].to_csv('1-P_f_d_i.csv')

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(25 + 15 + 15 + 15 + 15)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('6/7')

        # plot combined failure probability due to fire
        fig, ax = lineplot(
            x=[x],
            y=[np.sum([v for k, v in dict_P_f_d_i.items()], axis=0)],
            legend_labels=[None],
            n_legend_col=figure_legend_cols,
            xlabel='Equivalent of Time Exposure [$min$]',
            ylabel='Failure Probability [$year^{-1}$]',
            figsize=(figure_width, figure_height),
            xlim=(figure_xmin, figure_xmax),
            xlim_step=figure_xstep,
        )
        fig.savefig('5-P_fd.png', dpi=300, bbox_inches='tight', transparent=True)

        if qt_progress_signal_0:
            qt_progress_signal_0.emit(100)
        if qt_progress_signal_1:
            qt_progress_signal_1.emit('7/7')


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
