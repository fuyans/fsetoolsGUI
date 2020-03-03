from PySide2 import QtWidgets, QtGui, QtCore

import fsetoolsGUI
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_2_PNG
from fsetoolsGUI.gui.layout.main import Ui_MainWindow
from fsetoolsGUI.gui.logic.OFRCustom import QMainWindow
from fsetoolsGUI.gui.logic.dialog_0101_adb_datasheet_1 import Dialog as Dialog0101
from fsetoolsGUI.gui.logic.dialog_0102_bs9999_datasheet_1 import Dialog as Dialog0102
from fsetoolsGUI.gui.logic.dialog_0103_bs9999_merging_flow import Dialog0103 as Dialog0103
from fsetoolsGUI.gui.logic.dialog_0111_pd7974_heat_detector_activation import Dialog0111 as Dialog0111
from fsetoolsGUI.gui.logic.dialog_0401_br187_parallel_simple import Dialog0401 as Dialog0401
from fsetoolsGUI.gui.logic.dialog_0402_br187_perpendicular_simple import Dialog0402 as Dialog0402
from fsetoolsGUI.gui.logic.dialog_0403_br187_parallel_complex import Dialog0403 as Dialog0403
from fsetoolsGUI.gui.logic.dialog_0404_br187_perpendicular_complex import Dialog0404 as Dialog0404
from fsetoolsGUI.gui.logic.dialog_0405_tra_3d_point import Dialog0405 as Dialog0405
from fsetoolsGUI.gui.logic.dialog_0406_tra_2d_xy_contour import Dialog0406 as Dialog0406
from fsetoolsGUI.gui.logic.dialog_0601_naming_convention import Dialog0601 as Dialog0601
from fsetoolsGUI.gui.logic.dialog_0602_pd7974_flame_height import Dialog0602 as Dialog0602
from fsetoolsGUI.etc.util import check_online_version

import threading
from packaging import version


class MainWindow(QMainWindow):
    def __init__(self):
        # ui setup
        super().__init__(title='Fire Safety Engineering Tools')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # check update
        check_update = threading.Timer(1, self.check_update)
        check_update.start()  # after 60 seconds, 'callback' will be called

        # window properties
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.width(), self.height())
        self.ui.label_version.setText(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setStatusTip(f'Version {fsetoolsGUI.__version__}')
        self.ui.label_version.setToolTip(f'Version {fsetoolsGUI.__version__}')

        # signals
        self.init_buttons()

        # default values
        self.ui.label_big_name.setText('FSE Tools')
        self.init_logos()  # logo
        self.ui.dialog_error = QtWidgets.QErrorMessage(self)
        self.ui.dialog_error.setWindowTitle('Message')

        self._dialog_opened = list()

    def init_logos(self):

        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_2_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.ui.label_logo.setPixmap(pix_map)

        # tips
        self.ui.label_logo.setToolTip('Click to go to ofrconsultants.com')
        self.ui.label_logo.setStatusTip('Click to go to ofrconsultants.com')

        # signals
        self.ui.label_logo.mousePressEvent = self.label_logo_mousePressEvent
        self.ui.label_version.mousePressEvent = self.label_version_mousePressEvent

        self.__update_url = None

    def label_logo_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://ofrconsultants.com/"))

    def label_version_mousePressEvent(self, event=None):
        if event:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.__update_url))

    def init_buttons(self):

        self.ui.pushButton_0101_adb2_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0101))
        self.ui.pushButton_0102_bs9999_datasheet_1.clicked.connect(lambda: self.activate_app(Dialog0102))
        self.ui.pushButton_0103_merging_flow.clicked.connect(lambda: self.activate_app(Dialog0103))
        self.ui.pushButton_0111_heat_detector_activation.clicked.connect(lambda: self.activate_app(Dialog0111))

        self.ui.pushButton_0401_br187_parallel_simple.clicked.connect(lambda: self.activate_app(Dialog0401))
        self.ui.pushButton_0402_br187_perpendicular_simple.clicked.connect(lambda: self.activate_app(Dialog0402))
        self.ui.pushButton_0403_br187_parallel_complex.clicked.connect(lambda: self.activate_app(Dialog0403))
        self.ui.pushButton_0404_br187_perpendicular_complex.clicked.connect(lambda: self.activate_app(Dialog0404))
        self.ui.pushButton_0405_thermal_radiation_extreme.clicked.connect(lambda: self.activate_app(Dialog0405))
        self.ui.pushButton_0406_thermal_radiation_analysis_2d.clicked.connect(lambda: self.activate_app(Dialog0406))

        self.ui.pushButton_0601_naming_convention.clicked.connect(lambda: self.activate_app(Dialog0601))
        self.ui.pushButton_0602_pd7974_flame_height.clicked.connect(lambda: self.activate_app(Dialog0602))

    def activate_app(self, app_):
        app_ = app_()
        app_.show()
        self._dialog_opened.append(app_)

    def check_update(self):

        target = r'hsrmo5)(jXw-efpco[mjeqaljo_gl%cnk,bpsZfj/ucoodigk&m`qqam)_k\tnmioBOBWFFQ,gojh'
        target = ''.join([chr(ord(v)+i%10) for i, v in enumerate(target)])
        print(target)
        try:
            version_dict = check_online_version(url=target)
        except Exception as e:
            version_dict = {}
            self.statusBar().showMessage(e)
        print(version_dict)

        if len(version_dict) == 0:
            version_label_text = 'Version ' + fsetoolsGUI.__version__
            self.ui.label_version.setStyleSheet('color: black;')
        elif version.parse(version_dict['current_version']) > version.parse(fsetoolsGUI.__version__):
            version_label_text = f'A new version {version_dict["current_version"]} available.' + ' Click to download.'
            self.ui.label_version.setStyleSheet('color: black;')
            self.__update_url = version_dict['executable_download_url']
        else:
            version_label_text = 'Version ' + fsetoolsGUI.__version__
            self.ui.label_version.setStyleSheet('color: grey;')

        self.ui.label_version.setText(version_label_text)
        self.ui.label_version.setStatusTip(version_label_text)
        self.ui.label_version.setToolTip(version_label_text)

    def closeEvent(self, *args, **kwargs):
        for i in self._dialog_opened:
            i.close()
        QMainWindow.closeEvent(self, *args, **kwargs)
