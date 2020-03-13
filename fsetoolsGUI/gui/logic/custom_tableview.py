import csv
import io
import operator

from PySide2 import QtGui, QtCore, QtWidgets
from fsetoolsGUI.gui.images_base64 import OFR_LOGO_1_PNG


class TableWindow_QMainWindow(QtWidgets.QMainWindow):
    def __init__(
            self,
            data_list: list,
            header: list,
            window_title: str = None,
            window_geometry: tuple = (),
            parent=None,
            *args,
    ):

        super().__init__(
            parent=parent,
            *args
        )
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        if window_geometry:
            self.setGeometry(*window_geometry)

        if window_title:
            self.setWindowTitle(window_title)

        self.centralwidget = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)

        self.TableView = QtWidgets.QTableView(self.centralwidget)

        self.TableModel = TableModel(self, data_list, header)
        self.TableView.setModel(self.TableModel)
        self.TableView.setFont(QtGui.QFont("Courier New", 10))
        self.TableView.resizeColumnsToContents()
        self.TableView.setSortingEnabled(True)

        self.gridLayout.addWidget(self.TableView, 0, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        # window properties
        ba = QtCore.QByteArray.fromBase64(OFR_LOGO_1_PNG)
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(ba)
        self.setWindowIcon(pix_map)
        self.setWindowTitle(window_title)

        self.statusBar().setSizeGripEnabled(False)

        self.centralWidget().adjustSize()
        self.adjustSize()


class TableWindow(QtWidgets.QDialog):
    def __init__(
            self,
            data_list: list,
            header: list,
            window_title: str = None,
            window_geometry: tuple = (),
            parent=None,
            *args,
    ):

        super().__init__(parent, *args)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

        if window_geometry:
            self.setGeometry(*window_geometry)

        if window_title:
            self.setWindowTitle(window_title)

        self.TableModel = TableModel(self, data_list, header)

        self.TableView = QtWidgets.QTableView()
        self.TableView.setModel(self.TableModel)

        # set font
        font = QtGui.QFont("Courier New", 10)
        self.TableView.setFont(font)

        # set column width to fit contents (set font first!)
        self.TableView.resizeColumnsToContents()

        # enable sorting
        self.TableView.setSortingEnabled(True)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.TableView)
        self.setLayout(layout)

    def copy_selection(self):

        selection = self.TableView.selectedIndexes()

        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtGui.QClipboard().setText(stream.getvalue())

        return

    def keyPressEvent(self, event):
        if QtGui.QKeySequence(event.key() + int(event.modifiers())) == QtGui.QKeySequence('Ctrl+C'):
            self.copy_selection()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent: QtWidgets.QTableView, content: list, row_header: list, *args):
        super().__init__(parent=parent, *args)
        self.row_header = row_header
        self.content = content

    def flags(self, index):
        if index.column() < 99:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role: QtCore.Qt.EditRole):
        """
        Edit data in table cells
        :param index:
        :param value:
        :param role:
        :return:
        """
        row = index.row()
        column = index.column()
        print('row {} col {}'.format(row, column))  # This gives the expected values
        # print('data before: {}'.format(self.arraydata)) # The before state
        # self.arraydata[row][column] = value
        # print('data after: {}'.format(self.arraydata)) # The after state = the problem
        # self.dataChanged.emit(index, index)
        self.content[index.row()][index.column()] = value
        return True

    def rowCount(self, parent):
        return len(self.content)

    def columnCount(self, parent):
        return len(self.content[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.content[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.row_header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.content = sorted(
            self.content,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.content.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

    def removeRow(self, position: int, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position - 1)
        del self.content[position]
        self.endRemoveRows()
        return True

    def insertRow(self, position, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), position, position - 1)
        self.content.insert(position, [''] * len(self.content[0]))
        print(self.content)
        self.endInsertRows()
        return True


if __name__ == '__main__':
    # the solvent data ...
    header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
    # use numbers for numeric data to sort properly
    data_list = [
        ('ACETIC ACID', 117.9, 16.7, 1.049),
        ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
        ('ACETONE', 56.3, -94.7, 0.791),
        ('ACETONITRILE', 81.6, -43.8, 0.786)
    ]

    app = QtWidgets.QApplication([])
    win = TableWindow(data_list, header)
    win.show()
    app.exec_()
