import typing

from PySide2 import QtCore, QtWidgets, QtGui

from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG
from fsetoolsGUI.gui.logic.dialog_0002_tableview import TableWindow as TableWindow

try:
    from os.path import join, dirname
    style_css = open(join(dirname(__file__), 'style.css'), "r").read()
except FileNotFoundError:
    from fsetoolsGUI.gui.logic.style import style_css


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
            parent=None,
            shortcut_Return: typing.Callable = None,
            freeze_window_size: bool = False,
            quality_assurance_content: list = None,

    ):

        super().__init__(parent=parent)

        # window properties
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

    def set_frame_less(self):
        """
        todo: this is not in full working order. clicking combobox arrow will introduce an error that not clear why.
        """

        self.__is_frame_less = True

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.background_color = hex2QColor("efefef")
        # self.foreground_color = hex2QColor("333333")
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

    def show_quality_assurance_info(self):

        app_ = TableWindow(
            parent=self,
            data_list=self.__quality_assurance_content,
            header=self.__quality_assurance_header,
            window_title='Quality Assurance Log',
            # window_geometry=(300, 200, 570, 450)
        )

        app_.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        app_.TableView.resizeColumnsToContents()

        app_.show()

        self.dialog_list.append(app_)

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