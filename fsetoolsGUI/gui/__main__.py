# !/usr/bin/python
# coding:utf-8

# THIS SHOULD BE THE ONLY GUI APPLICATION ENTRY POINT
import logging
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(module)s - %(message)s'))
logger = logging.getLogger('gui')
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)

logger.info('Hi')


def main():
    import sys
    import PySide2
    from PySide2 import QtCore, QtWidgets
    from fsetoolsGUI.gui.logic.c0000_main import MainWindow

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
