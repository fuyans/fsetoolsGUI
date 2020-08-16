import os
import subprocess
from os.path import join, dirname

import fsetoolsGUI


def ui2py():

    dir_ui = join(fsetoolsGUI.__root_dir__, 'gui', 'layout', 'ui')
    list_ui_file_names = list()

    for dirpath, dirnames, filenames in os.walk(dir_ui):
        for fn in filenames:
            if fn.endswith('.ui'):
                list_ui_file_names.append(fn)
    
    destination_dir = dirname(dir_ui)

    cmd_list = list()
    for ui_file_name in list_ui_file_names:
        cmd = [
            'pyside2-uic',
            '--output', f'{join(destination_dir, ui_file_name.replace(".ui", ".py"))}',
            f'{join(dir_ui, ui_file_name)}'
        ]
        cmd_list.append(cmd)

    procs_list = list()
    for i, cmd in enumerate(cmd_list):
        print(' '.join(cmd), f' ({i+1}/{len(cmd_list)})')
        procs_list.append(subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE))

    for proc in procs_list:
        proc.wait()


if __name__ == '__main__':
    ui2py()
