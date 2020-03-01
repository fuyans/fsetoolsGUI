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
        'QLabel#label':
            {
                'color': '#888888',
                'background-color': 'white',
                # 'font-weight': 'bold',
            },
        'QLabel#label:active':
            {
                'color': '#1d90cd',
            },
        'QPushButton#button':
            {
                'color': 'grey',
                'background-color': 'grey',
                # 'font-weight': 'bold',
                'border': '1px',
                # 'padding': '5px',
            },
        'QPushButton#button:active':
            {
                'color': '#ffffff',
            },
        'QPushButton#button:hover':
            {
                'color': 'red',
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
            parent=None
    ):

        super().__init__(parent=parent)
        self.__title = title
        self.__icon = icon
        self.__shortcut_Return = shortcut_Return

        self._Validator_float_unsigned = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))

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
        elif event.key() == QtCore.Qt.Key_Return:
            try:
                self.__shortcut_Return()
            except TypeError:
                pass

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map
