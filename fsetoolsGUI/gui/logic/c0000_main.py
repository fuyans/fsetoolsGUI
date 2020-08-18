import logging
import threading
from os import path

import requests
from PySide2 import QtGui, QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QErrorMessage, QPushButton, QDialog, QMainWindow, QLineEdit, QInputDialog, QShortcut
from packaging import version

from fsetoolsGUI import __version__, __remote_version_url__, __root_dir__, logger
from fsetoolsGUI.gui.layout.i0000_main import Ui_MainWindow
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
# from fsetoolsGUI.gui.logic.c0700_imgur_uploader import App as App0700
from fsetoolsGUI.gui.logic.c0701_aws_s3_uploader import App as App0701
from fsetoolsGUI.gui.logic.common import filter_objects_by_name

try:
    qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    raise FileNotFoundError('UI style file not found')


class Apps:
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
        app = self.__apps[code](parent=parent)
        app.show()
        return app


def _test_Apps():
    apps = Apps()
    print(apps.print_all_app_info())


class Signals(QtCore.QObject):
    """
    Collection of signal(s) that used in the app.
    """

    check_update_complete = QtCore.Signal(bool)


class MainWindow(QMainWindow):

    def __init__(self):
        self.remote_version: dict = None
        self.is_executable: bool = True
        self.Signals = Signals()
        self.__activated_dialogs = list()
        self.__apps = Apps()

        # ui setup
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(qt_css)

        # self.setWindowIcon(icon_)

        self.setWindowTitle('Fire Safety Engineering Tools')
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        # self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.Signals.check_update_complete.connect(self.setEnabled_all_buttons)

        # check update
        threading.Timer(0, self.check_update).start()

        # window properties
        self.ui.label_version.setText(f'Version {__version__}')
        self.ui.label_version.setStatusTip(f'Version {__version__}')
        self.ui.label_version.setToolTip(f'Version {__version__}')
        self.ui.label_version.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # signals
        self.init_buttons()
        self.ui.label_version.mousePressEvent = self.label_version_mousePressEvent

        # default values
        self.ui.dialog_error = QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')
        self.__new_version_update_url = None
        self.__dialog_opened = list()

    @Slot(bool)
    def setEnabled_all_buttons(self, v: bool):
        """
        To disable/enable all buttons in `groupBox` depending on `v`.
        Used as Slot to disable all buttons depend on remote version data `is_executable`.
        """
        if not self.is_executable:
            all_push_buttons = filter_objects_by_name(
                object_parent_widget=self.ui.frame_userio,
                object_types=[QPushButton]
            )
            for pushButton in all_push_buttons:
                pushButton.setEnabled(v)

    def label_version_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_update_url))

    def init_buttons(self):
        """
        To assign Signal for all buttons
        """

        def set_btn(cls: QPushButton, module_code: str):
            cls.clicked.connect(lambda: self.activate_app(module_code))
            cls.setText(self.__apps.app_name_short(module_code))
            cls.setToolTip(self.__apps.app_name_long(module_code))

        set_btn(self.ui.pushButton_0101_adb2_datasheet_1, '0101')
        set_btn(self.ui.pushButton_0102_bs9999_datasheet_1, '0102')
        set_btn(self.ui.pushButton_0103_merging_flow, '0103')
        set_btn(self.ui.pushButton_0104_merging_flow, '0104')
        set_btn(self.ui.pushButton_0111_heat_detector_activation, '0111')
        set_btn(self.ui.pushButton_0401_br187_parallel_simple, '0401')
        set_btn(self.ui.pushButton_0402_br187_perpendicular_simple, '0402')
        set_btn(self.ui.pushButton_0403_br187_parallel_complex, '0403')
        set_btn(self.ui.pushButton_0404_br187_perpendicular_complex, '0404')
        set_btn(self.ui.pushButton_0407_tra_enclosure, '0407')
        set_btn(self.ui.pushButton_0601_naming_convention, '0601')
        set_btn(self.ui.pushButton_0602_pd7974_flame_height, '0602')
        set_btn(self.ui.pushButton_0611_ec_parametric_fire, '0611')
        set_btn(self.ui.pushButton_0630_safir_post_processor, '0630')

        QShortcut(QtGui.QKeySequence(QtCore.Qt.SHIFT + QtCore.Qt.Key_D), self).activated.connect(
            self.activate_app_module_id)

    def activate_app(self, module_id: str):
        logger.info(f'EXECUTED MODULE {module_id}')
        self.activated_dialogs.append(self.__apps.activate_app(code=module_id))

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
                self.activate_app(txt)

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


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow()
    app.show()
    qapp.exec_()
