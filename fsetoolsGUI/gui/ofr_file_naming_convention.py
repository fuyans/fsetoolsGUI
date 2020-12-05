import re
from datetime import datetime

from PySide2 import QtGui
from PySide2.QtWidgets import QGridLayout, QLabel, QCheckBox

from fsetoolsGUI.gui.bases.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.bases.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0601'
    app_name_short = 'OFR\nfile naming\nconvention'
    app_name_long = 'OFR File name generator'
    __re_date = re.compile(r'[0-9]{4,6}')
    __re_project_no = re.compile(r'[a-zA-Z]{2}[0-9]{5,6}')
    __re_project_stage = re.compile(r'.+')
    __re_project_title = re.compile(r'.+')

    def __init__(self, parent=None, post_stats: bool = True):
        # init
        super().__init__(parent=parent, post_stats=post_stats, ui=AppBaseClassUISimplified01)

        # ==============
        # Instantiate UI
        # ==============
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)

        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_date', 'Date', None, 180)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_revision', 'Revision', None, obj='QComboBox')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_project_no', 'Project no.', None)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_project_stage', 'Project stage', None)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_title', 'Document title', None)
        self.ui.p2_in_replace_spaces = QCheckBox('Replace spaces with underscores')
        self.ui.p2_layout.addWidget(self.ui.p2_in_replace_spaces, c.count, 1, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_type', 'Document type', None, obj='QComboBox')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_security_status', 'Security status', None, obj='QComboBox')

        self.ui.p2_in_revision.addItems([
            "Q00: First issue for internal review",
            "Q01: Reviewer's comments",
            "Q02: Authoriser's comments",
            "D00: First issue to others for comment",
            "D01: Sub-sequent external reviews",
            "R00: First issue",
            "R01: Second issue",
        ])
        self.ui.p2_in_type.addItems([
            "GA: General admin",
            "MD: Marketing",
            "FP: Fee proposal",
            "LT: Letter",
            "DN: Design note",
            "OF: Outline strategy",
            "DF: Detailed strategy",
            "RF: Retrospective strategy",
            "FA: Fire risk assessment",
            "FS: Fire survey report",
            "FN: File note",
            "MN: Meeting notes",
            "CS: Calculation sheet",
            "SK: Sketch",
            "DW: Drawing",
            "XO: Expert opinion",
        ])
        self.ui.p2_in_security_status.addItems([
            "CIC: Commercial in confidence",
            "WPC: Without prejudice and confidential",
            "SDS: Secure document",
            "FID: Free issue document (no security status)",
        ])

        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_out_result', 'File name', None)

        self.ui.p3_example.setHidden(True)
        self.ui.p2_in_date.setToolTip('In format YYMMDD (e.g. 210131) or YYYYMMDD (e.g. 20210131)')
        self.ui.p2_in_title.setToolTip('In plain English')
        self.ui.p2_out_result.setReadOnly(True)
        self.ui.p2_out_result.setToolTip('Double click to select text')

        # ==================
        # Set default values
        # ==================
        self.ui.p2_in_type.setCurrentIndex(4)
        self.ui.p2_in_replace_spaces.setChecked(True)
        self.ui.p2_in_date.setText(datetime.today().strftime('%Y%m%d')[2:])
        self.ui.p2_in_project_no.setText(None)
        self.ui.p2_in_project_stage.setText(None)
        self.ui.p2_in_title.setText(None)

        # =====================
        # Set placeholder texts
        # =====================
        # self.ui.p2_in_revision.setPlaceholderText('Q00')
        self.ui.p2_in_project_no.setPlaceholderText('XX00001')
        self.ui.p2_in_project_stage.setPlaceholderText('WP1')
        self.ui.p2_in_title.setPlaceholderText('Detailed Strategy')

        # =====================
        # Set signals and slots
        # =====================
        self.ui.p2_in_date.textChanged.connect(self.calculate)
        self.ui.p2_in_revision.currentTextChanged.connect(self.calculate)
        self.ui.p2_in_project_no.textChanged.connect(self.calculate)
        self.ui.p2_in_project_stage.textChanged.connect(self.calculate)
        self.ui.p2_in_title.textChanged.connect(self.calculate)
        self.ui.p2_in_type.currentTextChanged.connect(self.calculate)
        self.ui.p2_in_security_status.currentTextChanged.connect(self.calculate)
        self.ui.p2_in_replace_spaces.stateChanged.connect(self.calculate)

        # clean up
        # self.calculate()  # make file name, do not leave the output slot empty
        self.ui.p3_submit.setText('Copy')
        self.repaint()

    @property
    def input_parameters(self) -> dict:

        # ====================
        # parse values from ui
        # ====================
        date = self.ui.p2_in_date.text()
        revision = self.ui.p2_in_revision.currentText()[0:3]  # obtain the first three letters/digits, i.e. D00
        project_no = self.ui.p2_in_project_no.text().upper()  # capitalise office designation letters
        project_stage = self.ui.p2_in_project_stage.text()
        title = self.ui.p2_in_title.text()
        type = self.ui.p2_in_type.currentText()[0:2]
        security_status = self.ui.p2_in_security_status.currentText()[0:3]

        # =====================
        # validate input values
        # =====================
        if self.__re_date.match(date) is None:
            raise ValueError('Date should be in format YYMMDD or YYYYMMDD')
        if self.__re_project_no.match(project_no) is None:
            raise ValueError('Project number should be in format XX#####')
        if self.__re_project_stage.match(project_stage) is None:
            raise ValueError('Project stage is missing')
        if self.__re_project_title.match(title) is None:
            raise ValueError('Project title is missing')

        return dict(date=date, revision=revision, project_no=project_no, project_stage=project_stage, title=title,
                    type=type, security_status=security_status)

    def ok(self):
        self.calculate()
        self.copy_file_name()

    def calculate(self):
        # ======================
        # parse input parameters
        # ======================
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            self.statusBar().showMessage(f'{e}')
            return
        try:
            date = input_parameters['date']
            revision = input_parameters['revision']
            project_no = input_parameters['project_no']
            project_stage = input_parameters['project_stage']
            title = input_parameters['title']
            type = input_parameters['type']
            security_status = input_parameters['security_status']
        except KeyError:
            self.statusBar().showMessage('Missing input parameters from `self.input_parameters`')
            return

        # ==============
        # make file name
        # ==============
        file_name = '-'.join([date, revision, project_no, project_stage, title, type, security_status])
        if self.ui.p2_in_replace_spaces.isChecked():
            file_name = file_name.replace(' ', '_')
        output_parameters = dict(file_name=file_name)

        # ==================
        # cast results to ui
        # ==================
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'{e}')

        self.ui.p2_out_result.selectAll()
        self.ui.statusbar.showMessage('File name is copied.')

        self.repaint()

    def example(self):
        pass

    @property
    def output_parameters(self):
        return

    @output_parameters.setter
    def output_parameters(self, v):
        try:
            file_name = v['file_name']
        except KeyError:
            raise KeyError('Not enough output parameters provided to self.output_parameters')

        self.ui.p2_out_result.setText(file_name)

    def copy_file_name(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.ui.p2_out_result.text())
        self.ui.p2_out_result.selectAll()

        self.ui.statusbar.showMessage('File name is copied.')


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
