import logging
import threading
import typing
from datetime import datetime
from os import getlogin, path

from PySide2 import QtCore, QtWidgets, QtGui

import fsetoolsGUI
from fsetoolsGUI import AppInfo
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui.layout.i0001_text_browser import Ui_MainWindow

logger = logging.getLogger('gui')

# parse css for Qt GUI
try:
    qt_css = open(path.join(fsetoolsGUI.__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    raise FileNotFoundError('UI style file not found')


class Validator:
    def __init__(self):
        """Contains a number of QtGui validators using regex for flexibility
        """
        # validator templates
        self.__unsigned_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))
        self.__signed_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\+\-]*[0-9]*\.{0,1}[0-9]*!'))

    @property
    def unsigned_float(self):
        return self.__unsigned_float

    @property
    def signed_float(self):
        return self.__signed_float


class AboutDialog(QtWidgets.QMainWindow):
    """todo: docstring"""

    def __init__(self, fp_or_html: str = None, parent=None):

        super().__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('About this app')
        self.setWindowIcon(QtGui.QPixmap(path.join(fsetoolsGUI.__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))

        self.setStyleSheet(qt_css)

        try:
            with open(fp_or_html, 'r') as f:
                self.ui.textBrowser.setText(f.read())
        except Exception:
            self.ui.textBrowser.setText(fp_or_html)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            return


class QMainWindow(QtWidgets.QMainWindow):
    """todo: docstring"""

    def __init__(
            self,
            module_id: str,
            icon: typing.Union[bytes, QtCore.QByteArray, QtGui.QPixmap] = None,
            title: str = None,
            parent=None,
            freeze_window_size: bool = False,
            about_fp_or_md: str = None
    ):
        """
        todo: docstring
        """

        self.activated_dialogs: list = list()
        self.__AboutForm = None  # About ui

        # ============================
        # set default input parameters
        # ============================
        # make icon object
        if icon is None:
            icon = QtGui.QPixmap(path.join(fsetoolsGUI.__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png'))
        else:
            if isinstance(icon, bytes) or isinstance(icon, QtCore.QByteArray):
                bm = QtCore.QByteArray.fromBase64(QtCore.QByteArray(icon))
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(bm)
                icon = pixmap

        # =================
        # instantiate super
        # =================
        super().__init__(parent=parent)

        self.AppInfo = AppInfo(int(module_id))
        self.Validator = Validator()

        # =================
        # create properties
        # =================
        self.__id: str = module_id
        self.__title: str = title
        self.__icon: bytes = icon
        self.__is_frame_less: bool = False
        self.__is_freeze_window_size: bool = freeze_window_size
        self.__about_fp_or_md = about_fp_or_md  # process about data and prepare ui

    def init(self, cls):

        # window properties
        self.setWindowIcon(self.__icon)

        # set window title
        if self.__title:
            self.setWindowTitle(self.__title)
        else:
            self.setWindowTitle(self.AppInfo.long_name)

        self.setStyleSheet(qt_css)
        self.statusBar().setSizeGripEnabled(False)

        self.adjustSize()

        if self.__is_freeze_window_size:
            self.statusBar().setSizeGripEnabled(False)
            self.setFixedSize(self.width(), self.height())

        try:
            check_update = threading.Timer(1, self.__user_usage_stats)
            check_update.start()  # after 1 second, 'callback' will be called
        except Exception as e:
            logger.error(f'{str(e)}')

        # assign signal to standard layout items
        def set_action_name_and_tip(
                btncls,
                action: callable = None,
                name: str = '',
                tooltip: str = '',
                statustip: str = None):
            if action:
                btncls.clicked.connect(action)
            btncls.setText(name)
            btncls.setToolTip(tooltip)
            btncls.setStatusTip(statustip)

        if hasattr(cls.ui, 'pushButton_about'):
            set_action_name_and_tip(cls.ui.pushButton_about, self.about, 'About',
                                    'Click to show info about this app and quality management')
        if hasattr(cls.ui, 'pushButton_ok'):
            set_action_name_and_tip(cls.ui.pushButton_ok, self.ok, 'OK', 'Click (or press Enter) to calculate')
        if hasattr(cls.ui, 'pushButton_example'):
                set_action_name_and_tip(cls.ui.pushButton_example, self.example, 'Example',
                                        'Click to show example input parameters')

    def ok(self):
        """Placeholder method to be overridden by child classes.
        This method is expected to be triggered upon clicking the 'OK' or 'Calculate' button. The following comments
        are suggested procedure to be followed. This method is also connected by keyboard shortcut 'Enter'"""

        # Step 1. Get parameters from UI
        # Step 2. Perform analysis
        # Step 3. Cast result onto UI

        pass

    def example(self):
        """Placeholder method to be overriden by child classes.
        This method is expected to be triggered upon clicking the 'Example' button. The following comments are suggested
        procedures to be followed."""

        # Step 1. Prepare and cast example input parameters onto the UI
        # Step 2. Call `self.ok()`

        pass

    def about(self):
        """"""
        if self.__AboutForm is not None:
            self.__AboutForm.show()
        else:
            try:
                self.__AboutForm = AboutDialog(fp_or_html=self.AppInfo.doc_html)
                self.__AboutForm.show()
            except Exception as e:
                self.statusBar().showMessage(str(e))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.calculate()
        event.accept()

    def __user_usage_stats(self):
        rp = post_to_knack_user_usage_stats(
            # user indicator
            user=str(getlogin()),

            # current app version
            version=fsetoolsGUI.__version__,

            # datetime format following https://www.knack.com/developer-documentation/#type-date-time one line string
            # example "03/28/2014 10:30pm"
            date=datetime.now().strftime("%d%m%Y %H:%M%p"),

            # action is the current app id
            action=self.__id
        )

        logger.info(f'STATS POST STATUS {rp}')
        logger.debug(f'{rp.text}')

    def validate_show_statusBar_msg(self, var, type, err_msg: str):
        try:
            self.validate(var, type, err_msg)
        except Exception as e:
            self.statusBar().showMessage(f'{e}')

    @staticmethod
    def validate(var, type, err_msg: str):
        if type == 'unsigned float':
            try:
                assert isinstance(var, float)
                assert var >= 0
            except AssertionError:
                raise ValueError(err_msg)
        else:
            try:
                assert isinstance(var, type)
            except AssertionError:
                raise ValueError(err_msg)

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map

    @staticmethod
    def make_pixmap_from_fp(fp: str):
        return QtGui.QPixmap(fp)

    def closeEvent(self, event):
        if self.__AboutForm is not None:
            self.__AboutForm.close()
        event.accept()

    def message_box(self, msg: str, title: str):
        msgbox = QtWidgets.QMessageBox(parent=self)
        msgbox.setIconPixmap(path.join(fsetoolsGUI.__root_dir__, 'gui', 'images', 'LOGO_1_80_80.PONG'))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.setStandardButtons(msgbox.Ok)
        msgbox.exec_()

    @property
    def module_id(self) -> str:
        return self.__id


if __name__ == '__main__':
    pass
