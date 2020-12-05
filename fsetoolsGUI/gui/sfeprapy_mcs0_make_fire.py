import os

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel

from fsetoolsGUI import logger
from fsetoolsGUI.etc.sfeprapy_make_fires import mcs0_make_fires
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.bases.custom_plot_pyqtgraph import App as FigureApp
from fsetoolsGUI.gui.bases.custom_utilities import Counter


def str2indexes(str_: str) -> list:
    indexes = list()
    for i in str_.split(','):
        i = i.strip()
        if '-' in i:
            i_range = i.split('-')
            assert len(i_range) == 2
            i_range = [int(j.strip()) for j in i_range]
            indexes.extend(list(range(i_range[0], i_range[1] + 1, 1)))
        else:
            indexes.append(int(i))
    return indexes


def mcs0_make_fires_worker(
        fp_mcs_input: str,
        fp_mcs_output_dir: str,
        indexes: str,
        case_name: str,
):
    outputs = dict()
    for index in str2indexes(indexes):
        try:
            _ = mcs0_make_fires(
                fp_mcs_input=fp_mcs_input,
                fp_mcs_output_dir=fp_mcs_output_dir,
                index=index,
                case_name=case_name,
            )
            outputs[f'temperature {index}'] = _['temperature']
        except Exception as e:
            logger.error(f'Failed to generate fire curve for index {index}, {e}')
    outputs['time'] = _['time']
    return outputs


class App(AppBaseClass):
    app_id = '0643'
    app_name_short = 'SFEPRAPY MCS0\npost-proc.\nmake fires'
    app_name_long = 'SFEPRAPY MCS0 post-processor make fires'

    def __init__(self, parent=None, post_stats: bool = True):
        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.__input_parameters: dict = dict()
        self.__output_parameters: dict = dict()

        self.FigureApp = FigureApp(parent=self, title='MCS design fires')
        self.__figure_ax = self.FigureApp.add_subplot(0, 0, x_label='Time [min]', y_label='Temperature [<sup>o</sup>C]')
        self.__figure_ax.addLegend()

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_input', 'MCS input file', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_mcs_output', 'MCS output dir.', '...', unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_case_name', 'Case name', obj='QComboBox', min_width=200)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_index', 'Simulation iteration index')

        self.ui.p3_example.setVisible(False)
        self.ui.p3_about.setVisible(False)

        # defaults
        self.ui.p2_in_case_name.setEnabled(False)

        # =================
        # signals and slots
        # =================
        def _fp_mcs_input():
            fp_input = self.get_open_file_name('Select an mcs0 input file', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_mcs_input.setText)
            if not fp_input:
                return
            dir_mcs_output = os.path.join(os.path.dirname(fp_input), 'mcs.out')
            if os.path.exists(dir_mcs_output):
                self.ui.p2_in_fp_mcs_output.setText(dir_mcs_output)

        self.ui.p2_in_fp_mcs_input_unit.clicked.connect(_fp_mcs_input)

        self.ui.p2_in_fp_mcs_output_unit.clicked.connect(
            lambda: self.get_existing_dir('Select a folder containing MCS0 output files', func_to_assign_fp=self.ui.p2_in_fp_mcs_output.setText)
        )

        def workout_index_and_case_name():
            input_parameters = self.input_parameters
            if not os.path.exists(input_parameters['fp_mcs_input']) or not os.path.exists(input_parameters['fp_mcs_output_dir']):
                return
            try:
                df_input = pd.read_excel(input_parameters['fp_mcs_input'], index_col=0)
            except:
                try:
                    df_input = pd.read_csv(input_parameters['fp_mcs_input'], index_col=0)
                except Exception as e:
                    logger.error(f'Failed to load input data, {e}')
                    return
            case_names = df_input.columns.to_list()
            self.ui.p2_in_case_name.clear()
            self.ui.p2_in_case_name.addItems(case_names)
            self.ui.p2_in_case_name.setEnabled(True)

        self.ui.p2_in_fp_mcs_input.textChanged.connect(workout_index_and_case_name)
        self.ui.p2_in_fp_mcs_output.textChanged.connect(workout_index_and_case_name)

    def example(self):
        pass

    @property
    def input_parameters(self):

        return dict(
            fp_mcs_input=self.ui.p2_in_fp_mcs_input.text(),
            fp_mcs_output_dir=self.ui.p2_in_fp_mcs_output.text(),
            indexes=self.ui.p2_in_index.text(),
            case_name=self.ui.p2_in_case_name.currentText(),
        )

    @input_parameters.setter
    def input_parameters(self, v):
        self.__input_parameters = v

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v):
        self.__output_parameters = v

    def ok(self):
        try:
            self.output_parameters = mcs0_make_fires_worker(**self.input_parameters)
        except Exception as e:
            logger.error(f'Failed to analysis output data, {e}')
            self.statusBar().showMessage(f'Failed to analysis output data, {e}', timeout=30)
            raise e

        try:
            self.show_results_in_figure()
        except Exception as e:
            logger.error(f'Failed to plot figures, {e}')
            self.statusBar().showMessage(f'Failed to plot figures, {e}', timeout=30)

    def show_results_in_figure(self):
        output_parameters = self.output_parameters

        self.__figure_ax.getPlotItem().clear()
        time = output_parameters['time'] / 60.
        for i in output_parameters:
            if 'temperature' in i:
                self.FigureApp.plot(time, output_parameters[i] - 273.15, name=i.replace('temperature ', ''))
        self.FigureApp.show()


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
