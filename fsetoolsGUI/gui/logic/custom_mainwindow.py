import threading
import typing
from datetime import datetime
from os import getlogin
from os.path import join, dirname

from PySide2 import QtCore, QtWidgets, QtGui

import fsetoolsGUI
from fsetoolsGUI.etc.util import post_to_knack_user_usage_stats
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG
from fsetoolsGUI.gui.logic.custom_tableview import TableWindow as TableWindow

try:
    style_css = open(join(dirname(dirname(__file__)), 'style.css'), "r").read()
except FileNotFoundError:
    style_css = open(join(dirname(dirname(dirname(dirname(__file__)))), 'gui', 'style.css'), "r").read()


def list2htmltable(table_list: list, compact: bool = False):

    is_header = True
    table_html = list()
    table_html_append = table_html.append
    for row in table_list:
        if is_header:
            row = '\n'.join([f'<td><b>{i.strip()}</b>&nbsp;&nbsp;</td>' for i in row])
            is_header = False
        else:
            row = '\n'.join([f'<td>{i.strip()}&nbsp;&nbsp;</td>' for i in row])
        table_html_append(f'<tr>\n{row}\n</tr>')

    table_html = '\n'.join(table_html)
    table_html = f'<table>\n{table_html}\n</table>'
    if compact:
        table_html = table_html.replace('\n', '')

    return table_html


def _test_list2htmltable():
    table_list = [
        ['11', '12'],
        ['21', '22'],
    ]

    print(list2htmltable(table_list, compact=True))


class AboutDialog(QtWidgets.QDialog):

    def __init__(self, qa_list: list = None, parent=None):
        super().__init__(parent=parent)

        # Create widgets
        self.label_qa = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label_qa)
        self.setLayout(layout)

        self.label_qa.setText(list2htmltable(qa_list))


class QMainWindow(QtWidgets.QMainWindow):

    activated_dialogs: list = list()

    def __init__(
            self,
            id: str,
            title: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            parent=None,
            shortcut_Return: typing.Callable = None,
            freeze_window_size: bool = False,
            quality_assurance_content: list = None,

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

        # quality assurance data
        self.__quality_assurance_header = ['Date', 'Author', 'QA & Technical Review']
        if quality_assurance_content:
            self.__quality_assurance_content: list = quality_assurance_content
        else:
            self.__quality_assurance_content: list = len(self.__quality_assurance_header) * ['']

        # validator templates
        self._validator_float_unsigned = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))

    def init(self):

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
        self.__AboutForm = AboutDialog(
            qa_list=self.__quality_assurance_content,
            parent=self
        )
        self.__AboutForm.setWindowTitle(f'About `{self.__title}`')

        check_update = threading.Timer(1, self.user_usage_stats)
        check_update.start()  # after 1 second, 'callback' will be called

    def show_about(self):
        """"""
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
            user=str(getlogin()),
            version=fsetoolsGUI.__version__,
            date=datetime.now().strftime("%Y%m%d %H:%M:%S"),
            action=self.__id
        )
        print(rp, rp.text)

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map


if __name__ == '__main__':
    _test_list2htmltable()
