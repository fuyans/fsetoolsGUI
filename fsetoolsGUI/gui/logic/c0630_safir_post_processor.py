import os.path as path
import threading

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot

from fsetoolsGUI.etc.safir_post_processor import out2pstrain, pstrain2dict, save_csv, make_strain_lines_for_given_shell
from fsetoolsGUI.gui.layout.i0630_safir_postprocessor import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class Signals(QtCore.QObject):
    __process_safir_out_file_complete = QtCore.Signal(bool)

    @property
    def process_safir_out_file_complete(self) -> QtCore.Signal:
        return self.__process_safir_out_file_complete


class App(AppBaseClass):
    app_id = '0630'
    app_name_short = 'Safir\npost\nprocsser'
    app_name_long = 'Safir post processor'

    def __init__(self, parent=None, mode=None):
        self.__dict_out = None
        self.__Table = None
        self.__Figure = None
        self.__Figure_ax = None
        self.__fp_out = None
        self.__fp_out_processed = None
        self.__fp_out_strain_csv = None
        self.__strain_lines = None
        self.__Signals = Signals()
        self.__output_fire_curve = dict(time=None, temperature=None)

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # =======================
        # lineEdit default values
        # =======================
        self.ui.lineEdit_in_fp_out.setReadOnly(True)
        self.ui.lineEdit_in_shell.setEnabled(False)
        self.ui.comboBox_in_shell.setEnabled(False)
        # self.ui.lineEdit_in_initial_temperature.setText('20')

        # =================
        # lineEdit tip text
        # =================
        # self.ui.lineEdit_in_duration.setToolTip('Fire duration')

        # signals
        # self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_fp_out.clicked.connect(self.__upon_output_file_selection_step_1)
        self.ui.comboBox_in_shell.currentIndexChanged.connect(self.__upon_shell_combobox_change)

    @property
    def input_parameters(self):

        def str2int(v):
            try:
                return int(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================
        fp_out = self.ui.lineEdit_in_fp_out.text()
        unique_shell = str2int(self.ui.lineEdit_in_shell.text())

        # ======================================================
        # check if necessary inputs are provided for calculation
        # ======================================================

        # ==============================
        # validate individual parameters
        # ==============================

        # ================
        # units conversion
        # ================

        return dict(fp_out=fp_out, unique_shell=unique_shell)

    @property
    def output_parameters(self):
        return self.__output_fire_curve

    @output_parameters.setter
    def output_parameters(self, v):
        self.__output_fire_curve['time'] = v['time']
        self.__output_fire_curve['temperature'] = v['temperature']

    def __upon_output_file_selection_step_1(self):
        self.statusBar().showMessage('Processing *.out file ...')
        self.ui.lineEdit_in_shell.setDisabled(True)
        self.ui.comboBox_in_shell.setDisabled(True)
        self.ui.pushButton_ok.setDisabled(True)
        self.ui.pushButton_fp_out.setDisabled(True)

        # -----------------
        # resolve file path
        # -----------------
        fp = self.select_file_path()
        if not fp:
            self.statusBar().showMessage('Nothing selected.')
            self.ui.lineEdit_in_shell.setEnabled(True)
            self.ui.comboBox_in_shell.setEnabled(True)
            self.ui.pushButton_ok.setEnabled(True)
            self.ui.pushButton_fp_out.setEnabled(True)
            return
        else:
            self.ui.lineEdit_in_fp_out.setText(fp)
            self.__fp_out = fp
            self.__fp_out_strain_csv = path.join(path.dirname(fp), path.basename(fp) + '.strain.csv')
            self.__fp_out_processed = path.join(path.dirname(fp), path.basename(fp) + '.p')

        # -----------------------------------------------------------
        # convert *.out to *.out.p, *.out.p contains only strain data
        # -----------------------------------------------------------
        t = threading.Thread(target=self.__upon_output_file_selection_step_2)
        t.start()

        self.__Signals.process_safir_out_file_complete.connect(self.__upon_output_file_selection_step_3)

        # ... follow `self.__upon_output_file_selection_step_2` and `__upon_output_file_selection_step_3`

    def __upon_output_file_selection_step_2(self):
        """Upon output file selection, step 2, analysis the `*.out` file (i.e. `fp_out`)."""
        fp_out = self.__fp_out
        fp_out_processed = self.__fp_out_processed
        fp_out_strain_csv = self.__fp_out_strain_csv

        # -----------------------------------------------------------
        # convert *.out to *.out.p, *.out.p contains only strain data
        # -----------------------------------------------------------
        try:
            out2pstrain(fp_out, fp_out_processed)
        except Exception as e:
            self.__dict_out = ValueError(f'Failed to convert `*.out` to `*.out.p`. {e}')
            self.__Signals.process_safir_out_file_complete.emit(True)
            return

        # --------------------------------------
        # convert *.out.p to data in dict format
        # --------------------------------------
        # dict format {'list_shell': [...], 'list_surf': [...], 'list_rebar': [...], ...}
        try:
            dict_out = pstrain2dict(fp_out_processed)
        except Exception as e:
            self.__dict_out = ValueError(f'Failed to convert `*.out.p` to dict. {e}')
            self.__Signals.process_safir_out_file_complete.emit(True)
            return

        try:
            save_csv(fp_out_strain_csv, **dict_out)
        except Exception as e:
            self.__dict_out = ValueError(f'Failed to save strain data as *.csv. {e}')
            self.__Signals.process_safir_out_file_complete.emit(True)
            return

        self.__dict_out = dict_out

        self.__Signals.process_safir_out_file_complete.emit(True)

    @Slot(bool)
    def __upon_output_file_selection_step_3(self, v):
        if v:
            if isinstance(self.__dict_out, Exception):
                self.statusBar().showMessage(f'{self.__dict_out}')
                return

            list_unique_shell = list(set(self.__dict_out['list_shell']))
            list_unique_shell.sort()
            list_unique_shell = [f'{i:g}' for i in list_unique_shell]

            self.ui.comboBox_in_shell.setEnabled(True)
            self.ui.lineEdit_in_shell.setEnabled(True)
            self.ui.pushButton_ok.setEnabled(True)
            self.ui.comboBox_in_shell.clear()
            self.ui.comboBox_in_shell.currentIndexChanged.disconnect()
            self.ui.comboBox_in_shell.addItems(list_unique_shell)
            self.ui.comboBox_in_shell.currentIndexChanged.connect(self.__upon_shell_combobox_change)

            self.ui.pushButton_fp_out.setEnabled(True)
            self.statusBar().showMessage('Successfully processed *.out file.')
            self.repaint()

    def __upon_shell_combobox_change(self):
        self.ui.lineEdit_in_shell.setText(self.ui.comboBox_in_shell.currentText())
        self.ok_silent()

    def ok_silent(self):

        # --------------------
        # Parse inputs from UI
        # --------------------
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            return ValueError(f'Failed to parse inputs {e}')

        # Check if user defined `unique_shell` exists
        if not input_parameters['unique_shell'] in self.__dict_out['list_shell']:
            return ValueError(f'Shell index not found.')

        # -------------------------------------------------------
        # Make strain evaluation data for selected `unique_shell`
        # -------------------------------------------------------
        try:
            self.__strain_lines = make_strain_lines_for_given_shell(input_parameters['unique_shell'], **self.__dict_out)
        except Exception as e:
            return ValueError(f'Failed to make strain lines {e}')

        # ------------------
        # Cast outputs to UI
        # ------------------
        try:
            self.show_results_in_figure()
            self.show_results_in_table()
        except Exception as e:
            return ValueError(f'Failed to show figure and table {e}')

        self.statusBar().showMessage('Calculation complete')
        self.repaint()

        return 0

    def ok(self):

        res = self.ok_silent()

        if isinstance(res, Exception):
            self.statusBar().showMessage(f'{res}')

    def make_figure_and_table(self, unique_shell: int, **kwargs):
        self.__strain_lines = make_strain_lines_for_given_shell(**kwargs)

    def select_file_path(self):
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            "~/",
            "Safir output file (*.out *.OUT *.txt)")

        # paste the select file path to the ui object
        return path_to_file

    def show_results_in_table(self):

        # output_parameters = self.output_parameters

        list_x = [list(i['x']) for i in self.__strain_lines]
        list_y = [i['y'] for i in self.__strain_lines]
        list_label = [i['label'] for i in self.__strain_lines]

        # make a full x values
        x_all = []
        for i in self.__strain_lines:
            x_all += list(i['x'])
        x_all = list(set(x_all))
        x_all.sort()

        # fill y values to match len(x_all)
        for i in range(len(list_x)):
            x = list_x[i]
            y = list_y[i]
            y_ = [0] * len(x_all)
            for j, v in enumerate(x_all):
                try:
                    y_[j] = y[x.index(v)]
                except ValueError:
                    pass
            list_y[i] = y_
            print(len(y_))

        list_content = [x_all]
        [list_content.append(i) for i in list_y]
        list_content = [[float(j) for j in i] for i in zip(*list_content)]

        # print results (for console enabled version only)

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError as e:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=['time'] + list_label,
            window_title='Table',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        # output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Figure')
            self.__Figure_ax = self.__Figure.add_subplots()
            self.activated_dialogs = self.__Figure
            self.activated_dialogs = self.__Figure_ax
        else:
            self.__Figure_ax.clear()

        for i in self.__strain_lines:
            self.__Figure_ax.plot(i['x'] / 60, i['y'], label=i['label'])

        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Strain')
        self.__Figure_ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='small').set_visible(True)
        self.__Figure.figure.tight_layout()

        self.__Figure.figure_canvas.draw()
        self.__Figure.show()

        return True


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
