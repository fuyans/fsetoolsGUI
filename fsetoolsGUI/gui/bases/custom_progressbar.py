from typing import Callable

from PySide2 import QtCore, QtWidgets


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
        self.progress_label = QtWidgets.QLabel('Progress')

        self.grid_layout = QtWidgets.QHBoxLayout()
        self.grid_layout.addWidget(self.progressbar)
        self.grid_layout.addWidget(self.progress_label)

        self.setLayout(self.grid_layout)

        # =========================
        # instantiate signal object
        # =========================

        self.Signals = self.__Signals()

        # ======================
        # assign signal and slot
        # ======================
        self.Signals.progress.connect(self.update_progress_bar)
        self.Signals.progress_label.connect(self.update_progress_label)
        self.Signals.complete.connect(self.complete)

        self.resize(300, 50)

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

    @QtCore.Slot(int)
    def update_progress_bar(self, progress: int):
        self.progressbar.setValue(progress)

    @QtCore.Slot(str)
    def update_progress_label(self, text: str):
        self.progress_label.setText(text)

    @QtCore.Slot(bool)
    def complete(self, status: bool):
        if status:
            self.progressbar.setValue(100)
            self.progress_label.setText('Complete')


class ProgressBarStatusBar:
    def __init__(self, statusbar_settext: Callable):
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
        self.Signals.complete.connect(self.complete)

        self.resize(300, 50)

    @QtCore.Slot(int)
    def update_progress_bar(self, progress: int):
        self.progressbar.setValue(progress)

    @QtCore.Slot(str)
    def update_progress_label(self, text: str):
        self.progress_label.setText(text)

    @QtCore.Slot(bool)
    def complete(self, status: bool):
        if status:
            self.progressbar.setValue(100)
            self.progress_label.setText('Complete')
