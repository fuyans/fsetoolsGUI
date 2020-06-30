from scipy.special import cython_special

from fsetoolsGUI.gui.__main__ import *

fake_modules = [cython_special]
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    main()
