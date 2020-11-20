import datetime
import logging
import threading
from os import path

import requests
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QErrorMessage, QPushButton, QLineEdit, QInputDialog
from PySide2.QtWidgets import QMainWindow, QSizePolicy, QWidget, QGridLayout, QGroupBox, QLabel
from packaging import version

from fsetoolsGUI import __version__, __build__, __date_released__, __expiry_period_days__, __remote_version_url__, __root_dir__, logger
from fsetoolsGUI.gui import qt_css
from fsetoolsGUI.gui.c0000_utilities import *
from fsetoolsGUI.gui.c0101_adb_data_sheet_1 import App as App0101
from fsetoolsGUI.gui.c0102_bs9999_data_sheet_1 import App as App0102
from fsetoolsGUI.gui.c0103_bs9999_merging_flow import App as App0103
from fsetoolsGUI.gui.c0104_adb_merging_flow import App as App0104
from fsetoolsGUI.gui.c0111_pd7974_detector_activation import App as App0111
from fsetoolsGUI.gui.c0311_ec_external_column import App as App0311
from fsetoolsGUI.gui.c0401_br187_parallel_simple import App as App0401
from fsetoolsGUI.gui.c0402_br187_perpendicular_simple import App as App0402
from fsetoolsGUI.gui.c0403_br187_parallel_complex import App as App0403
from fsetoolsGUI.gui.c0404_br187_perpendicular_complex import App as App0404
from fsetoolsGUI.gui.c0405_tra_3d_point import App as App0405
from fsetoolsGUI.gui.c0406_tra_2d_xy_contour import App as App0406
from fsetoolsGUI.gui.c0407_tra_enclosure import App as App0407
from fsetoolsGUI.gui.c0411_ec_external_flame import App as App0411
from fsetoolsGUI.gui.c0601_naming_convention import App as App0601
from fsetoolsGUI.gui.c0602_pd7974_flame_height import App as App0602
from fsetoolsGUI.gui.c0610_ec_parametric_fire import App as App0610
from fsetoolsGUI.gui.c0611_travelling_fire import App as App0611
from fsetoolsGUI.gui.c0612_ec_protected_steel_heat_transfer import App as App0612
from fsetoolsGUI.gui.c0613_din_en_parametric_fire import App as App0613
from fsetoolsGUI.gui.c0614_travelling_fire_flux import App as App0614
from fsetoolsGUI.gui.c0615_iso_834_fire import App as App0615
from fsetoolsGUI.gui.c0620_probability_distribution import App as App0620
from fsetoolsGUI.gui.c0630_safir_batch_run import App as App0630
from fsetoolsGUI.gui.c0631_safir_tor2temfix import App as App0631
from fsetoolsGUI.gui.c0639_safir_post_processor_old import App as App0639
from fsetoolsGUI.gui.c0640_sfeprapy_mcs0 import App as App0640
from fsetoolsGUI.gui.c0641_sfeprapy_pre_bluebeam import App as App0641
from fsetoolsGUI.gui.c0642_sfeprapy_post_make_plots import App as App0642
from fsetoolsGUI.gui.c0643_sfeprapy_post_make_fire import App as App0643
from fsetoolsGUI.gui.c0660_ht1d_inexplicit import App as App0660


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class QDialogLogger(QtWidgets.QDialog, QPlainTextEditLogger):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle('Log')

        qt_logger = QPlainTextEditLogger(self)
        qt_logger.setLevel(logging.INFO)
        qt_logger.setFormatter(logging.Formatter('%(levelname)-8s [%(filename).5s:%(lineno)d] %(message)s'))
        logger.addHandler(qt_logger)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(qt_logger.widget)

        self.setLayout(layout)
        self.resize(600, 400)


