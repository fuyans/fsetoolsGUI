# !/usr/bin/python
# coding:utf-8

import datetime
import sys
import time

import PySide2
from PySide2 import QtCore, QtWidgets

import fsetoolsGUI
from fsetoolsGUI.gui.main import App

# load key which is used when the expiry date is passed
try:
    from fsetoolsGUI.__key__ import key

    KEY = key()
except ModuleNotFoundError:
    raise ModuleNotFoundError('fsetoolsGUI.__key__ is missing')

# enable qt optimisation for high dpi monitors
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def main_core():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    window = App()
    window.show()

    sys.exit(app.exec_())


def main():
    # ---------------------------------------------
    # Check expiry date and pass code if applicable
    # ---------------------------------------------
    date_current = datetime.datetime.now()
    date_expiration = fsetoolsGUI.__date_released__ + datetime.timedelta(days=fsetoolsGUI.__expiry_period_days__)
    if date_current >= date_expiration:

        app = QtWidgets.QApplication(sys.argv)

        if KEY is not None:
            from fsetoolsGUI.gui.c0001_pass_code import App

            app_ = App()
            app_.show()
            app_.exec_()

            try:
                pass_code = int(app_.pass_code)
            except ValueError:
                pass_code = None

            if pass_code != KEY:
                app_.edit.setText('Incorrect password')
                app_.repaint()
                time.sleep(5)
                raise ValueError('Incorrect password.')
            app_.close()
            del app_

    # make_nsh_files program starts
    main_core()


if __name__ == '__main__':
    main_core()
