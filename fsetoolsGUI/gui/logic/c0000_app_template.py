import threading
from datetime import datetime
from os import getlogin, path
from typing import Union

from PySide2.QtWidgets import QLabel, QGridLayout, QPushButton, QHBoxLayout, QSizePolicy, QGroupBox, QWidget, QStatusBar, QVBoxLayout, QTextBrowser, QScrollArea

from fsetoolsGUI import __root_dir__, __version__, logger
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui.logic.c0000_utilities import *

# parse css for Qt GUI
try:
    qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    raise FileNotFoundError('UI style file not found')


class AboutDialogUI(object):
    def setupUi(self, main_window):
        # TREE:
        # label ->
        # (scroll_area_widget_content_layout, scroll_area_widget_content) ->
        # scroll_area ->
        # (page_2, p2_layout) ->
        # (central_widget, p0_layout) ->
        # main_window

        self.central_widget = QWidget(main_window)
        self.page_2 = QGroupBox(self.central_widget)

        # create scroll area content
        self.scroll_area_widget_content = QWidget()
        self.text_browser = QTextBrowser(self.scroll_area_widget_content)
        self.scroll_area_widget_content_layout = QGridLayout(self.scroll_area_widget_content)
        self.scroll_area_widget_content_layout.addWidget(self.text_browser, 1, 0, 1, 1)

        # create scroll area
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setWidget(self.scroll_area_widget_content)

        self.p2_layout = QGridLayout(self.page_2)
        self.p2_layout.addWidget(self.scroll_area, 0, 0, 1, 1)

        self.p0_layout = QGridLayout(self.central_widget)
        self.p0_layout.addWidget(self.page_2, 0, 0, 1, 1)

        self.p0_layout.setSpacing(0), self.p0_layout.setContentsMargins(0, 0, 0, 0)
        self.p2_layout.setSpacing(0), self.p2_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_content_layout.setSpacing(0), self.scroll_area_widget_content_layout.setContentsMargins(0, 0, 0, 0)

        main_window.setCentralWidget(self.central_widget)


class AboutDialog(QtWidgets.QMainWindow):
    """todo: docstring"""

    def __init__(self, fp_or_html: str = None, parent=None):

        super().__init__(parent=parent)

        self.ui = AboutDialogUI()
        self.ui.setupUi(self)

        self.setWindowTitle('About this app')
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))

        self.setStyleSheet(qt_css)

        try:
            with open(fp_or_html, 'r') as f:
                self.ui.text_browser.setText(f.read())
            self.ui.text_browser.setFixedWidth(800)
        except Exception:
            self.ui.text_browser.setText(fp_or_html)
        self.resize(810, 600)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            return


class AppBaseClassUI(object):
    def setupUi(self, main_window):
        self.central_widget = QWidget(main_window)

        self.p0_layout = QGridLayout(self.central_widget)
        self.p0_layout.setSpacing(10), self.p0_layout.setContentsMargins(15, 15, 15, 15)

        self.page_1 = QWidget(self.central_widget)
        self.page_2 = QGroupBox(self.central_widget)
        self.page_3 = QWidget(self.central_widget)

        self.p0_layout.addWidget(self.page_1, 0, 0, 1, 1)
        self.p0_layout.addWidget(self.page_2, 0, 1, 1, 1)
        self.p0_layout.addWidget(self.page_3, 1, 0, 1, 2)

        self.statusbar = QStatusBar(main_window)

        main_window.setCentralWidget(self.central_widget)
        main_window.setStatusBar(self.statusbar)

        # instantiate buttons etc
        self.p3_layout = QHBoxLayout(self.page_3)
        self.p3_layout.setContentsMargins(0, 0, 0, 0)
        self.p3_about = QPushButton('About')
        self.p3_about.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_about)
        self.p3_layout.addSpacing(5)
        self.p3_example = QPushButton('Example')
        self.p3_example.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_example)
        self.p3_layout.addStretch(1)
        self.p3_submit = QPushButton('Submit')
        self.p3_submit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_submit)

        self.page_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.page_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.page_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


class AppBaseClassUISimplified01(object):
    def setupUi(self, main_window):
        self.central_widget = QWidget(main_window)

        self.p0_layout = QGridLayout(self.central_widget)
        self.p0_layout.setSpacing(10), self.p0_layout.setContentsMargins(15, 15, 15, 15)

        self.page_2 = QGroupBox(self.central_widget)
        self.page_3 = QWidget(self.central_widget)

        self.p0_layout.addWidget(self.page_2, 0, 0, 1, 1)
        self.p0_layout.addWidget(self.page_3, 1, 0, 1, 1)

        self.statusbar = QStatusBar(main_window)

        main_window.setCentralWidget(self.central_widget)
        main_window.setStatusBar(self.statusbar)

        # instantiate buttons etc
        self.p3_layout = QHBoxLayout(self.page_3)
        self.p3_layout.setContentsMargins(0, 0, 0, 0)
        self.p3_about = QPushButton('About')
        self.p3_about.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_about)
        self.p3_layout.addSpacing(5)
        self.p3_example = QPushButton('Example')
        self.p3_example.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_example)
        self.p3_layout.addStretch(1)
        self.p3_submit = QPushButton('Submit')
        self.p3_submit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_submit)

        self.page_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.page_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


