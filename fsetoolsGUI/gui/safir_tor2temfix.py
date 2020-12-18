import os

from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QGridLayout, QCheckBox

from fsetoolsGUI.etc.safir import safir_tor2tem, safir_pull_tems
from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.bases.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0631'
    app_name_short = 'Safir\ntor to tem'
    app_name_long = "Safir 'tor' to 'tem' batch processor"

    def __init__(self, parent=None, post_stats: bool = True):
        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        # ================================
        # instantiation super and setup ui
        # ================================
        self.ui.p3_example.setHidden(True)
        self.ui.p3_about.setHidden(True)
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_input_root_dir', 'Input files root dir.', '...', unit_obj='QPushButton', min_width=200)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_tor2temfix', 'TorToTemFix.exe file path', '...', unit_obj='QPushButton')
        self.ui.p2_in_pull_tem = QCheckBox('Pull all *.tem files?')
        self.ui.p2_layout.addWidget(self.ui.p2_in_pull_tem, c.count, 0, 1, 3)

        # default parameters
        self.ui.p2_in_fp_tor2temfix.setText(os.path.join('c:', os.sep, 'Program Files', 'GiD', 'GiD 12.0', 'problemtypes', 'SAFIR2019', 'Safir_Thermal_2d.gid', 'TorToTemFix.exe'))

        # signals and slots
        self.ui.p2_in_fp_input_root_dir_unit.clicked.connect(lambda: self.ui.p2_in_fp_input_root_dir.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')))
        self.ui.p2_in_fp_tor2temfix_unit.clicked.connect(
            lambda: self.dialog_open_file(
                'Select TorToTemFix executable',
                '(*.exe)',
                dir_default=self.ui.p2_in_fp_tor2temfix.text(),
                func_to_assign_fp=self.ui.p2_in_fp_tor2temfix.setText
            )
        )

    def submit(self):
        self.calculate(**self.input_parameters)

    @staticmethod
    def calculate(
            fp_input_root_dir,
            fp_tor2temfix=None,
            pull_tems: bool = False,
    ):
        safir_tor2tem(dir_work=fp_input_root_dir, fp_tor2temfix=fp_tor2temfix)

        if pull_tems:
            safir_pull_tems(dir_work=fp_input_root_dir)

    @property
    def input_parameters(self):
        return dict(
            fp_input_root_dir=self.ui.p2_in_fp_input_root_dir.text(),
            fp_tor2temfix=self.ui.p2_in_fp_tor2temfix.text(),
            pull_tems=self.ui.p2_in_pull_tem.isChecked()
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
