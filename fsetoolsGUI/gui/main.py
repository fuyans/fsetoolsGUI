import datetime
import logging
import threading
from os import path

import requests
from PySide2 import QtWidgets
from PySide2.QtWidgets import QErrorMessage, QPushButton
from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout, QGroupBox, QLabel
from packaging import version

from fsetoolsGUI import __version__, __build__, __date_released__, __expiry_period_days__, __remote_version_url__, __root_dir__, logger
from fsetoolsGUI.gui import qt_css
from fsetoolsGUI.gui.adb_data_sheet_1 import App as ADB_DataSheet1
from fsetoolsGUI.gui.bs9999_data_sheet_1 import App as BS9999_DataSheet1
from fsetoolsGUI.gui.bs9999_merging_flow import App as BS9999_MergingFlow
from fsetoolsGUI.gui.adb_merging_flow import App as ADB_MergingFlow
from fsetoolsGUI.gui.pd7974_detector_activation import App as PD7974_DetectorActivation
from fsetoolsGUI.gui.en_external_column import App as EC3_ExternalColumn
from fsetoolsGUI.gui.br187_parallel_complex import App as BR187_ParallelComplex
from fsetoolsGUI.gui.br187_perpendicular_complex import App as BR187_PerpendicularComplex
from fsetoolsGUI.gui.tra_2d_xy_contour import App as TRA_2DXYContour
from fsetoolsGUI.gui.tra_enclosure import App as TRA_EnclosureModel
from fsetoolsGUI.gui.en_external_flame import App as EC1_ExternalFlame
from fsetoolsGUI.gui.ofr_file_naming_convention import App as OFR_NamingConvention
from fsetoolsGUI.gui.pd7974_flame_height import App as PD7974_FlameHeight
from fsetoolsGUI.gui.en_parametric_fire import App as EC1_ParametricFire
from fsetoolsGUI.gui.travelling_fire import App as SFE_TravellingFire
from fsetoolsGUI.gui.en_protected_steel_heat_transfer import App as EC3_SteelHeatTransferProtected
from fsetoolsGUI.gui.din_en_parametric_fire import App as EC3_DinParametricFire
from fsetoolsGUI.gui.travelling_fire_flux import App as SFE_TravellingFireFlux
from fsetoolsGUI.gui.iso_834_fire import App as ISO834_StandardFire
from fsetoolsGUI.gui.stats_probability_distribution import App as PRA_ProbabilityDistribution
from fsetoolsGUI.gui.safir_batch_run import App as SAFIR_BatchRun
from fsetoolsGUI.gui.safir_tor2temfix import App as SAFIR_Tor2Fix
from fsetoolsGUI.gui.safir_post_processor_old import App as SAFIR_PostProcessorOld
from fsetoolsGUI.gui.ht1d_inexplicit import App as SFE_ConductiveHeatTransfer1DInexplicit
from fsetoolsGUI.gui.bases.custom_utilities import *
from fsetoolsGUI.gui.sfeprapy_mcs0 import App as SFEPRAPY_MCS0Simulation
from fsetoolsGUI.gui.sfeprapy_mcs0_make_fire import App as SFEPRAPY_PostProcessor
from fsetoolsGUI.gui.sfeprapy_mcs0_make_plots import App as SFEPRAPY_PostProcessorPlots
from fsetoolsGUI.gui.sfeprapy_pre_bluebeam import App as SFEPRAPY_PreprocessorBluebeam


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

        # self.page_2.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)


class MyLabel(QLabel):
    def __init__(self, parent, clicked=None):
        QLabel.__init__(self, parent)
        self.applets: list = list()
        self.__clicked = clicked

    def append_app(self, app):
        self.applets.append(app)

    def mousePressEvent(self, event):
        for app in self.applets:
            app.setVisible(not app.isVisible())
        if self.__clicked is not None:
            self.__clicked()


class App(QMainWindow):
    def __init__(self):
        self.update_data: dict = None
        self.is_executable: bool = True
        self.Signals = Signals()
        self.__activated_dialogs = list()

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
        # self.add_buttons()

        apps = {
            'B1 Means of escape': [
                ADB_DataSheet1,
                ADB_MergingFlow,
                BS9999_DataSheet1,
                BS9999_MergingFlow,
                PD7974_DetectorActivation,
                PD7974_FlameHeight,
            ],
            'B3 Elements of structure': [
                EC1_ExternalFlame,
                EC1_ParametricFire,
                EC3_ExternalColumn,
                EC3_SteelHeatTransferProtected,
                EC3_DinParametricFire,
                ISO834_StandardFire,
                SFE_TravellingFire,
                SFE_TravellingFireFlux,
                SFE_ConductiveHeatTransfer1DInexplicit,
            ],
            'B4 External fire spread': [
                # BR187_ParallelSimple,
                # BR187_PerpendicularSimple,
                BR187_ParallelComplex,
                BR187_PerpendicularComplex,
                # TRA_3DPoint,
                TRA_2DXYContour,
                TRA_EnclosureModel,
            ],
            'PRA': [
                PRA_ProbabilityDistribution,
                SFEPRAPY_MCS0Simulation,
                SFEPRAPY_PreprocessorBluebeam,
                SFEPRAPY_PostProcessorPlots,
                SFEPRAPY_PostProcessor,
            ],
            'SAFIR': [
                SAFIR_BatchRun,
                SAFIR_Tor2Fix,
                SAFIR_PostProcessorOld,
            ],
            'Miscellaneous': [
                OFR_NamingConvention,
            ],
        }

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(1), self.ui.p2_layout.setVerticalSpacing(1)

        def adjust_size():
            self.ui.p2_layout.setSizeConstraint(self.ui.p2_layout.SetFixedSize)
            self.ui.p0_layout.setSizeConstraint(self.ui.p0_layout.SetFixedSize)
            self.repaint()
            self.adjustSize()

        c = Counter()

        def activate_app(app_):
            def activate_app_worker():
                _ = app_(parent=self)
                _.show()
                return _

            return activate_app_worker

        for k, v in apps.items():
            label = MyLabel(f"<b>{k}</b>", clicked=adjust_size)
            label.setMinimumSize(280, 0)
            self.ui.p2_layout.addWidget(label, c.count, 0, 1, 1)
            for i in v:
                btn = QPushButton(text=i.app_name_short.replace('\n', ' '))
                btn.setStyleSheet('QPushButton{Text-align: left; padding-left: 4px; padding-right: 4px; padding-top: 1px; padding-bottom: 1px;}')
                btn.setHidden(True)
                btn.clicked.connect(activate_app(i))
                label.append_app(btn)
                self.ui.p2_layout.addWidget(btn, c.count, 0, 1, 1)

        # ------------
        # Check update
        # ------------
        # DEPRECIATED 20th Oct 2020. Checked updated moved to fsetoolsgui.gui.__main__
        self.Signals.check_update_complete.connect(self.ui.page_2.setEnabled)
        threading.Timer(0, self.check_update).start()

        # window properties
        self.ui.label_version.setText(f'Version {__version__}')
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

    def keyPressEvent(self, event):
        # logger.info(f'{event.key()} key pressed.')
        if event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_D:
            self.activate_app_module_id()
        elif event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_L:
            self.LoggerApp.show()
        event.accept()

    @property
    def activated_dialogs(self):
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d):
        self.__activated_dialogs.append(d)

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
    app = App()
    app.show()
    qapp.exec_()
