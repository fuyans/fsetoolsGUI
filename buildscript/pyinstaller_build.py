# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from os.path import join, realpath, dirname, relpath

from fsetoolsGUI import __version__, __root_dir__, logger

try:
    from buildscript.__key__ import key as key_

    key = key_()
except ModuleNotFoundError:
    key = None


def build_gui(app_name: str = 'FSETOOLS', fp_target_py: str = 'pyinstaller_build_entry.py', options: list = None):
    print('\n' * 2)

    os.chdir(dirname(realpath(__file__)))

    cmd_option_list = [
        f'-n={app_name}',
        "--icon=" + realpath(join("etc", "ofr_logo_1_80_80.ico")),

        # To exclude modules that not required in compiled GUI app
        '--exclude-module=' + 'docopt',
        '--exclude-module=' + 'setuptools',
    ]
    if 'dev' in __version__:
        logger.info('Dev. build is enabled.')
    else:
        cmd_option_list.append('--windowed')
        logger.info('Dev. build is not enabled.')

    if options:
        cmd_option_list.extend(options)

    # add encryption to pyz
    if key:
        cmd_option_list.append(f'--key={key}')
        logger.info('Encryption is enabled.')
    else:
        logger.info('Encryption is not enabled.')

    cmd = ['pyinstaller'] + cmd_option_list + [fp_target_py]
    logger.debug(f'COMMAND: {" ".join(cmd)}')

    with open('pyinstaller_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


def find_fp(dirwork: str, endswith: list) -> list:
    list_fp = list()
    list_fp_append = list_fp.append

    for dirpath, dirnames, filenames in os.walk(join(__root_dir__, 'gui')):

        for fn in filenames:
            if any([fn.endswith(suffix) for suffix in endswith]):
                list_fp_append(join(dirpath, fn))

    return list_fp


def main():
    options = [
        "--onedir",  # output unpacked dist to one directory, including an .exe file
        "--noconfirm",  # replace output directory without asking for confirmation
        # "--console",
        "--clean",  # clean pyinstaller cache and remove temporary files
        f'--add-data={realpath(join("etc", "ofr_logo_1_80_80.ico"))}{os.pathsep}etc',  # include icon file
    ]

    # include fsetoolsGUI/gui/*, i.e. image, icon, stylesheet and documentation (in html format) files
    options.extend([
        f'--add-data={fp}{os.pathsep}{relpath(dirname(fp), start=__root_dir__)}' for fp in find_fp(dirwork=join(__root_dir__, 'gui'), endswith=['.png', '.ico', '.css', '.html'])
    ])

    build_gui(options=options)


if __name__ == "__main__":
    main()
