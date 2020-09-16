import os

import pandas as pd
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel

from fsetoolsGUI import logger
from fsetoolsGUI.etc.sfeprapy_make_fires import mcs0_make_fires
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App(AppBaseClass):
    app_id = '0643'
    app_name_short = 'SFEPRAPY\npost-proc.\nmake fires'
    app_name_long = 'SFEPRAPY post-processor make fires'

    def __init__(self, parent=None, post_stats: bool = True):
        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        self.__output_parameters: dict = dict()
        self.__Table = None
        self.__Figure = None
        self.__Figure_ax = None

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
        def str2int(v):
            try:
                return int(v)
            except ValueError:
                return 0

        return dict(
            fp_mcs_input=self.ui.p2_in_fp_mcs_input.text(),
            fp_mcs_output_dir=self.ui.p2_in_fp_mcs_output.text(),
            index=str2int(self.ui.p2_in_index.text()),
            case_name=self.ui.p2_in_case_name.currentText(),
        )

    @input_parameters.setter
    def input_parameters(self, v):
        pass

    @property
    def output_parameters(self):
        return self.__output_parameters

    @output_parameters.setter
    def output_parameters(self, v):
        self.__output_parameters = v

    def ok(self):
        self.output_parameters = self.calculate(**self.input_parameters)

        self.show_results_in_table()
        self.show_results_in_figure()

    @staticmethod
    def calculate(
            fp_mcs_input: str,
            fp_mcs_output_dir: str,
            index: int,
            case_name: str,
    ):
        return mcs0_make_fires(
            fp_mcs_input=fp_mcs_input,
            fp_mcs_output_dir=fp_mcs_output_dir,
            index=index,
            case_name=case_name,
        )

    def show_results_in_table(self):

        output_parameters = self.output_parameters

        # print results (for console enabled version only)
        list_content = [[float(i), float(j)] for i, j in zip(output_parameters['time'], output_parameters['temperature'] - 273.15)]

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=['time [s]', 'temperature [°C]'],
            window_title='Time dependent temperature',
        )
        self.activated_dialogs.append(self.__Table)

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Fire curve')
            self.__Figure_ax = self.__Figure.add_subplots()
            self.activated_dialogs.append(self.__Figure)
        else:
            self.__Figure_ax.clear()

        self.__Figure_ax.plot(output_parameters['time'] / 60, output_parameters['temperature'] - 273.15, c='k')
        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Temperature [°C]')
        self.__Figure.figure.tight_layout()

        self.__Figure.figure_canvas.draw()
        self.__Figure.show()

        return True


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
