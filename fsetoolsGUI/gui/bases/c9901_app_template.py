import threading
from datetime import datetime
from os import getlogin, path
from typing import Union

from PySide2 import QtWidgets
from PySide2.QtWidgets import QLabel, QGridLayout, QPushButton, QHBoxLayout, QSizePolicy, QGroupBox, QWidget, QStatusBar, QVBoxLayout, QTextBrowser, QScrollArea

from fsetoolsGUI import __root_dir__, __version__, logger
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui import qt_css
from fsetoolsGUI.gui.bases.custom_utilities import *


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
        self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', '../icons', 'LOGO_1_80_80.png')))

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
        # self.p3_about = QPushButton(' i ')
        # self.p3_about.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;font: bold italic;')
        # self.p3_about.setToolTip('About this app')
        # self.p3_layout.addWidget(self.p3_about)
        # self.p3_layout.addSpacing(5)
        self.p3_example = QPushButton('Example')
        self.p3_example.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.p3_layout.addWidget(self.p3_example)
        self.p3_layout.addStretch(1)
        self.p3_submit = QPushButton('Submit')
        self.p3_submit.setAutoDefault(True)
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
        # self.p3_about = QPushButton(' i ')
        # self.p3_about.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;font: bold italic;')
        # self.p3_about.setToolTip('About this app')
        # self.p3_layout.addWidget(self.p3_about)
        # self.p3_layout.addSpacing(5)
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
        self.__clipboard = QtWidgets.QApplication.clipboard()

        super().__init__(parent=parent, *args, **kwargs)
        self.ui = ui()
        self.ui.setupUi(self)

        # set window title, icon and stylesheet
        self.setWindowTitle(self.app_name_long)
        if parent is None:
            try:
                self.setWindowIcon(QtGui.QPixmap(path.join(__root_dir__, 'gui', '../icons', 'LOGO_1_80_80.png')))
            except Exception as e:
                logger.error(f'Icon file not found {e}')
            self.setStyleSheet(qt_css)

        # instantiate and configure signals
        try:
            self.ui.p3_submit.clicked.connect(self.submit)
        except Exception as e:
            logger.warning(f'{e}')
        try:
            # todo: implement doc
            self.__about_dialog = self.__about_dialog or AboutDialog(fp_or_html=path.join(__root_dir__, 'gui', 'docs', f'{self.app_id}.html'))
            self.ui.p3_about.clicked.connect(lambda: self.__about_dialog.show())
        except Exception as e:
            # logger.warning(f'{e}')
            pass
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

    @staticmethod
    def num2str(num):
        if isinstance(num, int):
            return f'{num:g}'
        elif isinstance(num, float):
            return f'{num:.3f}'.rstrip('0').rstrip('.')
        elif isinstance(num, str):
            return num
        elif num is None:
            return ''
        else:
            return str(num)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

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
        """Keyboard shortcut implementation"""
        logger.debug(f'{event.key()} key pressed.')

        if event.key() == QtCore.Qt.Key_Escape:
            # ESC: Close the current window
            self.close()
        elif event.modifiers() & QtCore.Qt.ControlModifier and (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter):
            # CTRL+ENTER: Try to call `self.ok`, i.e. the `Submit` button on GUI
            try:
                getattr(self, 'submit')()
            except Exception as e:
                module_name = sys.modules[self.__module__].__name__
                logger.warning(f'Failed to call `submit` attribute from {module_name}, {e}')
        elif event.modifiers() & QtCore.Qt.ControlModifier and event.modifiers() & QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_C:
            # CTRL+SHIFT+C: Copy the current GUI as an image and store to clipboard
            try:
                self.__clipboard.setPixmap(self.ui.central_widget.grab())
                logger.info('Successfully copied image to clipboard.')
            except Exception as e:
                logger.warning(f'Failed to copied image to clipboard, {e}.')
        event.accept()

    def closeEvent(self, event):
        for dialog in self.activated_dialogs:
            try:
                dialog.close()
            except Exception as e:
                logger.debug(f'Failed to close {dialog:<10}, {e}')

        for i in ['FigureApp', 'TableApp']:
            try:
                getattr(self, i).close()
            except Exception as e:
                logger.debug(f'{e}')

        event.accept()

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
    def activated_dialogs(self) -> list:
        return self.__activated_dialogs

    @activated_dialogs.setter
    def activated_dialogs(self, d: list):
        self.__activated_dialogs.append(d)

    @staticmethod
    def user_usage_stats(content: str, is_dev: bool = 'dev' in __version__):
        if is_dev:
            logger.debug(f'Post usage stats ignored for dev version, {content}')
            return
        try:
            logger.debug(f'Post usage stats started {content} ...')
            rp = post_to_knack_user_usage_stats(
                user=str(getlogin()),  # user indicator
                version=__version__,  # current app version
                date=datetime.now().strftime("%d%m%Y %H:%M%p"),  # example "03/28/2014 10:30pm"
                content=content  # action is the current app id
            )
            logger.debug(f'Successfully posted usage stats, {rp}')
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

    def dialog_show_message(self, msg: str, info: str = None):
        msgbox = QtWidgets.QMessageBox(parent=self)
        msgbox.setStyleSheet('QPushButton {padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;}')
        msgbox.setIconPixmap(path.join(__root_dir__, 'gui', '../images', 'LOGO_1_80_80.PNG'))
        msgbox.setText(msg)
        msgbox.setInformativeText(info)
        msgbox.setStandardButtons(msgbox.Ok)

        msgbox.exec_()

    def dialog_open_file(self, window_title: str, filter_str: str, dir_default: str = '', func_to_assign_fp=None):
        fp = QtWidgets.QFileDialog.getOpenFileName(self, window_title, dir_default, filter_str)[0]
        if fp:
            fp = path.realpath(fp)
            if func_to_assign_fp:
                func_to_assign_fp(fp)
            return fp
        else:
            return ''

    def dialog_open_dir(self, window_title: str, dir_default: str = '', func_to_assign_fp=None):
        fp = QtWidgets.QFileDialog.getExistingDirectory(self, window_title, dir_default)
        if fp:
            fp = path.realpath(fp)
            if func_to_assign_fp:
                func_to_assign_fp(fp)
            return fp
        else:
            func_to_assign_fp(fp)
            return ''

    def dialog_save_file(self, window_title: str, filter_str: str, dir_default: str = '', func_to_assign_fp=None):
        fp = QtWidgets.QFileDialog.getSaveFileName(self, window_title, dir_default, filter_str)[0]
        if fp:
            fp = path.realpath(fp)
            if func_to_assign_fp:
                func_to_assign_fp(fp)
            return fp
        else:
            func_to_assign_fp(fp)
            return ''