class AppsCollection:
    __apps = {
        '0101': App0101,
        '0102': App0102,
        '0103': App0103,
        '0104': App0104,
        '0111': App0111,
        '0311': App0311,
        '0401': App0401,
        '0402': App0402,
        '0403': App0403,
        '0404': App0404,
        '0405': App0405,
        '0406': App0406,
        '0407': App0407,
        '0411': App0411,
        '0601': App0601,
        '0602': App0602,
        '0610': App0610,
        '0611': App0611,
        '0612': App0612,
        '0613': App0613,
        '0614': App0614,
        '0615': App0615,
        '0620': App0620,
        '0630': App0630,
        '0631': App0631,
        '0639': App0639,
        '0640': App0640,
        '0641': App0641,
        '0642': App0642,
        '0643': App0643,
        '0660': App0660,
    }

    def __init__(self):
        pass

    def app_name_long(self, code: str):
        try:
            return self.__apps[code].app_name_long
        except AttributeError:
            return None

    def app_name_short(self, code: str):
        try:
            return self.__apps[code].app_name_short
        except AttributeError:
            return None

    def app_name_short_and_long(self, code: str):
        return f'{self.app_name_short(code)}', f'{self.app_name_long(code)}'

    def doc_file_path(self, code: str):
        return path.join(__root_dir__, 'gui', 'docs', f'{code}.html')

    def doc_html(self, code: str):
        with open(self.doc_file_path(code), 'r') as f:
            return f.read()

    def print_all_app_info(self, sort_by: str = 'module_code', html: bool = True):
        module_code = list(self.__apps.keys())
        module_app_name_long = list()

        l1, l2 = 0, 0
        for i in self.__apps:
            module_app_name_long.append(self.__apps[i].app_name_long)

            if l1 < len(i):
                l1 = len(i)
            if l2 < len(module_app_name_long[-1]):
                l2 = len(module_app_name_long[-1])

        if sort_by == 'module_code':
            module_app_name_long = [x for _, x in sorted(zip(module_code, module_app_name_long))]
            module_code = sorted(module_code)
        elif sort_by == 'module_app_name_long':
            module_code = [x for _, x in sorted(zip(module_app_name_long, module_code))]
            module_app_name_long = sorted(module_app_name_long)
        else:
            raise ValueError('Unknown `sorted_by`, it can be either "module_code" or "module_app_name_long"')

        if html:
            table_html = ['<table style="float:left">']
            table_html.append('<tr>'
                              '<th style="text-align:left">Module Code    </th>'
                              '<th style="text-align:left">Module Name</th>'
                              '</tr>')
            for i in range(len(module_code)):
                table_html.append(f'<tr><td>{module_code[i]}</td><td>{module_app_name_long[i]}</td></tr>')
            table_html.append('</table>')
            return '\n'.join(table_html)
        else:
            return '\n'.join([f'{i:<{l1}}     {j:<{l2}}' for i, j in zip(module_code, module_app_name_long)])

    def activate_app(self, code: str, parent=None):
        def func():
            try:
                app = self.__apps[code]
                if code == '0101' or code == '0102':
                    # todo: 0101 and 0102 do not run without parent
                    app = app(parent=parent)
                else:
                    app = app()
                    parent.activated_dialogs.append(app)
                app.show()
                logger.info(f'Successfully loaded module {code}')
            except Exception as e:
                logger.error(f'Failed to load module {code}, {e}')
                raise e

        return func


class Signals(QtCore.QObject):
    """
    Collection of signal(s) that used in the app.
    """

    check_update_complete = QtCore.Signal(bool)


class AppUI(object):
    def setupUi(self, main_window):
        self.central_widget = QWidget(main_window)

        self.p0_layout = QGridLayout(self.central_widget)
        self.p0_layout.setSpacing(10), self.p0_layout.setContentsMargins(15, 15, 15, 15)

        self.page_2 = QGroupBox(self.central_widget)
        self.label_version = QLabel(__version__)
        self.label_version.setWordWrap(True)

        self.p0_layout.addWidget(self.page_2, 0, 0, 1, 1)
        self.p0_layout.addWidget(self.label_version, 1, 0, 1, 1)

        main_window.setCentralWidget(self.central_widget)

        self.page_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


