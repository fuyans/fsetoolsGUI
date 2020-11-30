import os
import threading
from os.path import join, realpath

import matplotlib
import numpy as np
import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel

from fsetoolsGUI import logger
from fsetoolsGUI.etc.sfeprapy_post_processor import lineplot, lineplot_matrix
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.custom_progressbar import ProgressBar
from fsetoolsGUI.gui.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0642'
    app_name_short = 'PRAPY MCS0\npost-proc.\nmake plots'
    app_name_long = 'SFEPRAPY MCS0 post-processor make plots'

    def __init__(self, parent=None, post_stats: bool = True):
        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.ProgressBar = ProgressBar('Progress', parent=self)
        self.activated_dialogs.append(self.ProgressBar)

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_input', 'MCS input file', '...', unit_obj='QPushButton', min_width=200)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_output', 'MCS output dir.', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_width', 'Plot width', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_height', 'Plot height', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_cols', 'Plot mat. cols')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xmin', 'Plot x min.', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xmax', 'Plot x max.', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_xstep', 'Plot x step', 'min')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_legend_cols', 'Plot legend cols', '')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_width', 'Plot mat. width', 'in')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_figure_matrix_height', 'Plot mat. height', 'in')

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
        self.ui.p2_in_figure_xmin.setText('15')
        self.ui.p2_in_figure_xmax.setText('180')
        self.ui.p2_in_figure_xstep.setText('15')
        self.ui.p2_in_figure_legend_cols.setText('1')

        # =================
        # signals and slots
        # =================
        def _fp_mcs_input():
            fp_input = self.get_open_file_name('Select a mcs0 input file', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_mcs_input.setText)
            if not fp_input:
                return
            dir_mcs_output = os.path.join(os.path.dirname(fp_input), 'mcs.out')
            if os.path.exists(dir_mcs_output):
                self.ui.p2_in_fp_mcs_output.setText(dir_mcs_output)

        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(_fp_mcs_input)

        self.ui.p2_in_fp_mcs_output_unit.clicked.connect(
            lambda: self.get_existing_dir('Select a folder containing MCS0 output files', func_to_assign_fp=self.ui.p2_in_fp_mcs_output.setText)
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
            qt_progress_signal_0=self.ProgressBar.Signals.progress,
            qt_progress_signal_1=self.ProgressBar.Signals.progress_label,
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
        self.ProgressBar.show()
        try:
            threading.Thread(target=self.calculate, kwargs=self.input_parameters).start()
        except Exception as e:
            logger.error(f'Failed to post process data, {e}')
            self.statusBar().showMessage(f'Failed to post process data, {e}', timeout=60)

    @staticmethod
    def calculate(
            fp_mcs_input: str,
            fp_mcs_output_dir: str,
            figure_height: float,
            figure_width: float,
            figure_matrix_height: float,
            figure_matrix_width: float,
            figure_matrix_cols: int,
            figure_xmin: float,
            figure_xmax: float,
            figure_xstep: float,
            figure_legend_cols: int,
            qt_progress_signal_0=None, qt_progress_signal_1=None
    ):
        figure_ystep = 0.1

        matplotlib.use('agg')  # this method will be called in a thread, no GUI allowed for matplotlib
        os.chdir(os.path.dirname(fp_mcs_output_dir))

        def update_progress(progress: int = None, label: str = None):
            if qt_progress_signal_0 and progress is not None:
                qt_progress_signal_0.emit(progress)
            if qt_progress_signal_1 and label is not None:
                qt_progress_signal_1.emit(label)

        update_progress(0, 'Initiating ...')

        bin_width = 0.2

        # ===============
        # load input data
        # ===============
        logger.info('Start to read SFEPRAPY MCS0 input data ...')
        try:
            df_input = pd.read_excel(fp_mcs_input, index_col=0)
        except Exception as e:
            logger.error(f'{e}')
            return

        # ================
        # load output data
        # ================
        logger.info('Start to read SFEPRAPY MCS0 simulation output data ...')
        update_progress(0, '1/7 Reading data')
        try:
            fp_csvs = [join(root, f) for root, dirs, files in os.walk(fp_mcs_output_dir) for f in files if f.endswith('.csv')]
            _ = list()
            for i, fp in enumerate(fp_csvs):
                _.append(pd.read_csv(fp))
                update_progress(int((i + 1) / len(fp_csvs) * 100))
            df_output: pd.DataFrame = pd.concat(_)
            df_output = df_output.loc[:, ~df_output.columns.str.contains('^Unnamed')]  # remove potential index column
            df_output.dropna(subset=['solver_time_equivalence_solved'], inplace=True)  # get rid of iterations without convergence for time equivalence
        except Exception as e:
            logger.error(f'{e}')
            return

        # =================
        # clean output data
        # =================
        logger.info('Start to clean data ...')
        try:
            df_output.replace('', np.inf, inplace=True)
            s = df_output['solver_time_equivalence_solved']
            assert all(s.values != np.nan)  # make sure all values are numerical
            df_output.loc[df_output['solver_time_equivalence_solved'] == np.inf, 'solver_time_equivalence_solved'] = np.amax(s[s < np.inf])
            df_output.loc[df_output['solver_time_equivalence_solved'] == -np.inf, 'solver_time_equivalence_solved'] = np.amin(s[s > -np.inf])
            df_output.loc[df_output['solver_time_equivalence_solved'] >= 18000., 'solver_time_equivalence_solved'] = 18000. - 1e-3
            df_output.loc[df_output['solver_time_equivalence_solved'] < 0., 'solver_time_equivalence_solved'] = 0. + 1e-3
            df_output['solver_time_equivalence_solved'] = df_output['solver_time_equivalence_solved'] / 60.  # Unit from second to minute
            assert df_output['solver_time_equivalence_solved'].max() != np.inf
            assert df_output['solver_time_equivalence_solved'].max() <= 300.
            assert df_output['solver_time_equivalence_solved'].min() != -np.inf
        except Exception as e:
            logger.error(f'{e}')
            return

        # =========================
        # prepare intermediate data
        # =========================
        logger.info("Start to analyse data ...")
        try:
            case_names = sorted(set(df_output['case_name']))
            edges = np.arange(0, 300 + bin_width, bin_width)
            x = (edges[1:] + edges[:-1]) / 2  # make x-axis values, i.e. time equivalence

            # Calculate the PDF and CDF of time equivalence, based upon the x-axis array
            dict_teq = {case_name: s[df_output['case_name'] == case_name].values for case_name in case_names}
            dict_teq_pdf = {k: np.histogram(v, edges)[0] / len(v) for k, v in dict_teq.items()}
            dict_teq_cdf = {k: np.cumsum(v) for k, v in dict_teq_pdf.items()}

            # Calculate design failure probability due to fire for individual compartments
            dict_P, is_probabilities_defined = dict(), False
            try:
                _ = df_input.index.tolist()
                if 'representative_floor_area' in _:
                    _[_.index('representative_floor_area')] = 'general_room_floor_area'
                    df_input.index = _

                assert all([i in df_input.index for i in ['p1', 'p2', 'p3', 'p4', 'general_room_floor_area']])
                for case_name, teq_cdf in dict_teq_cdf.items():
                    dict_P[case_name] = np.product([df_input.loc[i, case_name] for i in ['p1', 'p2', 'p3', 'p4', 'general_room_floor_area']])
                is_probabilities_defined = True
            except AssertionError:
                logger.warning('Failed to parse p1, p2, p3, p4 and general_room_floor_area, they are not defined in the input file, a unity is assigned')
                dict_P = {k: 1 for k in dict_teq_cdf.keys()}  # this is to prevent error in following codes

            dict_P_r_fi_i_weighted = {key: time_equivalence * (dict_P[key] / sum(dict_P.values())) for key, time_equivalence in dict_teq_cdf.items()}
            dict_P_f_d_i = dict()
            for key, teq in dict_teq_cdf.items():
                dict_P_f_d_i[key] = (1 - teq) * dict_P[key]

            P_r_fi_i = pd.DataFrame.from_dict({'TIME [min]': x, **dict_teq_cdf}).set_index('TIME [min]')
            P_r_fi_i_weighted = pd.DataFrame.from_dict({'TIME [min]': x, **dict_P_r_fi_i_weighted}).set_index('TIME [min]')
            P_r_fi_combined = pd.DataFrame.from_dict({'TIME [min]': x, **dict_P_r_fi_i_weighted}).set_index('TIME [min]')
            P_f_d_i = pd.DataFrame.from_dict({'TIME [min]': x, **dict_P_f_d_i}).set_index('TIME [min]')
        except Exception as e:
            logger.error(f'{e}')
            raise e

        # =====================
        # plot and save results
        # =====================
        # plot time equivalence in subplots matrix
        logger.info('Start to plot time equivalence (subplots) ...')
        update_progress(0, '2/7 P_r_fi_i')
        try:
            if len(dict_teq) > 6:
                fig, ax = lineplot_matrix(
                    dict_teq,
                    n_cols=figure_matrix_cols,
                    figsize=(figure_matrix_width, figure_matrix_height),
                    qt_progress_signal=qt_progress_signal_0,
                )
                fig.savefig('1-P_r_fi_i.png', dpi=300, bbox_inches='tight')
            else:
                logger.info('Skipped P_r_fi_i matrix line plot as only less than six dataset is provided')

        except Exception as e:
            logger.error(f'{e}')

        # plot and save time equivalence in one figure
        logger.info('Start to plot time equivalence ...')
        update_progress(0, '3/7 P_r_fi_i')
        try:
            _ = [30.1, 45.1, 60.1, 75.1, 90.1, 115.1, 120.1, 135.1, 150.1, 165.1, 180.1, 195.1, 210.1, 225.1, 240.1]
            P_r_fi_i.iloc[[P_r_fi_i.index.get_loc(i, method='nearest') for i in _]].to_csv('2-P_r_fi_i.csv')

            lineplot(
                x=[x] * len(case_names),
                y=[dict_teq_cdf[i] for i in case_names],
                legend_labels=case_names,
                n_legend_col=figure_legend_cols,
                xlabel='Equivalent of Time Exposure [$min$]',
                ylabel='$P_{r,fi}$ [-]',
                figsize=(figure_width, figure_height),
                xlim=(figure_xmin, figure_xmax),
                xticks=np.arange(0, figure_xmax + figure_xstep / 2., figure_xstep),
                ylim=(-0.01, 1.01),
                yticks=np.arange(0, 1. + 0.05, 0.1),
                qt_progress_signal=qt_progress_signal_0,
                fp_figure=realpath('2-P_r_fi_i.png')
            )
        except Exception as e:
            logger.error(f'Failed to plot time equivalence, {e}')

        if is_probabilities_defined:

            logger.info('Start to plot combined time equivalence ...')
            update_progress(0, '3/7 P_r_fi_i_combined')
            try:
                _ = [30.1, 45.1, 60.1, 75.1, 90.1, 115.1, 120.1, 135.1, 150.1, 165.1, 180.1, 195.1, 210.1, 225.1, 240.1]
                P_r_fi_i_weighted.iloc[[P_r_fi_i_weighted.index.get_loc(i, method='nearest') for i in _]].to_csv('3-P_r_fi_i_weighted.csv')
                P_r_fi_combined.iloc[[P_r_fi_combined.index.get_loc(i, method='nearest') for i in _]].to_csv('3-P_r_fi_i_combined.csv')

                lineplot(
                    x=[x],
                    y=[np.sum([v for k, v in dict_P_r_fi_i_weighted.items()], axis=0)],
                    legend_labels=[None],
                    n_legend_col=figure_legend_cols,
                    xlabel='Equivalent of Time Exposure [$min$]',
                    ylabel='Combined $P_{r,fi}$ [-]',
                    figsize=(figure_width, figure_height),
                    xlim=(figure_xmin, figure_xmax),
                    xticks=np.arange(0, figure_xmax + figure_xstep / 2., figure_xstep),
                    ylim=(-0.01, 1.01),
                    yticks=np.arange(0, 1. + 0.05, 0.1),
                    qt_progress_signal=qt_progress_signal_0,
                    fp_figure=realpath('3-P_r_fi_i_combined.png'),
                )
            except Exception as e:
                logger.error(f'Failed to plot combined time equivalence, {e}')

            # plot failure probability due to structurally significant fire
            logger.info('Started to plot failure probability ...')
            update_progress(0, '4/7 P_f_fi_i')
            try:
                lineplot(
                    x=[x] * len(case_names),
                    y=[1 - dict_teq_cdf[i] for i in case_names],
                    legend_labels=case_names,
                    n_legend_col=figure_legend_cols,
                    xlabel='Equivalent of Time Exposure [$min$]',
                    ylabel='Failure Probability $P_{f,fi}$ [-]',
                    figsize=(figure_width, figure_height),
                    xlim=(figure_xmin, figure_xmax),
                    xticks=np.arange(0, figure_xmax + figure_xstep / 2., figure_xstep),
                    ylim=(-0.01, 1.01),
                    yticks=np.arange(0, 1. + 0.05, 0.1),
                    qt_progress_signal=qt_progress_signal_0,
                    fp_figure=realpath('4-P_f_fi_i.png')
                )
            except Exception as e:
                logger.error(f'Failed to plot failure probability, {e}')

            # plot failure probability due to fire
            logger.info('Started to plot design failure probability ...')
            update_progress(0, '5/7 P_fd_i')
            try:
                _ = [30.1, 45.1, 60.1, 75.1, 90.1, 115.1, 120.1, 135.1, 150.1, 165.1, 180.1, 195.1, 210.1, 225.1, 240.1]
                P_f_d_i.iloc[[P_f_d_i.index.get_loc(i, method='nearest') for i in _]].to_csv('5-P_f_d_i.csv')

                lineplot(
                    x=[x] * len(case_names),
                    y=[dict_P_f_d_i[i] for i in case_names],
                    legend_labels=case_names,
                    n_legend_col=figure_legend_cols,
                    xlabel='Equivalent of Time Exposure [$min$]',
                    ylabel='Failure probability $P_{f,d}$ [$year^{-1}$]',
                    figsize=(figure_width, figure_height),
                    xlim=(figure_xmin, figure_xmax),
                    xticks=np.arange(0, figure_xmax + figure_xstep / 2., figure_xstep),
                    qt_progress_signal=qt_progress_signal_0,
                    fp_figure=realpath('5-P_fd_i.png')
                )

            except Exception as e:
                logger.error(f'Failed to plot design failure probability, {e}')

            # plot combined failure probability due to fire
            logger.info('Started to plot combined design failure probability ...')
            update_progress(0, '6/7 P_fd')
            try:
                lineplot(
                    x=[x],
                    y=[np.sum([v for k, v in dict_P_f_d_i.items()], axis=0)],
                    legend_labels=[None],
                    n_legend_col=figure_legend_cols,
                    xlabel='Equivalent of Time Exposure [$min$]',
                    ylabel='Failure Probability $P_{f,d}$ [$year^{-1}$]',
                    figsize=(figure_width, figure_height),
                    xlim=(figure_xmin, figure_xmax),
                    xticks=np.arange(0, figure_xmax + figure_xstep / 2., figure_xstep),
                    qt_progress_signal=qt_progress_signal_0,
                    fp_figure=realpath('6-P_fd.png')
                )
            except Exception as e:
                logger.error(f'Failed to plot combined design failure probability, {e}')

        update_progress(100, '7/7 Complete')


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
