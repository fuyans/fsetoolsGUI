import csv
import io
import operator
from typing import Union

from PySide2 import QtGui, QtCore, QtWidgets


class MyDelegate(QtWidgets.QItemDelegate):

    def createEditor(self, parent, option, index):
        # if index.column() == 2:
        #     return super(MyDelegate, self).createEditor(parent, option, index)
        # return None

        return super(MyDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        # if index.column() == 2:
        #     # Gets display text if edit data hasn't been set.
        #     text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        #     editor.setText(text)

        val = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)

        editor.setText(str(val))


class TableWindow(QtWidgets.QDialog):
    def __init__(
            self,
            content: list = None,
            col_headers: list = None,
            row_headers: list = None,
            window_title: str = None,
            window_geometry: Union[tuple, list, QtCore.QRect] = (),
            enable_sorting: bool = True,
            parent=None,
            *args,
    ):
        # =================
        # instantiate super
        # =================
        super().__init__(parent, *args)

        # =================
        # set ui properties
        # =================
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        if window_geometry:
            if isinstance(window_geometry, QtCore.QRect):
                self.setGeometry(window_geometry)
            elif isinstance(window_geometry, list) or isinstance(window_geometry, tuple):
                self.setGeometry(*window_geometry)
        if window_title:
            self.setWindowTitle(window_title)

        # =================
        # create ui objects
        # =================
        self.label_tip = QtWidgets.QLabel()
        self.label_tip.setText('Ctrl+A to select all, Ctrl+C to copy selected cells.')
        self.label_tip.wordWrap()

        delegate = MyDelegate()
        self.TableModel = TableModel(self)
        self.TableView = QtWidgets.QTableView()
        if content is not None:
            self.TableModel.update_model(content_data=content, row_headers=row_headers, col_headers=col_headers)
        self.TableView.setModel(self.TableModel)
        self.TableView.setItemDelegate(delegate)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.TableView)
        layout.addWidget(self.label_tip)
        self.setLayout(layout)

        # default values

        self.refresh_content_size(enable_sorting=enable_sorting)

    def refresh_content_size(self, enable_sorting: bool = True):
        # ====================
        # set table properties
        # ====================
        # set font
        # font = QtGui.QFont("Courier New", 10)
        # self.TableView.setFont(font)

        # enable sorting
        if enable_sorting:
            self.TableView.setSortingEnabled(True)

        # set column width to fit contents (set font first!)
        self.TableView.resizeColumnsToContents()
        self.TableView.resizeRowsToContents()

    def update_table_content(self, content_data: list, row_headers: list = None, col_headers: list = None):
        self.TableModel.update_model(content_data=content_data, row_headers=row_headers, col_headers=col_headers)
        self.refresh_content_size()

    def copy_selection(self):

        # get selection index
        selection = self.TableView.selectedIndexes()

        if selection:

            # create table data container
            rows = sorted(index.row() for index in selection)
            cols = sorted(index.column() for index in selection)
            row_count = rows[-1] - rows[0] + 1
            col_count = cols[-1] - cols[0] + 1
            table = [[''] * col_count for _ in range(row_count)]  # table data container

            # fill data into the container
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - cols[0]
                table[row][column] = index.data()

            # data to clipboard
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtGui.QClipboard().setText(stream.getvalue())

        return

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif QtGui.QKeySequence(event.key() + int(event.modifiers())) == QtGui.QKeySequence('Ctrl+C'):
            self.copy_selection()
        event.accept()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent: QtWidgets.QTableView):
        super().__init__(parent=parent)

        self.row_headers = list()
        self.col_headers = list()
        self.content = list()

    def update_model(self, content_data: list, row_headers=None, col_headers=None):

        if col_headers is None:
            # col_headers = list(range(len(content_data[0])))
            col_headers = [''] * len(content_data[0])
        if row_headers is None:
            # row_headers = list(range(len(content_data)))
            row_headers = [''] * len(content_data)

        self.row_headers = row_headers
        self.col_headers = col_headers
        self.content = content_data
        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        self.layoutChanged.emit()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    # def setHeaderData(self, section:int, orientation:QtCore.Qt.Orientation, value, role) -> bool:
    #     print(section, orientation)

    def setData(self, index, value, role: QtCore.Qt.EditRole):
        row = index.row()
        column = index.column()
        if row > len(self.content) or column > len(self.content[row]):
            return False
        else:
            if isinstance(self.content[row][column], float) or isinstance(self.content[row][column], int):
                try:
                    value = float(value)
                except Exception as e:
                    print(f'{str(e)}')
            self.content[row][column] = value
            return True

    def rowCount(self, parent):
        try:
            return len(self.content)
        except IndexError:
            return False

    def columnCount(self, parent):
        try:
            return len(self.content[0])
        except IndexError:
            return False

    def data(self, index, role):

        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        else:
            row, col = index.row(), index.column()
            # print(row, col, self.content[row][col])
            if row > len(self.content):
                return False
            elif role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                return self.content[row][col]

        return self.content[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            try:
                return self.col_headers[section]
            except IndexError:
                return None
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            try:
                return self.row_headers[section]
            except IndexError:
                return None
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
    col_header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
    row_header = ['1', '2', '3', '4']
    # use numbers for numeric data to sort properly
    content = [
        [11, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
        [41, 42, 43, 44],
    ]

    app = QtWidgets.QApplication([])
    win = TableWindow(content, col_headers=['col 1', 'col 2', 'col 3', 'col 4'], row_headers=['row 1', 'row 2', 'row 3', 'row 4'])

    content = [
        [21, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
        [41, 42, 43, 44],
        [41, 42, 43, 44],
    ]
    win.TableModel.update_model(content, col_headers=['col 1', 'col 2', 'col 3', 'col 4'], row_headers=['row 1', 'row 2', 'row 3', 'row 4'])

    win.show()
    app.exec_()
