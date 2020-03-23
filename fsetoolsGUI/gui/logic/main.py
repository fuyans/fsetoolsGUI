import threading

import requests
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot
from packaging import version

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_2_PNG
from fsetoolsGUI.gui.layout.main import Ui_MainWindow
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.dialog_0101_adb_datasheet_1 import Dialog as Dialog0101
from fsetoolsGUI.gui.logic.dialog_0102_bs9999_datasheet_1 import Dialog as Dialog0102
from fsetoolsGUI.gui.logic.dialog_0103_bs9999_merging_flow import Dialog0103 as Dialog0103
from fsetoolsGUI.gui.logic.dialog_0111_pd7974_heat_detector_activation import Dialog0111 as Dialog0111
from fsetoolsGUI.gui.logic.dialog_0401_br187_parallel_simple import Dialog0401 as Dialog0401
from fsetoolsGUI.gui.logic.dialog_0402_br187_perpendicular_simple import Dialog0402 as Dialog0402
from fsetoolsGUI.gui.logic.dialog_0403_br187_parallel_complex import Dialog0403 as Dialog0403
from fsetoolsGUI.gui.logic.dialog_0404_br187_perpendicular_complex import Dialog0404 as Dialog0404
from fsetoolsGUI.gui.logic.dialog_0406_tra_2d_xy_contour import Dialog0406 as Dialog0406
from fsetoolsGUI.gui.logic.dialog_0601_naming_convention import Dialog0601 as Dialog0601
from fsetoolsGUI.gui.logic.dialog_0602_pd7974_flame_height import Dialog0602 as Dialog0602


class CheckUpdateSignal(QtCore.QObject):
    signal = QtCore.Signal(bool)


