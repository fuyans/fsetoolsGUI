if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()

    fake_modules = list()
    from scipy.special import cython_special

    fake_modules.append(cython_special)

    from sys import platform

    if platform == "darwin":
        # OS X
        import _tkinter

        fake_modules.append(_tkinter)

    from fsetoolsGUI.gui.__main__ import *

    main()
