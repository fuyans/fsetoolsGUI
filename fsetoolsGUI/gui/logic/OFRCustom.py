import typing

from PySide2 import QtCore, QtWidgets, QtGui

from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG
from fsetoolsGUI.gui.logic.common import filter_objects_by_name
CSS = \
    {
        'QWidget':
            {
                'background-color': 'white',
            },
        'QGroupBox':
            {
                'background-color': 'white',

            },
        # 'QLabel#QLabel':
        #     {
        #         'color': '#888888',
        #         'background-color': 'white',
        #         # 'font-weight': 'bold',
        #     },
        # 'QLabel#QLabel:active':
        #     {
        #         'color': '#1d90cd',
        #     },
        'QPushButton':
            {
                'background-color': '#f5f5f5',
                'border-style': 'outset',
                'border-width': '1px',
                'border-color': 'grey',
            },
        # 'QPushButton:active':
        #     {
        #         'background-color': '#f5f5f5',
        #     },
        'QPushButton:hover':
            {
                'background-color': 'grey',
            }
    }


def dictToCSS(dictionary):
    stylesheet = ""
    for item in dictionary:
        stylesheet += item + "\n{\n"
        for attribute in dictionary[item]:
            stylesheet += "  " + attribute + ": " + dictionary[item][attribute] + ";\n"
        stylesheet += "}\n"
    return stylesheet


class QMainWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            title: str,
            icon: typing.Union[bytes, QtCore.QByteArray] = OFR_LOGO_1_PNG,
            shortcut_Return: typing.Callable = None,
            parent=None,
            freeze_window_size=False
    ):

        super().__init__(parent=parent)
        self.__title = title
        self.__icon = icon
        self.__shortcut_Return = shortcut_Return

        self._Validator_float_unsigned = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))

        if freeze_window_size:
            self.statusBar().setSizeGripEnabled(False)
            self.setFixedSize(self.width(), self.height())

    def init(self):

        # window properties
        ba = QtCore.QByteArray.fromBase64(self.__icon)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle(self.__title)

        # self.setStyleSheet(dictToCSS(CSS))
        self.statusBar().setSizeGripEnabled(False)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.__shortcut_Return()

    def update_label_text(self, QLabel:QtWidgets.QLabel, val: str):
        QLabel.setText(val)

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map
