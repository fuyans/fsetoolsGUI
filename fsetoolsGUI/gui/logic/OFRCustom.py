import typing

from PySide2 import QtCore, QtWidgets, QtGui

from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG

try:
    from os.path import join, dirname
    style_css = open(join(dirname(__file__), 'style.css'), "r").read()
except FileNotFoundError:
    from fsetoolsGUI.gui.logic.style import style_css

def dictToCSS(dictionary):
    stylesheet = ""
    for item in dictionary:
        stylesheet += item + "\n{\n"
        for attribute in dictionary[item]:
            stylesheet += "  " + attribute + ": " + dictionary[item][attribute] + ";\n"
        stylesheet += "}\n"
    return stylesheet


def hex2QColor(c):
    """Convert Hex color to QColor"""
    r=int(c[0:2],16)
    g=int(c[2:4],16)
    b=int(c[4:6],16)
    return QtGui.QColor(r,g,b)


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

        # window properties
        self.__title = title
        self.__icon = icon
        self.__shortcut_Return = shortcut_Return
        self.__frameless:bool = False

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

        self.setStyleSheet(style_css)
        self.statusBar().setSizeGripEnabled(False)

        self.centralWidget().adjustSize()
        self.adjustSize()

    def _set_frameless(self):

        self.__frameless = True

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.background_color = hex2QColor("efefef")
        self.foreground_color = hex2QColor("333333")
        self.border_radius = 7
        self.draggable = True
        self.__mousePressPos = None
        self.__mouseMovePos = None

        # path = QtGui.QPainterPath()
        # # self.resize(440, 220)
        # path.addRoundedRect(QtCore.QRectF(self.rect()), border_radius, border_radius)
        # mask = QtGui.QRegion(path.toFillPolygon().toPolygon())
        # self.setMask(mask)
        # # self.move(QtGui.QCursor.pos())

        sizegrip = QtWidgets.QSizeGrip(self)
        sizegrip.setVisible(True)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and self.__shortcut_Return:
            self.__shortcut_Return()
        event.accept()

    def update_label_text(self, QLabel:QtWidgets.QLabel, val: str):
        QLabel.setText(val)

    @staticmethod
    def make_pixmap_from_base64(image_base64: bytes):
        ba = QtCore.QByteArray.fromBase64(QtCore.QByteArray(image_base64))
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        return pix_map

    #center
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     delta = QtCore.QPoint(event.globalPos() - self.oldPos)
    #     # print(delta)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()