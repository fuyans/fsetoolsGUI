import os
from os.path import join

import numpy as np
import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QLineEdit
from sfeprapy.func.pp import lineplot, lineplot_matrix
# import seaborn as sns
from tqdm import tqdm

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter


class App(AppBaseClass):
    app_id = '0621'
    app_name_short = 'SFEPRAPY\npost-proc.\nfailure'
    app_name_long = 'SFEPRAPY failure probability post-processor'

    def __init__(self, parent=None, post_stats: bool = True):
        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)

        self.ui.p2_in_fp_mcs_output = QLineEdit()
        self.ui.p2_in_fp_mcs_output.setMinimumWidth(150)
        self.ui.p2_in_fp_mcs_output_unit = QPushButton('Select')
        self.ui.p2_in_fp_mcs_output_unit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p2_in_fp_mcs_input = QLineEdit()
        self.ui.p2_in_fp_mcs_input.setMinimumWidth(150)
        self.ui.p2_in_fp_mcs_input_unit = QPushButton('Select')
        self.ui.p2_in_fp_mcs_input_unit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('MCS output dir.'), c.value, 0, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_output, c.value, 1, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_output_unit, c.count, 2, 1, 1)
        self.ui.p2_layout.addWidget(QLabel('MCS input file'), c.value, 0, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_input, c.value, 1, 1, 1)
        self.ui.p2_layout.addWidget(self.ui.p2_in_fp_mcs_input_unit, c.count, 2, 1, 1)
        self.ui.p3_example.setVisible(False)

        # ============
        # set defaults
        # ============

        # =================
        # signals and slots
        # =================
        self.ui.p2_in_fp_mcs_output_unit.clicked.connect(
            lambda: self.ui.p2_in_fp_mcs_output.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select an input file', ''))
        )

        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(
            lambda: self.ui.p2_in_fp_mcs_input.setText(QtWidgets.QFileDialog.getOpenFileName(self, 'Select an input file', '', '(*.csv *.xlsx)')[0])
        )

    def example(self):
        pass

    @property
    def input_parameters(self):
        return dict(
            fp_mcs_input=self.ui.p2_in_fp_mcs_input.text(),
            fp_mcs_output_dir=self.ui.p2_in_fp_mcs_output.text()
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
        self.calculate(**self.input_parameters)

    @staticmethod
    def calculate(fp_mcs_input: str, fp_mcs_output_dir: str):
        os.chdir(os.path.dirname(fp_mcs_output_dir))

        fig_style = 'white'  # @param {type:"string"}
        fig_palette = 'muted'  # @param {type:"string"}
        fig_context = 'paper'  # @param {type:"string"}
        fig_size_width = 3.6  # @param {type:"number"}
        fig_size_height = 3.6  # @param {type:"number"}
        n_cols = 9
        # plotting styles setup
        # sns.set(style=fig_style, palette=fig_palette, color_codes=True)
        # sns.set_context(fig_context)
        bin_width = 0.25

        # load input data
        df_input = pd.read_excel(fp_mcs_input, index_col=0)

        # load output data
        fp_csvs = [join(root, f) for root, dirs, files in os.walk(fp_mcs_output_dir) for f in files if f.endswith('.csv')]
        df_output = pd.concat([pd.read_csv(fp) for fp in tqdm(fp_csvs)])
        df_output = df_output.loc[:, ~df_output.columns.str.contains('^Unnamed')]

        s = df_output['solver_time_equivalence_solved']
        assert all(s.values != np.nan)  # make sure all values are numerical
        s[s == np.inf] = np.amax(s[s != np.inf])  # remove inf
        s[s == -np.inf] = np.amin(s[s != -np.inf])  # remove -inf
        s[s > 18000] = 18000  # set max. cap
        s /= 60  # Unit from second to minute
        assert np.amax(df_output['solver_time_equivalence_solved'].values) != np.inf
        assert np.amin(df_output['solver_time_equivalence_solved'].values) != -np.inf
        # df_output['solver_time_equivalence_solved']=s

        edges = np.arange(0, np.amax(df_output['solver_time_equivalence_solved']) + 0.5 * bin_width, bin_width)
        x = (edges[1:] + edges[:-1]) / 2  # make x-axis values, i.e. time equivalence

        # Calculate the PDF and CDF of time equivalence, based upon the x-axis array
        dict_teq = {case_name: s[df_output['case_name'] == case_name].values for case_name in set(df_output['case_name'])}
        dict_teq_pdf = {k: np.histogram(v, edges)[0] / len(v) for k, v in dict_teq.items()}
        dict_teq_cdf = {k: np.cumsum(v) for k, v in dict_teq_pdf.items()}

        fig, ax = lineplot_matrix(dict_teq, n_cols, 'step_3.1-teq.png')
        fig.savefig('1-P_r_fi_i.png', dpi=300, bbox_inches='tight')

        fig, ax = lineplot(
            x=[x for i in sorted(set(df_output['case_name']))],
            y=[dict_teq_cdf[i] for i in sorted(set(df_output['case_name']))],
            legend_labels=sorted(set(df_output['case_name'])),
            n_legend_col=5,
            xlabel='Equivalent of Time Exposure [$minute$]',
            ylabel='$P_{r,fi}$ [-]',
        )

        # Save plot
        fig.savefig('2-P_r_fi_i.png', dpi=300, bbox_inches='tight', transparent=True)

        fig, ax = lineplot(
            x=[x for i in sorted(set(df_output['case_name']))],
            y=[1 - dict_teq_cdf[i] for i in sorted(set(df_output['case_name']))],
            legend_labels=sorted(set(df_output['case_name'])),
            n_legend_col=5,
            xlabel='Equivalent of Time Exposure [$minute$]',
            ylabel='$P_{f,fi}$ [-]',
        )
        fig.savefig('3-P_f_fi_i.png', dpi=300, bbox_inches='tight')

        # Calculate design failure probability due to fire for inidivudal compartments
        dict_P_f_d_i = dict()
        for k, teq_cdf in dict_teq_cdf.items():
            dict_P_f_d_i[k] = np.product([df_input.loc[i][k] for i in ['p1', 'p2', 'p3', 'p4', 'representative_floor_area']]) * (1 - teq_cdf)

        fig, ax = lineplot(
            x=[x for i in sorted(set(df_output['case_name']))],
            y=[dict_P_f_d_i[i] for i in sorted(set(df_output['case_name']))],
            legend_labels=sorted(set(df_output['case_name'])),
            n_legend_col=5,
            xlabel='Equivalent of Time Exposure [$minute$]',
            ylabel='Failure Probability [$year^{-1}$]',
        )

        # Save figure
        fig.savefig('4-P_fd_i.png', dpi=300, bbox_inches='tight', transparent=True)

        df_P_f_d_i = pd.DataFrame.from_dict({'TIME [min]': x, **dict_P_f_d_i}).set_index('TIME [min]')
        df_P_f_d_i.to_csv('4-P_fd_i.csv')

        fig, ax = lineplot(
            x=[x],
            y=[np.sum([v for k, v in dict_P_f_d_i.items()], axis=0)],
            legend_labels=[None],
            n_legend_col=5,
            xlabel='Equivalent of Time Exposure [$minute$]',
            ylabel='$P_{f,fi}$ [-]',
        )

        # Save plots
        fig.savefig('5-P_fd.png', dpi=300, bbox_inches='tight', transparent=True)


if __name__ == "__main__":
    App.calculate(
        r'E:\projects_FSE\!fleet_st\alpha\alpha.xlsx',
        r'E:\projects_FSE\!fleet_st\alpha\mcs.out',
    )

    # import sys
    #
    # qapp = QtWidgets.QApplication(sys.argv)
    # app = App(post_stats=False)
    # app.show()
    # qapp.exec_()
