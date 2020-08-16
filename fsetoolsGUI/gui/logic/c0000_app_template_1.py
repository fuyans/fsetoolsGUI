import threading
from datetime import datetime
from os import getlogin, path

from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout

from fsetoolsGUI import __root_dir__, __version__, logger
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui.layout.i0000_template_1 import Ui_MainWindow as main_ui
from fsetoolsGUI.gui.layout.i0001_text_browser import Ui_MainWindow as aboutform_ui
from fsetoolsGUI.gui.logic.c0000_utilities import *

# parse css for Qt GUI
try:
    qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    raise FileNotFoundError('UI style file not found')


class AboutDialog(QtWidgets.QMainWindow):
    """todo: docstring"""

    def __init__(self, fp_or_html: str = None, parent=None):

        super().__init__(parent=parent)

        self.ui = aboutform_ui()
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

    def __init__(self, parent=None, post_stats: bool = True, *args, **kwargs):
        self.__activated_dialogs = list()
        self.__about_dialog = None

        super().__init__(parent=parent, *args, **kwargs)
        self.ui = main_ui()
        self.ui.setupUi(self)

        self.__init_ui(post_stats)

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

    def __init_ui(self, post_stats: bool):
        # set window title, icon and stylesheet
        self.setWindowTitle(self.app_name_long)
        try:
            self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        except Exception as e:
            logger.error(f'Icon file not found {e}')
        self.setStyleSheet(qt_css)

        # instantiate buttons etc
        self.ui.p3_layout = QHBoxLayout(self.ui.page_3)
        self.ui.p3_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.p3_about = QPushButton('About')
        self.ui.p3_about.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p3_layout.addWidget(self.ui.p3_about)
        self.ui.p3_layout.addSpacing(5)
        self.ui.p3_example = QPushButton('Example')
        self.ui.p3_example.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p3_layout.addWidget(self.ui.p3_example)
        self.ui.p3_layout.addStretch(1)
        self.ui.p3_submit = QPushButton('Submit')
        self.ui.p3_submit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p3_layout.addWidget(self.ui.p3_submit)

        self.ui.page_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.ui.page_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.ui.page_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # instantiate and configure signals
        if hasattr(self.ui, 'p3_submit'):
            self.ui.p3_submit.clicked.connect(self.ok)
        if hasattr(self.ui, 'p3_about'):
            if self.__about_dialog is None:
                self.__about_dialog = AboutDialog(
                    fp_or_html=path.join(__root_dir__, 'gui', 'docs', f'{self.app_id}.html'))
            self.ui.p3_about.clicked.connect(lambda: self.__about_dialog.show())
        if hasattr(self.ui, 'p3_example'):
            self.ui.p3_example.clicked.connect(self.example)

        # post stats if required
        if post_stats:
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

    def add_lineedit_set_to_grid(
            self, grid: QGridLayout, row: int, name: str, description: str, unit: str, min_width: int = 50,
            descrip_cls: str = 'QLabel', col: int = 0
    ):
        # create description label, input box, unit label
        setattr(self.ui, f'{name}', QLineEdit())
        setattr(self.ui, f'{name}_label', getattr(QtWidgets, descrip_cls)(description))
        setattr(self.ui, f'{name}_unit', QLabel(unit))
        # set min. width for the input box
        getattr(self.ui, f'{name}').setMinimumWidth(min_width)
        # add the created objects to the grid
        grid.addWidget(getattr(self.ui, f'{name}_label'), row, col, 1, 1)
        grid.addWidget(getattr(self.ui, f'{name}'), row, col + 1, 1, 1)
        grid.addWidget(getattr(self.ui, f'{name}_unit'), row, col + 2, 1, 1)

    @property
    def activated_dialogs(self):
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d):
        self.__activated_dialogs.append(d)

    @staticmethod
    def user_usage_stats(content: str, is_dev: bool = 'dev' in __version__):
        if is_dev:
            logger.debug(f'DEV VERSION, STATS POST IGNORED FOR {content}')
            return
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
    class AppBaseClassTest(AppBaseClass):
        app_id = '0000'
        app_name_short = 'example name short'
        app_name_long = 'example name long'

        def __init__(self, parent=None):
            # instantiate ui
            super().__init__(
                parent=parent,
            )

            self.ui.p1_layout = QVBoxLayout(self.ui.page_1)
            self.ui.p1_layout.setContentsMargins(0, 0, 0, 0)

            self.ui.p1_intro = QLabel(
                'This is a brief description. \n\n'
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et '
                'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip '
                'ex ea commodo consequat.'
            )
            self.ui.p1_intro.setFixedWidth(350)
            self.ui.p1_intro.setWordWrap(True)
            self.ui.p1_image = QLabel('placeholder image')
            self.ui.p1_image.setFixedSize(350, 200)
            self.ui.p1_image.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.p1_layout.addWidget(self.ui.p1_intro)
            self.ui.p1_layout.addWidget(self.ui.p1_image)

            self.ui.p2_layout = QGridLayout(self.ui.page_2)
            self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
            self.ui.p2_layout.addWidget(QLabel('<b>Input parameter list</b>'), 0, 0, 1, 3)
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 1, 'p2_entry_1', 'test description 1', 'unit 1')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 2, 'p2_entry_2', 'test description 2', 'unit 2')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 3, 'p2_entry_3', 'test description 3', 'unit 3')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 4, 'p2_entry_4', 'test description 4', 'unit 4')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 5, 'p2_entry_5', 'test description 5', 'unit 5')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 6, 'p2_entry_6', 'test description 6', 'unit 6')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 7, 'p2_entry_7', 'test description 7', 'unit 7')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 8, 'p2_entry_8', 'test description 8', 'unit 8')
            self.ui.p2_layout.addWidget(QLabel('<b>Output parameter list</b>'), 9, 0, 1, 3)
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 10, 'p2_entry_10', 'test description 10', 'unit 10')
            self.add_lineedit_set_to_grid(self.ui.p2_layout, 11, 'p2_entry_11', 'test description 11', 'unit 11')

        def ok(self):
            pass

        def example(self):
            pass


    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = AppBaseClassTest()
    app.show()
    qapp.exec_()
