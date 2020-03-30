# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from os.path import join, realpath, dirname, relpath

import fsetoolsGUI

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
    if 'dev' in fsetoolsGUI.__version__:
        print('Dev. build is enabled.')
    else:
        cmd_option_list.append('--windowed')
        print('Dev. build is not enabled.')

    if options:
        cmd_option_list.extend(options)

    # add encryption to pyz
    if key:
        cmd_option_list.append(f'--key={key}')
        print('Encryption is enabled.')
    else:
        print('Encryption is not enabled.')

    cmd = ['pyinstaller'] + cmd_option_list + [fp_target_py]
    print('COMMAND:', ' '.join(cmd))

    with open('pyinstaller_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


def make_fp_images() -> list:
    list_fp = list()
    list_fp_append = list_fp.append

    for dirpath, dirnames, filenames in os.walk(join(fsetoolsGUI.__root_dir__, 'gui')):

        for fn in filenames:
            if fn.endswith('.png') or fn.endswith('.ico') or fn.endswith('.html') or fn.endswith('.css'):
                list_fp_append(join(dirpath, fn))

    return list_fp


def main():
    options = [
        "--onedir",  # output unpacked dist to one directory, including an .exe file
        "--noconfirm",  # replace output directory without asking for confirmation
        "--clean",  # clean pyinstaller cache and remove temporary files
        f'--add-data={realpath(join("etc", "ofr_logo_1_80_80.ico"))}{os.pathsep}etc',  # include icon file
    ]

    # include fsetoolsGUI/gui/*
    options.extend([f'--add-data={fp}{os.pathsep}{relpath(dirname(fp), start=fsetoolsGUI.__root_dir__)}' for fp in
                    make_fp_images()])

    # include fsetoolsGUI/gui/docs
    options.extend([f'--add-data={fp}{os.pathsep}{relpath(dirname(fp), start=fsetoolsGUI.__root_dir__)}' for fp in
                    make_fp_images()])

    # include fsetoolsGUI/gui/docs/*.md
    # options.extend([f'--add-data={fp}{os.pathsep}{join("gui", "docs")}' for fp in make_fp_about_md()])

    build_gui(options=options)


if __name__ == "__main__":
    main()