class App(QMainWindow):

    def __init__(self):
        self.update_data: dict = None
        self.is_executable: bool = True
        self.Signals = Signals()
        self.__activated_dialogs = list()

        self.AppsCollection = AppsCollection()

        # ui setup
        super().__init__()
        self.ui = AppUI()
        self.ui.setupUi(self)
        self.setStyleSheet(qt_css)

        self.setWindowTitle('Fire Safety Engineering Tools')
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        # self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        # ------------------------
        # Instantiate Logger panel
        # ------------------------
        self.LoggerApp = QDialogLogger(parent=self)
        self.LoggerApp.hide()

        # ------------------------
        # Logs showing app summary
        # ------------------------
        logger.info('=' * 23)
        logger.info('FSETOOLS')
        logger.info(f'VERSION: {__version__}.')
        logger.info(f'BUILD: {__build__[2:10]}.')
        logger.info(f'RELEASED: {__date_released__}.')
        _exp = __date_released__ + datetime.timedelta(days=__expiry_period_days__) - datetime.datetime.now()
        _exp_d, _ = divmod(_exp.total_seconds(), 24 * 60 * 60)
        _exp_h, _ = divmod(_, 60 * 60)
        _exp_m, _ = divmod(_, 60)
        logger.info(f'EXPIRES IN: {_exp_d:.0f} day(s), {_exp_h:.0f} hour(s) and {_exp_m:.0f} minute(s).')
        logger.info('=' * 23)

        # --------------------------------
        # Instantiate buttons for sub-apps
        # --------------------------------
        self.add_buttons()

        # ------------
        # Check update
        # ------------
        # DEPRECIATED 20th Oct 2020. Checked updated moved to fsetoolsgui.gui.__main__
        self.Signals.check_update_complete.connect(self.setEnabled_all_buttons)
        threading.Timer(0, self.check_update).start()

        # window properties
        self.ui.label_version.setText(f'Version {__version__}')
        self.ui.label_version.setStatusTip(f'Version {__version__}')
        self.ui.label_version.setToolTip(f'Version {__version__}')
        self.ui.label_version.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # signals
        def label_version_mouse_click(event=None):
            if event and self.new_version_update_url is not None:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_update_url))

        self.ui.label_version.mousePressEvent = label_version_mouse_click

        # default values
        self.ui.dialog_error = QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')
        self.__new_version_update_url = None
        self.__dialog_opened = list()

    def add_buttons(self):
        button_collection = {
            'Miscellaneous': ['0601', '0602', '0611', '0407', '0620'],
            'B1 Means of escape': ['0101', '0102', '0104', '0103', '0111'],
            'B3 Elements of structure': ['0311', '0630', '0640', '0660'],
            'B4 External fire spread': ['0403', '0404', '0411'],
        }

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)

        self.add_button_set_to_grid(self.ui.p2_layout, 'Miscellaneous', button_collection['Miscellaneous'], 0, 0, 5)
        self.add_button_set_to_grid(self.ui.p2_layout, 'B1 Means of escape', button_collection['B1 Means of escape'], 2, 0, 5)
        self.add_button_set_to_grid(self.ui.p2_layout, 'B3 Elements of structure', button_collection['B3 Elements of structure'], 4, 0, 5)
        self.add_button_set_to_grid(self.ui.p2_layout, 'B4 External fire spread', button_collection['B4 External fire spread'], 6, 0, 5)

    def add_button_set_to_grid(self, layout: QGridLayout, label: str, button_id_list: list, row_0: int, col_0: int,
                               cols: int):

        btn_stylesheet = '''
        QPushButton {
            background-color: #ffffff;
            Text-align: center;
            /*color: #000000;*/
            padding: 0px;
            padding-left: 1px;
            padding-right: 1px;
            padding-top: 2px;
            padding-bottom: 2px;
            border: 1px solid #d2d1d2;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
            color: #ffffff;
            border: 1.5px solid #56aafb;
        }
        QPushButton:focus {
            border: 1.5px solid #3295fd;
        }
        QPushButton:pressed {
            background-color: #106bfd;
        }
        QPushButton:disabled {
            background-color: #ecf0f1;
            /*font: 11px;*/
            padding: 3px;
            color: #98989d;
            border: 1px solid #d2d1d2;
        }
        '''

        row_i, col_i = Counter(), Counter()
        row_i.reset(row_0), col_i.reset(col_0)
        layout.addWidget(QLabel(f'<b>{label}</b>'), row_i.count, col_0, 1, cols)
        for v in button_id_list:
            act_app = self.AppsCollection.activate_app(v, self)
            btn = QPushButton(self.AppsCollection.app_name_short(v))
            btn.setAutoDefault(True)  # click button upon Enter
            # remove button padding to maximum text area
            btn.setStyleSheet(btn_stylesheet)
            setattr(self.ui, f'p2_in_{v}', btn)
            getattr(self.ui, f'p2_in_{v}').clicked.connect(act_app)
            getattr(self.ui, f'p2_in_{v}').setFixedSize(76, 76)
            layout.addWidget(getattr(self.ui, f'p2_in_{v}'), row_i.value, col_i.count, 1, 1)
        row_i.add()
        col_i.reset()

    @Slot(bool)
    def setEnabled_all_buttons(self, v: bool):
        """
        To disable/enable all buttons in `groupBox` depending on `v`.
        Used as Slot to disable all buttons depend on remote version data `is_executable`.
        """
        for button in self.ui.page_2.findChildren(QPushButton):
            try:
                if button.isEnabled() != v:
                    button.setEnabled(False)
            except Exception as e:
                logger.error(f'Failed to disable button, {e}')

    def activate_app_module_id(self):
        if self.is_executable:
            txt, ok = QInputDialog.getText(
                self,
                f'Activate App by Module Code',
                f'{self.AppsCollection.print_all_app_info(sort_by="module_app_name_long")}',
                QLineEdit.Normal,
                ""
            )
            if ok and txt:
                app = self.AppsCollection.activate_app(code=txt, parent=self)
                app()

    def check_update(self):
        """
        This method will be called in a thread! Try to avoid competing with the main GUI thread, e.g. avoid repaint etc.
        """

        # parse remote version info
        logger.info('Parsing update data ...')
        target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(__remote_version_url__)])
        try:
            self.update_data = requests.get(target).json()
            logger.info(f'Successfully parsed update data')
            logger.debug(f'{str(self.update_data)}.')
        except Exception as e:
            self.update_data = {}  # assign an empty dict if failed to parse remote version info
            logger.error(f'Failed to parse update data, {e}.')
            return

        logger.info('Analysing update data ...')
        try:
            latest_version = self.update_data['latest_version']
            logger.info(f'Successfully parsed the latest version, {latest_version}')
        except Exception as e:
            logger.error(f'Failed to get the latest version from update data, {e}')
            return

        try:
            if version.parse(latest_version) <= version.parse(__version__):
                self.ui.label_version.setStyleSheet('color: grey;')
                logger.info(f'No updates available')
                return
        except Exception as e:
            logger.error(f'Failed to analyse update data, {e}')
            return

        '''
        if no updates available -> version text change from black to grey
        
        if local version is lower than remote version, i.e. updates available, follow the procedures below:
        
            a) if local version is executable -> show update available message in black
            b) if local version IS NOT executable -> disable all modules (buttons) and show update message in black

        if failed to parse remote info or no local version specific data found in remote version data, leave version text in black colour.
        '''

        try:
            specific_remote_version_data = self.update_data[
                __version__.split('.dev')[0] if '.dev' in __version__ else __version__]
            logger.info(f'Successfully parsed local version from update data')
            logger.debug(f'{specific_remote_version_data}')
        except Exception as e:
            logger.error(f'Failed to parse local version from update data, {str(e)}')
            return

        # parse `is_executable` from remote version info
        # this will be used to check whether local version is executable
        try:
            is_local_version_executable = specific_remote_version_data['is_executable']
            logger.info(f'Successfully parsed `is_executable`, {is_local_version_executable}')
            if is_local_version_executable is False:
                logger.warning(f'Local version IS NOT executable, all features will be disabled')
                self.is_executable = is_local_version_executable
                self.Signals.check_update_complete.emit(self.is_executable)
        except Exception as e:
            logger.error(f'Failed to parse `is_executable`, {e}')
            return

        # parse `is_upgradable` from remote version info
        # this will be used to display upgrade notification
        try:
            is_local_version_upgradable = specific_remote_version_data['is_upgradable']
            logger.info(f'Successfully parsed `is_upgradable`, {is_local_version_upgradable}')
        except Exception as e:
            logger.error(f'Failed to parse `is_upgradable`, {e}.')
            return

        # parse `executable_download_url` from remote version info
        # this will be used to display upgrade notification
        try:
            try:
                upgrade_executable_url = specific_remote_version_data['executable_download_url']
                if upgrade_executable_url is None:
                    raise KeyError
                logger.info(f'Successfully parsed `executable_download_url`, {upgrade_executable_url}')
            except KeyError:
                upgrade_executable_url = self.update_data['latest_executable_download_url']
                logger.info(f'Successfully parsed `latest_executable_download_url`, {upgrade_executable_url}')
            self.new_version_update_url = upgrade_executable_url
        except Exception as e:
            # if both `executable_download_url` and `latest_executable_download_url` not exist, assign None and
            # print an indicative message.
            logger.error(f'Failed to parse `executable_download_url` or `latest_executable_download_url`, {e}')
            return

        if not is_local_version_executable:
            version_label_text = f'Running version {__version__}. A new version {latest_version} is available. Click here to download.'
        elif is_local_version_upgradable:
            version_label_text = f'This version {__version__} is disabled. A new version {latest_version} is available. Click here to download.'
        else:
            version_label_text = None
            self.ui.label_version.setStyleSheet('color: grey;')

        # update gui label text and tips
        if version_label_text:
            self.ui.label_version.setText(version_label_text)
            self.ui.label_version.setStatusTip(version_label_text)
            self.ui.label_version.setToolTip(version_label_text)

    @property
    def new_version_update_url(self):
        return self.__new_version_update_url

    @new_version_update_url.setter
    def new_version_update_url(self, url: str):
        self.__new_version_update_url = url

    def showEvent(self, event):
        event.accept()

    def closeEvent(self, event):

        logger.debug('Terminating activated dialogs ...')
        for i in self.activated_dialogs:
            try:
                i.close()
            except Exception as e:
                logger.warning(f'Unable to close {type(i).__name__}, {str(e)}')

        logger.debug('All activated dialogs are terminated')

        event.accept()

    @property
    def activated_dialogs(self):
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d):
        self.__activated_dialogs.append(d)

    def keyPressEvent(self, event):
        # logger.info(f'{event.key()} key pressed.')
        if event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_D:
            self.activate_app_module_id()
        elif event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_L:
            self.LoggerApp.show()
        event.accept()


def _test_Apps():
    apps = AppsCollection()
    print(apps.print_all_app_info())


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    qapp.exec_()
