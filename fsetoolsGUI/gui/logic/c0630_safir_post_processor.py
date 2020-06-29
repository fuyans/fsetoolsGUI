import copy
import logging
import multiprocessing as mp
import os
import subprocess
import threading
import time
from os import path
from typing import List, Dict, Callable

import numpy as np
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Slot

from fsetoolsGUI.etc.safir_post_processor import out2pstrain, pstrain2dict, save_csv, make_strain_lines_for_given_shell
from fsetoolsGUI.gui.layout.i0630_safir_postprocessor import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_app_template import AppBaseClass
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow

logger = logging.getLogger('gui')


def safir_batch_run_worker(args: List) -> List:
    def worker(
            cmd: str,
            cwd: str,
            fp_stdout: str = None,
            timeout_seconds: int = 1 * 60,
    ) -> List:
        try:
            if fp_stdout:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(fp_stdout, 'w+'))
            else:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(os.devnull, 'w'))
            return [cmd, 'Success']
        except subprocess.TimeoutExpired:
            return [cmd, 'Timed out']

    kwargs, q = args
    result = worker(**kwargs)
    q.put(1)
    return result


def safir_batch_copy_bc_to_input_folder(fp_bc: str, ):
    pass


class Signals(QtCore.QObject):
    __process_safir_out_file_complete = QtCore.Signal(bool)
    __progress_batch_run = QtCore.Signal(int)

    @property
    def process_safir_out_file_complete(self) -> QtCore.Signal:
        return self.__process_safir_out_file_complete

    @property
    def progress_batch_run(self) -> QtCore.Signal:
        return self.__progress_batch_run


class ProgressBar(QtWidgets.QDialog):
    def __init__(self, title: str = None, initial_value: int = 0, parent=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setWindowTitle(title)
        self.setSizeGripEnabled(False)

        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)
        self.progressbar.setValue(initial_value)

        self.button_cancel = QtWidgets.QPushButton("Cancel")

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.progressbar, 1, 0)
        self.grid_layout.addWidget(self.button_cancel, 1, 1)

        self.setLayout(self.grid_layout)

        self.resize(300, 50)

    @QtCore.Slot(int)
    def update_progress_bar(self, progress: int):
        self.progressbar.setValue(progress)


