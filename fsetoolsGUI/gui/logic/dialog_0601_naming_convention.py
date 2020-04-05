import re
from datetime import datetime

from PySide2 import QtGui

from fsetoolsGUI.gui.layout.dialog_0601_naming_convention import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow


class Dialog0601(QMainWindow):
    __re_date = re.compile(r'[0-9]{4,6}')
    __re_project_no = re.compile(r'[a-zA-Z]{2}[0-9]{5,6}')
    __re_project_stage = re.compile(r'.+')
    __re_project_title = re.compile(r'.+')

    def __init__(self, parent=None):
        # init
        super().__init__(
            module_id='0601',
            parent=parent,
            shortcut_Return=self.copy_file_name,
            freeze_window_size=True,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # default values
        self.ui.comboBox_6_type.setCurrentIndex(4)
        self.ui.checkBox_replace_spaces.setChecked(True)
        self.ui.lineEdit_1_date.setText(datetime.today().strftime('%Y%m%d')[2:])
        self.ui.lineEdit_3_project_no.setText(None)
        self.ui.lineEdit_4_project_stage.setText(None)
        self.ui.lineEdit_5_title.setText(None)

        # placeholder texts
        self.ui.lineEdit_3_project_no.setPlaceholderText('XX00001')
        self.ui.lineEdit_4_project_stage.setPlaceholderText('Stage 3')
        self.ui.lineEdit_5_title.setPlaceholderText('Fire safety strategy')

        # validators
        # self.ui.lineEdit_1_date.setValidator((QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]{6,8}'))))
        # self.ui.lineEdit_3_project_no.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[A-Z]{1,2}[0-9]{1,5}')))
        # self.ui.lineEdit_4_project_stage.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\w\-. ]+$')))
        # self.ui.lineEdit_5_title.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\w\-. ]+$')))

        # signal and slots
        self.ui.lineEdit_1_date.textChanged.connect(self.calculate)
        self.ui.comboBox_2_revision.currentTextChanged.connect(self.calculate)
        self.ui.lineEdit_3_project_no.textChanged.connect(self.calculate)
        self.ui.lineEdit_4_project_stage.textChanged.connect(self.calculate)
        self.ui.lineEdit_5_title.textChanged.connect(self.calculate)
        self.ui.comboBox_6_type.currentTextChanged.connect(self.calculate)
        self.ui.comboBox_7_security_status.currentTextChanged.connect(self.calculate)
        self.ui.checkBox_replace_spaces.stateChanged.connect(self.calculate)
        self.ui.pushButton_ok.clicked.connect(self.copy_file_name)

        # clean up
        self.calculate()  # make file name, do not leave the output slot empty
        self.ui.pushButton_ok.setText('Copy')
        self.ui.pushButton_ok.setToolTip('Click (or press Enter) to copy the generated file name')
        self.repaint()

    @property
    def input_parameters(self) -> dict:

        # ====================
        # parse values from ui
        # ====================
        date = self.ui.lineEdit_1_date.text()
        revision = self.ui.comboBox_2_revision.currentText()[0:3]  # obtain the first three letters/digits, i.e. D00
        project_no = self.ui.lineEdit_3_project_no.text().upper()  # capitalise office designation letters
        project_stage = self.ui.lineEdit_4_project_stage.text()
        title = self.ui.lineEdit_5_title.text()
        type = self.ui.comboBox_6_type.currentText()[0:2]
        security_status = self.ui.comboBox_7_security_status.currentText()[0:3]

        # =====================
        # validate input values
        # =====================
        if self.__re_date.match(date) is None:
            raise ValueError('Date should be in format YYMMDD or YYYYMMDD')
        if self.__re_project_no.match(project_no) is None:
            raise ValueError('Project number should be in format XX#####, '
                             'where XX is office designation and # is a project number')
        if self.__re_project_stage.match(project_stage) is None:
            raise ValueError('Project stage is missing')
        if self.__re_project_title.match(title) is None:
            raise ValueError('Project title is missing')

        return dict(date=date, revision=revision, project_no=project_no, project_stage=project_stage, title=title,
                    type=type, security_status=security_status)

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
        if self.ui.checkBox_replace_spaces.isChecked():
            file_name = file_name.replace(' ', '_')
        output_parameters = dict(file_name=file_name)

        # ==================
        # cast results to ui
        # ==================
        try:
            self.output_parameters = output_parameters
        except Exception as e:
            self.statusBar().showMessage(f'{e}')

        self.ui.lineEdit_out_result.selectAll()
        self.ui.statusbar.showMessage('File name is copied.')

        self.repaint()

    @property
    def output_parameters(self):
        return

    @output_parameters.setter
    def output_parameters(self, v):
        try:
            file_name = v['file_name']
        except KeyError:
            raise KeyError('Not enough output parameters provided to self.output_parameters')

        self.ui.lineEdit_out_result.setText(file_name)

    def copy_file_name(self):
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(self.ui.lineEdit_out_result.text())
        self.ui.lineEdit_out_result.selectAll()

        self.ui.statusbar.showMessage('File name is copied.')


if __name__ == "__main__":
    from PySide2 import QtWidgets
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0601()
    app.show()
    qapp.exec_()
