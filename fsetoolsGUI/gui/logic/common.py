from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QGridLayout, QDialog, QRadioButton


def filter_objects_by_name(
        object_parent_widget: QtWidgets.QWidget,
        object_types: list,
        names: list = None):

    list_objects = list()
    for i in object_types:
        for j in object_parent_widget.findChildren(i):
            if names:
                for k in names:
                    if k in j.objectName():
                        list_objects.append(j)
            else:
                list_objects.append(j)

    return list_objects


class GridDialog(QDialog):
    def __init__(
            self,
            labels:list,
            grid_shape: tuple = None,
            parent = None,
            window_title = None,
            signal_upon_selection:Signal = None):

        self.labels = labels
        self.signal_upon_selection = signal_upon_selection

        super().__init__(parent=parent)

        if grid_shape is None:
            grid_shape = (len(labels), 1)

        if window_title:
            self.setWindowTitle(window_title)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.radio_buttons = list()
        loop_count = 0
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                # create button
                self.radio_buttons.append(QRadioButton(labels[loop_count]))
                self.radio_buttons[-1].released.connect(lambda x=loop_count: self.emit_selected_index(x))
                # add to layout
                grid_layout.addWidget(self.radio_buttons[-1], i, j)

                loop_count += 1
                if loop_count >= len(labels):
                    break

            if loop_count >= len(labels):
                break

    def emit_selected_index(self, selected_index: int):
        if self.signal_upon_selection:
            self.signal_upon_selection.emit(selected_index)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    grid_dialog = GridDialog(labels=['a', 'b', 'c'])
    grid_dialog.show()
    sys.exit(app.exec_())