class App(AppBaseClass):
    app_id = '0630'
    app_name_short = 'Safir\npost\nprocsser'
    app_name_long = 'Safir post processor'

    def __init__(self, parent=None, mode=None):
        super().__init__(parent=parent)

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
        self.__progress_bar = ProgressBar('Progress', parent=self, initial_value=0)

        # ================================
        # instantiation super and setup ui
        # ================================
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

        self.init_batch_run()
        self.init_batch_bc()

        self.__Signals.progress_batch_run.connect(self.__progress_bar.update_progress_bar)

    def init_batch_run(self):

        def select_safir_exe_path():
            try:
                default_dir = path.dirname(path.realpath(self.ui.lineEdit_batch_run_in_safir_exe_path.text()))
                if not (path.exists(default_dir) and path.isdir(default_dir)):
                    default_dir = '~/'
            except Exception as e:
                logger.error(f'Unable to get old dir {e}')
                default_dir = '~/'

            fp = self.select_file_path(title='Select Safir executable', default_dir=default_dir,
                                       file_type="Safir executable (*.exe)")
            if fp:
                self.ui.lineEdit_batch_run_in_safir_exe_path.setText(fp)

        def select_safir_input_root_folder():
            try:
                default_dir = path.realpath(self.ui.lineEdit_batch_run_in_safir_input_folder.text())
                if not (path.exists(default_dir) and path.isdir(default_dir)):
                    default_dir = '~/'
            except Exception as e:
                logger.error(f'Unable to get old dir {e}')
                default_dir = '~/'
            fp = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder', default_dir)
            if fp:
                self.ui.lineEdit_batch_run_in_safir_input_folder.setText(fp)

        def batch_run():
            try:
                fp_safir_exe = self.ui.lineEdit_batch_run_in_safir_exe_path.text()
                dir_work = self.ui.lineEdit_batch_run_in_safir_input_folder.text()
                timeout_seconds = int(self.ui.lineEdit_batch_run_in_timeout.text())

                list_fp_in = list()
                for root, dirs, files in os.walk(dir_work):
                    for file_ in files:
                        if file_.endswith('.in'):
                            list_fp_in.append(path.join(root, file_))

                list_kwargs_in = list()
                for i in list_fp_in:
                    list_kwargs_in.append(dict(
                        cmd=[fp_safir_exe, path.basename(i).replace('.in', '')],
                        cwd=path.dirname(i),
                        fp_stdout=path.join(path.dirname(i), path.basename(i).replace('.in', '.stdout.txt')),
                        timeout_seconds=timeout_seconds,
                    ))

                kwargs = dict(
                    list_kwargs_in=list_kwargs_in,
                    func_mp=safir_batch_run_worker,
                    n_proc=int(self.ui.lineEdit_batch_run_in_processes.text()) or 1,
                    dir_work=dir_work
                )
                t = threading.Thread(target=self.safir_batch_run, kwargs=kwargs)
                t.start()

                self.__progress_bar.show()

            except Exception as e:
                self.statusBar().showMessage(f'Simulation failed {e}')

        self.ui.pushButton_batch_run_in_safir_exe_path.clicked.connect(select_safir_exe_path)
        self.ui.pushButton_batch_run_in_safir_input_folder.clicked.connect(select_safir_input_root_folder)
        self.ui.pushButton_batch_run_submit.clicked.connect(batch_run)

    def init_batch_bc(self):
        def select_root_dir():
            fp = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
            if fp:
                fp = path.realpath(fp)
                self.ui.lineEdit_batchbc_root_dir.setText(fp)

                list_fp = list()
                for root, dirs, files in os.walk(fp):
                    for file_ in files:
                        if file_.endswith('.in'):
                            relative_path = path.realpath(root).lstrip(fp)
                            # relative_path.lstrip(fp)
                            print(relative_path, fp)
                            list_fp.append(relative_path)
                list_fp = list(set(list_fp))
                list_fp = ['rel_dir,val'] + [f'{i},{j}' for i, j in zip(list_fp, [1] * len(list_fp))]

                with open(path.join(fp, 'bc_reduction_template.csv'), 'w+') as f:
                    f.write('\n'.join(list_fp))

        def select_bc_file():
            fp, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select bc file')
            if fp:
                self.ui.lineEdit_batchbc_bc_file.setText(fp)

        def run():
            dir_work = self.ui.lineEdit_batchbc_root_dir.text()
            fp_bc = self.ui.lineEdit_batchbc_bc_file.text()
            is_apply_reduction_factor = self.ui.checkBox_batchbc_reduction_factor.isChecked()

            bc = np.genfromtxt(fp_bc, delimiter=',')

            list_dir = list()
            for root, dirs, files in os.walk(dir_work):
                for file_ in files:
                    if file_.endswith('.in'):
                        list_dir.append(path.realpath(root))

            dict_reduction = dict()
            if is_apply_reduction_factor:
                for i, j in np.recfromcsv(path.join(dir_work, 'bc_reduction.csv'), autostrip=True, dtype=None):
                    k = i.decode('utf-8')
                    dict_reduction[k] = j

            for dir in list_dir:
                if dict_reduction:
                    k = dir.lstrip(dir_work)
                    print(k, list(dict_reduction.keys()))
                    reduction_value = dict_reduction[k]
                    bc_ = copy.copy(bc)
                    bc_[:, 1] = bc_[:, 1] * reduction_value
                else:
                    bc_ = bc
                np.savetxt(path.join(dir, path.basename(fp_bc)), bc_, delimiter=',', fmt='%g')

        self.ui.pushButton_batchbc_root_dir.clicked.connect(select_root_dir)
        self.ui.pushButton_batchbc_bc_file.clicked.connect(select_bc_file)
        self.ui.pushButton_batchbc_ok.clicked.connect(run)
        pass

    def safir_batch_run(self, list_kwargs_in: List[Dict], func_mp: Callable, n_proc: int = 1, dir_work: str = None, ):
        # ------------------------------------------
        # prepare variables used for multiprocessing
        # ------------------------------------------
        m, p = mp.Manager(), mp.Pool(n_proc, maxtasksperchild=1000)
        q = m.Queue()
        jobs = p.map_async(func_mp, [(dict_, q) for dict_ in list_kwargs_in])
        n_simulations = len(list_kwargs_in)

        # ---------------------
        # multiprocessing start
        # ---------------------
        while True:
            if jobs.ready():
                self.__Signals.progress_batch_run.emit(100)
                break  # complete
            else:
                self.__Signals.progress_batch_run.emit(int(q.qsize() / n_simulations * 100))
                time.sleep(1)  # in progress

        # --------------------------------------------
        # pull results and close multiprocess pipeline
        # --------------------------------------------
        print('d')
        p.close()
        p.join()
        mp_out = jobs.get()
        time.sleep(0.5)

        # ----------------------
        # save and print summary
        # ----------------------
        if dir_work:
            out = mp_out
            len_1 = int(max([len(' '.join(i[0])) for i in out]))
            summary = '\n'.join([f'{" ".join(i[0]):<{len_1}} - {i[1]:<{len_1}}' for i in out])
            print(summary)
            with open(path.join(dir_work, 'summary.txt'), 'w+') as f:
                f.write(summary)

        return mp_out

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
        self.post_strain_ok_slient()

    def post_strain_ok_slient(self):

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

    def post_strain_ok(self):

        res = self.post_strain_ok_slient()

        if isinstance(res, Exception):
            self.statusBar().showMessage(f'{res}')

    def make_figure_and_table(self, unique_shell: int, **kwargs):
        self.__strain_lines = make_strain_lines_for_given_shell(**kwargs)

    def select_file_path(self, title: str = "Select file", default_dir: str = "~/",
                         file_type: str = "Safir output file (*.out *.OUT *.txt)"):
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, title, default_dir, file_type)

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

    def ok(self):
        pass

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


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    # app2 = ProgressBar('Progress bar')
    # app2.show()
    qapp.exec_()
