from PySide2 import QtCore, QtGui, QtWidgets


class Validator:
    def __init__(self):
        """Contains a number of QtGui validators using regex for flexibility
        """
        # validator templates
        self.__unsigned_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[0-9]*\.{0,1}[0-9]*!'))
        self.__signed_float = QtGui.QRegExpValidator(QtCore.QRegExp(r'^[\+\-]*[0-9]*\.{0,1}[0-9]*!'))

    @property
    def unsigned_float(self):
        return self.__unsigned_float

    @property
    def signed_float(self):
        return self.__signed_float


class ProgressBar(QtWidgets.QDialog):
    def __init__(self, title: str = None, initial_value: int = 0, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setWindowTitle(title)
        self.setSizeGripEnabled(False)

        # ==============
        # instantiate ui
        # ==============
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setMinimum(0), self.progressbar.setMaximum(100), self.progressbar.setValue(initial_value)
        self.progress_label = QtWidgets.QLabel('--')

        self.grid_layout = QtWidgets.QHBoxLayout()
        self.grid_layout.addWidget(self.progressbar)
        self.grid_layout.addWidget(self.progress_label)

        self.setLayout(self.grid_layout)

        # =========================
        # instantiate signal object
        # =========================
        class __Signals(QtCore.QObject):
            __process_complete = QtCore.Signal(bool)
            __progress = QtCore.Signal(int)
            __progress_label = QtCore.Signal(str)

            @property
            def complete(self) -> QtCore.Signal:
                return self.__process_complete

            @property
            def progress(self) -> QtCore.Signal:
                return self.__progress

            @property
            def progress_label(self) -> QtCore.Signal:
                return self.__progress_label

        self.Signals = __Signals()

        # ======================
        # assign signal and slot
        # ======================
        self.Signals.progress.connect(self.update_progress_bar)
        self.Signals.progress_label.connect(self.update_progress_label)

        self.resize(300, 50)

    @QtCore.Slot(int)
    def update_progress_bar(self, progress: int):
        self.progressbar.setValue(progress)

    @QtCore.Slot(str)
    def update_progress_label(self, text: str):
        self.progress_label.setText(text)


class Counter:
    def __init__(self):
        self.__v: int = 0

    def __add__(self, other):
        if isinstance(other, int):
            self.__v = self.__v + other
        elif isinstance(other, Counter):
            self.__v = self.__v + other.__v
        else:
            raise TypeError

    def __repr__(self):
        return f'{self.__v:d}'

    def add(self):
        self.__v += 1

    def reset(self, v: int = 0):
        if isinstance(v, int):
            self.__v = v
        else:
            raise TypeError

    @property
    def count(self):
        self.add()
        return self.__v - 1

    @property
    def value(self):
        return self.__v

    @value.setter
    def value(self, v: int):
        assert isinstance(v, int)
        self.__v = v


def copy_to_clipboard(s: str):
    clipboard = QtGui.QGuiApplication.clipboard()
    clipboard.setText(s)


if __name__ == '__main__':
    counter = Counter()
    counter.add()
    print(counter)
    counter + 5
    print(counter)
    counter.reset(-1)
    print(counter)
