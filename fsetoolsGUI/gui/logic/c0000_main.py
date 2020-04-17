import logging
import threading

import requests
from PySide2 import QtGui, QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QErrorMessage
from packaging import version

import fsetoolsGUI
from fsetoolsGUI.gui.layout.i0000_main import Ui_MainWindow
from fsetoolsGUI.gui.logic.c0101_adb_data_sheet_1 import App as App0101
from fsetoolsGUI.gui.logic.c0102_bs9999_data_sheet_1 import Dialog0102 as App0102
from fsetoolsGUI.gui.logic.c0103_bs9999_merging_flow import Dialog0103 as App0103
from fsetoolsGUI.gui.logic.c0104_adb_merging_flow import Dialog0104 as App0104
from fsetoolsGUI.gui.logic.c0111_pd7974_detector_activation import Dialog0111 as App0111
from fsetoolsGUI.gui.logic.c0401_br187_parallel_simple import Dialog0401 as App0401
from fsetoolsGUI.gui.logic.c0402_br187_perpendicular_simple import Dialog0402 as App0402
from fsetoolsGUI.gui.logic.c0403_br187_parallel_complex import Dialog0403 as App0403
from fsetoolsGUI.gui.logic.c0404_br187_perpendicular_complex import Dialog0404 as App0404
from fsetoolsGUI.gui.logic.c0406_tra_2d_xy_contour import Dialog0406 as App0406
from fsetoolsGUI.gui.logic.c0407_tra_enclosure import App as App0407
from fsetoolsGUI.gui.logic.c0601_naming_convention import Dialog0601 as App0601
from fsetoolsGUI.gui.logic.c0602_pd7974_flame_height import Dialog0602 as App0602
from fsetoolsGUI.gui.logic.c0611_parametric_fire import App0611 as App0611
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow

logger = logging.getLogger('gui')


class Signals(QtCore.QObject):
    """
    Collection of signal(s) that used in the app.
    """

    check_update_complete = QtCore.Signal(bool)


class MainWindow(QMainWindow):
    remote_version: dict = None
    is_executable: bool = True
    Signals = Signals()

    def __init__(self):
        # ui setup
        super().__init__(
            module_id='0000',
            title='Fire Safety Engineering Tools',
            freeze_window_size=True,
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        self.Signals.check_update_complete.connect(self.setEnabled_all_buttons)

        # check update
        check_update = threading.Timer(0, self.check_update).start()

        # window properties
        # self.setFixedSize(self.width(), self.height())
        self.ui.label_version.setText(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setStatusTip(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setToolTip(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # signals
        self.init_buttons()

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
            for pushButton in filter_objects_by_name(self.ui.verticalGroupBox, object_types=[QtWidgets.QPushButton]):
                pushButton.setEnabled(v)

    def label_version_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_update_url))

    def init_buttons(self):
        """
        To assign Signal for all buttons
        """

        def set_btn(btncls, action: callable = None, name: str = '', tip: str = None):
            btncls.clicked.connect(lambda: self.activate_app(action))
            btncls.setText(name)
            btncls.setToolTip(tip)
            btncls.setStatusTip(tip)

        module_info = fsetoolsGUI.AppInfo

        set_btn(self.ui.pushButton_0101_adb2_datasheet_1, App0101, *module_info('0101').short_and_long_names)
        set_btn(self.ui.pushButton_0102_bs9999_datasheet_1, App0102, *module_info('0102').short_and_long_names)
        set_btn(self.ui.pushButton_0103_merging_flow, App0103, *module_info('0103').short_and_long_names)
        set_btn(self.ui.pushButton_0104_merging_flow, App0104, *module_info('0104').short_and_long_names)
        set_btn(self.ui.pushButton_0111_heat_detector_activation, App0111, *module_info('0111').short_and_long_names)

        set_btn(self.ui.pushButton_0401_br187_parallel_simple, App0401, *module_info('0401').short_and_long_names)
        set_btn(self.ui.pushButton_0402_br187_perpendicular_simple, App0402, *module_info('0402').short_and_long_names)
        set_btn(self.ui.pushButton_0403_br187_parallel_complex, App0403, *module_info('0403').short_and_long_names)
        set_btn(self.ui.pushButton_0404_br187_perpendicular_complex, App0404, *module_info('0404').short_and_long_names)
        set_btn(self.ui.pushButton_0406_thermal_radiation_analysis_2d, App0406, *module_info('0406').short_and_long_names)
        set_btn(self.ui.pushButton_0407_tra_enclosure, App0407, *module_info('0407').short_and_long_names)

        set_btn(self.ui.pushButton_0601_naming_convention, App0601, *module_info('0601').short_and_long_names)
        set_btn(self.ui.pushButton_0602_pd7974_flame_height, App0602, *module_info('0602').short_and_long_names)
        set_btn(self.ui.pushButton_0611_ec_parametric_fire, App0611, *module_info('0611').short_and_long_names)

    def activate_app(self, app_):
        logger.info(f'EXECUTED MODULE {app_}')
        if app_ is App0101 or app_ is App0102:
            # it has been found that these two modules crash when executed without parent
            # the actual cause has not yet identified
            app_ = app_(self)
        else:
            app_ = app_()
        app_.show()

    def check_update(self):
        """
        This method will be called in a thread! Try to avoid competing with the main GUI thread, e.g. avoid repaint etc.
        """

        # parse remote version info
        target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(fsetoolsGUI.__remote_version_url__)])
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
            version_label_text = 'Version ' + fsetoolsGUI.__version__
            self.ui.label_version.setStyleSheet('color: black;')

        elif version.parse(version_dict['latest_version']) > version.parse(fsetoolsGUI.__version__):
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
                if '.dev' in fsetoolsGUI.__version__:
                    local_version = fsetoolsGUI.__version__.split('.dev')[0]
                else:
                    local_version = fsetoolsGUI.__version__
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
                    logger.info(f'SUCCESSFULLY PARSED `latest_executable_download_url`. {upgrade_executable_url}')
            except Exception as e:
                # if both `executable_download_url` and `latest_executable_download_url` not exist, assign None and
                # print an indicative message.
                logger.warning(f'FAILED TO LOCAL VERSION FROM REMOVE VERSION DATA. ERROR {e}')

            # ==============================================
            # actions in accordance with parsed version data
            # ==============================================
            if is_local_version_upgradable:
                if is_local_version_executable:
                    version_label_text = f'Running version {fsetoolsGUI.__version__}. ' \
                                         f'A new version {version_dict["latest_version"]} is available. ' \
                                         f'Click here to download.'
                    self.ui.label_version.setStyleSheet('color: black;')
                else:
                    version_label_text = f'This version {fsetoolsGUI.__version__} is disabled. ' \
                                         f'A new version {version_dict["latest_version"]} is available. ' \
                                         f'Click here to download.'
                    self.ui.label_version.setStyleSheet('color: black;')
                    self.is_executable = False

                self.new_version_update_url = upgrade_executable_url
            else:
                version_label_text = f'Version {fsetoolsGUI.__version__}'
                self.ui.label_version.setStyleSheet('color: grey;')

        else:
            # if local version is equal to remote version, i.e. no update available
            # version label -> display local version in grey color
            version_label_text = f'Version {fsetoolsGUI.__version__}'
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


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = MainWindow()
    app.show()
    qapp.exec_()
