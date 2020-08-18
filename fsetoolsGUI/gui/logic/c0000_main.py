import threading
from os import path

import requests
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QErrorMessage, QPushButton, QDialog, QLineEdit, QInputDialog
from PySide2.QtWidgets import QMainWindow, QSizePolicy, QWidget, QGridLayout, QGroupBox, QLabel
from packaging import version

from fsetoolsGUI import __version__, __remote_version_url__, __root_dir__, logger
from fsetoolsGUI.gui.logic.c0000_utilities import *
from fsetoolsGUI.gui.logic.c0101_adb_data_sheet_1 import App as App0101
from fsetoolsGUI.gui.logic.c0102_bs9999_data_sheet_1 import App as App0102
from fsetoolsGUI.gui.logic.c0103_bs9999_merging_flow import App as App0103
from fsetoolsGUI.gui.logic.c0104_adb_merging_flow import App as App0104
from fsetoolsGUI.gui.logic.c0111_pd7974_detector_activation import App as App0111
from fsetoolsGUI.gui.logic.c0311_ec_external_column import App as App0311
from fsetoolsGUI.gui.logic.c0401_br187_parallel_simple import App as App0401
from fsetoolsGUI.gui.logic.c0402_br187_perpendicular_simple import App as App0402
from fsetoolsGUI.gui.logic.c0403_br187_parallel_complex import App as App0403
from fsetoolsGUI.gui.logic.c0404_br187_perpendicular_complex import App as App0404
from fsetoolsGUI.gui.logic.c0405_tra_3d_point import App as App0405
from fsetoolsGUI.gui.logic.c0406_tra_2d_xy_contour import App as App0406
from fsetoolsGUI.gui.logic.c0407_tra_enclosure import App as App0407
from fsetoolsGUI.gui.logic.c0411_ec_external_flame import App as App0411
from fsetoolsGUI.gui.logic.c0601_naming_convention import App as App0601
from fsetoolsGUI.gui.logic.c0602_pd7974_flame_height import App as App0602
from fsetoolsGUI.gui.logic.c0611_parametric_fire import App as App0611
from fsetoolsGUI.gui.logic.c0620_probability_distribution import App as App0620
from fsetoolsGUI.gui.logic.c0630_safir_post_processor import App as App0630
from fsetoolsGUI.gui.logic.c0701_aws_s3_uploader import App as App0701
from fsetoolsGUI.gui.logic.common import filter_objects_by_name

try:
    qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    raise FileNotFoundError('UI style file not found')


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
        '0611': App0611,
        '0620': App0620,
        '0630': App0630,
        '0701': App0701,
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

    def print_all_app_info(self):
        module_code = list(self.__apps.keys())
        module_app_name_long = list()

        l1, l2 = 0, 0
        for i in self.__apps:
            module_app_name_long.append(self.__apps[i].app_name_long)

            if l1 < len(i):
                l1 = len(i)
            if l2 < len(module_app_name_long[-1]):
                l2 = len(module_app_name_long[-1])

        return '\n'.join([f'{i:<{l1}}     {j:<{l2}}' for i, j in zip(module_code, module_app_name_long)])

    def activate_app(self, code: str, parent=None):
        def func():
            app = self.__apps[code](parent=parent)
            app.show()

        return func


class Signals(QtCore.QObject):
    """
    Collection of signal(s) that used in the app.
    """

    check_update_complete = QtCore.Signal(bool)


class AppUI(object):
    def setupUi(self, main_window):
        self.centralwidget = QWidget(main_window)

        self.p0_layout = QGridLayout(self.centralwidget)
        self.p0_layout.setSpacing(10), self.p0_layout.setContentsMargins(15, 15, 15, 15)

        self.page_2 = QGroupBox(self.centralwidget)
        self.label_version = QLabel(__version__)
        self.label_version.setWordWrap(True)

        self.p0_layout.addWidget(self.page_2, 0, 0, 1, 1)
        self.p0_layout.addWidget(self.label_version, 1, 0, 1, 1)

        main_window.setCentralWidget(self.centralwidget)

        self.page_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


