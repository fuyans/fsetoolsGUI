# !/usr/bin/python
# coding:utf-8


def main():
    import sys
    import PySide2
    from PySide2 import QtCore, QtWidgets
    from fsetoolsGUI.gui.logic.main import MainWindow

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
