# -*- coding: utf-8 -*-
import os
import sys
import zlib
from base64 import urlsafe_b64encode
from datetime import datetime
from os.path import join, realpath, dirname, relpath

__root_dir__ = join(dirname(dirname(realpath(__file__))), 'fsetoolsGUI')


def build_write(fp, date_cls: datetime = datetime.now(), date_format: str = '%Y%m%d%H%M') -> str:
    datetime_str = date_cls.strftime(date_format)
    datetime_str = zlib.compress(datetime_str.encode(), 0)
    datetime_str = urlsafe_b64encode(datetime_str)
    datetime_str = datetime_str.decode()
    with open(fp, 'w+') as f:
        f.write(datetime_str)
    return datetime_str


def make_build_info():
    build_info = datetime.now().strftime('%y%m%d%H%M')
    with open(os.path.join(__root_dir__, 'build.txt'), 'w+') as f:
        f.write(build_info)
    return build_info


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

    if options:
        cmd_option_list.extend(options)

    cmd = ['pyinstaller'] + cmd_option_list + [fp_target_py]
    print(f'COMMAND: {" ".join(cmd)}')

    with open('pyinstaller_build.log', 'wb') as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for c in iter(lambda: process.stdout.read(1), b''):  # replace '' with b'' for Python 3
            sys.stdout.write(c.decode('utf-8'))
            f.write(c)


def find_fp(dir_work: str, endswith: list) -> list:
    list_fp = list()
    list_fp_append = list_fp.append

    for dirpath, dirnames, filenames in os.walk(dir_work):

        for fn in filenames:
            if any([fn.endswith(suffix) for suffix in endswith]):
                list_fp_append(join(dirpath, fn))

    return list_fp


def main():
    build_write(fp=os.path.join(__root_dir__, 'build'))

    options = [
        "--onedir",  # output unpacked dist to one directory, including an .exe file
        "--noconfirm",  # replace output directory without asking for confirmation
        # "--windowed",
        "--noconsole",
        "--clean",  # clean pyinstaller cache and remove temporary files
        f'--add-data={realpath(join("etc", "ofr_logo_1_80_80.ico"))}{os.pathsep}etc',  # include icon file
    ]

    # include fsetoolsGUI/gui/*, i.e. image, icon, stylesheet and documentation (in html format) files
    options.extend([
        f'--add-data={fp}{os.pathsep}{relpath(dirname(fp), start=__root_dir__)}' for fp in find_fp(dir_work=join(__root_dir__, 'gui'), endswith=['.png', '.ico', '.css', '.html'])
    ])
    options.extend(
        [f'--add-data={join(__root_dir__, "build")}{os.pathsep}{relpath(__root_dir__, start=__root_dir__)}']
    )

    build_gui(options=options)


if __name__ == "__main__":
    make_build_info()
    main()

    import subprocess

    fp_exe = f'{os.path.join(os.path.realpath(os.path.dirname(__file__)), "dist", "FSETOOLS", "FSETOOLS.exe")}'
    print(fp_exe)
    subprocess.Popen([fp_exe])
