# !/usr/bin/python
# coding:utf-8

import datetime
import os
import sys
import time
import warnings

import PySide2
from PySide2 import QtCore, QtWidgets

import fsetoolsGUI
from fsetoolsGUI.gui.logic.c0000_main import MainWindow

# load key which is used when the expiry date is passed
try:
    from fsetoolsGUI.__key__ import key

    KEY = key()
except ModuleNotFoundError:
    raise ModuleNotFoundError('fsetoolsGUI.__key__ is missing')

warnings.filterwarnings("ignore")

# configure logger


# enable qt optimisation for high dpi monitors
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PySide2.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def main_core():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


def main():
    # ---------------------------------
    # Splash screen showing app summary
    # ---------------------------------
    print(os.path.realpath(__file__))
    print('=' * 80)
    print('FSETOOLS')
    print(f'VERSION: {fsetoolsGUI.__version__}.')
    print(f'RELEASED: {fsetoolsGUI.__date_released__.strftime("%Y %B %d")}.')
    _exp = fsetoolsGUI.__date_released__ + datetime.timedelta(
        days=fsetoolsGUI.__expiry_period_days__) - datetime.datetime.now()
    _exp_d, _ = divmod(_exp.total_seconds(), 24 * 60 * 60)
    _exp_h, _ = divmod(_, 60 * 60)
    _exp_m, _ = divmod(_, 60)
    print(f'EXPIRES IN: {_exp_d:.0f} day(s), {_exp_h:.0f} hour(s) and {_exp_m:.0f} minute(s).')
    print('THIS WINDOW IS ONLY VISIBLE IN DEV MODE WHEN VERSION CONTAINS DEV KEYWORD.')
    print('=' * 80)

    # ---------------------------------------------
    # Check expiry date and pass code if applicable
    # ---------------------------------------------
    date_current = datetime.datetime.now()
    date_expiration = fsetoolsGUI.__date_released__ + datetime.timedelta(days=fsetoolsGUI.__expiry_period_days__)
    if date_current >= date_expiration:

        app = QtWidgets.QApplication(sys.argv)
        if KEY is not None:
            from fsetoolsGUI.gui.logic.c0001_pass_code import App

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
    main()
