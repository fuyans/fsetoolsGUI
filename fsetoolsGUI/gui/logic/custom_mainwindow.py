import threading
import typing
from datetime import datetime
from os import getlogin
from os.path import join

from PySide2 import QtCore, QtWidgets, QtGui

import fsetoolsGUI
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats, md2html
from fsetoolsGUI.gui import md_css
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG
from fsetoolsGUI.gui.logic.custom_tableview import TableWindow as TableWindow

try:
    style_css = open(join(fsetoolsGUI.__root_dir__, 'gui', 'style.css'), "r").read()
except FileNotFoundError:
    style_css = None


def list2htmltable(table_list: list, compact: bool = False):
    # css style generated using https://divtable.com/table-styler/
    table_css = '<style type="text/css">table.minimalistBlack{border:3px solid ' \
                '#000;width:100%;text-align:left;border-collapse:collapse}table.minimalistBlack td,' \
                'table.minimalistBlack th{border:1px solid #000;padding:5px 4px}table.minimalistBlack thead{' \
                'border-bottom:3px solid black}table.minimalistBlack thead th{' \
                'font-weight:400;text-align:left}table.minimalistBlack tfoot td{font-size:14px}</style>'

    # generate table
    is_header = True
    table_html = list()
    table_html_append = table_html.append
    for row in table_list:
        row = '\n'.join([f'<td>{i.strip()}&nbsp;&nbsp;</td>' for i in row])
        table_html_append(f'<tr>\n{row}\n</tr>')

    table_html = f'<thead>{"".join(table_html[0]).replace("td>", "th>")}</thead><tbody>{"".join(table_html[1:])}</tbody>'

    # table_html = '\n'.join(table_html)
    table_html = f'<table class="minimalistBlack">\n{table_html}\n</table>'
    if compact:
        table_html = table_html.replace('\n', '')

    table_html = table_css + table_html

    return table_html


def _test_list2htmltable():
    table_list = [
        ['11', '12'],
        ['21', '22'],
    ]

    print(list2htmltable(table_list, compact=True))


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, fp_or_md: str = None, parent=None):
        super().__init__(parent=parent)

        self.resize(731, 593)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(35, 35, 35, 35)
        self.textBrowser_content = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser_content.setMinimumSize(QtCore.QSize(641, 0))
        self.textBrowser_content.setMaximumSize(QtCore.QSize(641, 16777215))

        self.verticalLayout.addWidget(self.textBrowser_content)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.setStyleSheet(style_css)

        css = f"<style type='text/css'>{md_css}</style>"
        md = md2html(fp_or_md)

        print(md)

        self.textBrowser_content.setText(css + md)


class QMainWindow(QtWidgets.QMainWindow):
    activated_dialogs: list = list()
    __AboutForm = None  # About form object (QDialog)

    def __init__(
            self,
            id: str,
            title: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            parent=None,
            shortcut_Return: typing.Callable = None,
            freeze_window_size: bool = False,
            quality_assurance_content: list = None,
            about_fp_or_md: str = None

    ):
        """
        todo: finalise docstr
        :param quality_assurance_content:
            Quality assurance review log data complies format [[{date}, {author}, {reviewer}], [{date}, ...], ...].
            Where:
                date        YYYYMMDD is the date of the check.
                author      name of the author who made latest changes to the module.
                reviewer    name of the person who checked the module.
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

    def __init_subclass__(cls, **kwargs):
        print(hasattr(cls, 'ui'))

    def init(self, pushButton_about=None):

        # window properties
        ba = QtCore.QByteArray.fromBase64(self.__icon)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle(self.__title)

        self.setStyleSheet(style_css)
        self.statusBar().setSizeGripEnabled(False)

        self.centralWidget().adjustSize()
        self.adjustSize()

        if self.__is_freeze_window_size:
            self.statusBar().setSizeGripEnabled(False)
            self.setFixedSize(self.width(), self.height())

        # quality assurance data
        # self.__AboutForm = AboutDialog(
        #     fp_or_md=self.__about_fp_or_md,
        #     parent=self
        # )
        # self.__AboutForm.setWindowTitle(f'About `{self.__title}`')

        check_update = threading.Timer(1, self.user_usage_stats)
        check_update.start()  # after 1 second, 'callback' will be called

        # assign signal to standard layout items
        if pushButton_about:
            pushButton_about.clicked.connect(self.show_about)  # `About` button

    def show_about(self):
        """"""
        if self.__AboutForm:
            self.__AboutForm.show()
        else:
            self.__AboutForm = AboutDialog(fp_or_md=self.__about_fp_or_md)
            self.__AboutForm.show()

    def show_quality_assurance_info_backedup(self):

        app_ = TableWindow(
            parent=self,
            data_list=self.__quality_assurance_content,
            header=self.__quality_assurance_header,
            window_title='Quality Assurance Log',
            window_geometry=(300, 200, 570, 450)
        )

        app_.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        app_.TableView.resizeColumnsToContents()

        app_.show()

        self.activated_dialogs.append(app_)

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


if __name__ == '__main__':
    _test_list2htmltable()
