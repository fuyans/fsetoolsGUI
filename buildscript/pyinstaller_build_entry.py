if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()
    from scipy.special import cython_special

    fake_modules = [cython_special]
    from fsetoolsGUI.gui.__main__ import *

    main()
