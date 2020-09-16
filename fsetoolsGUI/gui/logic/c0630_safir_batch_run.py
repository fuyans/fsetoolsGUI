import os
import threading
from os import path

from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QLabel, QGridLayout, QFileDialog

from fsetoolsGUI import logger
from fsetoolsGUI.etc.safir import safir_batch_run
from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter, ProgressBar


class Signals(QtCore.QObject):
    __process_safir_out_file_complete = QtCore.Signal(bool)
    __progress = QtCore.Signal(int)

    @property
    def process_safir_out_file_complete(self) -> QtCore.Signal:
        return self.__process_safir_out_file_complete

    @property
    def progress(self) -> QtCore.Signal:
        return self.__progress


class App(AppBaseClass):
    app_id = '0630'
    app_name_short = 'Safir\nbatch\nprocsser'
    app_name_long = 'Safir batch run processor'

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        self.__Signals = Signals()
        self.__progress_bar = ProgressBar('Progress', parent=self, initial_value=0)
        self.activated_dialogs.append(self.__progress_bar)

        # ================================
        # instantiation super and setup ui
        # ================================
        self.ui.p3_example.setHidden(True)
        self.ui.p3_about.setHidden(True)
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_input_root_dir', 'Input files root dir.', '...', 0, unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_safir_exe', 'Safir exe file path', '...', 150, unit_obj='QPushButton')
        _ = QLabel('SAFIR 2019.a.3 later do not run torsion files. This app switches back to SAFIR 2016.c.0 for running torsion analysis, make sure `safir2016c0.exe` '
                   'is available in the above selected folder.')
        _.setWordWrap(True)
        self.ui.p2_layout.addWidget(_, c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_n_mp', 'No. of processes')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_timeout', 'timeout', 's')

        # default parameters
        self.ui.p2_in_fp_safir_exe.setText(os.path.join('c:', os.sep, 'work', 'fem', 'SAFIR', 'safir.exe'))
        self.ui.p2_in_n_mp.setText('2')
        self.ui.p2_in_timeout.setText('3600')

        # signals and slots
        self.__progress_bar.Signals.progress.connect(self.__progress_bar.update_progress_bar)
        self.ui.p2_in_fp_safir_exe_unit.clicked.connect(
            lambda: self.ui.p2_in_fp_safir_exe.setText(QFileDialog.getOpenFileName(self, 'Select SAFIR executable', self.ui.p2_in_fp_safir_exe.text(), '(*.exe)')[0])
        )
        self.ui.p2_in_fp_input_root_dir_unit.clicked.connect(lambda: self.ui.p2_in_fp_input_root_dir.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')))

    def example(self):
        pass  # placeholder method to stop warning, not used.

    def ok(self):
        self.__progress_bar.show()
        self.calculate(**self.input_parameters)

    @staticmethod
    def calculate(
            fp_safir_exe,
            fp_input_root_dir,
            timeout,
            n_mp,
            qt_progress_signal=None,
            qt_progress_signal_label=None,
            *_, **__):
        list_fp_in = list()
        for root, dirs, files in os.walk(fp_input_root_dir):
            for file_ in files:
                if file_.endswith('.in'):
                    list_fp_in.append(path.join(root, file_))

        list_kwargs_in = list()
        for i in list_fp_in:
            with open(i, 'r') as f:
                in_script = f.read()

            if 'TORSION' in in_script:
                logger.warning(f'Torsional analysis input file identified {i}')
                fp_safir_exe_ = os.path.realpath(os.path.join(os.path.dirname(fp_safir_exe), 'safir2016c0.exe'))
            else:
                fp_safir_exe_ = fp_safir_exe

            list_kwargs_in.append(dict(
                cmd=[fp_safir_exe_, path.basename(i).replace('.in', '')],
                cwd=path.dirname(i),
                fp_stdout=path.join(path.dirname(i), path.basename(i).replace('.in', '.stdout.txt')),
                timeout_seconds=timeout,
            ))

        kwargs = dict(
            list_kwargs_in=list_kwargs_in,
            n_proc=n_mp,
            dir_work=fp_input_root_dir,
            qt_progress_signal=qt_progress_signal,
            qt_progress_signal_label=qt_progress_signal_label,
        )
        t = threading.Thread(target=safir_batch_run, kwargs=kwargs)
        t.start()

    @property
    def input_parameters(self):
        def str2int(v_):
            try:
                return int(v_)
            except ValueError:
                return 0

        return dict(
            fp_safir_exe=self.ui.p2_in_fp_safir_exe.text(),
            n_mp=str2int(self.ui.p2_in_n_mp.text()) if str2int(self.ui.p2_in_n_mp.text()) else 2,
            timeout=str2int(self.ui.p2_in_timeout.text()) if str2int(self.ui.p2_in_n_mp.text()) else 1800,
            fp_input_root_dir=self.ui.p2_in_fp_input_root_dir.text(),
            qt_progress_signal=self.__progress_bar.Signals.progress,
            qt_progress_signal_label=self.__progress_bar.Signals.progress_label
        )

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
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