class MainWindow(QMainWindow):
    remote_version: dict = None
    is_executable: bool = True
    signal_check_update = CheckUpdateSignal()

    def __init__(self):
        # ui setup
        super().__init__(id='0000', title='Fire Safety Engineering Tools')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        self.signal_check_update.signal.connect(self.setEnabled_all_buttons)

        # check update
        check_update = threading.Timer(0, self.check_update)
        check_update.start()  # after 1 second, 'callback' will be called

        # window properties
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.width(), self.height())
        self.ui.label_version.setText(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setStatusTip(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setToolTip(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # signals
        self.init_buttons()

        # default values
        self.ui.label_big_name.setText('')
        self.ui.label_copy_right.setText('')
        self.init_logos()  # logo
        self.ui.dialog_error = QtWidgets.QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')
        self.__new_version_update_url = None
        self.__dialog_opened = list()

    def init_logos(self):

        self.ui.label_logo.setPixmap(self.make_pixmap_from_base64(OFR_LOGO_2_PNG))
        self.ui.label_logo.setToolTip('Click to go to ofrconsultants.com')
        self.ui.label_logo.setStatusTip('Click to go to ofrconsultants.com')

        # signals
        self.ui.label_logo.mousePressEvent = self.label_logo_mousePressEvent
        self.ui.label_version.mousePressEvent = self.label_version_mousePressEvent

    @Slot(bool)
    def setEnabled_all_buttons(self, v: bool):
        """
        To disable/enable all buttons in `groupBox` depending on `v`.
        Used as Slot to disable all buttons depend on remote version data `is_executable`.
        """
        if not self.is_executable:
            for pushButton in filter_objects_by_name(self.ui.groupBox_misc, object_types=[QtWidgets.QPushButton]):
                pushButton.setEnabled(v)

    def label_logo_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://ofrconsultants.com/"))

    def label_version_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.new_version_update_url))

    def init_buttons(self):
        """
        To assign Signal for all buttons
        """

        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0101))
        self.ui.pushButton_0102_bs9999_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0102))
        self.ui.pushButton_0103_merging_flow.clicked.connect(lambda: self.activate_app(Dialog0103))
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(lambda: self.activate_app(Dialog0111))

        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(lambda: self.activate_app(Dialog0401))
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(lambda: self.activate_app(Dialog0402))
        self.ui.pushButton_0403_br187_parallel_complex.clicked.connect(lambda: self.activate_app(Dialog0403))
        self.ui.pushButton_0404_br187_perpendicular_complex.clicked.connect(lambda: self.activate_app(Dialog0404))
        # self.ui.pushButton_0405_thermal_radiation_extreme.clicked.connect(lambda: self.activate_app(Dialog0405))
        self.ui.pushButton_0406_thermal_radiation_analysis_2d.clicked.connect(lambda: self.activate_app(Dialog0406))

        self.ui.pushButton_0601_naming_convention.clicked.connect(lambda: self.activate_app(Dialog0601))
        self.ui.pushButton_0602_pd7974_flame_height.clicked.connect(lambda: self.activate_app(Dialog0602))

    def activate_app(self, app_):
        app_ = app_()
        app_.show()
        self.__dialog_opened.append(app_)

    def check_update(self):

        # parse remote version info
        target = ''.join([chr(ord(v) + i % 10) for i, v in enumerate(fsetoolsGUI.__remote_version_url__)])
        try:
            version_dict = requests.get(target).json()
        except Exception as e:
            version_dict = {}  # assign an empty dict if failed to parse remote version info
            self.statusBar().showMessage(str(e))
        self.remote_version = version_dict  # assign version info to object
        print(f'PARSED REMOTE VERSION. REMOTE VERSION INFO: {str(version_dict)}.')

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

            # parse local version specific info from remote version data
            specific_remote_version = None
            try:
                specific_remote_version = self.remote_version[fsetoolsGUI.__version__]
                print(
                    f'SUCCESSFULLY PARSED LOCAL VERSION FROM REMOTE VERSION DATA. {self.remote_version[fsetoolsGUI.__version__]}')
            except Exception as e:
                print(f'FAILED PARSED LOCAL SPECIFIC DATA FROM REMOTE VERSION DATA. ERROR {e}.')

            # parse `is_executable` from remote version info
            is_local_version_executable = None
            try:
                assert specific_remote_version
                is_local_version_executable = specific_remote_version['is_executable']
                print(f'SUCCESSFULLY PARSED `is_executable`. {is_local_version_executable}')
            except Exception as e:
                print(f'FAILED TO PARSE `is_executable`. ERROR {e}.')

            # parse `is_upgradable` from remote version info
            is_local_version_upgradable = None
            try:
                assert specific_remote_version
                is_local_version_upgradable = specific_remote_version['is_upgradable']
                print(f'SUCCESSFULLY PARSED `is_upgradable`. {is_local_version_upgradable}')
            except Exception as e:
                print(f'FAILED TO PARSE `is_upgradable`. ERROR {e}.')

            # parse `executable_download_url` from remote version info
            upgrade_executable_url = None
            try:
                if 'executable_download_url' in specific_remote_version:
                    upgrade_executable_url = specific_remote_version['executable_download_url']
                    print(f'SUCCESSFULLY PARSED `executable_download_url`. {upgrade_executable_url}')
                elif 'latest_executable_download_url' in self.remote_version:
                    upgrade_executable_url = self.remote_version['latest_executable_download_url']
                    print('SUCCESSFULLY PARSED `latest_executable_download_url`.')
            except Exception as e:
                # if both `executable_download_url` and `latest_executable_download_url` not exist, assign None and
                # print an indicative message.
                print(f'FAILED TO LOCAL VERSION FROM REMOVE VERSION DATA. ERROR {e}')

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

        # emit signal to disable modules/buttons if necessary
        self.signal_check_update.signal.emit(self.is_executable)

        # DO NOT REPAINT AS THIS METHOD IS CALLED IN A DIFFERENT THREAD

    @property
    def new_version_update_url(self):
        return self.__new_version_update_url

    @new_version_update_url.setter
    def new_version_update_url(self, url: str):
        self.__new_version_update_url = url

    def closeEvent(self, *args, **kwargs):
        for i in self.__dialog_opened:
            i.close()
        QMainWindow.closeEvent(self, *args, **kwargs)