class AppBaseClassExample(AppBaseClass):
    app_id = '0000'
    app_name_short = 'example name short'
    app_name_long = 'example name long'

    __input_items = dict(
        entry_1=dict(i1='test', i2='test', i3='test'),
        entry_2=dict(),
        entry_3=dict(),
        entry_4=dict(),
        entry_5=dict(),
        entry_6=dict(),
        entry_7=dict(),
        entry_8=dict(),
    )
    __output_items = dict()

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

        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Input parameter list</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_1', 'test description 1', 'unit 1')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_2', 'test description 2', 'unit 2')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_3', 'test description 3', 'unit 3')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_4', 'test description 4', 'unit 4')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_5', 'test description 5', 'unit 5')
        btn_show_message = QPushButton('Show message')
        btn_show_message.clicked.connect(lambda: self.dialog_show_message('hello world', 'hello message box'))
        self.ui.p2_layout.addWidget(btn_show_message, c.count, 0, 1, 3)
        btn_show_message = QPushButton('Save file')
        btn_show_message.clicked.connect(lambda: self.dialog_show_message(self.dialog_save_file('Save', '*.txt')))
        self.ui.p2_layout.addWidget(btn_show_message, c.count, 0, 1, 3)
        btn_show_message = QPushButton('Open file')
        btn_show_message.clicked.connect(lambda: self.dialog_show_message(self.dialog_open_file('Open', '*.txt')))
        self.ui.p2_layout.addWidget(btn_show_message, c.count, 0, 1, 3)
        btn_show_message = QPushButton('Open a directory')
        btn_show_message.clicked.connect(lambda: self.dialog_show_message(self.dialog_open_dir('Open a directory')))
        self.ui.p2_layout.addWidget(btn_show_message, c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('<b>Output parameter list</b>'), c.count, 0, 1, 3)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_10', 'test description 10', 'unit 10')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_entry_11', 'test description 11', 'unit 11')

    def submit(self):
        pass

    def example(self):
        pass

    def about(self):
        pass


if __name__ == '__main__':
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = AppBaseClassExample()
    app.show()
    qapp.exec_()
