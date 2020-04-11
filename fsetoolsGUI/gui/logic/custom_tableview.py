import csv
import io
import operator

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
            data_list: list,
            header_col: list = None,
            header_row: list = None,
            window_title: str = None,
            window_geometry: tuple = (),
            enable_sorting: bool = True,
            parent=None,
            *args,
    ):
        # ================
        # super properties
        # ================
        super().__init__(parent, *args)

        # =====================
        # set object properties
        # =====================
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        if window_geometry:
            self.setGeometry(*window_geometry)
        if window_title:
            self.setWindowTitle(window_title)

        # =================
        # create ui objects
        # =================
        delegate = MyDelegate()
        self.TableModel = TableModel(self, data_list, header_col=header_col, header_row=header_row)
        self.TableView = QtWidgets.QTableView()
        self.TableView.setModel(self.TableModel)
        self.TableView.setItemDelegate(delegate)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.TableView)
        self.setLayout(layout)

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
    def __init__(self, parent: QtWidgets.QTableView, content: list, header_row: list = None, header_col: list = None,
                 *args):
        super().__init__(parent=parent, *args)

        if not header_col:
            header_col = list(range(len(content)))
        if not header_row:
            header_row = list(range(len(content[0])))

        self.row_header = header_row
        self.col_header = header_col
        self.content = content

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

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
        return len(self.content)

    def columnCount(self, parent):
        return len(self.content[0])

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
            return self.row_header[section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self.col_header[section]
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
        ['ACETIC ACID', 117.9, 16.7, 1.049],
        ['ACETIC ANHYDRIDE', 140.1, -73.1, 1.087],
        ['ACETONE', 56.3, -94.7, 0.791],
        ['ACETONITRILE', 81.6, -43.8, 0.789],
    ]

    app = QtWidgets.QApplication([])
    win = TableWindow(content)

    win.show()
    app.exec_()
