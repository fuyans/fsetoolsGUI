import threading
import typing
from datetime import datetime
from os import getlogin
from os.path import join

from PySide2 import QtCore, QtWidgets, QtGui

import fsetoolsGUI
from fsetoolsGUI import AppInfo
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats, md2html
from fsetoolsGUI.gui import md_css
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG

# parse css for Qt GUI
try:
    qt_css = open(join(fsetoolsGUI.__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    qt_css = None


class AboutDialog(QtWidgets.QDialog):
    """todo: docstring"""

    def __init__(self, fp_or_md: str = None, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle('About this app')
        self.setWindowIcon(QMainWindow.make_pixmap_from_base64(OFR_LOGO_1_PNG))

        self.resize(731, 593)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(15, 15, 15, 15)

        self.textBrowser_content = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_content.setMinimumSize(QtCore.QSize(641, 0))
        self.textBrowser_content.setMaximumSize(QtCore.QSize(641, 16777215))

        self.verticalLayout.addWidget(self.textBrowser_content)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.setStyleSheet(qt_css)

        css = f"<style type='text/css'>{md_css}</style>"
        md = md2html(fp_or_md)

        self.textBrowser_content.setText(css + md)


class QMainWindow(QtWidgets.QMainWindow):
    """todo: docstring"""

    activated_dialogs: list = list()
    __AboutForm = None  # About form object (QDialog)

    def __init__(
            self,
            id: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            title: str = None,
            parent=None,
            shortcut_Return: typing.Callable = None,
            freeze_window_size: bool = False,
            about_fp_or_md: str = None
    ):
        """
        todo: docstring
        """

        super().__init__(parent=parent)

        # window properties
        self.__id: str = id
        self.__title: str = title
        self.__icon: bytes = icon
        self.__shortcut_Return: typing.Callable = shortcut_Return
        self.__is_frame_less: bool = False
        self.__is_freeze_window_size: bool = freeze_window_size

        # process about data and prepare ui
        self.__about_fp_or_md = about_fp_or_md

        # validator templates
        self._validator_unsigned_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))
        self._validator_signed_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\+\-]*[0-9]*\.{0,1}[0-9]*!'))

    def init(self, cls=None):

        # window properties
        self.setWindowIcon(self.make_pixmap_from_base64(self.__icon))

        # set window title
        if self.__title:
            self.setWindowTitle(self.__title)
        else:
            self.setWindowTitle(AppInfo(int(self.__id)).long_name)

        self.setStyleSheet(qt_css)
        self.statusBar().setSizeGripEnabled(False)

        self.centralWidget().adjustSize()
        self.adjustSize()

        if self.__is_freeze_window_size:
            self.statusBar().setSizeGripEnabled(False)
            self.setFixedSize(self.width(), self.height())

        check_update = threading.Timer(1, self.user_usage_stats)
        check_update.start()  # after 1 second, 'callback' will be called

        # assign signal to standard layout items
        if cls:
            def set_action_name_and_tip(btncls, action: callable = None, name: str = '', tooltip: str = '',
                                        statustip: str = None):
                if action:
                    btncls.clicked.connect(action)
                btncls.setText(name)
                btncls.setToolTip(tooltip)
                btncls.setStatusTip(statustip)

            if hasattr(cls.ui, 'pushButton_about'):
                set_action_name_and_tip(cls.ui.pushButton_about, self.show_about, 'About',
                                        'Click to show info about this app and quality management')
            if hasattr(cls.ui, 'pushButton_ok'):
                set_action_name_and_tip(cls.ui.pushButton_ok, None, 'OK', 'Click to calculate')
            if hasattr(cls.ui, 'pushButton_example'):
                set_action_name_and_tip(cls.ui.pushButton_example, None, 'Example',
                                        'Click to show example input parameters')

    def show_about(self):
        """"""
        if self.__AboutForm:
            self.__AboutForm.show()
        else:
            self.__AboutForm = AboutDialog(fp_or_md=self.__about_fp_or_md)
            self.__AboutForm.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.__shortcut_Return:
            self.__shortcut_Return()
        event.accept()

    def update_label_text(self, QLabel:QtWidgets.QLabel, val: str):
        QLabel.setText(val)

    def user_usage_stats(self):
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

        print(f'STATS POST STATUS: {rp} {rp.text}')

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map

    @staticmethod
    def make_pixmap_from_fp(fp: str):
        return QtGui.QPixmap(fp)


if __name__ == '__main__':
    pass
