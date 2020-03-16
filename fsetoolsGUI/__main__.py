def pyinstaller_entry_point():

    import datetime
    import os
    import sys
    import time
    import warnings

    warnings.filterwarnings("ignore")

    import fsetoolsGUI
    from fsetoolsGUI.gui.__main__ import main
    from PySide2 import QtWidgets
    try:
        from buildscript.__key__ import key
        KEY = key()
    except ModuleNotFoundError:
        KEY = None

    # splash screen
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

    # check expiry date and check pass code
    if datetime.datetime.now() > (
            fsetoolsGUI.__date_released__ + datetime.timedelta(days=fsetoolsGUI.__expiry_period_days__)):
        app = QtWidgets.QApplication(sys.argv)
        if KEY is not None:
            from fsetoolsGUI.gui.logic.dialog_0001_pass_code import Dialog0001
            app_ = Dialog0001()
            app_.show()
            app_.exec_()
            if int(app_.pass_code) != KEY:
                time.sleep(2)
                raise ValueError('Incorrect password.')
            app_.close()
            del app_

    # make_nsh_files program starts
    main()


if __name__ == '__main__':
    pyinstaller_entry_point()