"""fsetoolsGUI CLI Help.
Usage:
    fsetoolsgui
    fsetoolsgui -m=<module_id>

Options:
    -m      Trigger a specific module

Commands:
    fsetoolsgui
        `fsetoolsgui` graphical user interface.
"""


import os

from docopt import docopt

import fsetoolsGUI


def helper_get_list_filepath_end_width(cwd: str, end_with: str) -> list:
    filepath_all = list()
    for (dirpath, dirnames, filenames) in os.walk(cwd):
        filepath_all.extend(filenames)
        break  # terminate at level 1, do not go to sub folders.

    filepath_end_with = list()
    for i in filepath_all:
        if i.endswith(end_with):
            filepath_end_with.append(os.path.join(cwd, i))

    return filepath_end_with


def gui():
    from fsetoolsGUI.gui.__main__ import main as main_gui
    print(fsetoolsGUI.__version__)
    main_gui()


def main():
    arguments = docopt(__doc__)
    print(arguments)
    if len(arguments) == 0:
        gui()
