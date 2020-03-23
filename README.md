# fsetoolsGUI

[![Build Status](https://travis-ci.com/fsepy/fsetools.svg?branch=master)](https://travis-ci.com/fsepy/fsetools)

`fsetoolsGUI` = Fire safety Engineering Tools Graphical User Interface, is a GUI wrapper to [`fsetools`](https://github.com/fsepy/fsetools).

## Getting started

Documentation is work in progress.

This tool is recommended to be used via three ways:

1. Install the app on your machine. No Python runtime is required (i.e. no programming involved).
2. Use command line interface implemented in `fsetoolsGUI`. This requires Python runtime and installation of `fsetoolsGUI` as a library.
3. Use as a library (i.e. to make changes)

As always, `fsetoolsGUI` can be used as a Python library (`import fsetoolsgui as ft`). Uses are documented in docstring.

### Graphical user interface

Compiled GUI executable can be downloaded on the [Releases](https://github.com/fuyans/fsetoolsGUI/releases) page.

GUI components can also accessed from the CLI (see section below).

### Command line interface

Once `fsetoolsGUI` is installed as a Python library, CLI usage can be revealed using the following command:

```shell
(base) C:\Users\Fu>fsetoolsgui -h
```

### Installation of fsetoolsGUI as a library

[Python](https://www.python.org/downloads/) 3.7 or later is required. [Anaconda Distribution](https://www.anaconda.com/distribution/#download-section) is recommended for new starters, it includes Python and few useful packages including a package management tool pip (see below).

[pip](https://pypi.org/) is a package management system for installing and updating Python packages. pip comes with Python, so you get pip simply by installing Python. On Ubuntu and Fedora Linux, you can simply use your system package manager to install the `python3-pip` package. [The Hitchhiker's Guide to Python](https://docs.python-guide.org/starting/installation/) provides some guidance on how to install Python on your system if it isn't already; you can also install Python directly from [python.org](https://www.python.org/getit/). You might want to [upgrade pip](https://pip.pypa.io/en/stable/installing/) before using it to install other programs.

1. to use `pip` install from PyPI:

    ```sh
    pip install --upgrade fsetoolsGUI
    ```

2. to use `pip` install from GitHub (requires [git](https://git-scm.com/downloads)):  

    *Note installing `fsetoolsGUI` via this route will include the latest commits/changes to the library.*  

    ```sh
    pip install --upgrade "git+https://github.com/fuyans/fsetoolsGUI.git@master"
    ```

Dependencies see [requirements.txt](.\requirements.txt).

## Project structure

```
fsetoolsGUI/
├── fsetoolsGUI/
│   ├── cli/
│   ├── etc/
│   └── gui/
│       ├── images/
│       ├── layout/
│       └── logic/
└── buildscript/
```

The root directory contains two folder, `fsetoolsGUI` and `buildscript` are for source code / data and compile script, respectively.

Within `fsetoolsGUI`:

 - `cli` command line interface modules.
 - `etc` helper / utility functions that useful to wider project modules.
 - `gui` graphical user interface modules:
    - `layout` UI layouts.
    - `logic` UI logic.

## Summary of available and planned modules

Module code follows the format below:

- 00**. Utility modules that the main application dependent on, e.g. update routine etc.
- 01**. Means of escape related calculations.
- 04**. External fire spread related calculations.
- 06**. Miscellaneous and/or uncategorised tools.

Status designation:

- Planned. Planned but not started.
- WIP. Work in progress.
- Completed. Completed and peer reviewed.

| Module code | Module name                       | Status    |
| ----------- | --------------------------------- | --------- |
| 0101        | ADB data sheet no. 1              | Completed |
| 0102        | BS 9999 data sheet no. 1          | Completed |
| 0103        | BS 9999 merging flow              | Completed |
| 0104        | PD 7974 kitchen hob radiation     | Planned   |
| 0111        | PD 7974 heat detector activation  | Completed |
| 0401        | BR 187 parallel centered          | Completed |
| 0402        | BR 187 perpendicular centered     | Completed |
| 0403        | BR 187 parallel non-centered      | WIP       |
| 0404        | BR 187 perpendicular non-centered | WIP       |
| 0405        | TRA 3D single point               | Planned   |
| 0406        | TRA 2D parallel contour           | WIP       |
| 0601        | OFR file naming protocol          | Completed |
| 0602        | PD 7974 flame height              | Completed |
| 0603        | FDS mesh resolution               | Planned   |
| 0604        | FDS minimum vent size             | Planned   |

## Authors

**Ian Fu** - *fuyans@gmail.com*

## License

This project is licensed under the Apache License version 2.0 - see the [LICENSE](LICENSE) file for details