class AppBaseClass(QtWidgets.QMainWindow):

    def __init__(self, parent=None, post_stats: bool = True, ui=AppBaseClassUI, *args, **kwargs):
        self.__activated_dialogs = list()
        self.__about_dialog = None
        self.__clipboard = QtWidgets.QApplication.clipboard()

        super().__init__(parent=parent, *args, **kwargs)
        self.ui = ui()
        self.ui.setupUi(self)

        # set window title, icon and stylesheet
        self.setWindowTitle(self.app_name_long)
        try:
            self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', 'icons', 'LOGO_1_80_80.png')))
        except Exception as e:
            logger.error(f'Icon file not found {e}')
        self.setStyleSheet(qt_css)

        # instantiate and configure signals
        try:
            self.ui.p3_submit.clicked.connect(self.ok)
        except Exception as e:
            logger.warning(f'{e}')
        try:
            self.__about_dialog = self.__about_dialog or AboutDialog(fp_or_html=path.join(__root_dir__, 'gui', 'docs', f'{self.app_id}.html'))
            self.ui.p3_about.clicked.connect(lambda: self.__about_dialog.show())
        except Exception as e:
            logger.warning(f'{e}')
        try:
            self.ui.p3_example.clicked.connect(self.example)
        except Exception as e:
            logger.warning(f'{e}')

        # post stats if required
        if post_stats:
            try:
                threading.Thread(target=self.user_usage_stats, args=[self.app_id]).start()
            except Exception as e:
                logger.warning(f'{e}')

        self.adjustSize()

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

    def keyPressEvent(self, event):
        logger.info(f'{event.key()} key pressed.')

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            try:
                getattr(self, 'ok')()
            except Exception as e:
                raise e
        elif event.modifiers() & QtCore.Qt.ControlModifier and event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_C:
            try:
                self.__clipboard.setPixmap(self.ui.central_widget.grab())
                logger.info('Successfully set image to clipboard.')
            except Exception as e:
                logger.warning(f'Failed to set image to clipboard, {e}.')
        event.accept()

    def validate_show_statusBar_msg(self, var, type, err_msg: str):
        try:
            self.validate(var, type, err_msg)
        except Exception as e:
            self.statusBar().showMessage(f'{e}')

    def closeEvent(self, event):
        try:
            self.__about_dialog.close()
        except:
            pass
        for dialog in self.activated_dialogs:
            try:
                dialog.close()
            except:
                pass
        event.accept()

    def message_box(self, msg: str, title: str):
        msgbox = QtWidgets.QMessageBox(parent=self)
        msgbox.setIconPixmap(path.join(__root_dir__, 'gui', 'images', 'LOGO_1_80_80.PNG'))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.setStandardButtons(msgbox.Ok)
        msgbox.exec_()

    def add_lineedit_set_to_grid(
            self,
            grid: QGridLayout,
            row: Union[int, Counter],
            name: str,
            description: str,
            unit: str = None,
            min_width: int = 50,
            label_obj: str = 'QLabel',
            col: int = 0,
            unit_obj: str = 'QLabel',
            obj: str = 'QLineEdit'
    ):
        if isinstance(row, Counter):
            row = row.count

        # instantiate objects: label, input box, unit label
        setattr(self.ui, f'{name}_label', getattr(QtWidgets, label_obj)(description))
        setattr(self.ui, f'{name}', getattr(QtWidgets, obj)())
        if unit:
            setattr(self.ui, f'{name}_unit', getattr(QtWidgets, unit_obj)(unit))

        # formatting
        getattr(self.ui, f'{name}').setMinimumWidth(min_width)
        if label_obj == 'QPushButton':
            getattr(self.ui, f'{name}_label').setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        if unit_obj == 'QPushButton' and unit:
            getattr(self.ui, f'{name}_unit').setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')

        # add the created objects to the grid
        grid.addWidget(getattr(self.ui, f'{name}_label'), row, col, 1, 1)
        grid.addWidget(getattr(self.ui, f'{name}'), row, col + 1, 1, 1)
        if unit:
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
            logger.debug(f'Post usage stats ignored for dev version, {content}')
            return
        try:
            logger.info(f'Post usage stats started {content} ...')
            rp = post_to_knack_user_usage_stats(
                user=str(getlogin()),  # user indicator
                version=__version__,  # current app version
                date=datetime.now().strftime("%d%m%Y %H:%M%p"),  # example "03/28/2014 10:30pm"
                content=content  # action is the current app id
            )
            logger.info(f'Successfully posted usage stats, {rp}')
            logger.debug(f'{rp.text}')
        except Exception as e:
            logger.error(f'Failed to post usage stats, {e}')

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