class App(QMainWindow):

    def __init__(self):
        self.remote_version: dict = None
        self.is_executable: bool = True
        self.Signals = Signals()
        self.__activated_dialogs = list()
        self.__apps = AppsCollection()

        # ui setup
        super().__init__()
        self.ui = AppUI()
        self.ui.setupUi(self)
        self.setStyleSheet(qt_css)

        self.setWindowTitle('Fire Safety Engineering Tools')
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        # self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.add_buttons()

        # check update
        self.Signals.check_update_complete.connect(self.setEnabled_all_buttons)
        threading.Timer(0, self.check_update).start()

        # window properties
        self.ui.label_version.setText(f'Version {__version__}')
        self.ui.label_version.setStatusTip(f'Version {__version__}')
        self.ui.label_version.setToolTip(f'Version {__version__}')
        self.ui.label_version.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # signals
        self.ui.label_version.mousePressEvent = lambda event: QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_update_url)) if event else None

        # default values
        self.ui.dialog_error = QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')
        self.__new_version_update_url = None
        self.__dialog_opened = list()

    def add_buttons(self):
        button_collection = {
            'Miscellaneous': ['0601', '0602', '0611', '0407', '0630'],
            'B1 Means of escape': ['0101', '0102', '0104', '0103', '0111'],
            'B4 External fire spread': ['0401', '0402', '0403', '0404', '0411'],
        }

        table_cols = 5

        row_i = Counter()
        col_i = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5), self.ui.p2_layout.setVerticalSpacing(5)

        for k in button_collection.keys():
            self.ui.p2_layout.addWidget(QLabel(f'<b>{k}</b>'), row_i.count, 0, 1, table_cols)
            for v in button_collection[k]:
                act_app = self.__apps.activate_app(v, self)
                setattr(self.ui, f'p2_in_{v}', QPushButton(self.__apps.app_name_short(v)))
                getattr(self.ui, f'p2_in_{v}').clicked.connect(act_app)
                getattr(self.ui, f'p2_in_{v}').setFixedSize(76, 76)
                self.ui.p2_layout.addWidget(getattr(self.ui, f'p2_in_{v}'), row_i.v, col_i.count, 1, 1)
            row_i.add()
            col_i.reset()

    @Slot(bool)
    def setEnabled_all_buttons(self, v: bool):
        """
        To disable/enable all buttons in `groupBox` depending on `v`.
        Used as Slot to disable all buttons depend on remote version data `is_executable`.
        """
        if not self.is_executable:
            all_push_buttons = filter_objects_by_name(
                object_parent_widget=self.ui.page_2,
                object_types=[QPushButton]
            )
            for pushButton in all_push_buttons:
                pushButton.setEnabled(v)

    def activate_app_module_id(self):

        if self.is_executable:
            txt, ok = QInputDialog.getText(
                self,
                f'Activate app by Module Code',
                f'{self.__apps.print_all_app_info()}\n\nModule code:',
                QLineEdit.Normal,
                ""
            )
            if ok and txt:
                self.activated_dialogs.append(self.__apps.activate_app(code=txt))

    def check_update(self):
        """
        This method will be called in a thread! Try to avoid competing with the main GUI thread, e.g. avoid repaint etc.
        """

        # parse remote version info
        target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(__remote_version_url__)])
        try:
            version_dict = requests.get(target).json()
        except Exception as e:
            version_dict = {}  # assign an empty dict if failed to parse remote version info
            self.statusBar().showMessage(str(e))
        self.remote_version = version_dict  # assign version info to object
        logger.info(f'PARSED REMOTE VERSION')
        logger.debug(f'{str(version_dict)}.')

        # update gui version label accordingly
        if len(version_dict) == 0:
            '''
            if failed to parse version info
            version label -> display local software version in black color
            '''
            version_label_text = 'Version ' + __version__
            self.ui.label_version.setStyleSheet('color: black;')

        elif version.parse(version_dict['latest_version']) > version.parse(__version__):
            '''
            if local version is lower than remote version, i.e. updates available, follow the procedures below.
            
                if update available and local version executable ->
                    show update available message in black
                if update available and local version NOT executable ->
                    disable all modules (buttons)
                    show update message in black
                if no update available
                    show local version in grey

            caveat.
                only local version specific data is parsed from the remote version data.
                if no local version specific data available in remote version data, this will be effectively be
                `no update available` as above.
            '''

            # ============================================
            # parse relevant info from remote version data
            # ============================================
            # parse local version specific data, i.e. specifically for `fsetoolsgui.__version__`
            specific_remote_version_data = None
            try:
                if '.dev' in __version__:
                    local_version = __version__.split('.dev')[0]
                else:
                    local_version = __version__
                specific_remote_version_data = self.remote_version[local_version]
                logger.info(f'PARSED LOCAL VERSION FROM REMOTE VERSION DATA')
                logger.debug(f'{specific_remote_version_data}')
            except Exception as e:
                logger.warning(f'FAILED TO PARSE LOCAL VERSION FROM REMOTE VERSION DATA. ERROR {str(e)}.')

            # parse `is_executable` from remote version info
            # this will be used to check whether local version is executable
            is_local_version_executable = None
            try:
                assert specific_remote_version_data
                is_local_version_executable = specific_remote_version_data['is_executable']
                logger.info(f'PARSED `is_executable`')
                logger.debug(f'{is_local_version_executable}')
            except Exception as e:
                logger.warning(f'FAILED TO PARSE `is_executable`. ERROR {e}.')

            # parse `is_upgradable` from remote version info
            # this will be used to display upgrade notification
            is_local_version_upgradable = None
            try:
                assert specific_remote_version_data
                is_local_version_upgradable = specific_remote_version_data['is_upgradable']
                logger.info(f'PARSED `is_upgradable`')
                logger.debug(f'{is_local_version_upgradable}')
            except Exception as e:
                logger.warning(f'FAILED TO PARSE `is_upgradable`. ERROR {e}.')

            # parse `executable_download_url` from remote version info
            # this will be used to display upgrade notification
            upgrade_executable_url = None
            try:
                if 'executable_download_url' in specific_remote_version_data:
                    upgrade_executable_url = specific_remote_version_data['executable_download_url']
                    logger.info(f'SUCCESSFULLY PARSED `executable_download_url`')
                    logger.debug(f'{upgrade_executable_url}')
                if 'latest_executable_download_url' in self.remote_version and upgrade_executable_url is None:
                    upgrade_executable_url = self.remote_version['latest_executable_download_url']
                    logger.info('SUCCESSFULLY PARSED `latest_executable_download_url`.')
                    logger.debug(f'{upgrade_executable_url}')
            except Exception as e:
                # if both `executable_download_url` and `latest_executable_download_url` not exist, assign None and
                # print an indicative message.
                logger.warning(f'FAILED TO LOCAL VERSION FROM REMOVE VERSION DATA. ERROR {e}')

            # ==============================================
            # actions in accordance with parsed version data
            # ==============================================
            if is_local_version_upgradable:
                if is_local_version_executable:
                    version_label_text = f'Running version {__version__}. ' \
                        f'A new version {version_dict["latest_version"]} is available. ' \
                        f'Click here to download.'
                    self.ui.label_version.setStyleSheet('color: black;')
                else:
                    version_label_text = f'This version {__version__} is disabled. ' \
                        f'A new version {version_dict["latest_version"]} is available. ' \
                        f'Click here to download.'
                    self.ui.label_version.setStyleSheet('color: black;')
                    self.is_executable = False

                self.new_version_update_url = upgrade_executable_url
            else:
                version_label_text = f'Version {__version__}'
                self.ui.label_version.setStyleSheet('color: grey;')

        else:
            # if local version is equal to remote version, i.e. no update available
            # version label -> display local version in grey color
            version_label_text = f'Version {__version__}'
            self.ui.label_version.setStyleSheet('color: grey;')

        # update gui label text and tips
        self.ui.label_version.setText(version_label_text)
        self.ui.label_version.setStatusTip(version_label_text)
        self.ui.label_version.setToolTip(version_label_text)

        # emit a signal to disable modules/buttons if necessary
        self.Signals.check_update_complete.emit(self.is_executable)

        # DO NOT REPAINT AS THIS METHOD IS CALLED IN A DIFFERENT THREAD

    @property
    def new_version_update_url(self):
        return self.__new_version_update_url

    @new_version_update_url.setter
    def new_version_update_url(self, url: str):
        self.__new_version_update_url = url

    def closeEvent(self, event):

        logger.debug('Terminating children')
        for i in self.findChildren(QMainWindow) + self.findChildren(QDialog):
            try:
                i.close()
            except Exception as e:
                logger.error(f'{str(e)}')

        logger.debug('Terminating activated dialogs/mainwindows')
        for i in self.activated_dialogs:
            try:
                i.close()
            except Exception as e:
                logger.error(f'{str(e)}')

        logger.debug('All subroutines terminated')

        event.accept()

    @property
    def activated_dialogs(self):
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d):
        self.__activated_dialogs.append(d)


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
