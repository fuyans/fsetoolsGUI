import logging
import threading
from datetime import datetime
from os import getlogin, path

from PySide2 import QtCore, QtWidgets, QtGui

from fsetoolsGUI import __root_dir__, __version__
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui.layout.i0001_text_browser import Ui_MainWindow

logger = logging.getLogger('gui')

# parse css for Qt GUI
try:
    qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
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


def copy_to_clipboard(s: str):
    clipboard = QtGui.QGuiApplication.clipboard()
    clipboard.setText(s)


class AboutDialog(QtWidgets.QMainWindow):
    """todo: docstring"""

    def __init__(self, fp_or_html: str = None, parent=None):

        super().__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('About this app')
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))

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


class AppBaseClass(QtWidgets.QMainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.__activated_dialogs = list()
        self.__about_dialog = None

    def __init_subclass__(cls, **kwargs):
        def assert_attr(attr_: str):
            try:
                assert hasattr(cls, attr_)
            except AssertionError:
                raise AttributeError(f'Attribute `{attr_}` not defined')

        # -------------------------
        # validate subclass methods
        # -------------------------
        assert_attr('app_id')
        assert_attr('app_name_short')
        assert_attr('app_name_long')
        try:
            assert_attr('ok')
        except AttributeError:
            logger.warning('`ok` method not defined')

        pass

    def init(self):
        self.setWindowTitle(self.app_name_long)
        try:
            self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        except Exception as e:
            logger.error(f'Icon file not found {e}')

        self.setStyleSheet(qt_css)

        if hasattr(self.ui, 'pushButton_ok'):
            self.ui.pushButton_ok.clicked.connect(self.ok)
        if hasattr(self.ui, 'pushButton_about'):
            if self.__about_dialog is None:
                self.__about_dialog = AboutDialog(
                    fp_or_html=path.join(__root_dir__, 'gui', 'docs', f'{self.app_id}.html'))
            self.ui.pushButton_about.clicked.connect(lambda: self.__about_dialog.show())
        if hasattr(self.ui, 'pushButton_example'):
            self.ui.pushButton_example.clicked.connect(self.example)

        self.adjustSize()

        threading.Thread(target=self.user_usage_stats, args=[self.app_id]).start()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            try:
                getattr(self, 'ok')()
            except Exception as e:
                raise e
        event.accept()

    def validate_show_statusBar_msg(self, var, type, err_msg: str):
        try:
            self.validate(var, type, err_msg)
        except Exception as e:
            self.statusBar().showMessage(f'{e}')

    def closeEvent(self, event):
        if self.__about_dialog is not None:
            self.__about_dialog.close()
        event.accept()

    def message_box(self, msg: str, title: str):
        msgbox = QtWidgets.QMessageBox(parent=self)
        msgbox.setIconPixmap(path.join(__root_dir__, 'gui', 'images', 'LOGO_1_80_80.PNG'))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.setStandardButtons(msgbox.Ok)
        msgbox.exec_()

    @property
    def activated_dialogs(self):
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d):
        self.__activated_dialogs.append(d)

    @staticmethod
    def user_usage_stats(content: str):
        try:
            logger.debug(f'STATS POST STARTED FOR {content}')
            rp = post_to_knack_user_usage_stats(
                user=str(getlogin()),  # user indicator
                version=__version__,  # current app version
                date=datetime.now().strftime("%d%m%Y %H:%M%p"),  # example "03/28/2014 10:30pm"
                content=content  # action is the current app id
            )
            logger.info(f'STATS POST STATUS {rp}')
            logger.debug(f'{rp.text}')
        except Exception as e:
            logger.error(f'User stats post failed {e}')

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map

    @staticmethod
    def make_pixmap_from_fp(fp: str):
        return QtGui.QPixmap(fp)

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


if __name__ == '__main__':
    pass
